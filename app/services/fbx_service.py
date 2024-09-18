import requests
from fastapi import HTTPException

def convert_to_fbx(pkl_url: str, song_name: str):
    url = "https://fbx-1-f0e6e5cdebetdnfy.eastus-01.azurewebsites.net/convert-pkl"
    
    # Prepare the payload to send in the request
    payload = {
        "pkl_url": pkl_url,
        "song_name": song_name
    }

    try:
        # Send a POST request to the conversion endpoint
        response = requests.post(url, json=payload)

        # Raise an exception if the response code is not successful
        response.raise_for_status()

        # Return the response as JSON if successful
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=response.status_code, detail="Failed to convert to FBX")
    except Exception as err:
        print(f"An error occurred: {err}")
        raise HTTPException(status_code=500, detail="An error occurred while converting to FBX")