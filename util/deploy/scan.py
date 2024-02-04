from glob import glob
from .deploy import *

def scan():
    # first look for requirements.txt and build the venv (add in set)
    deployments = set()
    packages = set()

    print(">>> Scan:")
    reqs =  glob("packages/*/*/requirements.txt") + glob("packages/*/*/package.json")
    # req = reqs[0]
    # from util.deploy.deploy import *
    for req in reqs:
        print(">", req)
        sp = req.split("/")
        sp = build_zip(sp)
        deployments.add("/".join(sp))
        packages.add(sp[1])
        
    mains = glob("packages/*/*/index.js") + glob("packages/*/*/__main__.py")
    # main = mains[2]
    for main in mains: 
        print(">", main)
        sp = main.split("/")
        sp = build_action(sp)
        deployments.add("/".join(sp))
        packages.add(sp[1])    

    singles = glob("packages/*/*.py") +  glob("packages/*/*.js")
    # single = singles[0]
    for single in singles:
        print(">", single)
        deployments.add(single)
        packages.add(sp[1])

    print(">>> Deploying:")

    for package in packages:
        print("%", package)
        deploy_package(package)
    
    for action in deployments:
        print("^", action)
        deploy_action(action.split("/"))
