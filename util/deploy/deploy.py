def deploy_web(_dir, _file):
    dir = "/".join(_dir)
    file = "/".join(_file)
    print(f"cd {dir}")
    print(f"nuv upload {file} {_dir[-2]}/{file}")

def deploy_action(_path, package, file):
    [name, typ] = file.rsplit(".", 1)
    path = "/".join(_path)
    if package != "default":
        print(f"package update {package}")
    print(f"action update {package}/{name} {path}")

def build_venv(sp):
    print(f"build:venv A={sp[1]}/{sp[2]}")

def build_action(sp):
    print(f"build:act A={sp[1]}/{sp[2]}")

def deploy_zip(sp):
    zip = "/".join(sp)+".zip"
    print(f"deploy {zip}")

"""
file = "packages/deploy/web/index.html"
file = "web/index.html"
file = "packages/deploy/hello.py"
file = "packages/deploy/multi/__main__.py"
file = "packages/deploy/multi/requirements.txt"
file = "packages/deploy/multi/requirements.txt"
"""
def deploy(file):
    print(f"*** {file}")
    sp = file.split("/")
    if sp[0] == "web":
        deploy_web(sp[0], sp[1:])
    elif len(sp) > 3 and sp[2] == "web":
        deploy_web(sp[0:3], sp[3:])
    #elif len(sp) == 2:
    #    deploy_action(sp, "default", sp[1])
    elif len(sp) == 3:
        deploy_action(sp, sp[1], sp[2])
    elif len(sp) > 3:
        if sp[-1] == "requirements.txt":
            build_venv(sp)
        else:
            build_action(sp)
        deploy_zip(sp[:-1])

