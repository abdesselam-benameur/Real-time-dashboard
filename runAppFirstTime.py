import os
import subprocess

# Fill th database with real time data since it's the first time
# and install the required packages

# if we are in windows
if os.name == 'nt':
    os.system("python real_time_data.py")
    os.system("pip install -r requirements.txt")
# if we are in linux
else:
    os.system("python3 real_time_data.py")
    os.system("pip3 install -r requirements.txt")

os.system("streamlit run 🏠_Home.py")
