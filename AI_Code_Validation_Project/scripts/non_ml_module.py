import subprocess
import json

def run_bandit(file_path):
    result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)
    if result.stdout:
        return json.loads(result.stdout)["results"]
    else:
        return []
