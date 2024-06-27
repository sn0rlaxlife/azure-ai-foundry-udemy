# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from openai import AzureOpenAI
import json

# Deployment name of DALL-3 Model
# Replace <your-deployment-name> with the name of your DALL-E 3 deployment
deployment = os.environ["DALLE3_DEPLOYMENT"]

client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

try:
    prompt = input("Enter a prompt: ")
except Exception as e:
    print("An error occurred: ", e)
if not prompt:
    print("Prompt is required")

# For DALL-E 3, use the `generate` method - the `model` parameter should be set to <your-deployment-name>, and the `n` parameter should be set to 1 <if you desire 1 image>
result = client.images.generate(
    model=deployment, # the name of your DALL-E 3 deployment
    prompt=prompt,
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print("Generated image URL:", image_url)
