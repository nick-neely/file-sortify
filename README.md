# File Sortify

File Sortify is a Python application that automatically sorts files in a specified directory into categorized folders based on their file types.

## Setup

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up a virtual environment and activate it:

```bash
# Create a virtual environment
python -m venv env
```

## Activate the virtual environment

### On Windows

```bash
env\Scripts\activate
```

### On Unix or MacOS

```bash
source env/bin/activate
```

## Configuration

The config.json file is used to configure the application. It should contain the following keys:

    downloads_folder: The path to the folder you want to sort.
    destination_folders: A dictionary mapping categories to destination folder paths.
    file_types: A dictionary mapping categories to lists of file extensions.

Here's an example config.json:

```json
{
  "downloads_folder": "/path/to/downloads",
  "destination_folders": {
    "images": "/path/to/images",
    "documents": "/path/to/documents",
    "music": "/path/to/music",
    "videos": "/path/to/videos"
  },
  "file_types": {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "music": [".mp3", ".wav", ".aac", ".flac"],
    "videos": [".mp4", ".mkv", ".avi", ".mov"]
  }
}
```

## Running the Application

To run the application, execute the file-sortify.py script:

```bash
python file-sortify.py
```

## Setting Up Task Scheduler

The setup.py script is used to set up a task in the Windows Task Scheduler that runs the application at regular intervals. To set up the task, run the setup.py script:

```bash
python setup.py
```

Please note that you might need to run the script as an administrator to have the necessary permissions to create a task.

Remember to replace /path/to/downloads, /path/to/images, and /path/to/documents with the actual paths on your machine.
