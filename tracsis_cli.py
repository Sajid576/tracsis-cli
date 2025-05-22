#!/usr/bin/env python3
"""
Tracsis Command Line Tool
A CLI tool for interacting with the Tracsis API
"""

import argparse
import requests
import json
import sys
from typing import Dict, Any


class TracsisAPI:
    """Handle Tracsis API interactions"""
    
    BASE_URL = "https://tracsisapi.apsissolutions.com/api/v1"
    
    def __init__(self):
        self.session = requests.Session()
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def login(self, user: str, password: str) -> Dict[Any, Any]:
        """
        Authenticate with the Tracsis API
        
        Args:
            user: Username for authentication
            password: Password for authentication
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "user": user,
            "password": password
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Request failed: {str(e)}",
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
        except json.JSONDecodeError:
            return {
                "error": True,
                "message": "Invalid JSON response from server",
                "status_code": response.status_code,
                "raw_response": response.text
            }


def handle_login(args):
    """Handle the login command"""
    api = TracsisAPI()
    
    # Use the hardcoded credentials as specified
    user = "abu.syeed@apsissolutions.com"
    password = "123456"
    
    print(f"Attempting to login as {user}...")
    response = api.login(user, password)
    
    # Pretty print the response
    print(json.dumps(response, indent=2))
    
    # Exit with error code if login failed
    if response.get('error'):
        sys.exit(1)


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