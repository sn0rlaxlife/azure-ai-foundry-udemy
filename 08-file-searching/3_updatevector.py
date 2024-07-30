import os
from openai import AzureOpenAI

# Step 3 updatevector.py represents the use of updating the assistant with the vector store that was created in vector.py
# Once we run this script the assistant will have the ability to search through the files we've uploaded in the vector store

# Vector store Id that is needed - if you don't have this on hand on Azure AI Studio -> Vector Store
vector_store_id = os.getenv("VECTOR_STORE_ID")

# Assistant ID you've gotten this previously from the create.py
assistant_id = os.getenv("ASSISTANT_ID")

# Needed for the assistant to access the underlying LLM Model
deployment_name = os.getenv("DEPLOYMENT_NAME")


# Initialize the client call
client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )


# Add the vector store to the assistant
assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
)

# Print the response to validate the update
print("Update Response:", assistant)
