# deploy
nuv action list
task --list-all

task d F=openai/chat.py
task d F=mastrogpt/display.zip

# test demo
task d F=mastrogpt/demo.py
nuv invoke mastrogpt/demo
nuv invoke mastrogpt/demo -p input html
nuv invoke mastrogpt/demo -p input code
nuv invoke mastrogpt/demo -p input chess

# test display
chess = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"
task d F=mastrogpt/display.zip
nuv invoke mastrogpt/display -p "message" "hello"
nuv invoke mastrogpt/display -p "html" "<h1>hello</h1>"
nuv invoke mastrogpt/display -p "code" "def sum(a,b):\n  return a + b\n" -p language python
nuv invoke mastrogpt/display -p chess  "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1"

# test extraction
task cli




