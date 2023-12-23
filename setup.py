import os
import win32com.client

# Define the parameters for the task
script_path = os.path.abspath('file-sortify.py')
python_executable = 'C:\Python312\python.exe'  # Replace with the path to your python.exe
task_name = "File Sortify"  # Replace with a name for your task

# Connect to the Task Scheduler
scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()
root_folder = scheduler.GetFolder('\\')

# Create a new task definition
task_def = scheduler.NewTask(0)

# Create trigger for task (at system startup)
startup_trigger = task_def.Triggers.Create(8)  # 8 is the logon trigger
startup_trigger.Enabled = True

# Set up the action to run the Python script
action = task_def.Actions.Create(0)  # 0 means TaskActionExec
action.ID = "TaskId1"
action.Path = python_executable
action.Arguments = script_path

# Set parameters
task_def.RegistrationInfo.Description = "Runs my Python script at system startup"
task_def.Settings.Enabled = True
task_def.Settings.StopIfGoingOnBatteries = False
task_def.Settings.DisallowStartIfOnBatteries = False

# Register the task
# If the task already exists, it will be updated
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
root_folder.RegisterTaskDefinition(
    task_name,  # Task name
    task_def,
    TASK_CREATE_OR_UPDATE,
    '',  # No user
    '',  # No password
    TASK_LOGON_NONE)

print(f"Task {task_name} has been created/updated.")
