## Project Structure

tracsis-cli/
├── venv/                   # Virtual environment (if created)
├── tracsis_cli.py         # Main CLI script
├── requirements.txt       # Dependencies
├── setup.py              # Package setup (optional)
└── README.md             # Documentation (optional)

## Project Documentation

# Tracsis CLI Tool

A command-line interface for interacting with the Tracsis API.

## Project Structure

tracsis-cmd/
├── tracsis_cli.py         # Main CLI script
├── tracsis_api.py         # API interaction logic
├── command_handlers.py    # Command handlers for CLI
├── requirements.txt       # Dependencies
├── setup.py               # Package setup
└── README.md              # Documentation

## Building and Installing the CLI Tool

You can build and install the CLI tool globally using setuptools. This allows you to run the `tracsis` command from anywhere on your system.

### 1. Build and Install (All Platforms)

#### Using pip (Recommended)

```bash
pip install .
```
#### macOS/Linux
You may need to use sudo for global installation
```bash
sudo pip install .
```
#### Windows
```bash
py -m pip install .
```

To check where the CLI is installed:(Linux/macOS)
```bash
which tracsis
```
(Windows)
```bash
where tracsis
```

### 2. Install Dependencies

1. Clone/download this project
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python tracsis_cli.py login`

## Usage

```bash
# Firstly, Set credentials only one time
python tracsis_cli.py set-creds

# Get task list
python tracsis_cli.py tasks

# Get logs for a specific task
python tracsis_cli.py logs <task_id>

# Take screenshot of a task page
python tracsis_cli.py snap <task_id>

# Fetch git commits for a username
python tracsis_cli.py genlog <git_username> --path <repo_path>

# Create a new task
python tracsis_cli.py create-task
```

## Troubleshooting

### Common Issues:

1. **Python not found**: Make sure Python is installed and added to PATH
2. **Permission denied**: On Unix systems, run `chmod +x tracsis_cli.py`
3. **Module not found**: Make sure virtual environment is activated and dependencies are installed
4. **Network errors**: Check internet connection and API endpoint availability

