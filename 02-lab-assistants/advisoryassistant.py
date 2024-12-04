import os
import time
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Needed for the assistant to access the underlying LLM Model
deployment_name = os.getenv("DEPLOYMENT_NAME")

# Vector ID from the vector store - vector.py
vector_store_id = os.getenv("VECTOR_STORE_ID")

# Initialize the client call
client = AzureOpenAI(
    api_key= os.getenv("AZURE_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    )

# Create the assistant this can have file_search, code_interpreter, or a function as the tools parameter.
try:
    assistant = client.beta.assistants.create(
        name="AI Security Advisor",
        instructions="""You're a senior security advisor that assists organizations with various risks in adoption of Generative AI.
          You're tasked with providing guidance on how to secure AI models and data. You can ask questions to get started.
          You're well versed in the OWASP Top 10 LLM, and can provide guidance on how to secure AI models and data.
          You can code if needed to provide guidance on how to secure AI models and data.""",
        model=deployment_name
    )
    print(assistant.model_dump_json(indent=2))
except Exception as e:
    print(f"Error creating assistant: {e}")
    exit(1)

# Second try/except block to create a thread and run the assistant
try:
    # Create a thread
    thread = client.beta.threads.create()
    thread_id = thread.id

    print(f"Thread ID: {thread_id}")

    user_input = input("Enter your prompt: ")
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input # Replace this with your prompt
      )

# Validate thread_id exists before creating run
    if thread_id:
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id
        )
        
        # Monitor run status
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,  # Use stored thread_id 
            run_id=run.id
        )

        # Handle run completion
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread_id  # Use stored thread_id
            )
            print(messages)
        elif run.status == 'requires_action':
            print("Run requires action")
        else:
            print(f"Run failed with status: {run.status}")

except Exception as e:
  print(f"Error in execution: {e}")
  exit(1)
