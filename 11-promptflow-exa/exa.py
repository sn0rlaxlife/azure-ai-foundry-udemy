from exa_py import Exa
from dotenv import load_dotenv
import json
import logging
from promptflow.core import tool
import os
import sys
from typing import List, Dict, Any


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# load env variables
load_dotenv()

try: 
    exa_api_key = os.getenv("EXA_API_KEY")
    if not exa_api_key:
        raise  ValueError("EXA_API_KEY is not set")

    # Initialize Exa Client
    exa = Exa(api_key=exa_api_key)
    logger.info("Exa client initialized successfully")

except Exception as e:
    logger.error(f"Error initializing Exa client: {str(e)}")
    raise

# Define the search function
@tool
def search(query: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Perform a search using Exa SDK

    Args:
      query: Search query to Exa Search
    Returns:
        List[Dict[str, Any]]: List of search results
    """
    try:
        result = exa.search_and_contents(
            query=query,
            type="neural",
            use_autoprompt=True,
            num_results=3,
            text=True,
            subpages=3
        )
        if not result or not result.results:
            logger.warning("No search results found")
            return [], "No search results found"

        output = [{
                "title": item.title,
                "summary": item.text,
                "entity_id": item.url
        } for item in result.results]
        # Logging for completion of the query
        logger.info(f"Search completed for query: {query}")
        return output
    except Exception as e:
        logger.error(f"Error performing search: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python search.py <query>")
        sys.exit(1)
    try:
        query = sys.argv[1]
        results = search(query)
        print(json.dumps(results, indent=4))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
