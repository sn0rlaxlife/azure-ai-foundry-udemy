import os
import time
import json
import requests
from openai import AzureOpenAI
from pathlib import Path
from typing import Optional
from rich.console import Console


# Rich initialize the console for colors
console = Console()

## Establish the function to needed parameters
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = "2024-05-01-preview"
deployment_name = os.getenv("DEPLOYMENT_NAME")
bing_search_subscription_key = os.getenv("BING_SEARCH_SUBSCRIPTION_KEY")
bing_search_url = "https://api.bing.microsoft.com/v7.0/search"
api_key = os.getenv("AZURE_OPENAI_API_KEY")



# Initialize the client
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)


# Define the search function
def search(query: str) -> list:
    """
    Perform a bing search against the given query

    @param query: Search query
    @return: List of search results

    """
    headers = {"Ocp-Apim-Subscription-Key": bing_search_subscription_key}
    params = {"q": query, "textDecorations": False}
    response = requests.get(bing_search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    output = []

    for result in search_results["webPages"]["value"]:
        output.append({"title": result["name"], "link": result["url"], "snippet": result["snippet"]})

    return json.dumps(output)


# Define conversation
def run_conversation():
    # Initial user message that is passed to the API
    query = input('Enter your desired query: ')
    messages = [{"role": "user", "content": query}]

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": "Search for any query that is not known or understood by the model.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "LLM Security encompasses a variety of approaches that should be considered such as OWASP Top 10 LLMs.",
                        },
                    },
                    "required": ["query"],
                },
            }
        }
    ]
    # First API Call: Ask the model nicely to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=800,
    )

    # Process the model response
    response_message = response.choices[0].message
    messages.append(response_message)

    # Print the response
    console.print("Model's Response:", style="bold red")
    console.print(messages, style="bold green")

    # Handle the function call
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "search":
                function_args = json.loads(tool_call.function.arguments)
                console.print(f"Function arguments: {function_args}", style="bold blue")
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "search",
                    "content": search(**function_args)
                })
    else:
        print("No function call was made.")

    # Second API Call: Send the function response to the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )
    # Print the final response however this cleans the response so you gather content clearly to end user from terminal
    final = final_response.choices[0].message.content
    
    # Distinguish the print with a color to understand the function call
    console.print("Final Response:", final, style="bold blue")

    # Validate the function is called 
    console.print("Raw Final Response:", final_response, style="bold yellow")

    # Return the final response is needed otherwise you can comment this out
    # return final
print(run_conversation())
