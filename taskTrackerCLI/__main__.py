from taskTrackerCLI.src.task import Task

tasks = Task()
#tasks.addTask("Buy groceries")
while True:
    tasks.treatCLI(input(">>"))