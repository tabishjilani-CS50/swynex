import pytest

from task_manager.exceptions import TaskValidationError
from task_manager.models import Task


def test_task_creation_strips_text() -> None:
    task = Task(1, "  Learn Python  ", "  Practice classes  ")
    assert task.title == "Learn Python"
    assert task.description == "Practice classes"
    assert task.completed is False


def test_empty_title_is_rejected() -> None:
    with pytest.raises(TaskValidationError):
        Task(1, "   ")


def test_title_over_100_characters_is_rejected() -> None:
    with pytest.raises(TaskValidationError):
        Task(1, "x" * 101)


def test_round_trip_dict_conversion() -> None:
    original = Task(2, "Build project", completed=True)
    restored = Task.from_dict(original.to_dict())
    assert restored == original
