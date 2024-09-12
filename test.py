import requests

# Define the API key and the endpoint
api_key = "AIzaSyAwLB3TGsHTItz3iZQAfg1OhsM4L2dKzrk"
url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Define the data payload
data = {
    "homeMobileCountryCode": 404,
    # "homeMobileCountryCode": 310,
    "homeMobileNetworkCode": 11,
    # "homeMobileNetworkCode": 410,
    "radioType": "gsm",
    "carrier": "Free",
    "considerIp": True
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    print("Google Maps Geolocation API returned:", response.json())
else:
    print("Error:", response.status_code, response.text)
