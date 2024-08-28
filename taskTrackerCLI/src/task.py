from datetime import datetime
import json
from tabulate import tabulate
import os
class Task:
    id = 1
    instances = []

    def load_tasks(self):
        try:
            with open("taskTrackerCLI/data/data.json", "r") as file:
                Task.instances = json.load(file)
        except FileNotFoundError:
            Task.instances = []

    def save_tasks():
        with open("taskTrackerCLI/data/data.json", "w") as file:
            json.dump(Task.instances, file, indent=4)

    def __init__(self) -> None:
        self.load_tasks()
        if len(Task.instances) > 0:
            Task.id = Task.instances[-1]["id"]+1

    def addTask(self,name):
        data ={
            "id": Task.id,
            "name": name,
            "status": "Todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        Task.id+=1
        Task.instances.append(data)
        with open("taskTrackerCLI/data/data.json", "w") as file:
            json.dump(Task.instances, file, indent=4)
        print(f'Task added successfully (ID: {data["id"]})')
        
    def listTasks(self, params = "All"):
        if params == "All":
            headers = ["Id","Name", "Status","CreatedAt", "UpdatedAt"]
            data = [headers]
            for task in Task.instances:
                data.append([task["id"],task["name"],task["status"],task["createdAt"],
                     task["createdAt"]])
            print(tabulate(data,tablefmt="fancy_grid", headers="firstrow"))

    def searchTask(self,id):
        pass

    def updateTask(self,id):
        pass

    def delete(self,id):
        pass
    
    def markAs(self,status):
        pass

    def treatCLI(self, command:str):
        beginning = "task-cli "
        if command == "clear":
            os.system("clear")
            return
        #Verifies the default beginning of the other command lines
        elif command[0:len(beginning)] != beginning:
            print("Invalid command")
        #places the command string to the arguments to process them
        command = command[len("task-cli "):]
        if command == "list":
            self.listTasks()
            return
        elif command[0:3] == "add":
            self.addTask(name=command[4:])
            return 
