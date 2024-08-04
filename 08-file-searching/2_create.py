import os
import time
import json
from openai import AzureOpenAI

# Step 2 create.py represents the use of creating a assistant that will use the file_search tool
# This is a tool that allows the assistant to search through files and provide guidance based on the content of the files

# Needed for the assistant to access the underlying LLM Model
deployment_name = os.getenv("DEPLOYMENT_NAME")


# Initialize the client call
client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

assistant = client.beta.assistants.create(
    name="AI Security Advisor",
    instructions=f"You're a senior security advisor that assists organizations with various risks in adoption of Generative AI."
    f"You're tasked with providing guidance on how to secure AI models and data. You can ask questions to get started."
    f"You're well versed in the OWASP Top 10 LLM, and can provide guidance on how to secure AI models and data."
    f"You can code if needed to provide guidance on how to secure AI models and data.",
    model="filesearcher", # replace with model deployment name. 
    tools=[{"type":"file_search"}],
    )

# Print the assistant model dump - this will show the creation of the assistant
print(assistant.model_dump_json(indent=2))
