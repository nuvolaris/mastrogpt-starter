import argparse
from os.path import isdir, exists
from .scan import scan
from .watch import watch
from .deploy import set_dry_run, deploy

def main():
    parser = argparse.ArgumentParser(description='Deployer')
    parser.add_argument('-w', '--watch', action='store_true', help='Watch for changes', required=False)
    parser.add_argument('-d', '--dry-run', action='store_true', help='Dry Run', required=False)
    parser.add_argument('-s', '--single', type=str, default="", help='Deploy a single action, either a single file or a directory.')

    args = parser.parse_args()
    set_dry_run(args.dry_run)
    
    if args.single != "":
        action = args.single
        if not action.startswith("packages/"):
            action = f"packages/{action}"
        if not exists(action):
            print(f"action {action} not found: must be either a file or a directory under packages")
            return
        print(f"Deploying {action}")
        deploy(action)
        return
    
    # walk and deploy
    scan()
    
    # watch if requested
    if  args.watch:
        print(">>> Watching:")
        watch()

if __name__ == "__main__":
    main()