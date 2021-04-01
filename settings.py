import os
from dotenv import load_dotenv
load_dotenv()

HOME_LATITUDE = float(os.getenv("HOME_LATITUDE"))
HOME_LONGITUDE = float(os.getenv("HOME_LONGITUDE"))
STATE = os.getenv("STATE")
DISTANCE_THRESHOLD_MILES = int(os.getenv("DISTANCE_THRESHOLD_MILES", 50))
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", 20))

CUB_COOKIE = os.getenv("CUB_COOKIE")
CUB_SEARCH_DAYS = os.getenv("CUB_SEARCH_DAYS", 7)
