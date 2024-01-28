import os
from  os.path import exists
from subprocess import Popen

dry_run = False

def set_dry_run(b):
    global dry_run
    dry_run = b

def exec(cmd):
    global dry_run
    print("$", cmd)
    if not dry_run:
        Popen(cmd, shell=True, env=os.environ).wait()

def extract_args(file):
    res = []
    if exists(file):
        with open(file, "r") as f:
            for line in f.readlines():
                if line.startswith("#-"):
                    res.append(line.strip()[1:])
    return res

# root _dir and _file (split)
# def deploy_web(_dir, _file):
#    dir = "/".join(_dir)
#    file = "/".join(_file)
#    print(f"cd {dir}")
#    print(f"TODO: upload {file} {_dir[-2]}/{file}")

package_done = set()

def deploy_package(package):
    global package_done
    # package args
    ppath = f"packages/{package}.args"
    pargs = " ".join(extract_args(ppath))
    cmd = f"nuv package update {package} {pargs}"
    if not cmd in package_done:
        exec(cmd)
        package_done.add(cmd)

def build_venv(sp):
    exec(f"task build:venv A={sp[1]}/{sp[2]}")
    res = sp[:-1]
    res[-1] += ".zip"
    return res

def build_action(sp):
    exec(f"task build:action A={sp[1]}/{sp[2]}")
    res = sp[:-1]
    res[-1] += ".zip"
    return res

def deploy_action(sp):
    [name, typ] = sp[-1].rsplit(".", 1)
    package = sp[1]
    artifact = "/".join(sp)

    deploy_package(package)

    if typ == "zip":
        src = "/".join(sp)[:-4]+"/__main__.py"
    else:
        src = "/".join(sp)
    
    args = " ".join(extract_args(src))
    exec(f"nuv action update {package}/{name} {artifact} {args}")


"""
file = "packages/deploy/hello.py"
file = "packages/deploy/multi.zip"
file = "packages/deploy/multi/__main__.py"
file = "packages/deploy/multi/requirements.txt"
"""
def deploy(file):
    print(f"*** {file}")
    sp = file.split("/")
    
    # no web incremental upload for now
    #if sp[0] == "web":
    #    deploy_web(sp[0], sp[1:])
    #elif len(sp) > 3 and sp[2] == "web":
    #    deploy_web(sp[0:3], sp[3:])
    #elif len(sp) == 2:
    #    deploy_action(sp, "default", sp[1])
    
    # packages/action/file.ext

    if len(sp) == 3:
        deploy_action(sp)
    elif len(sp) > 3: 
        #package/action/file/requrements.txt
        if sp[-1] == "requirements.txt":
            sp = build_venv(sp)
        #package/action/file/__main__.py
        else:
            sp = build_action(sp)
        deploy_action(sp)
