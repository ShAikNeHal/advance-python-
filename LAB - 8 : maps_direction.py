import json
import webbrowser
from urllib.parse import quote

# Take input from terminal
source = input("Enter source: ")
destination = input("Enter destination: ")

# Create JSON data
data = {
    "source": source,
    "destination": destination
}

# Convert data to JSON
json_data = json.dumps(data, indent=4)

print("\nJSON data:")
print(json_data)

# Get values from JSON
data = json.loads(json_data)

source = data["source"]
destination = data["destination"]

# Create Google Maps directions URL
url = (
    "https://www.google.com/maps/dir/?api=1"
    f"&origin={quote(source)}"
    f"&destination={quote(destination)}"
)

# Open Google Maps
webbrowser.open(url)

print("\nOpening Google Maps...")
