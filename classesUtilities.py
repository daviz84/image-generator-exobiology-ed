import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

observer = Observer()

def on_modified(event):
    print("ARQUIVO MODIFICADO")

def on_any_event(event):
    print(event.src_path)


def monitorar():

    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_modified
    event_handler.on_any_event = on_any_event

    path = "C:/Users/davio/Desktop/fileMod"


    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("Monitorando")
        while True:
            time.sleep(1)
    except:
        observer.stop()
        print("Terminado")
    observer.join()