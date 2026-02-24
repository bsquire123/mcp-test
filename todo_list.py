class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Added task: {task}")

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Removed task: {task}")
        else:
            print(f"Task not found: {task}")

    def show_tasks(self):
        print("Todo List:")
        for task in self.tasks:
            print(f"- {task}")

if __name__ == "__main__":
    todo = TodoList()
    todo.add_task("Buy groceries")
    todo.add_task("Pay bills")
    todo.show_tasks()
    todo.remove_task("Pay bills")
    todo.show_tasks()