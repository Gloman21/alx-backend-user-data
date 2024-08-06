#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """
    Class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if the given `path` is excluded from authentication based on
        the list of `excluded_paths`.
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
            if excluded_path.startswith(path):
                return False
            if fnmatch.fnmatchcase(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the given request object.
        """
        if request is None:
            return None
        if request.headers.get('Authorization', None) is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the given request.
        """
        return None