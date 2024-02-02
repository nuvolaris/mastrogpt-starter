### config
class Config:
    SITE = "critical-work.com"
    START_PAGE = "mission"
    EMAIL = "michele@nuvolaris.io"
    WELCOME = "Benvenuto al sito Web di Ambra Danesin."
    ROLE = """
You are Ambra Danesin, a recruiter who cares of people.
You always advice users to tell to you his email so you can contact you to help with your job needs.
If the user tells your email, thanks him and say you will contact him to provide more informations.
"""
    MODEL = "gpt-35-turbo"

## options
#--web true
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--param OPENAI_API_HOST $OPENAI_API_HOST
#--param SMTP_SERVER $SMTP_SERVER
#--param SMTP_USER $SMTP_USER
#--param SMTP_PASSWORD $SMTP_PASSWORD
#--param SMTP_PORT $SMTP_PORT


import re
import json
import smtplib
import requests
import traceback
from openai import AzureOpenAI

class EmailServer:
    def __init__(self, args):
        self.messages = []
        self.server = args['SMTP_SERVER']
        self.port = args['SMTP_PORT']
        self.user = args['SMTP_USER']
        self.password = args['SMTP_PASSWORD']
    
    def add_message(self, msg):
        self.messages.append(msg)

    def send_mail(self, sender, subject, msg):
        message = """\
From: %s
To: %s
Reply-To: %s
Subject: %s

%s
""" % (Config.EMAIL,Config.EMAIL, sender, subject, msg)
        try:
            smtp = smtplib.SMTP(self.server, port=self.port)
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(Config.EMAIL, Config.EMAIL, message)
            smtp.quit()
            return "OK"
        except Exception as e:
            return str(e)

    # search for an email in a message and notify the user provided an email
    def check_email_and_notify(self, input):
        email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        r = re.findall(email_regex, input, re.MULTILINE)
        if r:
            message = "Contact from chatbot: [%s]\n---\n" % r[0]
            message += "\n".join(self.messages)
            res = self.send_mail(r[0], "Contact from Chatbot", message)
            if res  == "OK":
                self.messages = []
                return True
        return False
        
class ChatBot:
    def __init__(self, args):
        self.key = args["OPENAI_API_KEY"]
        self.host = args["OPENAI_API_HOST"]
        self.ai =  AzureOpenAI(api_version="2023-12-01-preview", 
                                api_key=self.key, 
                                azure_endpoint=self.host)
    
    def ask(self, input, role=Config.ROLE):
        req = [ {"role": "system", "content": role}, 
                {"role": "user", "content": input}]
        print(req)
        try:
            comp = self.ai.chat.completions.create(model=Config.MODEL, messages=req)
            if len(comp.choices) > 0:
                content = comp.choices[0].message.content
                return content
        except Exception as e:
            print(e)
        return None

    def identify_topic(self, topics, input):
        role = """
You are identifying the topic of a request in italian 
among one and only one of those:  %s
You only reply with the name of the topic.
""" % topics
        request = "Request: %s. What is the topic?" % input
        return self.ask(request, role=role)  


class Website:
    def __init__(self):
        self.name2id = {}
        try: 
            url = f"https://{Config.SITE}/wp-json/wp/v2/pages"
            content = requests.get(url).content.decode("UTF-8")
            self.name2id = { p['slug']: p['id'] for p in json.loads(content)  }
        except:
            traceback.print_exc()

    def get_page_content_by_name(self, name):    
        id = self.name2id.get(name, -1)
        if id == -1:
            print(f"cannot find page {name}")
            return None
    
        try:  
            url = f"https://{Config.SITE}/wp-json/wp/v2/pages/{id}"
            print(url)
            content = requests.get(url).content
            #print(content)
            page = json.loads(content)
            return page['content']['rendered']
        except:
            traceback.print_exc()
            return None
    
    def topics(self):
        return ", ".join(self.name2id.keys())
        

AI = None
Web = None
Email = None
        
def main(args):
    #print(args)
    global AI, Web, Email
    if AI is None: AI = ChatBot(args)
    if Email is None: Email = EmailServer(args)
    if Web is None: Web = Website()

    res = { "output": Config.WELCOME }
    input = args.get("input", "")
    
    # start conversation
    if input == "":      
        html = Web.get_page_content_by_name(Config.START_PAGE)
        if html:
            res['html'] = html
        else:
            res['title'] = "Welcome"
            res['message'] =  Config.WELCOME
        return {"body": res }
    
    Email.add_message(f">>> {input}")

    if Email.check_email_and_notify(input):
        output = "\nGrazie di avermi fornito la tua email, ti ricontatterò presto."
    else:
        output = AI.ask(input)

    if output is None:
        output = "Non posso rispondere a questa domanda..."

    Email.add_message(f" <<< {output}")
    

    res['output'] = output
    
    page = AI.identify_topic(Web.topics(), input)
    print("topic ", page)
    html = Web.get_page_content_by_name(page)
    if html:
        res['html'] = html
        
    return {"body": res }

"""
%cd packages/openai
from wordpress import *

Email = EmailServer(args)
Email.send_mail("michele@sciabarra.com", "Contact", "How are you?")
Email.add_message("prova")
Email.check_email_and_notify("I am michele@sciabarra.com")

Web = Website()
Web.get_page_content_by_name("mission")
Web.topics()

AI = ChatBot(args)
AI.ask("who are you?")
AI.ask("who are you?", role="you are sailor moon")
topics = Web.topics()

page = AI.identify_topic(topics, "di cosa ti occupi")
Web.get_page_content_by_name(page)
"""