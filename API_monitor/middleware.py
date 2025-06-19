import time
import threading
import json
import psutil
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
import geoip2.database
from .config import APIMonitorConfig
from .utils import send_log,extract_app_name

# In-memory store for rate limiting
api_call_counts = {}

class APIMonitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        client_ip = request.META.get("REMOTE_ADDR", "Unknown")
        api_call_counts[client_ip] = api_call_counts.get(client_ip, 0) + 1
        return None

    def process_response(self, request, response):
        if APIMonitorConfig.ACCESS_KEY and APIMonitorConfig.MONITORED_APPS:
            app_name = extract_app_name(request)
            if app_name and app_name in APIMonitorConfig.MONITORED_APPS:
                latency = round((time.time() - request.start_time) * 1000, 2)
                db_time = sum(float(query["time"]) for query in connection.queries) * 1000
                response_size = len(response.content)
                client_ip = request.META.get("REMOTE_ADDR", "Unknown")
                user = str(request.user) if request.user.is_authenticated else "Anonymous"
                
                # GeoIP Lookup
                location = "Unknown"
                try:
                    reader = geoip2.database.Reader(APIMonitorConfig.GEOIP_DB_PATH)
                    geo_info = reader.city(client_ip)
                    location = f"{geo_info.city.name}, {geo_info.country.name}"
                except Exception:
                    pass
                
                # Check for potential abuse
                if APIMonitorConfig.RATE_LIMIT_THRESHOLD is not None:
                    abuse_detected = api_call_counts[client_ip] > APIMonitorConfig.RATE_LIMIT_THRESHOLD
                
                log_data = {
                    "access_key": APIMonitorConfig.ACCESS_KEY,
                    "log_data": {
                        "app_name": app_name,
                        "tags": APIMonitorConfig.TAGS,
                        "endpoint": request.path,
                        "method": request.method,
                        "status_code": response.status_code,
                        "latency": latency,
                        "db_execution_time": round(db_time * 1000, 2),
                        "response_size": response_size,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "request_headers": dict(request.headers),
                        "query_params": dict(request.GET),
                        "user": user,
                        "client_ip": client_ip,
                        "location": location,
                        "cpu_usage": psutil.cpu_percent(),
                        "memory_usage": psutil.virtual_memory().percent,
                        "abuse_detected": abuse_detected or None,
                        "error": response.content.decode()[:500] if response.status_code >= 400 else None,
                    }
                }
                threading.Thread(target=send_log, args=(log_data,APIMonitorConfig.TRACKING_SERVER_URL)).start()
        return response
