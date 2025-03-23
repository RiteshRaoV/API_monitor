from .config import APIMonitorConfig
from .middleware import APIMonitorMiddleware

def initialize_monitoring(secret_key,encryption_key,tracking_server_url, monitored_apps,rate_limit_threshold, tags=None):
    """
    Initializes the API monitoring SDK.
    :param secret_key: Unique key for authentication with the tracking server.
    :param monitored_apps: List of Django apps to track.
    :param tags: Optional tags for categorization.
    """
    APIMonitorConfig.initialize(secret_key,encryption_key,tracking_server_url, monitored_apps,rate_limit_threshold, tags)
