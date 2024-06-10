import requests

url = input('Enter the URL of the article you want to summarize: ')

# Use the https://r.jina.ai/ for reading urls/pdfs or use https://s.jina.ai/ for the search aspect.
def scrape_jina_ai(url: str) -> str:
  response = requests.get("https://r.jina.ai/" + url)
  print(response.text)
  return response.text

scrape_jina_ai(url)
