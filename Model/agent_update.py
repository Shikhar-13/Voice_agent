import asyncio
import requests
from main import VoiceAgent, VoiceAgentConfig, AgentPresets

BASE_URL = "https://api.chat-dash.com/v1/public"
AUTH_TOKEN = "CD.d4f82cc37d21f0b4c4972bec3089f9b5"
chatbot_id = "678162c52eaa21a7a56bf60f"
llm_ids = {
    "gpt4": "llm_678142e62eaa21a7a564a9f2",
    "gpt4o": "llm_678142e62eaa21a7a564a9f3",
    "gpt4o-mini": "llm_678142e62eaa21a7a564a9f4",
    "claude-3-5-sonnet-20240620": "llm_678142e62eaa21a7a564a9f5",
    "claude-3-5-sonnet-20240620-mini": "llm_678142e62eaa21a7a564a9f6"
}

def update_chatbot(base_url, auth_token, chatbot_data):
    """
    Updates the chatbot using a synchronous PUT request.
    """
    url = f"{base_url}/chatbots/{chatbot_id}"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    response = requests.request("PUT", url, json=chatbot_data, headers=headers)

    print(response.text)

async def create_and_update_chatbot():
    """
    Creates a VoiceAgent asynchronously and then updates the chatbot using synchronous requests.
    """
    # Initialize the VoiceAgent with the correct configuration
    agent = VoiceAgent(api_key="key_9e5f870bfb716e851b060662e1d6", config=AgentPresets.GPT4_ADRIAN)

    # Create the agent asynchronously and await the result
    agent_id = await agent.create_agent()

    # Prepare the chatbot data
    chatbot_data = {
        "apiId": agent_id,
        "apiKey": "key_9e5f870bfb716e851b060662e1d6"
    }

    # Now update the chatbot using synchronous request
    chatbot_response = update_chatbot(BASE_URL, AUTH_TOKEN, chatbot_data)
    if "error" in chatbot_response:
        print(f"Failed to update chatbot: {chatbot_response['error']}")
    else:
        print("Chatbot updated:", chatbot_response)
        global chatbot_id
        chatbot_id = chatbot_response.get("id")

if __name__ == "__main__":
    # Running the asynchronous function
    asyncio.run(create_and_update_chatbot())
