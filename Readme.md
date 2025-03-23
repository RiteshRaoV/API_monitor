# API Monitor SDK

## Overview

The **API Monitor SDK** is a Django middleware package that logs API request and response details, including latency, database execution time, request headers, user details, and more. This helps in monitoring API performance and detecting anomalies in real time.

## Features

- Tracks API latency and database execution time.
- Logs request headers, query parameters, and response size.
- Identifies the authenticated user making the request.
- Monitors CPU and memory usage per request.
- Detects potential abuse attempts.
- Sends logs asynchronously to a remote monitoring server.

## Installation

### Install via Git

```bash
pip install git+https://github.com/RiteshRaoV/API_monitor.git
```

### Install Locally (For Development)

```bash
pip install -e .
```

Ensure `setuptools` and `wheel` are installed:

```bash
pip install --upgrade setuptools wheel
```

## Setup

### 1. Add Middleware

In your `settings.py`, add the middleware:

```python
MIDDLEWARE = [
    ...
    'API_monitor.middleware.APIMonitorMiddleware',
]
```
### 2. Add Configurations

In your application's `settings.py`, update your configurations:

```python
from api_monitor import initialize_monitoring

initialize_monitoring(
    secret_key="agdffgakghffah",
    tracking_server_url = "http://your-tracking-server-url",
    monitored_apps=["TEST"],
    rate_limit_threshold = 100,
    tags=["high-priority"]
)
```

## Usage

Once the middleware is enabled and sdk is initialized, the SDK automatically logs API activity for the configured apps.

### Example log:

```json
{
  "secret_key": "agdffgakghffah",
  "app_name": "TEST",
  "tags": ["high-priority"],
  "endpoint": "/get-details/",
  "method": "GET",
  "status_code": 200,
  "latency": 53.81,
  "db_execution_time": 16.0,
  "response_size": 576,
  "timestamp": "2025-03-15 12:59:32",
  "request_headers": {
    "Content-Length": "",
    "Content-Type": "text/plain",
    "Host": "localhost:8080",
    "Connection": "keep-alive",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "X-Csrftoken": "KonpuBi8ychomsuFPJymknoRRt6TsyMHbuz6SCh1AhUP8NTUujqcJenSlmOkHQB7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Sec-Ch-Ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "http://localhost:8080/swagger/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "JSESSIONID=EFFD42A91D6A0061089026849713882A; csrftoken=BgmRyb93cfNBWvzpPK20z19bE3SBpsZA"
  },
  "query_params": {},
  "user": "Anonymous",
  "client_ip": "127.0.0.1",
  "location": "Unknown",
  "cpu_usage": 0.0,
  "memory_usage": 86.5,
  "abuse_detected": null,
  "error": null
}

```

## Contributing

1. Fork the repository.
2. Clone your fork.
   ```bash
   git clone https://github.com/RiteshRaoV/api-monitor.git
   ```
3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Create a feature branch, make changes, and submit a PR.

## License

MIT License

## Author

Developed by [Ritesh x ChatGPT](https://github.com/RiteshRaoV)

