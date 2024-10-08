from datetime import datetime
import json
from tabulate import tabulate
import os

class Task:
    def __init__(self):
        self.instances = self.load_tasks()
        if self.instances:
            self.id = self.instances[-1]["id"] + 1
        else:
            self.id = 1

    def load_tasks(self):
        try:
            with open("taskTrackerCLI/data/data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open("taskTrackerCLI/data/data.json", "w") as file:
            json.dump(self.instances, file, indent=4)

    def add_task(self, name):
        data = {
            "id": self.id,
            "name": name,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }
        self.id += 1
        self.instances.append(data)
        self.save_tasks()
        print(f'Task added successfully (ID: {data["id"]})')

    def list_tasks(self, params="All"):
        if params == "All":
            headers = ["Id", "Name", "Status", "Created At", "Updated At"]
            data = [headers]
            for task in self.instances:
                data.append(
                    [
                        task["id"],
                        task["name"],
                        task["status"],
                        task["createdAt"],
                        task["createdAt"],
                    ]
                )
            print(tabulate(data, tablefmt="fancy_grid", headers="firstrow"))
        else:
            print(params)
            filtered_tasks = [
                task for task in self.instances if task["status"] == params.lower()
            ]
            if filtered_tasks:
                headers = ["Id", "Name", "Status", "Created At", "Updated At"]
                data = [headers]
                for task in filtered_tasks:
                    data.append(
                    [
                        task["id"],
                        task["name"],
                        task["status"],
                        task["createdAt"],
                        task["createdAt"],
                    ]
                )
                print(tabulate(data, tablefmt="fancy_grid", headers="firstrow"))
            else:
                print(f"No tasks found with status '{params}'.")

    def search_task(self, task_id):
        for index, task in enumerate(self.instances):
            if task["id"] == task_id:
                return index
        return None

    def update_task(self, task_id, new_name):
        print(new_name)
        task_index = self.search_task(task_id)
        if task_index is not None:
            self.instances[task_index]["name"] = new_name
            self.instances[task_index]["updatedAt"] = datetime.now().isoformat()
            self.save_tasks()
            print(f"Task '{task_id}' updated successfully.")
        else:
            print(f"Task with ID '{task_id}' not found.")

    def delete_task(self, task_id):
        task_index = self.search_task(task_id)
        if task_index is not None:
            self.instances.pop(task_index)
            self.save_tasks()
            print(f"Task '{task_id}' deleted successfully.")
        else:
            print(f"Task with ID '{task_id}' not found.")

    def mark_as(self, task_id, status):
        valid_statuses = ["in-progress", "done"]
        if status.lower() not in valid_statuses:
            print(f"Invalid status. Valid options are: {', '.join(valid_statuses)}")
            return

        task_index = self.search_task(task_id)
        if task_index is not None:
            self.instances[task_index]["status"] = status.lower()
            self.instances[task_index]["updatedAt"] = datetime.now().isoformat()
            self.save_tasks()
            print(f"Task '{task_id}' marked as '{status}' successfully.")
        else:
            print(f"Task with ID '{task_id}' not found.")

    def handle_cli(self, command:str):
        if command.startswith("clear"):
            os.system("clear")
            return 1
        if command.startswith("exit"):
            return 0
        # split at the first found whitespace
        parts = command.split(maxsplit=1)
        base_command = parts[0]
        if base_command not in ["add", "list", "update", "delete", "mark-done", "mark-in-progress"]:
            print("Invalid command. Valid commands are: add, list, update, delete, mark-done, mark-in-progress, clear")
            return 1
        
        if base_command == "add":
            if len(parts) > 1:
                self.add_task(parts[1])
            else:
                print("Please provide a task name.")
        elif base_command == "list":
            if len(parts) > 1:
                self.list_tasks(parts[1])
            else:
                self.list_tasks()
        elif base_command == "update":
            print(parts)
            if len(parts) > 1:
                update_parts = parts[1].split(maxsplit=1)
                if len(update_parts) == 2:
                    try:
                        task_id = int(update_parts[0])
                        new_name = " ".join(update_parts[1:])
                        self.update_task(task_id, new_name)
                    except ValueError:
                            print("Invalid task ID.")
                else:
                    print("Usage: update <task_id> <new_name>")
            else:
                print("Usage: update <task_id> <new_name>")
        elif base_command == "delete":
            if len(parts) > 1:
                try:
                    task_id = int(parts[1])
                    self.delete_task(task_id)
                except ValueError:
                    print("Invalid task ID.")
            else:
                print("Usage: delete <task_id>")
        elif base_command == "mark-done" or base_command == "mark-in-progress":
            if len(parts) > 1:
                try:
                    task_id = int(parts[1])
                    status = "done" if base_command == "mark-done" else "in-progress"
                    self.mark_as(task_id, status)
                except ValueError:
                    print("Invalid task ID.")
            else:
                print("Usage: mark-<status> <task_id>")
        return 1