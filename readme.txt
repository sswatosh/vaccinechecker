Setup
-----
1. Install python 3.8 or later: https://www.python.org/downloads/
2. Change to the root directory of the project
3. Create a virtual environment:
     python3 -m venv ./venv
4. Activate virtual environment (platform specific): https://docs.python.org/3/library/venv.html
5. Install requirements:
     pip install -r requirements.txt
6. Create a settings file in the root project directory, named ".env"
7. In the settings file, enter values for the following settings:
   - HOME_LATITUDE and HOME_LONGITUDE: the coordinates to search around (right-click in google maps to copy both)
   - STATE: two-letter abbreviation for the state to retrieve results from
   - DISTANCE_THRESHOLD_MILES (optional): The maximum distance from the coordinates to consider. Defaults to 50 miles.
   - CHECK_INTERVAL_SECONDS (optional): The frequency to retrieve data. Defaults to 20 seconds.

   example .env contents:
HOME_LATITUDE=40.89,
HOME_LONGITUDE=-98.23
STATE=NE


Running
-------
From the project directory, and with the virtual environment activated, run:
  python3 checker.py

When new appointments show up on vaccinechecker.org, the program will output a text summary of the
appointments, and open a browser window to the relevant scheduling site for each location.
