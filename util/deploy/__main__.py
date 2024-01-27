import argparse
from .scan import scan
from .watch import watch
from .deploy import set_dry_run

def main():
    parser = argparse.ArgumentParser(description='Deployer')
    parser.add_argument('-w', '--watch', action='store_true', help='Watch for changes', required=False)
    parser.add_argument('-d', '--dry-run', action='store_true', help='Dry Run', required=False)
    args = parser.parse_args()
    set_dry_run(args.dry_run)
    # walk and deploy
    scan()
    # watch if requested
    if  args.watch:
        print(">>> Watching:")
        watch()

if __name__ == "__main__":
    main()