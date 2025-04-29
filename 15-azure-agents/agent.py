## Initialize the environment client.
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentThread
from semantic_kernel.functions import kernel_function
from semantic_kernel import Kernel
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
import os
import requests
import json
from typing import Any, Callable, Set, Dict, List, Optional
import asyncio

load_dotenv()

# Environment Example - Custom for your perspective can change
connection = os.environ.get("AZURE_AI_AGENT_PROJECT_CONNECTION_STRING") # Azure AI Foundry connection string
finance_agent = os.environ.get("FINANCE_AGENT_ID") # Created agent in Azure AI Foundry
editor_agent = os.environ.get("EDITOR_AGENT_ID") # Created agent in Azure AI Foundry
writer_agent = os.environ.get("WRITER_AGENT_ID") # Created agent in Azure AI Foundry
bing_search_subscription_key = os.environ.get("BING_SEARCH_SUBSCRIPTION_KEY") # Bing Search API key
bing_search_url = os.environ.get("BING_SEARCH_URL") # Bing Search API URL

# Define build client initialization
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=connection
)

## Define our search function
class SearchPlugin:
    def __init__(self, bing_search_subscription_key, bing_search_url):
        self.bing_search_subscription_key = bing_search_subscription_key
        self.bing_search_url = bing_search_url
    @kernel_function(
            description = "Performs a Bing search against the given query",
            name = "search",
    )

    def search(self, query: str) -> list:
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
## --- Search Function --- ##



def load_funds(file_path: str) -> list:
    """
    Load funds from a plain text file into a list.

    @param file_path: Path to the funds.txt file
    @return: List of fund codes
    """
    with open(file_path, 'r') as file:
        funds = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace
    return funds

funds_file_path = "funds.txt"
funds = load_funds(funds_file_path)
print(f"Loaded funds: {funds}")

# Clean the format funds as string
# Convert the list of funds into a comma-separated string
funds_string = ", ".join(funds)
print(f"Funds string: {funds_string}")

# Define our prompt to run against the agent with dynamic portfolio parameters
age = 25
risk_tolerance = "medium 7/10"
time_range = "25 years"
us_equity_allocation = 65
intl_equity_allocation = 35

portfolio_prompt = f"""
I'm {age} years old with a {risk_tolerance} risk tolerance. I want to create a balanced portfolio 
with approximately {us_equity_allocation}% US equities and {intl_equity_allocation}% International Equity with a time horizon of {time_range}.

Based on the following list of available funds, please recommend a specific allocation that 
meets my investment goals:

Available funds: {funds_string}

For each recommended fund:
1. Provide the allocation percentage
2. Explain why it's appropriate for my age and risk profile and time horizon
3. Describe its role in the overall portfolio strategy
"""

# Create a client to connect to the Azure OpenAI service
credential = DefaultAzureCredential()
client = AzureAIAgent.create_client(credential=credential, conn_str=connection)

