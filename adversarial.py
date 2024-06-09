import os
import aiohttp
from typing import List, Dict, Any
from promptflow.evals.synthetic import AdversarialSimulator
from promptflow.evals.synthetic.adversarial_scenario import AdversarialScenario
from azure.identity import DefaultAzureCredential
import asyncio
from openai import AzureOpenAI


# Azure AI project details
azure_ai_project = {
    "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
    "resource_group_name": os.environ["AZURE_RESOURCE_GROUP"],
    "project_name": os.environ["AZURE_WORKSPACE_NAME"],
    "credential": DefaultAzureCredential(),
}

# Define the scenario
scenario = AdversarialScenario.ADVERSARIAL_CONVERSATION
simulator = AdversarialSimulator(azure_ai_project=azure_ai_project)
# Get the Azure AI project details and API Key
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]

# Define the function to call your endpoint -> for AzureOpenAI follow this example/pattern
async def function_call_to_your_endpoint(query: str) -> str:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_deployment=deployment,
        api_key=api_key,
        api_version="2024-02-01",
    )
# Call the Azure OpenAI API, the exception will return if any errors occurs ensure you have all environment variables declared (EastUS2 is supported as of 6/4/2024)
    try:
        response = client.chat.completions.create(model=deployment, messages=[{"role": "user", "content": query}])
        # Extract the generated text from the response
        generated_text = [choice.message.content for choice in response.choices]
        return {"generated_text": generated_text}
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,
) -> dict:
    query = messages["messages"][0]["content"]
    context = None

    # Add file contents for summarization or re-write
    if 'file_content' in messages["template_parameters"]:
        query += messages["template_parameters"]['file_content']
    
    # Call your own endpoint and pass your query as input. Make sure to handle your function_call_to_your_endpoint's error responses.
    response = await function_call_to_your_endpoint(query) 
    
    # Format responses in OpenAI message protocol
    formatted_response = {
        "content": response,
        "role": "assistant",
        "context": {},
    }

    messages["messages"].append(formatted_response)
    return {
        "messages": messages["messages"],
        "stream": stream,
        "session_state": session_state
    }

# Define the async function to run the simulation - this is the main function that will be called to run the simulation - its is also encouraged to use the jailbreak in a separate simulation
async def run_simulation():
    outputs = await simulator(
        scenario=scenario,
        target=callback,
        max_conversation_turns=1,
        max_simulation_results=3,
        jailbreak=False
    )
    return outputs
# Outside of the async function
outputs = asyncio.run(run_simulation())
print(outputs.to_eval_qa_json_lines())

# Print out just in jsoln format
print(outputs.to_json_lines())