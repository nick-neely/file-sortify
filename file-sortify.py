from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import logging
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)

# Attempt to load configuration settings from a file
def load_configuration(config_path):
    try:
        with config_path.open('r') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        logging.error(f"Failed to read configuration: {e}")
        raise
    
# Define the configuration file path
config_path = Path('./config.json') 

# Load the configuration
config = load_configuration(config_path)

# Set up folder paths and file types based on the configuration
DOWNLOADS_FOLDER = Path(config['downloads_folder'])
DEST_FOLDERS = {category: Path(path) for category, path in config['destination_folders'].items()}
EXTENSION_TO_TYPE = {ext: category for category, extensions in config['file_types'].items() for ext in extensions}

# File event handler class
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_path = Path(event.src_path)
        file_extension = file_path.suffix.lower()

        if not has_file_size_stabilized(file_path):
            logging.warning(f"File size has not stabilized: {file_path}")
            return

        category = EXTENSION_TO_TYPE.get(file_extension)
        if category:
            dest_folder = DEST_FOLDERS.get(category)
            if not dest_folder.exists():
                try:
                    dest_folder.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logging.error(f"Failed to create directory {dest_folder}: {e}")
                    return

            dest_file_path = dest_folder / file_path.name
            try:
                file_path.rename(dest_file_path)
                logging.info(f"Moved {file_path} to {dest_folder}")
            except Exception as e:
                logging.error(f"Error moving file {file_path} to {dest_folder}: {e}")
            
def has_file_size_stabilized(file_path: Path, interval=1, retries=5) -> bool:
    """
    Check if a file's size has stabilized, indicating that writing to it has finished.
    :param file_path: The Path object to the file.
    :param interval: The time interval in seconds to wait between size checks.
    :param retries: The number of times to check if the file size has changed.
    :return: True if the file size has stabilized, False otherwise.
    """
    last_size = -1

    for _ in range(retries):
        try:
            current_size = file_path.stat().st_size
        except FileNotFoundError:
            # If the file does not exist or is inaccessible, we assume it's not ready.
            return False

        if current_size == last_size:
            return True

        last_size = current_size
        time.sleep(interval)

    return False

def start_monitoring():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
