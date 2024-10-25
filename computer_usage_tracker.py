import time
import socket
import pymongo
import datetime
from dotenv import load_dotenv
import os

# MongoDB Atlas Connection
client = pymongo.MongoClient("mongodb+srv://yakubuanas04:KOFEiHoWAUS2J0Zy@cluster0.z5fnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['computer_usage_db']
collection = db['usage_records']

# Function to get the current timestamp
def get_timestamp():
    return datetime.datetime.now()

# Function to check if connected to the internet
def is_connected():
    try:
        socket.gethostbyname("www.google.com")
        return True
    except socket.error:
        return False

# Function to log time spent on the computer in hours, minutes, and seconds
def log_time_spent(start_time, end_time):
    # Calculate time spent as a timedelta
    time_spent = end_time - start_time
    
    # Extract hours, minutes, and seconds from timedelta
    hours, remainder = divmod(time_spent.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    record = {
        'date': start_time.date(),
        'start_time': start_time,
        'end_time': end_time,
        'time_spent': {
            'hours': int(hours),
            'minutes': int(minutes),
            'seconds': int(seconds)
        }
    }

    collection.insert_one(record)
    print(f"Record saved: {record}")

# Main function to track and log computer usage every 10 minutes
def track_usage():
    start_time = None
    accumulated_time = 0  # Tracks time in seconds

    try:
        while True:
            if is_connected():
                if start_time is None:
                    start_time = get_timestamp()
                    print(f"Internet connected. Tracking started at: {start_time}")
                else:
                    accumulated_time += 10  # Add 10 seconds to accumulated time
                    if accumulated_time >= 600:  # Check if 10 minutes (600 seconds) have passed
                        end_time = get_timestamp()
                        log_time_spent(start_time, end_time)
                        start_time = get_timestamp()  # Reset start time for the next interval
                        accumulated_time = 0  # Reset accumulated time
                    print("Internet is connected; tracking continues...")
            else:
                if start_time:
                    end_time = get_timestamp()
                    print(f"Internet disconnected at: {end_time}. Logging usage.")
                    log_time_spent(start_time, end_time)
                    start_time = None
                    accumulated_time = 0  # Reset accumulated time
                else:
                    print("Waiting for internet connection...")

            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        if start_time:
            end_time = get_timestamp()
            log_time_spent(start_time, end_time)
        print("Tracking stopped.")

# Run the script
if __name__ == "__main__":
    track_usage()
