#!/usr/bin/env python3
"""
Tracsis API Client
Handles all API interactions with the Tracsis backend
"""

import requests
import json
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
        self.access_token = None
        self.refresh_token = None
    
    def set_tokens(self, access_token: str, refresh_token: str):
        """Set authentication tokens"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        # Update session headers with Bearer token
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
        })
    
    def is_authenticated(self) -> bool:
        """Check if API client is authenticated"""
        print(f"Access Token: {self.access_token}")
        print(f"Refresh Token: {self.refresh_token}")
        return self.access_token is not None and self.refresh_token is not None
    
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
        
        print("\nLogin Request:")
        print(f"URL: {url}")
        print(f"Headers: {self.session.headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}\n")
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if not result.get('error', True) and 'data' in result:
                data = result['data']
                if 'access_token' in data and 'refresh_token' in data:
                    self.set_tokens(data['access_token'], data['refresh_token'])
            
            return result
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
    
    def get_task_list(self, user_id: int = 6010, page: int = 1, per_page: int = 10) -> Dict[Any, Any]:
        """
        Get task list from the Tracsis API
        
        Args:
            user_id: User ID to filter tasks for (default: 6010)
            page: Page number for pagination (default: 1)
            per_page: Number of items per page (default: 10)
            
        Returns:
            API response as dictionary
        """
        if not self.is_authenticated():
            return {
                "error": True,
                "message": "Not authenticated. Please login first.",
                "status_code": 401
            }
        
        url = f"{self.BASE_URL}/master-grid/grid-data"
        payload = {
            "slug": "pts_my_tasks",
            "extra": {
                "extra_condition": f"pts_tasks.assign_user_id = {user_id}"
            },
            "page": page,
            "per_page": per_page,
            "search_key": {},
            "search_data": []
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
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
    
    def get_task_logs(self, task_id: int, page: int = 1, per_page: int = 10) -> Dict[Any, Any]:
        """Get logs for a specific task from the Tracsis API
        
        Args:
            task_id: Task ID to fetch logs for
            page: Page number for pagination (default: 1)
            per_page: Number of items per page (default: 10)
            
        Returns:
            API response as dictionary
        """
        if not self.is_authenticated():
            return {
                "error": True,
                "message": "Not authenticated. Please login first.",
                "status_code": 401
            }
        
        url = f"{self.BASE_URL}/master-grid/grid-data"
        payload = {
            "slug": "pts_my_logs",
            "extra": {},
            "page": page,
            "per_page": per_page,
            "search_key": {},
            "search_data": []
        }

        print("\nTask Logs Request:")
        print(f"URL: {url}")
        print(f"Headers: {self.session.headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}\n")
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
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
    
    def log_task_work(self, task_id: int, status: str, work_title: str, work_date: str, log_hour: float) -> Dict[Any, Any]:
        """Log work for a task

        Args:
            task_id: ID of the task to log work for
            status: Task status ('i' for in_progress or 'c' for completed)
            work_title: Title of the work done
            work_date: Date of the work in ISO format
            log_hour: Number of hours worked

        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}/pts/task/log"

        # Convert status to task_status number
        task_status = 3 if status == 'c' else 4

        payload = {
            "role_id": 2,
            "task_status": task_status,
            "task_id": task_id,
            "work": [
                {
                    "key": 0,
                    "work_title": work_title,
                    "work_date": work_date,
                    "work_type": "Development",
                    "log_hour": log_hour,
                    "log_details": None
                }
            ]
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Request failed: {str(e)}",
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }