def extract_articles_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    articles = []
    article = {}
    is_reading_abstract = False
    abstract_text = ''

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("Category:"):
            pass  # You can capture the category here if needed.
        elif stripped_line.startswith("Title:"):
            article["title"] = stripped_line.split("Title:", 1)[1].strip()
        elif stripped_line.startswith("Authors:"):
            pass  # You can capture the authors here if needed.
        elif stripped_line.startswith("Date:"):
            pass  # You can capture the date here if needed.
        elif stripped_line.startswith("Abstract:"):
            is_reading_abstract = True
            abstract_text = stripped_line.split("Abstract:", 1)[1].strip()
        elif stripped_line == "" and is_reading_abstract:  # Assuming a blank line means the end of the abstract.
            is_reading_abstract = False
            article["snippet"] = abstract_text
            articles.append(article)
            article = {}
            abstract_text = ''
        elif is_reading_abstract:
            abstract_text += " " + stripped_line

    return articles


if __name__ == "__main__":
    articles = extract_articles_from_file("/arxiv/arxiv_abstracts.txt")
    save_articles(articles)
