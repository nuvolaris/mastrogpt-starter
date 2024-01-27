#--web true

def main(args):
    
    code = None
    language = None
    chess = None
    message = None
    html = None
  
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
        output = """Welcome, this is MastroGPT demo chat.
Please try asking for code, chess, html. """
        message = "Watch here for rich output."     
    elif input == "code":
        code = """
for i in range(1,10):
    print(i)
"""
        language = "python"
        output = f"Here is some python code.\n```python\n{code}\n```"
    elif input == "chess":
        chess = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
        output = f"Check this chess position.\n```fen\n{chess}\n```"    
    elif input ==  "html":
        html = """
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
    else:
        output =  "Request not supported."
        
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

    return { "body": res } 
