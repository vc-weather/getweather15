import requests
import sqlite3
import time

# Set up the API endpoint and authentication keys
endpoint = "https://api.ambientweather.net/v1/devices/"
apiKey = "07f15d0bc27943ea8a858bb17b27e4019efd0b8bbaf945c4a5eb73e0b878491e"
appKey = "8533cedd5dcd40e3a5770ef06075acb41b9d1277138546e693a13f9d1e17d2a7"

# Connect to the database
conn = sqlite3.connect('database-1.crrlkzkwiovq.us-west-2.rds.amazonaws.com')

# Create a cursor object
c = conn.cursor()

# Create a table to store the API responses
c.execute('''CREATE TABLE IF NOT EXISTS api_responses
             (id INTEGER PRIMARY KEY,
              response_text TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# Define the interval between API calls (in seconds)
interval = 900 # 15 minutes

# Infinite loop to make periodic API calls and store the response in the database
while True:
    # Make an API call to the endpoint
    response = requests.get(endpoint, params={"apiKey": apiKey, "applicationKey": appKey})

    # Insert the API response into the database
    c.execute("INSERT INTO api_responses (response_text) VALUES (?)", (response.text,))

    # Commit the changes to the database
    conn.commit()

    # Wait for the specified interval before making the next API call
    time.sleep(interval)
