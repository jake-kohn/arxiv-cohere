
from flask import Flask, render_template, request, jsonify
import cohere
from extract_arxiv import extract_articles_from_file
from decouple import config

COHERE_KEY = config('COHERE_KEY')

co = cohere.Client(COHERE_KEY)

def get_response(question):
    preface = """I have included abstracts from recently published articles on arxiv. In a moment, I will add a user question. 
    Your job is to use the context to answer the questions. Make sure you reference which articles you cite. You should be professional
    and courteous. Please keep your response fairly short and direct. Here is the user's question: \n
    
    """
    response = co.chat(
        message=preface + question,
        documents=extract_articles_from_file('arxiv/arxiv_abstracts_small.txt'),
        model="command",
        temperature=0.1
    )
    
    return response.text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['user_input']
    results = get_response(user_input)
    return jsonify({"response": str(results)})


if __name__ == "__main__":
    app.run(debug=True)