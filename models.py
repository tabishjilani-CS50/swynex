"""Domain models and validation."""

from dataclasses import asdict, dataclass
from typing import Any

from .exceptions import TaskValidationError


@dataclass
class Task:
    """Represent one task."""

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        if not isinstance(self.id, int) or self.id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")

        if not isinstance(self.title, str) or not self.title.strip():
            raise TaskValidationError("Task title cannot be empty.")

        if len(self.title.strip()) > 100:
            raise TaskValidationError("Task title cannot exceed 100 characters.")

        if not isinstance(self.description, str):
            raise TaskValidationError("Task description must be text.")

        if not isinstance(self.completed, bool):
            raise TaskValidationError("Task completion status must be true or false.")

        self.title = self.title.strip()
        self.description = self.description.strip()

    def to_dict(self) -> dict[str, Any]:
        """Convert the task to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Build a Task from a dictionary and validate its fields."""
        if not isinstance(data, dict):
            raise TaskValidationError("Task data must be an object.")

        required = {"id", "title"}
        missing = required - data.keys()
        if missing:
            raise TaskValidationError(
                f"Task is missing required fields: {', '.join(sorted(missing))}."
            )

        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )
