import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def on_modified(event):
    print("ARQUIVO MODIFICADO")

def on_any_event(event):
    print(event.src_path)


class Watchdog:

    if __name__ == "__main__":
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified
        event_handler.on_any_event = on_any_event

        path = "C:/Users/davio/Desktop/fileMod"

        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            print("Monitorando")
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            print("Terminado")
            observer.join()
