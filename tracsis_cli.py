#!/usr/bin/env python3
"""
Tracsis Command Line Tool
A CLI tool for interacting with the Tracsis API
"""

import argparse
import sys
from command_handlers import handle_login, handle_task_list, handle_task_logs,handle_snap,handle_gen_log    

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description='Tracsis CLI Tool',
        prog='tracsis'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to Tracsis API')
    login_parser.set_defaults(func=handle_login)
    
    # Task list command
    task_parser = subparsers.add_parser('tasks', help='Get task list from Tracsis API')
    task_parser.add_argument(
        '--user-id', 
        type=int, 
        default=6010, 
        help='User ID to filter tasks for (default: 6010)'
    )
    task_parser.add_argument(
        '--page', 
        type=int, 
        default=1, 
        help='Page number for pagination (default: 1)'
    )
    task_parser.add_argument(
        '--per-page', 
        type=int, 
        default=10, 
        help='Number of items per page (default: 10)'
    )
    task_parser.set_defaults(func=handle_task_list)
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Get logs for a specific task')
    logs_parser.add_argument(
        'task_id',
        type=int,
        help='Task ID to fetch logs for' 
    )
    logs_parser.add_argument(
        '--page',
        type=int,
        default=1,
        help='Page number for pagination (default: 1)'
    )
    logs_parser.add_argument(
        '--per-page',
        type=int,
        default=10,
        help='Number of items per page (default: 10)'
    )
    logs_parser.set_defaults(func=handle_task_logs)
    
    # Log work command
    log_parser = subparsers.add_parser('log', help='Log work for a task')
    log_parser.add_argument(
        'task_id',
        type=int,
        help='Task ID to log work for'
    )
    log_parser.add_argument(
        'status',
        choices=['i', 'c'],
        help='Task status: i=in_progress, c=completed'
    )
    log_parser.set_defaults(func=handle_task_logs)
    
    # Snap command
    snap_parser = subparsers.add_parser('snap', help='Take screenshot of task page in headless mode')
    snap_parser.add_argument(
        'task_id',
        type=int,
        help='Task ID to take screenshot for'
    )
    snap_parser.set_defaults(func=handle_snap)
    
    # Git commits command
    git_parser = subparsers.add_parser('genlog', help='Fetch git commits for a username in specified path')
    git_parser.add_argument(
        'username',
        type=str,
        help='Git username to fetch commits for'
    )
    git_parser.add_argument(
        '--path',
        type=str,
        default='./',
        help='Path to search for git repositories (default: current directory)'
    )
    git_parser.set_defaults(func=handle_gen_log)
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the appropriate function
    args.func(args)

if __name__ == '__main__':
    main()