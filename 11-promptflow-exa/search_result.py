import json
import logging
import sys
from promptflow.core import tool
from typing import Union, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def process_search_results(results: Union[Dict, List, None]) -> str:
    """
    Process search results from Exa SDK with proper validation and error handling.

    Args:
        results: Search results in dict/list format or None
    Returns:
        str: Processed search results or empty string
    """
    try:
        if results is None:
            logger.warning("No search results found")
            return ""

        # Handle single result case
        if isinstance(results, dict):
            results = [results]
        
        # Validate input type    
        if not isinstance(results, list):
            raise ValueError(f"Expected list or dict, got {type(results)}")

        # If result is JSON string, parse it
        if isinstance(results[0], str):
            results = json.loads(results[0])

        def format_article(article: dict) -> str:
            """Format a single article entry"""
            return (f"Title: {article.get('title', 'No Title')}\n"
                   f"Summary: {article.get('summary', 'No Summary')}\n"
                   f"ID: {article.get('entity_id', 'No ID')}")

        formatted_articles = []
        for result in results:
            if not isinstance(result, dict):
                logger.warning(f"Skipping invalid result format: {type(result)}")
                continue
            
            formatted_articles.append({
                'title': result.get('title', ''),
                'summary': result.get('summary', ''),
                'entity_id': result.get('entity_id', '')
            })
        
        return "\n\n" + "\n\n".join([format_article(a) for a in formatted_articles]) + "\n\n" if formatted_articles else ""

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Error processing results: {e}")
        return ""

if __name__ == "__main__":
    try:
        results = json.loads(sys.argv[1])
        processed_results = process_search_results(results)
        print(processed_results)
    except IndexError:
        logger.error("No input provided")
    except json.JSONDecodeError:
        logger.error("Invalid JSON input")
