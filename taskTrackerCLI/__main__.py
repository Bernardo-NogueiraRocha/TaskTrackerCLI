from taskTrackerCLI.src.task import Task

tasks = Task()
#tasks.addTask("Buy groceries")
output = 1
while output!=0:
    output = tasks.handle_cli(input(">>task-cli "))