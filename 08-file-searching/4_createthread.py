
import os
from typing_extensions import override
from openai import AssistantEventHandler, AzureOpenAI

# environment variables
vector_id = os.getenv("VECTOR_STORE_ID")
assistants_id= os.getenv("ASSISTANT_ID")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

vector_store_id='vs_KfNzzgVJnlh6K6dNCkJNGkc4'
# Debugging: Print the vector_id to ensure it's set correctly
print(f"VECTOR_ID: {vector_id}")

if not azure_endpoint or not deployment_name or not api_key:
   raise ValueError("Missing one or more required environment variables.")

# Initialize the client call
client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment= os.getenv("DEPLOYMENT_NAME")
    )

 
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user", 
            "content": "What is NIST AI-100-1?",
        }
    ],
)
 
# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)


with client.beta.threads.runs.stream(
    thread_id=thread.id
) as stream:
    for response in stream:
        print(response)