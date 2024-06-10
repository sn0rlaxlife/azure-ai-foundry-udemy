import os
import requests
from openai import AzureOpenAI

# Use of these in environment variables
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
key = os.environ["AZURE_OPENAI_KEY"]

# Initialize the AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=key,
    api_version="2024-02-01",
)

url = input('Enter the URL of the article you want to summarize: ')
def scrape_jina_ai(url: str) -> str:
    response = requests.get("https://r.jina.ai/" + url)
    content = response.text
    return content
    

def generate_summary(content: str, deployment: str, client: AzureOpenAI) -> str:
    # Create the prompt
    messages = [
        {
            "role": "system",
            "content": "In your own words, summarize the content from the scraped content."
        },
        {
            "role": "assistant",
            "content": f"Here is your summary of the following {content}"
        }
    ]

    # Send the content from this to the LLM
    response = client.chat.completions.create(
        model=deployment,
        messages=messages
    )
    # Extract the summary from the response
    summaries = response.choices[0].message.content
    print(summaries)
    return summaries
# Scrape the content    
content = scrape_jina_ai(url)

# Generate the summary
summary = generate_summary(content, deployment, client)

# Print the summary
print(summary)
