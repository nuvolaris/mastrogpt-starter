from .deploy import deploy
import os

def walk_subtree(top_directory):
    for dirpath, dirnames, filenames in os.walk(top_directory):
        #print(f'Found directory: {dirpath}')
        for filename in filenames:
            deploy(f"{dirpath}/{filename}")

def walk():
    walk_subtree('packages')