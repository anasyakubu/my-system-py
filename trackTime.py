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
        # Try to resolve hostname -- tells us if we're connected to the internet
        socket.gethostbyname("www.google.com")
        return True
    except socket.error:
        return False

# Function to log the hours spent on the computer
def log_hours_spent(start_time, end_time):
    # Calculate total time spent in hours
    total_time_spent = (end_time - start_time).total_seconds() / 3600  # convert seconds to hours
    
    # Create a record for the database
    record = {
        'date': start_time.date(),  # Log the date
        'start_time': start_time,
        'end_time': end_time,
        'hours_spent': round(total_time_spent, 2)  # Save hours with 2 decimal places
    }

    # Save the record to the MongoDB database
    collection.insert_one(record)
    print(f"Record saved: {record}")

# Main function to track and log computer usage
def track_usage():
    # Start time when the computer is turned on or script begins running
    start_time = get_timestamp()
    print(f"Computer usage started at: {start_time}")

    try:
        while True:
            # Check every 10 seconds if the computer is connected to the internet
            time.sleep(10)
            if is_connected():
                # End time when connecting to the internet
                end_time = get_timestamp()
                print(f"Connected to the internet at: {end_time}")
                
                # Log the time spent on the computer and save it to the database
                log_hours_spent(start_time, end_time)
                
                # Reset the start time after logging
                start_time = get_timestamp()
    except KeyboardInterrupt:
        # If the script is stopped manually, log the current session
        end_time = get_timestamp()
        log_hours_spent(start_time, end_time)
        print("Tracking stopped.")

# Run the script
if __name__ == "__main__":
    track_usage()
