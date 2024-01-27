import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .deploy import deploy

counter = 0

class ChangeHandler(FileSystemEventHandler):
    """Logs all the events captured."""
    
    last_modified = {}

    def on_any_event(self, event):
        if event.is_directory or event.event_type != "modified":
            return
        src = event.src_path
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
    observer.schedule(event_handler, "web", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

