from flask import Flask, request, jsonify, send_from_directory
from google import genai
import os

app = Flask(__name__)

# Aapki original correct key
client = genai.Client(api_key=os.environ.get("API_KEY"))
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_data = request.json
    user_prompt = user_data.get('prompt', '')
    
    system_context = f"Create a short strategy or execution steps based on this product requirements: {user_prompt}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_context
        )
        return jsonify({'result': response.text})
    except Exception as e:
        return jsonify({'result': f"Backend Error: {str(e)}"})

if __name__ == '__main__':
    print("\n🚀 Server running on http://127.0.0.1:5000/ \n")
    app.run(debug=True, port=5000)