import pytest

from task_manager.exceptions import TaskNotFoundError
from task_manager.repository import JsonTaskRepository
from task_manager.services import TaskService


def test_add_and_list_tasks(tmp_path) -> None:
    service = TaskService(JsonTaskRepository(tmp_path / "tasks.json"))

    created = service.add_task("Build a Python project", "Write tests")
    tasks = service.list_tasks()

    assert created.id == 1
    assert len(tasks) == 1
    assert tasks[0].title == "Build a Python project"


def test_complete_task(tmp_path) -> None:
    service = TaskService(JsonTaskRepository(tmp_path / "tasks.json"))
    created = service.add_task("Finish README")

    updated = service.complete_task(created.id)

    assert updated.completed is True
    assert service.list_tasks()[0].completed is True


def test_delete_missing_task_raises(tmp_path) -> None:
    service = TaskService(JsonTaskRepository(tmp_path / "tasks.json"))

    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)
