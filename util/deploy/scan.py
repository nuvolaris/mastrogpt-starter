from glob import glob
from .deploy import *

def scan():
    # first look for requirements.txt and build the venv (add in set)
    deployments = set()

    print(">>> Scan:")
    reqs =  glob("packages/*/*/requirements.txt")
    for req in reqs:
        print(">", req)
        sp = req.split("/")
        sp = build_venv(sp)
        deployments.add("/".join(sp))
    
    mains = glob("packages/*/*/__main__.py")
    for main in mains: 
        print(">", main)
        sp = main.split("/")
        sp = build_action(sp)
        deployments.add("/".join(sp))

    singles = glob("packages/*/*.py")
    for single in singles:
        print(">", single)
        deployments.add(single)

    print(">>> Deploying:")
    for action in deployments:
        print("^", action)
        deploy_action(action.split("/"))