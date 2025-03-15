from django.urls import resolve
import requests

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
        response = requests.post(url, json=log_data, timeout=2)
        response.raise_for_status()
    except requests.RequestException:
        pass  # Ignore failures to avoid impacting app performance
