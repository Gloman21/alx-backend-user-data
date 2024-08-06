#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User
import base64
import binascii
from typing import List, TypeVar


class BasicAuth(Auth):
    """Basic Authentication Class"""

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        Extracts the Base64 encoded authorization header from the given header.
        """
        # Check if the authorization header is None
        if authorization_header is None:
            return None

        # Check if the authorization header is not a string
        if not isinstance(authorization_header, str):
            return None

        # Check if the authorization header starts with 'Basic '
        if not authorization_header.startswith('Basic '):
            return None

        # Extract and return the Base64 encoded authorization header
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Decodes a base64 encoded authorization header.
        """
        try:
            if base64_authorization_header is None:
                return None
            elif not isinstance(base64_authorization_header, str):
                return None
            utf8_encoded_string = base64_authorization_header.encode('utf-8')
            coded_string = base64.b64decode(utf8_encoded_string)
            return coded_string.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) ->(str, str):
        """
        Extracts the user email and password from the Base64 decoded
        value of the authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user, pwd = decoded_base64_authorization_header.split(':', 1)
        return user, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Validates the user credentials and returns the corresponding User
        object.
        """
        if user_email is None and not isinstance(user_email, str):
            return None
        if user_pwd is None and not isinstance(user_pwd, str):
            return None
        try:
            if User.count() == 0:
                return None
        except KeyError:
            return None
        current_user = User.search({'email': user_email})
        if not current_user or len(current_user) == 0:
            return None
        current_user = current_user[0]
        if current_user.is_valid_password(user_pwd):
            # print(f"{current_user.display_name()}+++++")
            return current_user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request headers.
        """
        header = self.authorization_header(request)
        base64_auth_h = self.extract_base64_authorization_header(
            header)
        decoded_auth_h = self.decode_base64_authorization_header(
            base64_auth_h)
        user_mail, user_pass = self.extract_user_credentials(
            decoded_auth_h)
        user_res = self.user_object_from_credentials(user_mail, user_pass)
        return user_res