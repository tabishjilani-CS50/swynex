"""Application-specific exceptions."""


class TaskManagerError(Exception):
    """Base exception for expected application errors."""


class TaskValidationError(TaskManagerError):
    """Raised when task data fails validation."""


class TaskNotFoundError(TaskManagerError):
    """Raised when a requested task cannot be found."""


class StorageError(TaskManagerError):
    """Raised when task persistence fails."""
