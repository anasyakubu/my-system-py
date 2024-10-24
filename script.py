import urllib.request
import json
import socket
import pymongo
import datetime

# MongoDB Atlas Connection
client = pymongo.MongoClient("mongodb+srv://yakubuanas04:KOFEiHoWAUS2J0Zy@cluster0.z5fnu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['internet_connection_db']
collection = db['connection_records']

# Function to get public IP and location data using urllib
def get_location_data():
    try:
        # Open the URL and get the response from ipinfo.io
        with urllib.request.urlopen('https://ipinfo.io/json') as response:
            data = response.read()  # Read the response data
            ip_info = json.loads(data)  # Convert the data from JSON

            # Extract location data
            location_data = {
                'ip': ip_info.get('ip'),
                'city': ip_info.get('city'),
                'region': ip_info.get('region'),
                'country': ip_info.get('country'),
                'loc': ip_info.get('loc'),  # Latitude and longitude
                'org': ip_info.get('org')   # Organization/ISP
            }
            return location_data
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

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

# Main function to log the connection record
def log_connection():
    if is_connected():
        location_data = get_location_data()
        if location_data:
            record = {
                'timestamp': get_timestamp(),
                'location': location_data
            }
            collection.insert_one(record)
            print("Record saved:", record)
        else:
            print("Location data unavailable.")
    else:
        print("No internet connection detected.")

# Run the log function
if __name__ == "__main__":
    log_connection()
