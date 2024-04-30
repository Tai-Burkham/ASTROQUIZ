import os
import subprocess

# Get the absolute path of the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the script you want to run
relative_path = "Game Files/main.py"

# Construct the absolute path
script_path = os.path.join(current_dir, relative_path)


try:
    # Change the working directory to the directory containing the script
    os.chdir(os.path.dirname(script_path))
    
    # Call the script using subprocess
    subprocess.run(["python", os.path.basename(script_path)], check=True)
except subprocess.CalledProcessError as e:
    print("Error:", e)
