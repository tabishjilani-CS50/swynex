import json

tasks = []

try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    print ("Error")
    tasks = []


def save():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


def add_task():
    task = input("Enter task: ")

    if task == "":
        print("Task cannot be empty")
        return

    tasks.append([task, False])
    save()
    print("Task added")


def show_tasks():
    if len(tasks) == 0:
        print("No tasks")

    for i in range(len(tasks)):
        if tasks[i][1]:
            status = "Done"
        else:
            status = "Not Done"

        print(i + 1, tasks[i][0], "-", status)


def complete_task():
    show_tasks()

    try:
        number = int(input("Enter task number: "))

        if number < 1 or number > len(tasks):
            print("Invalid task number")
            return

        tasks[number - 1][1] = True
        save()
        print("Task completed")

    except ValueError:
        print("Please enter a number")


while True:
    print("\n1. Add Task")
    print("2. Show Tasks")
    print("3. Complete Task")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        show_tasks()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        break

    else:
        print("Invalid choice")