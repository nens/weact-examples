import requests
from datetime import datetime, timedelta
import pandas as pd

start = datetime.fromisoformat("2024-01-01T01:00:00+00:00")

end = datetime.now()

base_url = 'http://localhost:8002/api/'
bearer_token = 'testing'
organisation_name = 'testing_kizje'

json_headers = {
    'Authorization': f'Bearer {bearer_token}'}

def get_organisation_uuid(organisation_name):
    org_url = base_url+ "organisations/"
    params = {"name": organisation_name}
    r = requests.get(org_url, headers=json_headers, params=params)
    orgs = pd.DataFrame(r.json()["results"])
    orgs_uuid = orgs['uuid'][0]
    return orgs_uuid

def get_locations_list(base_url, organisation_uuid):
    # Measuringstations
    location_url = base_url+ "locations/"

    params = {
        "organisation__uuid": organisation_uuid,
        "page_size": 10000,
    }
    r = requests.get(location_url, headers=json_headers, params=params)
    locations = pd.DataFrame(r.json()["results"])
    return locations


def get_locations_single(base_url, organisation_uuid,loc_code):
    # Measuringstations
    location_url = base_url+ "locations/"

    params = {
        "organisation__uuid": organisation_uuid,
        "code": loc_code,
        "page_size": 10000,
    }
    r = requests.get(location_url, headers=json_headers, params=params)
    location = pd.DataFrame(r.json()["results"])
    return location


def get_observation_list(base_url):
    observation_url = base_url+ "observationtypes/"
    r = requests.get(observation_url, headers=json_headers)
    observations = pd.DataFrame(r.json()["results"])
    return observations


def get_timeseries_list(base_url, organisation_uuid):
    ts_url = base_url + "timeseries/"
    params = {
        "organisation__uuid": organisation_uuid,
        "page_size": 10000,
    }
    r = requests.get(ts_url, headers=json_headers, params=params)
    timeseries = pd.DataFrame(r.json()["results"])
    return timeseries


def get_timeseries_events(base_url, ts_uuid,start, end ):
    ts_url  = base_url + "timeseries/" + ts_uuid + "/events/"
    params = {
        "start": start,
        "end": end,
        "page_size": "100000",
    }
    time_series_events = pd.DataFrame(
        requests.get(url=ts_url, headers=json_headers, params=params).json()["results"]
    )
    return time_series_events


obs = get_observation_list(base_url)
org_uuid = get_organisation_uuid(organisation_name)
locations = get_locations_list(base_url, org_uuid)
timeseries = get_timeseries_list(base_url,org_uuid )
ts_uuid = timeseries['uuid'][0]
ts_events = get_timeseries_events(base_url, ts_uuid, start, end)
