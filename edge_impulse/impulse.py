import requests
import sys

sys.path.append('../')
from credentials.edge_impulse import username, password, project_id, api_key
# url = "https://studio.edgeimpulse.com/v1/api-login"

# payload = {
#     "username": username,
#     "password": password
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)
# token = response.json()["token"]
def delete_impulse(project_id, api_key):
    url = f"https://studio.edgeimpulse.com/v1/api/{project_id}/impulse"

    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
    }
    response = requests.delete(url, headers=headers)

    print(response.text)
def create_impulse(project_id, api_key):
    url = f"https://studio.edgeimpulse.com/v1/api/{project_id}/impulse"

    payload = {
        "inputBlocks": [
            {
                "type": "time-series",
                "primaryVersion": False,
                "id": 1,
                "name": "Time series",
                "title": "Time series data",
                "windowSizeMs": 1300,
                "frequencyHz": 50,
                "padZeros": False,
                "windowIncreaseMs": 1000
            }
        ],
        "dspBlocks": [
            {
                "primaryVersion": False,
                "id": 2,
                "type": "spectral-analysis",
                "name": "Spectral features",
                "title": "Spectral Analysis",
                "input": 1,
                "valuesPerAxis": 2,
                "enabled": True,
                "implementationVersion": 1,
                "mutated": True,
                "description": "Reduced learning rate and more layers",
                "createdBy": "createImpulse",
                "axes": ["phi_r", "theta_r"]
            }
        ],
        "learnBlocks": [
            {
                "type": "keras",
                "primaryVersion": True,
                "id": 3,
                "name": "NN Classifier",
                "dsp": [2],
                "title": "Classification (Keras)",
                "mutated": True
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
def generate_features(project_id,api_key):
    url = "https://studio.edgeimpulse.com/v1/api/286138/jobs/generate-features"

    payload = { "dspId": 2 }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "ei_7b5eb37478bcee6336899c9c27c05d118a2dec9469e0e30f"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
def generate_model(project_id,api_key):
    pass
generate_features(project_id,api_key)