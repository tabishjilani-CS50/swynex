# Task Manager CLI

A clean, beginner-friendly Python command-line task manager demonstrating:

- Modular project structure
- Input validation
- Custom exceptions
- Safe JSON persistence
- Centralized error handling
- Type hints and docstrings
- Automated tests with `pytest`
- GitHub-ready documentation and setup instructions

## Features

- Add tasks with a title and optional description
- List all tasks
- Mark tasks as completed
- Delete tasks
- Validate task IDs and user input
- Persist data to a local JSON file
- Handle malformed/missing data gracefully

## Project Structure

```text
python-task-manager/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── cli.py
│       ├── exceptions.py
│       ├── models.py
│       ├── repository.py
│       └── services.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── data/
│   └── .gitkeep
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.10 or newer
- `pip`

Runtime dependencies are intentionally kept at zero. Development/testing uses `pytest`.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/python-task-manager.git
cd python-task-manager
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

```bash
python -m pip install -e ".[dev]"
```

## Usage

Run the application with:

```bash
python -m task_manager.cli
```

The menu lets you:

1. Add a task
2. List tasks
3. Complete a task
4. Delete a task
5. Exit

## Run Tests

```bash
pytest
```

For more detail:

```bash
pytest -v
```

## Validation and Error Handling

The project uses:

- `TaskValidationError` for invalid task data
- `TaskNotFoundError` when a requested task does not exist
- `StorageError` for persistence problems
- Input validation before tasks are saved
- Defensive handling of invalid JSON
- A CLI-level error boundary so expected errors are shown as friendly messages instead of tracebacks

## Data Storage

Tasks are stored in:

```text
data/tasks.json
```

The file is created automatically when the application first saves a task.

For a real production application, this repository layer could later be replaced with SQLite or PostgreSQL without changing the service/business logic significantly.

## Development

Recommended workflow:

```bash
python -m pip install -e ".[dev]"
pytest -v
```

You can also compile-check the package:

```bash
python -m compileall src
```

## GitHub Setup

After creating your GitHub repository:

```bash
git init
git add .
git commit -m "Create clean Python task manager"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/python-task-manager.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Future Improvements

- Search and filter tasks
- Task priorities and due dates
- SQLite repository
- REST API with Flask or FastAPI
- Authentication
- CI with GitHub Actions
- Structured logging

## License

MIT License. See `LICENSE`.
