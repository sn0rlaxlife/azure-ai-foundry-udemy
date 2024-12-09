from exa_py import Exa
from dotenv import load_dotenv
import json
from promptflow.core import tool
import os
import sys
from typing import Tuple, List, Dict, Any


# load env variables
load_dotenv()
exa_api_key = os.getenv("EXA_API_KEY")


# Initialize Exa Client
exa = Exa(api_key=exa_api_key)

# Define the search function
@tool
def search(query: str, count: int) -> Tuple[List[Dict[str, Any]], str]:
    """
    Perform a search using Exa SDK

    @param query: Search query
    @param count: Number of results to return
    @return: Tuple of (list of search results, search message)
    """

    result = exa.search_and_contents(
        query=query,
        type="neural",
        use_autoprompt=True,
        num_results=5,
        text=True,
        include_domains=["arxiv.org","bing.com","google.com"]
    )
    output = []

    for i, item in enumerate(result.results):
        output.append({
            "title": item.title,
            "summary": item.text,
            "entity_id": item.url
        })

    # Ensure output is a list
    if not isinstance(output, list):
        output = list(output) if hasattr(output, '__iter__') else [output]

    return output, f"Searching for: {query}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <query> <count")
        sys.exit(1)
    entity = sys.argv[1]
    count = int(sys.argv[2])

    search_results, search_message = search(entity, count)
    print(search_message)
    print(json.dumps(search_results, indent=4))
