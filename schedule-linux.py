import subprocess
import getpass
from datetime import datetime, timedelta

sudo_password = '483131'

hours = ['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']
hours = ['9']
mins = ['00', '15', '30', '45']
mins = list(range(30, 61, 3))


# def schedule_wake_event(hour, minute):
#     command = f'echo {sudo_password} | sudo -S pmset schedule wake "{date} {hour}:{minute}:00"'
#     subprocess.run(command, shell=True, check=True)
# print(command)


def schedule_wake_event(hour, minute):
    date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%Y')
    time = f"{hour}:{str(minute).zfill(2)}"  # Format time as HH:MM

    # Create the wake task using schtasks
    command = f'schtasks /create /tn "WakeUpTask_{hour}_{minute}" /tr "cmd.exe /c exit" /sc once /st {time} /sd {date} /f /ri 1 /it /z /ru SYSTEM'

    # Add /it and /ru SYSTEM to ensure the task runs with system privileges and without needing a password
    subprocess.run(command, shell=True, check=True)
    print(command)  # Print the command for debugging


if __name__ == '__main__':
    date = (datetime.now() + timedelta(days=1)).strftime('%m/%d/%y')

    for h in hours:
        for m in mins:
            schedule_wake_event(h, m)
