import asyncio
import websockets
import json
import requests
from main import VoiceAgent, VoiceAgentConfig, AgentPresets

BASE_URL = "https://api.chat-dash.com/v1/public"
AUTH_TOKEN = "CD.d4f82cc37d21f0b4c4972bec3089f9b5"
chatbot_id = "678162c52eaa21a7a56bf60f"

# Define the LLMs
llm_ids = {
    "gpt4": "llm_f1fbe2eefad955e589c03fa8040c",
    "gpt4o": "llm_678142e62eaa21a7a564a9f3",
    "gpt4o-mini": "llm_5cf191215e52d2d19e8630a73a84",
    "claude-3-5-sonnet-20240620": "llm_9721fe6634b83c65c7ad29978816",
    "claude-3-5-sonnet-20240620-mini": "llm_5dd10ecfa33c4f667f9652e08b08"
}

async def create_and_update_chatbot(llm_choice):
    """
    Creates a VoiceAgent asynchronously and then updates the chatbot using synchronous requests.
    """
    # Map the LLM choice to the correct configuration
    llm_id = llm_ids.get(llm_choice)
    if not llm_id:
        return f"Invalid LLM choice '{llm_choice}'. Please select a valid model."

    try:
        # Initialize the VoiceAgent with the correct configuration based on LLM
        agent = VoiceAgent(api_key="key_9e5f870bfb716e851b060662e1d6", config=VoiceAgentConfig(
            llm_id=llm_id,
            llm_type="retell-llm",  # Use the correct LLM type
            voice_id="11labs-Adrian",  # Set the appropriate voice ID
        ))

        # Create the agent asynchronously and await the result
        agent_id = await agent.create_agent()
        if not agent_id:
            return "Failed to create VoiceAgent. No agent ID returned."

        # Prepare the chatbot data for update
        chatbot_data = {
            "apiId": agent_id,
            "apiKey": "key_9e5f870bfb716e851b060662e1d6"
        }

        # Update the chatbot (synchronously)
        response = update_chatbot(chatbot_data)
        return response

    except Exception as e:
        return f"Error during agent creation or chatbot update: {str(e)}"

def update_chatbot(chatbot_data):
    """
    Updates the chatbot using a synchronous PUT request.
    """
    url = f"{BASE_URL}/chatbots/{chatbot_id}"
    headers = {
        "Authorization": AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(url, json=chatbot_data, headers=headers)
        if response.status_code == 200:
            return f"Chatbot successfully updated: {response.text}"
        else:
            return f"Failed to update chatbot. Status code: {response.status_code}, Response: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request error during chatbot update: {str(e)}"

async def websocket_handler(websocket, path):
    try:
        # Receive the data from the WebSocket client
        message = await websocket.recv()
        data = json.loads(message)

        # Assuming the action is "create_and_update_chatbot" and data contains the 'llm' field
        llm_choice = data.get("llm")
        if not llm_choice:
            await websocket.send("Error: LLM choice not provided in the request.")
            return

        result = await create_and_update_chatbot(llm_choice)

        # Send the result back to the client, only if the connection is still open
        if websocket.open:
            await websocket.send(result)

    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed by client")

    except Exception as e:
        print(f"Error handling WebSocket message: {e}")
        if websocket.open:
            await websocket.send(f"Error: {str(e)}")

async def main():
    async with websockets.serve(websocket_handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(main())
