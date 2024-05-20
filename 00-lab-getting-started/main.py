
import os
from openai import AzureOpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key=os.environ["AZURE_OPENAI_API_KEY"]
      
# Create a client      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

# Enter a query is added to the messages list
user_query = input("Enter your query: ")



completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": user_query,
        },
    ]
)
##completion_dict = completion.to_dict()
##response_content = completion_dict['choices'][0]['message']['content']
##print(response_content)

# Raw Response      
print(completion.to_json())

