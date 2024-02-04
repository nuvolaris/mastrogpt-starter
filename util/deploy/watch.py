ALLOWED = set(["py", "js", "txt", "json" ])
import os, time
from subprocess import Popen
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .deploy import deploy

class ChangeHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    
    last_modified = {}

    def on_any_event(self, event):
        if event.event_type != "modified": return
        if event.is_directory: return
        src = event.src_path

        rs = src.rsplit(".", -1)
        if len(rs) < 2: return
        if not rs[-1] in ALLOWED: return

        cur = time.time()
        last = self.last_modified.get(src, 0)
        #print(event, cur, last)
        if cur - last  < 1:
            return
        self.last_modified[src] = cur
        deploy(src)

def watch():
    observer = Observer()
    event_handler = ChangeHandler()
    observer.schedule(event_handler, "packages", recursive=True)
    #observer.schedule(event_handler, "web", recursive=True)
    observer.start()
    try:
        serve()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# serve web area
def serve():
    Popen("task serve", shell=True, env=os.environ)