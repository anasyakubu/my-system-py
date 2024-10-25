import time
import socket
import pymongo
import datetime

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

# Function to log the hours spent on the computer
def log_hours_spent(start_time, end_time):
    total_time_spent = (end_time - start_time).total_seconds() / 3600  # convert seconds to hours
    
    record = {
        'date': start_time.date(),
        'start_time': start_time,
        'end_time': end_time,
        'hours_spent': round(total_time_spent, 2)
    }

    collection.insert_one(record)
    print(f"Record saved: {record}")

# Main function to track and log computer usage
def track_usage():
    start_time = None

    try:
        while True:
            if is_connected():
                if start_time is None:
                    start_time = get_timestamp()
                    print(f"Internet connected. Tracking started at: {start_time}")
                else:
                    print("Internet is connected; tracking continues...")
            else:
                if start_time:
                    end_time = get_timestamp()
                    print(f"Internet disconnected at: {end_time}. Logging usage.")
                    log_hours_spent(start_time, end_time)
                    start_time = None
                else:
                    print("Waiting for internet connection...")

            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        if start_time:
            end_time = get_timestamp()
            log_hours_spent(start_time, end_time)
        print("Tracking stopped.")

# Run the script
if __name__ == "__main__":
    track_usage()
