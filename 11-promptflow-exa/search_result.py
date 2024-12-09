import json
import sys
from promptflow.core import tool

@tool
def process_search_results(results):
    if results is None:
        return ""
        
    if isinstance(results, tuple):
        results = results[0]  
    
    if not isinstance(results, list):
        return ""

    def format_article(article: dict):
        title = article.get('title') or 'No Title'
        summary = article.get('summary') or 'No Summary'
        entity_id = article.get('entity_id') or 'No ID'
        return f"Title: {title}\nSummary: {summary}\nID: {entity_id}"

    try:
        formatted_articles = []
        for result in results:
            if not isinstance(result, dict):
                continue
            
            formatted_articles.append({
                'title': result.get('title', '') or '',
                'summary': result.get('summary', '') or '',
                'entity_id': result.get('entity_id', '') or ''
            })
        
        return "\n\n" + "\n\n".join([format_article(a) for a in formatted_articles]) + "\n\n" if formatted_articles else ""
    except Exception as e:
        print(f"Error processing results: {e}", file=sys.stderr)
        return ""

# Example usage
if __name__ == "__main__":
    # Load results from input
    results = json.loads(sys.argv[1])
    processed_results = process_search_results(results)
    print(processed_results)
