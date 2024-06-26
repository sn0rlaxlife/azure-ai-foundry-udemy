from promptflow.core import tool

@tool
def process_search_results(results: list):
    def format_article(article: dict):
        return f"Title: {article['title']}\nSummary: {article['summary']}\nURL: {article['url']}"

    try:
        formatted_articles = []
        for result in results:
            formatted_articles.append({
                'title': result['title'],
                'summary': result['summary'],
                # Use .get() to provide a default value if 'entry_id' is missing
                'url': result.get('entry_id', 'No entry ID')  # Provide a sensible default or handle the absence as needed
            })
        articles_str = "\n\n" + "\n\n".join([format_article(a) for a in formatted_articles]) + "\n\n"
        return articles_str
    except Exception as e:
        print(f"Error: {e}")
        return ""
