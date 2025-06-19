import json
from django.urls import resolve
import requests

from .config import APIMonitorConfig
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

def encrypt_payload(payload):
    # Decode the base64 key
    key = base64.b64decode(APIMonitorConfig.ENCRYPTION_KEY)

    # Validate key size (16, 24, or 32 bytes)
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid AES key size. Must be 16, 24, or 32 bytes.")

    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Convert payload to bytes
    data = json.dumps(payload).encode('utf-8')

    # Add padding to the data
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create cipher and encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Return IV + encrypted data (Base64 encoded for transport)
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

def extract_app_name(request):
    """
    Extracts the app name from the Django view function or class-based view.
    Supports function-based views, class-based views, DRF views, and nested views.
    """
    try:
        resolver_match = resolve(request.path)

        view_func = resolver_match.func

        if hasattr(view_func, "view_class"):  # CBVs & DRF APIViews
            module_path = view_func.view_class.__module__
        else:
            module_path = view_func.__module__

        app_name = module_path.split('.')[0]  # Extract app name from module path
        return app_name
    except Exception:
        return None  # Return None if resolution fails

def send_log(log_data,url):
    """ Sends API monitoring data to the tracking server. """
    try:
        access_key = log_data.get("access_key")
        encrypted_log_data = encrypt_payload(log_data)
        log_data = {
            "access_key" : access_key,
            "log_data":encrypted_log_data
        }
        response = requests.post(url, json=log_data, timeout=2)
        response.raise_for_status()
    except requests.RequestException:
        pass