async def main():
    async with client:
    # Create a kernel
        kernel = Kernel()

        # Create the search plugin to add to kernel
        search_plugin = SearchPlugin(bing_search_subscription_key, bing_search_url)
        kernel.add_plugin(plugin=search_plugin, plugin_name="search")

        # Establish our existing agent by going to portal retrieve the assistant id or agent id
        finance_definition = await client.agents.get_agent(agent_id=finance_agent)

        advisor_agent = AzureAIAgent(client=client, definition=finance_definition, kernel=kernel)
        
        
        # Use the agent to run a prompt and get a response
        editor_definition = await client.agents.get_agent(agent_id=editor_agent)
        editing_agent = AzureAIAgent(client=client, definition=editor_definition, kernel=kernel)


        # Writer Agent that is defined also leveraged for final step
        writer_definition = await client.agents.get_agent(agent_id=writer_agent)
        writing_agent = AzureAIAgent(client=client, definition=writer_definition, kernel=kernel)

        # Define our prompt to run against the agent
        ##prompt = "What is the best method of evasion for ML models?, I'm looking for tactics of evasion that are effective against ML models."

        # Create threads for three agents
        advisor_thread = AzureAIAgentThread(client=client)
        editor_thread = AzureAIAgentThread(client=client)
        writer_thread = AzureAIAgentThread(client=client)

        # try to run the agent and research threads concurrently
        try:
            # Get response from first agent
            print(f"\n--- Response from {advisor_agent.name} ---")
            agent_response = await advisor_agent.get_response(messages=[portfolio_prompt], thread=advisor_thread)

            # Debug to check the structure of the response
            print(f"Response type: {type(agent_response)}")
            print(f"Content type: {(agent_response.message.content)}")

            # Extract the text content safely based on the actual structure
            if isinstance(agent_response.message.content, list):
                if isinstance(agent_response.message.content[0], str):
                    first_agent_text = agent_response.message.content[0]
                elif hasattr(agent_response.message.content[0], 'text'):
                    first_agent_text = agent_response.message.content[0].text
                else:
                    first_agent_text = str(agent_response.message.content[0])
            else:
                first_agent_text = str(agent_response.message.content)
            
            # Create a new prompt for the research agent that includes the first agent's response
            editor_prompt = f"""
            I received the following investment portfolio recommendation from a financial advisor:

            {first_agent_text}

            Please review this portfolio recommendation for a {age}-year-old investor with {risk_tolerance} risk tolerance 
            aiming for {us_equity_allocation}% US equities and {intl_equity_allocation}% International Equity.

            Please analyze:
            1. The appropriateness of fund selection and allocation percentages
            2. Any gaps or overlooked areas in the portfolio
            3. Potential optimizations for tax efficiency or risk management
            4. Additional considerations based on the investor's age and risk profile

            Provide clear, actionable feedback that would improve this recommendation.
            """

            # Get response from research agent
            print(f"\n--- Response from {editor_definition.name} --- based on Financial Advisor's output")
            research_response = await editing_agent.get_response(messages=[editor_prompt], thread=editor_thread)
            # Extract the research text safely
            if isinstance(research_response.message.content, list):
                if isinstance(research_response.message.content[0], str):
                    research_text = research_response.message.content[0]
                elif hasattr(research_response.message.content[0], 'text'):
                    research_text = research_response.message.content[0].text
                else:
                    research_text = str(research_response.message.content[0])
            else:
                research_text = str(research_response.message.content)
                
            print(research_text)

            # Optional: Ask a follow-up question that combines both insights
            combined_insights = f"""
            Initial Portfolio Recommendation from Financial Advisor:
            {first_agent_text}

            Expert Analysis and Improvements from Editor:
            {research_text}
            """

            FOLLOW_UP = f"""
            Based on both the initial recommendation and expert analysis, create a comprehensive investment plan for a {age}-year-old 
            investor with {risk_tolerance} risk tolerance targeting {us_equity_allocation}% US equities and {intl_equity_allocation}% International Equity.

            Your response should be formatted as a professional investment report with:
            1. Executive Summary
            2. Recommended Fund Allocation (with percentages)
            3. Investment Rationale for Each Selected Fund
            4. Implementation Strategy and Timeline
            5. Expected Performance and Risk Assessment
            6. Monitoring and Rebalancing Guidelines

            Present this in a clear, client-ready format with appropriate sections and formatting.
            """
            # Send follow-up to the first agent with both response
            
            # Send follow-up to the first agent with both responses
            print(f"\n--- Final Investment Report from {writer_definition.name} ---")
            agent_followup = await writing_agent.get_response(
                messages=[combined_insights, FOLLOW_UP], 
                thread=writer_thread
            )
            # Extract the follow-up text safely
            if isinstance(agent_followup.message.content, list):
                if isinstance(agent_followup.message.content[0], str):
                    followup_text = agent_followup.message.content[0]
                elif hasattr(agent_followup.message.content[0], 'text'):
                    followup_text = agent_followup.message.content[0].text
                else:
                    followup_text = str(agent_followup.message.content[0])
            else:
                followup_text = str(agent_followup.message.content)
                
            print(followup_text)
        finally:
            # Clean up threads
            if advisor_thread:
                await advisor_thread.delete()
            if editor_thread:
                await editor_thread.delete()
            if writer_thread:
                await writer_thread.delete()
if __name__ == "__main__":
    asyncio.run(main())
    # Run the main function
