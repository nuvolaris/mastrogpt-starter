#--web true
import json, requests

def main(args):

    NOTE = """There is no AI in this chat. 
It only demonstrated what the chat can disply.
Plese select one of:

    - code
    - message
    - html
    - upload
    - chess
    
Exact word, please.
"""


    output = NOTE
    code = None
    language = None
    chess = None
    message = None
    html = None
    upload = None

    # initialize state
    title =  "MastroGPT Demo"
    try:
        # get the state if available
        counter = int(args.get("state")) +1
    except:
        # initialize the state
        counter = 1
        
    message =  f"You made {counter} requests"
    state = str(counter)
    
    input = args.get("input", "")
    print("input='%s'" %  input)

    if input == "":
        output = f"""Welcome, this is MastroGPT demo chat showing what it can display.\n{NOTE}"""
        message = "Watch here for rich output."     
    elif input == "code":
        code = """
def sum_to(n):
    sum = 0
    for i in range(1,n+1):
        sum += i
    return sum
"""
        language = "python"
        output = f"Here is some python code.\n```python\n{code}\n```"
    elif input == "chess":
        chess = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        output = f"Check this chess position.\n\n{chess}"    
    elif input ==  "html":
        html = """
<h1>Sample Form</h1>
<form action="/submit-your-form-endpoint" method="post">
  <div>
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" required>
  </div>
  <div>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password" required>
  </div>
  <div>
    <button type="submit">Login</button>
  </div>
</form>
"""
        output = f"Here is some HTML.\n```html\n{html}\n```"
    elif input == "message":
        message = "This is the message."
        title = "This is the title"
        output = "Here is a sample message."
    elif input == "upload":
        upload = "Upload your document"
        output = "Here is your upload form."
    elif input.startswith("wordpress"):
        pagenr = input.split(" ")[-1]
        if pagenr == "wordpress": pagenr = "110"
        pagejs = json.loads(requests.get(f"https://critical-work.com/wp-json/wp/v2/pages/{pagenr}").content)
        html = pagejs["content"]["rendered"]
        output = "Please check the right area."
    else:
        output = NOTE
        
    # state is a counter incremented at any invocation
    res = {
        "output": output,
    }

    if language: res['language'] = language
    if message: res['message'] =  message     
    if state: res['state'] =  state
    if title: res['title'] = title
    if chess: res['chess'] = chess
    if code: res['code'] = code
    if html: res['html'] = html
    if upload: res['upload'] = upload

    return { "body": res } 
