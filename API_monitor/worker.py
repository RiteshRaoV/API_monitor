# apimonitor/worker.py
import queue
import threading
from .config import APIMonitorConfig
from .utils import send_log

log_queue = queue.Queue()

def log_worker():
    """Background worker to send logs to server."""
    while True:
        log_data = log_queue.get()
        if log_data is None:
            break
        try:
            send_log(log_data, APIMonitorConfig.TRACKING_SERVER_URL)
        except Exception:
            pass  # optionally log locally
        finally:
            log_queue.task_done()

# Start worker
worker_thread = threading.Thread(target=log_worker, daemon=True)
worker_thread.start()

def enqueue_log(log_data):
    """Public function to push logs into the queue."""
    log_queue.put(log_data)
