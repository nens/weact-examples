import requests
import json
import numpy as np
import pandas as pd
from get_functions import *
base_url =  "https://kghub.caiag.kg/api/"
org_uuid = "421f9617-3714-4700-b063-6c4c6d6889be"

bearer_token = 'testing'

json_headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json'  # Specify that the data is in JSON format
}

def create_location( organisation_uuid, location_name, location_code, coordinates):
    """
    Creates a location on the server using the specified data.

    Parameters:
    - organisation_uuid (str): The UUID of the organization.
    - location_name (str): The name of the location.
    - access_modifier (int): Access level for the location.
    - location_code (str): Unique code for the location.
    - coordinates (tuple): A tuple of (longitude, latitude, elevation).

    Returns:
    - dict: JSON response from the server.
    """
    location_url = base_url+ "locations/"

    # Data payload for the POST request
    data = {
        'name': location_name,
        'code': location_code,
        'organisation': organisation_uuid,
        'geometry': {
            "type": "Point",
            "coordinates": list(coordinates)
        },
        'extra_met': True
    }
    # Send POST request to create location
    response = requests.post(url=location_url, data=json.dumps(data), headers=json_headers)

    # Return JSON response
    return response.json()

def create_timeseries(name, code, location_uuid, observation_code, base_url, json_headers):
    """
    Function to create a timeseries entry.

    Args:
        name (str): Name for the location.
        code (str): Unique code for the location (letters and numbers).
        location_uuid (str): UUID of the location.
        observation_code (int): Code representing the type of observation.
        timeseries_url (str): URL endpoint for posting the timeseries data.
        json_headers (dict): Headers to include with the request (e.g., authentication and content type).

    Returns:
        dict: JSON response from the API.

    """

    timeseries_url = base_url+ "timeseries/"

    data = {
        'name': name,
        'code': code,
        'location': location_uuid,
        'value_type': 1,
        'observation_type': observation_code,
        'timeseries_type': None
    }

    response = requests.post(
        url=timeseries_url,
        data=json.dumps(data),
        headers=json_headers
    )

    return response.json()



def create_events(timeseries_uuid, datafile, base_url, json_headers):
    """
    Function to create events in an existing timeseries

    Args:
        timeseries_uuid (str): Uuid of the timeseries
        datafile (str): Path to a csv file with the data. This file should have 2 columns
            1. datetime: datetimestrings in ISO8601 format
            2. value: values of the matching timeseries
        base_url (str): URL endpoint for the DWH API
        json_headers (dict): Headers to include with the request (e.g., authentication and content type).

    Returns:
        dict: JSON response from the API.
    """
    
    url = f"{base_url}timeseries/{timeseries_uuid}/events/"
    print(url)

    df = pd.read_csv(datafile)

    data = []
    for index, row in df.iterrows():
        data.append(
            {
                "time": row["datetime"],
                "value": row["value"]
            }
        )
    i = 0

    chunks = np.ceil(len(data)/1000)

    for chunk in np.array_split(data, chunks):
        i+=1
        print(f"Posting chunk {i}") 
        r = requests.post(url=url, data=json.dumps(chunk.tolist()), headers=json_headers)
        try:
            r.raise_for_status()
            print(f"Chunk {i} posted")
        except:
            print(f"Chunk {i} post failed")
            print(r.json())
            raise

    return r.json()

if __name__ == "__main__()":
    post = create_location("421f9617-3714-4700-b063-6c4c6d6889be",
                        'bishkek precipitation', "bishkek_precip",
                        (74.590958, 42.871773, 0.0))
    loc_uuid = get_locations_single(base_url,org_uuid,'bishkek_precip' )['uuid'][0]
    ts = create_timeseries('precipitation data gpm','precip_gpm', loc_uuid, 1 , base_url, json_headers)