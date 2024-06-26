import re
import arxiv
from promptflow.core import tool

def decode_str(string):
    return string.encode().decode("unicode-escape").encode("latin1").decode("utf-8")


def remove_nested_parentheses(string):
    pattern = r"\([^()]+\)"
    while re.search(pattern, string):
        string = re.sub(pattern, "", string)
    return string

# get access to client
@tool
def get_arxiv_articles(entity: str, count: int = 3):
    print(f"Query: {entity}, Max Results: {count}")
    client = arxiv.Client()
    search = arxiv.Search(
        query=entity,
        max_results=count,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = list(client.results(search))  # Convert results to a list here
    print(f"Results obtained: {len(results)}")  # Now results is a list, so this is fine

    processed_results = []
    for result in results:
        # Append processed data to the list
        processed_results.append({
            'title': result.title,  # Consider processing this if necessary
            'summary': result.summary,
            'url': result.entry_id
        })
    # Print process results in the loop
    for article in processed_results:
        print("\nTitle:", article['title'])
        print("Summary:", article['summary'])
        print("URL:", article['url'])
        print("-" * 80)  # Separator for readability

    return processed_results

if __name__ == "__main__":
    get_arxiv_articles()
