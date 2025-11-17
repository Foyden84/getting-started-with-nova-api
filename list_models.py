import requests
import json
from nova_key import NOVA_API_KEY

#######################################################
###
### A simple python script to retrieve and display list 
### of NOVA models allowed for your API Key
###
#######################################################

def list_nova_models():
    # Replace with your actual token
    api_url = "https://api.nova.amazon.com/v1/models"
    auth_token = NOVA_API_KEY

    # Create the headers dictionary, including the Authorization header
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"  # Example: adjust if your API requires a different content type
    }

    try:
        # Make a GET request with the authorization header
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        # Process the response data
        data = response.json()
        #print("Response data:", json.dumps(data, indent=2))
        for item in data["data"]:
            print(f"{item['display_name']} -> {item['id']}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    list_nova_models()