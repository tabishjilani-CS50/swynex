"""Business logic for task management."""

from .exceptions import TaskNotFoundError, TaskValidationError
from .models import Task
from .repository import JsonTaskRepository


class TaskService:
    """Coordinate validation, business rules, and persistence."""

    def __init__(self, repository: JsonTaskRepository) -> None:
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        """Return all stored tasks."""
        return self.repository.load()

    def add_task(self, title: str, description: str = "") -> Task:
        """Create, validate, persist, and return a new task."""
        tasks = self.repository.load()
        next_id = max((task.id for task in tasks), default=0) + 1
        task = Task(id=next_id, title=title, description=description)
        tasks.append(task)
        self.repository.save(tasks)
        return task

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed."""
        tasks = self.repository.load()
        task = self._find(tasks, task_id)
        task.completed = True
        self.repository.save(tasks)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID."""
        tasks = self.repository.load()
        task = self._find(tasks, task_id)
        tasks.remove(task)
        self.repository.save(tasks)

    @staticmethod
    def _find(tasks: list[Task], task_id: int) -> Task:
        """Find a task or raise a meaningful error."""
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")

        for task in tasks:
            if task.id == task_id:
                return task

        raise TaskNotFoundError(f"No task exists with ID {task_id}.")
