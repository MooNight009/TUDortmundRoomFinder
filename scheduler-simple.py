import time
import subprocess

# Path to the Python executable
python_executable = r"C:\Users\aamaj\PycharmProjects\RoomFinder\.venv\Scripts\python.exe"  # Update with your Python path
# Path to the script you want to run
script_path = r"C:\Users\aamaj\PycharmProjects\RoomFinder\new_rooms.py"  # Update with your script path

while True:
    # Run the script
    subprocess.run([python_executable, script_path])

    # Wait for 3 minutes (180 seconds)
    time.sleep(30)