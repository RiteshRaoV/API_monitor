class APIMonitorConfig:
    ACCESS_KEY = None
    ENCRYPTION_KEY = None
    TRACKING_SERVER_URL = None
    MONITORED_APPS = []
    TAGS = []
    RATE_LIMIT_THRESHOLD = None
    GEOIP_DB_PATH = "GeoLite2-City.mmdb"

    @classmethod
    def initialize(cls, access_key,encryption_key,tracking_server_url,monitored_apps,rate_limit_threshold, tags=None):
        cls.ENCRYPTION_KEY = encryption_key
        cls.ACCESS_KEY = access_key
        cls.TRACKING_SERVER_URL = tracking_server_url
        cls.MONITORED_APPS = monitored_apps
        cls.TAGS = tags or []
        cls.RATE_LIMIT_THRESHOLD = rate_limit_threshold
