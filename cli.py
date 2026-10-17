"""Command-line interface for the task manager."""

from pathlib import Path

from .exceptions import TaskManagerError
from .repository import JsonTaskRepository
from .services import TaskService


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "tasks.json"


def _print_tasks(service: TaskService) -> None:
    tasks = service.list_tasks()
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nTasks:")
    for task in tasks:
        status = "DONE" if task.completed else "TODO"
        print(f"[{status}] {task.id}: {task.title}")
        if task.description:
            print(f"       {task.description}")


def _read_task_id() -> int:
    raw = input("Task ID: ").strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError("Task ID must be a number.") from exc


def main() -> None:
    """Run the interactive application."""
    service = TaskService(JsonTaskRepository(DATA_FILE))

    print("=== Python Task Manager ===")

    while True:
        print("\n1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                description = input("Description (optional): ")
                task = service.add_task(title, description)
                print(f"Created task #{task.id}.")

            elif choice == "2":
                _print_tasks(service)

            elif choice == "3":
                task_id = _read_task_id()
                service.complete_task(task_id)
                print("Task marked as completed.")

            elif choice == "4":
                task_id = _read_task_id()
                service.delete_task(task_id)
                print("Task deleted.")

            elif choice == "5":
                print("Goodbye!")
                return

            else:
                print("Please choose an option from 1 to 5.")

        except (TaskManagerError, ValueError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
