import subprocess
import webbrowser
import time
import os

script = "dashboard.py"

process = subprocess.Popen(
    ["streamlit", "run", script, "--server.headless=true"]
)

time.sleep(2)

webbrowser.open("http://localhost:8501")

process.wait()