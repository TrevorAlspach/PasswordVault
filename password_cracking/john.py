import subprocess
import os
import sys
import time

path_to_john = None
path_to_password = f"{os.getcwd()}/password_cracking/pass.txt"
path_to_wordlist = f"--wordlist={os.getcwd()}/password_cracking/wordlist.txt"

if sys.platform == "win32":
    path_to_john = f"{os.getcwd()}/password_cracking/john-1.9.0-jumbo-1/run/john.exe"

if sys.platform == "darwin" or sys.platform == "linux":
    path_to_john = f"{os.getcwd()}/password_cracking/john-1.9.0-jumbo-1/run/john"


# This will run John the Ripper as a subprocess. If the password provided is one of 10 million most common passwords, returns True. Else returns False

def run_john_wordlist(hash_type, password):
    subprocess.run([path_to_john, "--format=Raw-SHA256", path_to_wordlist,
                    path_to_password]) #capture_output=True)
    # remove the found passwords to allow for consistent output from JTR
    # If the size of the found passwords file not zero, password was found
    if os.stat(f"{os.getcwd()}/password_cracking/john-1.9.0-jumbo-1/run/john.pot").st_size != 0:
        open(
            f"{os.getcwd()}/password_cracking/john-1.9.0-jumbo-1/run/john.pot", "w").close()
        return True

    return False
