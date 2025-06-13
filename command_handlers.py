#!/usr/bin/env python3
"""Command handlers for the Tracsis CLI"""

import json
import sys
import os
from tracsis_api import TracsisAPI
import readline

# Global API instance to maintain session and tokens across commands
api_instance = None

def load_config():
    """Load configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your credentials.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not a valid JSON file.")
        sys.exit(1)

def get_api_instance():
    """Get or create the global API instance"""
    global api_instance
    if api_instance is None:
        api_instance = TracsisAPI()
    return api_instance

def handle_login(args):
    """Handle the login command"""
    api = get_api_instance()
    
    # Load credentials from config file
    config = load_config()
    user = config['credentials']['user']
    password = config['credentials']['password']
    
    print(f"Attempting to login as {user}...")
    response = api.login(user, password)
    
    # Pretty print the response
    print(json.dumps(response, indent=2))
    
    # Show authentication status
    if not response.get('error', True) and api.is_authenticated():
        print(f"\n✓ Login successful! Tokens have been stored for subsequent API calls.")
        print(f"✓ Access token: {api.access_token[:20]}...")
        print(f"✓ Refresh token: {api.refresh_token}")
    else:
        print(f"\n✗ Login failed!")
        sys.exit(1)

def handle_task_list(args):
    """Handle the task list command"""
    api = get_api_instance()
    
    # Check if user is logged in, if not, perform login first
    if not api.is_authenticated():
        print("Not authenticated. Performing login first...")
        config = load_config()
        user = config['credentials']['user']
        password = config['credentials']['password']
        
        login_response = api.login(user, password)
        
        if login_response.get('error', True):
            print("Login failed!")
            print(json.dumps(login_response, indent=2))
            sys.exit(1)
        print("Login successful!\n")
    
    user_id = args.user_id
    page = args.page
    per_page = args.per_page
    
    response = api.get_task_list(user_id, page, per_page)
    
    if response.get('error'):
        print('Error fetching tasks:')
        print(json.dumps(response, indent=2))
        sys.exit(1)

    # Get the tasks from response and reverse them to show latest first
    tasks = response.get('data', {}).get('items', [])

    # Clear screen and move cursor to top
    print('\033[2J\033[H', end='')
    
    # Print each task in a formatted way
    current_task = 0
    while current_task < len(tasks):
        task = tasks[current_task]
        print('\033[1;33m' + '=' * 80 + '\033[0m')  # Yellow separator
        print(f'\033[1;36mTask ID:\033[0m {task.get("hidden_task_id")}')
        print(f'\033[1;36mTitle:\033[0m {task.get("task_title")}')
        print(f'\033[1;36mProject:\033[0m {task.get("project_name")}')
        print(f'\033[1;36mDelivery Date:\033[0m {task.get("formatted_date")}')
        print(f'\033[1;36mEstimated Hours:\033[0m {task.get("estimated_hour")}')
        print(f'\033[1;36mTask Type:\033[0m {task.get("module_name")}')
        print('\033[1;33m' + '=' * 80 + '\033[0m\n')  # Yellow separator

        # Wait for user input
        user_input = input('Press Enter to continue, q to quit...')
        if user_input.lower() == 'q':
            break
        
        current_task += 1
        if current_task < len(tasks):
            # Clear screen for next task
            print('\033[2J\033[H', end='')

def handle_task_logs(args):
    """Handle the task log command"""
    api = get_api_instance()

    # Check if user is logged in
    if not api.is_authenticated():
        print("Not authenticated. Performing login first...")
        config = load_config()
        user = config['credentials']['user']
        password = config['credentials']['password']
        
        login_response = api.login(user, password)
        
        if login_response.get('error', True):
            print("Login failed!")
            print(json.dumps(login_response, indent=2))
            sys.exit(1)
        print("Login successful!\n")

    # Example of setting a specific completer for work title
    def work_title_completer(text, state):
        options = [
            'Development',
            'Code Review',
            'Testing',
            'Documentation',
            'Meeting'
        ]
        matches = [i for i in options if i.startswith(text)]
        return matches[state] if state < len(matches) else None

    # Save the original completer
    original_completer = readline.get_completer()
    readline.set_completer(work_title_completer)
    
    work_title = input("title> ")
    
    # Restore the original completer
    readline.set_completer(original_completer)
    
    # Get current date as default value in YYYY/MM/DD format
    from datetime import datetime
    default_date = datetime.now().strftime('%Y/%m/%d')
    work_date = input(f"date> [{default_date}] ") or default_date
    
    log_hour = float(input("log_hour> "))

    response = api.log_task_work(
        task_id=args.task_id,
        status=args.status,
        work_title=work_title,
        work_date=work_date,
        log_hour=log_hour
    )

    if response.get('error'):
        print('Error logging task work:')
        print(json.dumps(response, indent=2))
        sys.exit(1)

    print("\n✓ Work logged successfully!")
      
    # Exit with error code if request failed
    if response.get('error'):
        sys.exit(1)


def setup_autocomplete():
    """Setup auto-completion for the CLI"""
    def completer(text, state):
        # Define your completion options here
        options = [
            'login',
            'task-list',
            'task-logs',
            # Add more commands as needed
         ]
        
        matches = [i for i in options if i.startswith(text)]
        if state < len(matches):
            return matches[state]
        else:
            return None

    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer)


def handle_snap(args):
    """Handle the snap command with improved login verification"""
    print("\nTaking screenshot...")
    task_id = args.task_id
    
    config = load_config()
    user = config['credentials']['user']
    password = config['credentials']['password']
    
    # Import Selenium components
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    print("\nOpening browser in headless mode...")
    
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # First login to the web interface
        driver.get("https://tracsis.apsissolutions.com/signin")
        
        email_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='email']"))  # Wait for clickable, not just present
        )
        # email_field.clear()  # Clear any existing text
        
        email_field.send_keys(user)

        password_field = WebDriverWait(driver, 10).until(  # Wait for password field too
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='password']"))
        )
        
        # password_field.clear()  # Clear any existing text
        password_field.send_keys(password)

    # Add a small delay to ensure fields are populated
        import time
        time.sleep(1)

        # Verify fields have values before submitting
        if email_field.get_attribute('value') and password_field.get_attribute('value'):
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            print('user:', email_field.get_attribute('value'))
            print('password:', password_field.get_attribute('value'))
            submit_button.click()
            print("Login In Progress.....")
        else:
            print("Fields not properly filled!")
            print(f"Email field value: '{email_field.get_attribute('value')}'")
            print(f"Password field value: '{password_field.get_attribute('value')}'")

    
        
        WebDriverWait(driver, 10).until(
            EC.url_matches(r"https://tracsis\.apsissolutions\.com/(?!signin).*")
        )
        print("Successfully navigated to post-login page")
        # Now navigate to task page
        task_url = f"https://tracsis.apsissolutions.com/pts/my-task/tasks/view/{task_id}?parent=my-task"
        driver.get(task_url)
        
        # Verify we reached the task page
        modal_close_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-table-container"))
            )
        
        modal_close_button.click()
        print("Successfully reached task page")
            
        # Final screenshot
        element = driver.find_element(By.CSS_SELECTOR, ".ant-table")
        desired_height = 1200  # pixels
        driver.execute_script(f"arguments[0].style.height = '{desired_height}px';", element)
        driver.execute_script("arguments[0].style.overflow = 'hidden';", element)  # Hide overflow

        # Wait for changes to apply
        import time
        time.sleep(1)
        screenshot_path = f"task_{task_id}_screenshot.png"
        element.screenshot(screenshot_path)
        print(f"\nFinal screenshot saved as: {screenshot_path}")
        
    except Exception as e:
        print(f"Error during screenshot process: {str(e)}")
        raise
    finally:
        driver.quit()


def handle_gen_log(args):
    """Handle git commits command"""
    from datetime import datetime
    import subprocess
    import os
    import csv
    
    username = args.username
    path = os.path.abspath(args.path)  # Get absolute path
    date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Fetching git commits for user {username} in {path} on {date}...")
    
    try:
        # Verify path exists
        if not os.path.exists(path):
            print(f"Error: Path {path} does not exist")
            sys.exit(1)
            
        # Find all git repositories in subdirectories
        find_cmd = f"find {path} -type d -name .git | sed 's/\.git$//'"
        repos = subprocess.run(find_cmd, shell=True, check=True, capture_output=True, text=True).stdout.splitlines()
        
        if not repos:
            print(f"No git repositories found in {path}")
            return
            
        original_dir = os.getcwd()  # Save original directory
        
        # Create CSV file
        csv_filename = f"git_commits_{username}_{date}.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['title', 'date', 'log_hour'])
            
            for repo in repos:
                repo_path = os.path.abspath(repo)  # Get absolute path
                print(f"\nCommits in {repo_path}:")
                
                try:
                    os.chdir(repo_path)
                    
                    # Get commits for this repository
                    cmd = f"git log --all --author={username} --since='{date} 00:00:00' --until='{date} 23:59:59' --pretty=format:'%h - %an, %ar : %s'"
                    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

                    if len(result.stdout) > 0:
                        commit_message = result.stdout
                        print(commit_message)
                        
                        # Parse commit messages and write to CSV
                        for line in commit_message.split('\n'):
                            if ':' in line:
                                title = line.split(':')[-1].strip()
                                # Default to 1 hour for each commit
                                writer.writerow([title, date, 1.0])
                
                except FileNotFoundError:
                    print(f"Warning: Could not access repository at {repo_path}")
                    continue
                    
                finally:
                    # Always return to original directory
                    os.chdir(original_dir)
        
        print(f"\nCSV file generated: {csv_filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching git commits: {e.stderr}")
        sys.exit(1)