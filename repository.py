"""JSON persistence layer."""

import json
from pathlib import Path
from typing import Any

from .exceptions import StorageError
from .models import Task


class JsonTaskRepository:
    """Persist tasks in a JSON file."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load(self) -> list[Task]:
        """Load tasks from disk, returning an empty list if the file is absent."""
        if not self.file_path.exists():
            return []

        try:
            raw: Any = json.loads(self.file_path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise StorageError("Task storage must contain a JSON list.")
            return [Task.from_dict(item) for item in raw]
        except json.JSONDecodeError as exc:
            raise StorageError("Task storage contains invalid JSON.") from exc
        except OSError as exc:
            raise StorageError(f"Could not read task storage: {exc}") from exc

    def save(self, tasks: list[Task]) -> None:
        """Write all tasks to disk atomically enough for a small local app."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            payload = [task.to_dict() for task in tasks]
            self.file_path.write_text(
                json.dumps(payload, indent=2),
                encoding="utf-8",
            )
        except (OSError, TypeError) as exc:
            raise StorageError(f"Could not save tasks: {exc}") from exc
