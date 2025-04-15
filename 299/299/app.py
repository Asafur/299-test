from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, static_folder=".", template_folder=".")

# Ollama API endpoint (ensure Ollama is running on port 11434)
OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

@app.route('/')
def index():
    # Serve index.html from the same folder
    return render_template("index.html")

@app.route('/api/chat', methods=['POST'])
def chat():
    """Proxy requests to Ollama for the 'asafur' model."""
    payload = request.get_json()
    # Force the model name to 'asafur' so it uses my .modelfile
    payload["model"] = "asafur"
    
    try:
        # Forward the request to Ollama
        resp = requests.post(OLLAMA_API_URL, json=payload)
        if resp.status_code != 200:
            # If Ollama returned an error, pass that back
            return jsonify({"error": resp.json()}), resp.status_code

        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
