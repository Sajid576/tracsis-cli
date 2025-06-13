#!/usr/bin/env python3
"""
Tracsis Command Line Tool
A CLI tool for interacting with the Tracsis API
"""

import argparse
import sys
from command_handlers import handle_login, handle_task_list, handle_task_logs, handle_snap, handle_gen_log, handle_set_credentials

def create_login_parser(subparsers):
    login_parser = subparsers.add_parser('login', help='Login to Tracsis API')
    login_parser.set_defaults(func=handle_login)
    return login_parser

def create_tasks_parser(subparsers):
    task_parser = subparsers.add_parser('tasks', help='Get task list from Tracsis API')
    task_parser.add_argument('--user-id', type=int, default=6010, help='User ID to filter tasks for (default: 6010)')
    task_parser.add_argument('--page', type=int, default=1, help='Page number for pagination (default: 1)')
    task_parser.add_argument('--per-page', type=int, default=10, help='Number of items per page (default: 10)')
    task_parser.set_defaults(func=handle_task_list)
    return task_parser

def create_logs_parser(subparsers):
    logs_parser = subparsers.add_parser('logs', help='Get logs for a specific task')
    logs_parser.add_argument('task_id', type=int, help='Task ID to fetch logs for')
    logs_parser.add_argument('--page', type=int, default=1, help='Page number for pagination (default: 1)')
    logs_parser.add_argument('--per-page', type=int, default=10, help='Number of items per page (default: 10)')
    logs_parser.set_defaults(func=handle_task_logs)
    return logs_parser

def create_snap_parser(subparsers):
    snap_parser = subparsers.add_parser('snap', help='Take screenshot of task page in headless mode')
    snap_parser.add_argument('task_id', type=int, help='Task ID to take screenshot for')
    snap_parser.set_defaults(func=handle_snap)
    return snap_parser

def create_genlog_parser(subparsers):
    git_parser = subparsers.add_parser('genlog', help='Fetch git commits for a username in specified path')
    git_parser.add_argument('username', type=str, help='Git username to fetch commits for')
    git_parser.add_argument('--path', type=str, default='./', help='Path to search for git repositories (default: current directory)')
    git_parser.set_defaults(func=handle_gen_log)
    return git_parser

def create_set_creds_parser(subparsers):
    set_creds_parser = subparsers.add_parser('set-creds', help='Set credentials in config.json')
    set_creds_parser.set_defaults(func=handle_set_credentials)
    return set_creds_parser

def setup_parsers():
    parser = argparse.ArgumentParser(description='Tracsis CLI Tool', prog='tracsis')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    create_login_parser(subparsers)
    create_tasks_parser(subparsers)
    create_logs_parser(subparsers)
    create_snap_parser(subparsers)
    create_genlog_parser(subparsers)
    create_set_creds_parser(subparsers)
    
    return parser

def main():
    """Main entry point for the CLI"""
    parser = setup_parsers()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == '__main__':
    main()
    
   
   