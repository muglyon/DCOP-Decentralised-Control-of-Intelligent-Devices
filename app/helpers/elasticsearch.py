import requests

from helpers.constants import Constants

ROOT_URL = "http://localhost:9200/"


def save_data(payload):

    index = "log_dcop/log/"

    if '"type": "' + Constants.STATE + '"' in payload:
        index = "state/state/"

    if '"type": "' + Constants.DFS + '"' in payload:
        index = "dfs/dfs/"

    response = requests.post(ROOT_URL + index,
                             headers={"Content-Type": "application/json"},
                             data=payload)

    if b'error' in response.content:
        print("\nUnable to save log in elasticsearch for " + index)
        print(payload)
        print(response.content, '\n')
