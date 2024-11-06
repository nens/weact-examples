import requests
import json

base_url =  'http://kghub.caiag.kg/api/'


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


post = create_location("421f9617-3714-4700-b063-6c4c6d6889be",
                       'bishkek precipitation', "bishkek_precip",
                       (74.590958, 42.871773, 0.0))

