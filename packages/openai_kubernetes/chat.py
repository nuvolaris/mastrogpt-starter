#--web true
#--kind python:default
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--param OPENAI_API_HOST $OPENAI_API_HOST

from openai import AzureOpenAI
import json

data_to_display = ""
last_context = ""
AI = None

# FUNCTION CALLING SECTION
import requests
def list_objects(of_kind: str):
    global data_to_display

    url = "https://nuvkube.nuvolaris.app/api/my/nuvkube-api/list-objects"
    response =  requests.get(url, params = {"kind": of_kind})

    data = response.json()
    status_counts = {}

    for object in data:
        del object["apiVersion"]
        del object["kind"]

        if of_kind == "pods":
            object["status"] = object["status"]["phase"]

            current_status = object["status"]
            status_counts[current_status] = status_counts.get(current_status, 0) + 1


    response = {
        "data": data,
        "metadata": {
            "numbers_of_objects": len(data),
            "pods_statues_count": status_counts 
        }
    }
    data_to_display = data
    return response

def get_object(of_kind: str, with_name: str):
    global data_to_display

    url = "https://nuvkube.nuvolaris.app/api/my/nuvkube-api/get-object"
    response = requests.get(url, params = {"kind": of_kind, "name": with_name})
    if response.status_code == 200:
        data_to_display = response.json()
        return response.json()
    data_to_display = None
    return None

openai_custom_functions = [
    {
        'name': 'list_objects',
        'description': "Get a list of all the objects of a given kind.",
        'parameters': {
            'type': 'object',
            'properties': {
                'of_kind': {
                    'type': 'string',
                    'description': 'The kind of the requested objects',
                    "enum": ["nodes", "pods"],
                },            
            }
        }
    },
    {
        'name': 'get_object',
        'description': 'Get info about a specific object, selected by its kind and name',
        'parameters': {
            'type': 'object',
            'properties': {
                'of_kind': {
                    'type': 'string',
                    'description': 'The kind of the requested objects',
                    "enum": ["nodes", "pods"],
                },  
                'with_name': {
                    'type': 'string',
                    'description': 'The unique name of the requested objects',
                },           
            }
        }
    }
]

# END FUNCTION CALLING SECTION

ROLE = """
If you find a JSON list of objects in the "# Context" section, give a small response to the user query.
Reply in italian.
"""

TITLE_MAKER_ROLE = """
You will get a sentence from the user, you have to return a brief title (max 5 words) to describe wha the user is talking about.
"""

SUBJECT_CHANGE_ROLE = """
You will be given two texts. A context and a query. 
If you think you can respond correctly to the query with the given context, return Yes. Otherwhise, return No.
Examples:
(State of the all nodes, State of the first one) -> Yes
(State of the all nodes, State of the pods) -> No
(All the clusters, What about the nodes) -> No 
"""

MODEL = "gpt-35-turbo"

def req(msg):
    return [{"role": "system", "content": ROLE}, 
            {"role": "user", "content": msg}]

def title_maker(msg):
    return [{"role": "system", "content": TITLE_MAKER_ROLE}, 
            {"role": "user", "content": msg}]

def conversation_checker(msg):
    return [{"role": "system", "content": SUBJECT_CHANGE_ROLE}, 
            {"role": "user", "content": msg}]

def ask_for_conversation_check(input):
    comp = AI.chat.completions.create(model=MODEL, messages=conversation_checker(input))
    if len(comp.choices) < 0:
        return "ERROR"
    return comp.choices[0].message.content

def ask_for_title(input):
    comp = AI.chat.completions.create(model=MODEL, messages=title_maker(input))
    if len(comp.choices) < 0:
        return "ERROR"
    return comp.choices[0].message.content

def ask_without_fn_calling(input):
    # print(input)
    comp = AI.chat.completions.create(model=MODEL, messages=req(input))
    # print(comp)
    if len(comp.choices) < 0:
        return "ERROR"
    return comp.choices[0].message.content

def ask(input):
    global last_context
    # print("user input is:", input)
    comp = AI.chat.completions.create(model=MODEL, messages=req(input), functions=openai_custom_functions, function_call="auto")
    if len(comp.choices) > 0:
        message = comp.choices[0].message

        if message.function_call:
            # print("OpenAI called a function.")
            fn_name = message.function_call.name
            values = json.loads(message.function_call.arguments)
            print(message.function_call)
            if fn_name == "list_objects":
                data = list_objects(**values)
            elif fn_name == 'get_object':
                data = get_object(**values)
            else:
                print("C'è qualcosa che non va!")
                return "C'è qualcosa che non va!"
            
            last_context = data
            new_data = f"""
# Context:
{data}
# User query:
{input}
# Response to user is:
"""
            # print(new_data)
            response = ask_without_fn_calling(new_data)
            # print(response)
            return response
            
        if message.content:
            # print("OpenAI didn't call a function.")
            content = message.content
            # print("content", content)
            return content
    return "ERROR"

def main(args):
    global data_to_display
    global last_context
    global AI

    (key, host) = (args["OPENAI_API_KEY"], args["OPENAI_API_HOST"])
    AI = AzureOpenAI(api_version="2023-12-01-preview", api_key=key, azure_endpoint=host)
    
    last_argument = args.get("state", None)
    print("last argument was:", last_argument)

    input = args.get("input", "")
    
    if input == "":
        res =  {
            "output":  "Ciao. Chiedimi quello che vuoi sui tuoi nodi / pods di Kubernetes.",
            "title": "Titolo di prova",
            "message": "Load your data"
        } 
        return {"body": res}
    # else, if there was an user input
    
    if input.startswith("COMMAND"):
        #  we take the command
        command = input.split("COMMAND:")[1].strip()
        # print(f"Executing command: {command =}" )
        if command == "Show Nodes":
            context = list_objects("nodes")
        elif command == "Show Pods":
            context = list_objects("pods")

        new_data = f"""
            # Context:
            {context}
            # User query:
            {input}
            # Response to user is:
            """
        inference = ask_without_fn_calling(new_data)

        res = {
            "output": inference,
            "title": "Risposta",
            "openai-kubernetes-list": data_to_display
        }
        res["state"] = context
        return {"body": res}
    
    # else, if not command was issued
    inference = ask(input)
    res = {
        "output": inference,
        "title": "Risposta",
        "openai-kubernetes-list": data_to_display
    }
    
    # res["state"] = content
    return {"body": res}

    content = ask_for_title(input)
    print(f"New conversation title is {content = }")
    if not last_argument:
        inference = ask(input)
        res = {
            "output": inference,
            "title": "Risposta",
            "openai-kubernetes-list": data_to_display
        }
        res["state"] = content
        return {"body": res}
    
    # else, if there was a last_argument
    print(f"{input = } \n {last_context = }")
    same_subject = ask_for_conversation_check( f"({input}, {last_context}) -> ")
    print(f"Can you reply with the given context? {same_subject = }" )
    if same_subject == "Yes":
        new_data = f"""
        # Context:
        {last_context}
        # User query:
        {input}
        # Response to user is:
        """
        inference = ask_without_fn_calling(new_data)
    else: 
        inference = ask(input)
        
    res = {
        "output": inference,
        "title": "Risposta",
        "openai-kubernetes-list": data_to_display
    }
    res["state"] = content

    return {"body": res}