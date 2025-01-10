import requests

def create_client(base_url, auth_token, client_data):
    url = f"{base_url}/clients"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=client_data, headers=headers)
    return response.json()

def create_chatbot(base_url, auth_token, chatbot_data):
    url = f"{base_url}/chatbots"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=chatbot_data, headers=headers)
    return response.json()

def create_project(base_url, auth_token, project_data):
    url = f"{base_url}/projects"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=project_data, headers=headers)
    return response.json()

def get_chatbots(base_url, auth_token):
    url = f"{base_url}/chatbots"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    return response.json()

def assign_chatbot_to_project(base_url, auth_token, project_id, chatbot_id):
    url = f"{base_url}/projects/{project_id}"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    payload = {"chatbotId": chatbot_id}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def get_project_details(base_url, auth_token, project_id):
    url = f"{base_url}/projects/{project_id}"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    return response.json()

def get_embed_widget_code(base_url, auth_token, chatbot_id):
    url = f"{base_url}/chatbots/{chatbot_id}/embed"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    return response.json()

# Replace these placeholders with actual values
BASE_URL = "https://api.chat-dash.com/v1/public"
AUTH_TOKEN = "CD.d4f82cc37d21f0b4c4972bec3089f9b5"

# Step 1: Create Client
client_data = {
    "name": "Test Client",
    "loginId": "test_client_001",
    "email": "testclient@example.com",
    "password": "securepassword",
    "language": "en"
}
client_response = create_client(BASE_URL, AUTH_TOKEN, client_data)
print("Client Created:", client_response)
client_id = client_response.get("id")

# Step 2: Create Chatbot
chatbot_data = {
    "platform": "retell",
    "apiId": "agent_67fc01fa17422279863a3b9c16",
    "apiKey": "key_9e5f870bfb716e851b060662e1d6",
    "name": "Test Chatbot"
}
chatbot_response = create_chatbot(BASE_URL, AUTH_TOKEN, chatbot_data)
print("Chatbot Created:", chatbot_response)
chatbot_id = chatbot_response.get("id")
print(chatbot_id)

# Step 3: Create Project
project_data = {
    "clientId": client_id,
    "chatbotId": chatbot_id,
    "name": "Test Project"
}
project_response = create_project(BASE_URL, AUTH_TOKEN, project_data)
print("Project Created:", project_response)
project_id = project_response.get("id")

# Step 4: Retrieve Chatbots
chatbots = get_chatbots(BASE_URL, AUTH_TOKEN)
print("Chatbots:", chatbots)

# Step 5: Assign Chatbot to Project
assignment_response = assign_chatbot_to_project(BASE_URL, AUTH_TOKEN, project_id, chatbot_id)
print("Chatbot Assigned to Project:", assignment_response)

# Step 6: Get Project Details
project_details = get_project_details(BASE_URL, AUTH_TOKEN, project_id)
print("Project Details:", project_details)

# Step 7: Get Embed Widget Code
embed_code_response = get_embed_widget_code(BASE_URL, AUTH_TOKEN, chatbot_id)
print("Embed Widget Code:", embed_code_response)
