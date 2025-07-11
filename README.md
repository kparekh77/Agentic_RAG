# Agentic RAG: Python Package Tutorial Assistant

An agentic, retrieval-augmented generation (RAG) tool that dynamically pulls live documentation and auto-generates runnable tutorials with five code examples for any Python package.

---

## Project Description

Agentic RAG combines live web search via SerpAPI, LangChain document loaders, Chroma vector embeddings, and LangGraph orchestration to build an AI teaching assistant. Given a package name, it:

1. **Discovers** up-to-date documentation URLs via Google Search  
2. **Ingests** and **chunks** the pages into manageable text  
3. **Embeds** and **indexes** the chunks for semantic retrieval  
4. **Orchestrates** a LangGraph workflow that loops between a retrieval tool and an OpenAI chat model  
5. **Produces** a step-by-step tutorial with five runnable code examples

---

## Features

- 🔍 **Dynamic Documentation Retrieval**  
  Uses SerpAPI to find and load the latest doc links for any package.

- 🧠 **Semantic Context Engineering**  
  Splits, embeds, and stores documentation chunks in Chroma for relevant, focused retrieval.

- 🤖 **Agentic Workflow**  
  Leverages LangGraph’s state machine and ToolNode pattern to call retrieval tools on-demand.

- ✍️ **Prompt Engineering**  
  System + user messages guide the model to output a clear, five-example tutorial.

- ⚙️ **Fallback & Logging**  
  Automatically falls back to canonical URLs if live search fails, with INFO/WARNING logs.

---

## Tech Stack

- **Language & Runtime:** Python 3.12  
- **LLM & Embeddings:** OpenAI Chat API, `langchain_openai.embeddings.OpenAIEmbeddings`  
- **Retrieval:** SerpAPI, `UnstructuredURLLoader` (LangChain)  
- **Vector Store:** Chroma (via `langchain_community.vectorstores.Chroma`)  
- **Orchestration:** LangGraph (`StateGraph`, `ToolNode`, `MemorySaver`)  
- **Tooling:** Poetry or pip, python-dotenv for configuration  

---

## Installation

```bash
# Clone the repo
git clone git@github.com:kparekh77/Agentic_RAG.git
cd Agentic_RAG

# Create and activate a virtualenv (optional, but recommended)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt


```

---

## Configuration

Create a .env file in the project root:

- OPENAI_API_KEY=sk-...
- OPENAI_MODEL=gpt-4.1-mini
- SERPAPI_API_KEY=your_serpapi_key

---

## Example Usage

```bash

python -m src.main flask
```

## Example Output


INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:src.clients.context_retriever:retrieve_context: found 6 links for 'flask'
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Flask is a lightweight and easy-to-use Python web framework that allows you to build web applications quickly. It is designed to be simple and flexible, making it a great choice for beginners and small to medium projects.

Here's a step-by-step tutorial on using Flask, including five runnable code examples demonstrating key features:

### Step 1: Installation
First, install Flask using pip:
```bash
pip install flask
```

### Step 2: Basic Flask Application
Create a simple web server that returns "Hello, World!" when accessed.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```
Run this script and open http://127.0.0.1:5000/ in your browser.

---

### Example 1: Routing with Variables
You can capture parts of the URL as variables.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'

if __name__ == '__main__':
    app.run(debug=True)
```
Accessing `/user/Alice` will display "User: Alice".

---

### Example 2: HTTP Methods (GET and POST)
Handle different HTTP methods in your routes.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Logging in...'
    else:
        return 'Please log in.'

if __name__ == '__main__':
    app.run(debug=True)
```
Visit `/login` with GET and POST requests to see different responses.

---

### Example 3: Rendering Templates
Use HTML templates to render dynamic content.

Create a folder named `templates` and inside it create `hello.html`:
```html
<!doctype html>
<title>Hello</title>
<h1>Hello, {{ name }}!</h1>
```

Then use this Flask app:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
```
Access `/hello/World` to see the rendered HTML.

---

### Example 4: Using URL Query Parameters
Read query parameters from the URL.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f'Search results for: {query}'

if __name__ == '__main__':
    app.run(debug=True)
```
Visit `/search?q=flask` to see the search query echoed.

---

### Example 5: JSON Response
Return JSON data from your Flask app.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = {'name': 'Flask', 'type': 'framework', 'language': 'Python'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```
Access `/api/data` to get a JSON response.

---

These examples cover the basics of Flask: routing, handling HTTP methods, templates, query parameters, and JSON responses. Flask is very flexible and can be extended with many plugins for databases, authentication, and more. For detailed documentation, visit https://flask.palletsprojects.com/.
