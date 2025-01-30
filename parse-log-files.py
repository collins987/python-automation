#This script automates log monitoring by collecting critical system and application logs, extracting error messages, categorizing them by log file, and saving them in an `errors.log` file for troubleshooting. It helps system administrators quickly identify and diagnose issues in a Linux environment.
import shutil
import os

# Define log files and their target names
logs = {
    "/var/log/syslog": "system.log",
    "/var/log/auth.log": "authentication.log",
    "/var/log/kern.log": "kernel.log",
    "/var/log/apache2/error.log": "apache.log",
    "/var/log/nginx/error.log": "nginx.log",
    "/var/log/mysql/error.log": "mysql.log",
    os.path.expanduser("~/.xsession-errors"): "user.log"
}

# List to store available log files
available_log_files = []

# Function to collect logs
def collect_logs():
    for source, destination in logs.items():
        try:
            # Check if the log file exists
            if os.path.exists(source):  
                # copies file from source to destination location
                shutil.copy(source, destination)
                available_log_files.append(destination)
                print("Copying available log...")
                print(f"    Copied {source} to {destination}")
            else:
                print(f" {source} not found!...")
        except PermissionError:
            print(f"Permission denied: {source}. Try running as sudo!")
        except Exception as e:
            print(f"Error copying {source}: {e}")

# Function to parse logs and extract ERROR lines, grouping them by file
def parse_logs():
    print("\n*** Extracting 'ERROR' lines from logs... ***\n")
    error_data = {}

    for log_file in available_log_files:
        try:
            with open(log_file, 'r') as file:
                errors = [line.strip() for line in file if "ERROR" in line]
                
                if errors:
                    error_data[log_file] = errors
                    print(f"The following are errors found in {log_file}:")
                    for error in errors:
                        print(f"   ... {error}")
                    print("-" * 50)  # Separator for readability
                else:
                    print(f"No errors found in {log_file}...")

        except Exception as e:
            print(f" Error reading {log_file}: {e}")

    # Save errors to a separate file
    save_errors(error_data)

# Function to save errors to errors.log
def save_errors(error_data):
    with open("errors.log", "w") as error_file:
        for log_file, errors in error_data.items():
            error_file.write(f"=== Errors from {log_file} ===\n")
            for error in errors:
                error_file.write(f"{error}\n")
            error_file.write("\n" + "-" * 50 + "\n")
    
    print("\n*** All extracted errors have been saved to 'errors.log'. ***")

if __name__ == "__main__":
    collect_logs()  # Step 1: Collect logs
    parse_logs()    # Step 2: Parse logs for ERROR messages
