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

### Build and Install (All Platforms)

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
### Usage

```bash
# Firstly, Set credentials only one time
tracsis set-creds

# Get task list
tracsis tasks

# Create logs for a specific task
tracsis logs <task_id>

# Take screenshot of a task page
tracsis snap <task_id>

# Fetch git commits for a username
tracsis genlog <git_username> --path <repo_path>

# Create a new task
tracsis create-task
```

## Setup Guide for Development

### Prerequisites

- Python 3.7+
- Pip (Python package installer)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tracsis-cli.git
cd tracsis-cli
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Firstly, Set credentials only one time
python tracsis_cli.py set-creds

# Get task list
python tracsis_cli.py tasks

# Create logs for a specific task
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

