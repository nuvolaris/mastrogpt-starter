import argparse
from .scan import scan
from .watch import watch

def main():
    parser = argparse.ArgumentParser(description='Deployer')
    parser.add_argument('-w', '--watch', action='store_true', help='Watch for changes', required=False)
    args = parser.parse_args()
    # walk and deploy
    print("Scan:")
    scan()
    # watch if requested
    if  args.watch:
        print("Watching:")
        watch()

if __name__ == "__main__":
    main()