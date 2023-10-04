import requests
from xml.etree import ElementTree as ET

# List of arXiv categories (you can extend this list as needed)
categories = ['quant-ph', 'hep-th', 'math', 'cs', 'stat', 'astro-ph', 'cond-mat', 'physics']

# Function to fetch articles from a specific category
def fetch_articles_from_category(category):
    URL = f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&start=0&max_results=200"
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to fetch data from arXiv for category {category}.")
        return []
    
    # Parse the API Response
    root = ET.fromstring(response.content)
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    
    # Extract the desired details
    articles = []
    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        published_date = entry.find('{http://www.w3.org/2005/Atom}published').text
        abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text
        
        articles.append({
            'title': title,
            'authors': ", ".join(authors),
            'date': published_date,
            'abstract': abstract
        })
    
    return articles

# Fetch articles across all categories
all_articles = []
for category in categories:
    all_articles.extend(fetch_articles_from_category(category))

# Sort the articles by date
all_articles.sort(key=lambda x: x['date'], reverse=True)

# Save the details to a .txt File
with open('arxiv/arxiv_abstracts.txt', 'w', encoding='utf-8') as f:
    for article in all_articles[:1000]:  # Take the top 1000 articles by date
        f.write("Category: " + article['category'] + '\n')
        f.write("Title: " + article['title'] + '\n')
        f.write("Authors: " + article['authors'] + '\n')
        f.write("Date: " + article['date'] + '\n')
        f.write("Abstract: " + article['abstract'] + '\n\n')

print("Details saved to arxiv_abstracts.txt")
