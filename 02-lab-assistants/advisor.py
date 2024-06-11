import os
import time
import json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

assistant = client.beta.assistants.create(
    instructions="You're a senior security advisor that assists organizations with various risks in adoption of Generative AI.",
    model="<model_name>", # replace with model deployment name. 
    tools=[{"type":"code_interpreter"}]
    )

# Create a thread
thread = client.beta.threads.create()

# Add a user question to the thread
try:
    user_input = input("Enter your prompt: ")
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input # Replace this with your prompt
)
except Exception as e:
   print(f"An error occured: {e}")

# Run the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

# Looping until the run completes or fails
while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

if run.status == 'completed':
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages)
elif run.status == 'requires_action':
  # the assistant requires calling some functions
  # and submit the tool outputs back to the run
  pass
else:
  print(run.status)
