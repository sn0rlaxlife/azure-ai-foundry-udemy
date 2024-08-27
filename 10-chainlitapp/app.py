import json
import ast
import os
from openai import AsyncAzureOpenAI, AzureOpenAI
from dotenv import load_dotenv
from exa_py import Exa
import chainlit as cl


# Load environment variables
load_dotenv()

# Variables that are needed for AsyncAzureOpenAI
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_version = "2024-05-01-preview"
deployment_name = os.environ.get("DEPLOYMENT_NAME")

# Async call to Azure OpenAI
client = AsyncAzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    azure_deployment=deployment_name,
    api_version=api_version)

# Initialize Exa Client
exa = Exa(api_key=os.getenv("EXA_API_KEY"))



# Initialize the client
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)


MAX_ITER = 5

cl.instrument_openai()


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
# Define the search function
def search(query: str) -> list:
    """
    Perform a search using Exa SDK

    @param query: Search query
    @return: List of search results

    """
    result = exa.search_and_contents(
        query=query,
        type="auto", # Can be either Neural, Keyword, or 'Auto' which will automatically determine the best search type based on the query.
        use_autoprompt=True, 
        num_results=10,
        text=True,
        include_domains=["bing.com","google.com","weather.com", "finance.yahoo.com"], # Depending on your use-case you can expand or minimize the targets of search domains you'd like to use exa for.
    )

    output = []

    for item in result.results:
        output.append({"title": item.title, "link": item.url, "snippet": item.text})

    return json.dumps(output)

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


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.step(type="tool")
async def call_tool(tool_call, message_history):
    function_name = tool_call.function.name
    arguments = ast.literal_eval(tool_call.function.arguments)

    current_step = cl.context.current_step
    current_step.name = function_name

    current_step.input = arguments

    function_response = search(
        query=arguments.get("query"),
    )

    current_step.output = function_response
    current_step.language = "json"

    message_history.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
            "tool_call_id": tool_call.id,
        }
    )


async def call_gpt4(message_history):
    settings = {
        "model": deployment_name,
        "tools": tools,
        "tool_choice": "auto",
        "max_tokens": 800,
    }

    response = client.chat.completions.create(
        messages=message_history, **settings
    )

    message = response.choices[0].message

    for tool_call in message.tool_calls or []:
        if tool_call.type == "function":
            await call_tool(tool_call, message_history)

    if message.content:
        cl.context.current_step.output = message.content

    elif message.tool_calls:
        completion = message.tool_calls[0].function

        cl.context.current_step.language = "json"
        cl.context.current_step.output = completion

    return message


@cl.on_message
async def run_conversation(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"name": "user", "role": "user", "content": message.content})

    cur_iter = 0

    while cur_iter < MAX_ITER:
        message = await call_gpt4(message_history)
        if not message.tool_calls:
            await cl.Message(content=message.content, author="Answer").send()
            break

        cur_iter += 1
