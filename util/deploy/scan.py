from glob import glob
from .deploy import *

def scan():
    # first look for requirements.txt and build the venv (add in set)
    reqs =  glob("packages/*/*/requirements.txt")
    for req in reqs:
        build_venv(req.split("/"))
    
    mains = glob("packages/*/*/__main__.py")
    for main in mains: 
        build_action(main.split("/"))

    singles = glob("packages/*/*.py")
    for single in singles:
        deploy_action(single.split("/"))

