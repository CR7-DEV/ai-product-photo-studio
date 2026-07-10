import os
from flask import Flask, send_from_directory, request, jsonify
from google import genai

app = Flask(__name__)

# API Key initialization
client = genai.Client(api_key=os.environ.get("API_KEY"))

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_data = request.json
    user_prompt = user_data.get('prompt', '')
    studio = user_data.get('studio', 'product') # Konsa studio select hua hai

    # Har studio ke liye alag instruction (System Context)
    if studio == 'linkedin':
        system_context = "You are an expert corporate photographer and LinkedIn branding specialist. Provide a short, actionable strategy and execution plan to convert a casual photo into a professional headshot based on user requirement."
    elif studio == 'dating':
        system_context = "You are an expert dating profile consultant. Provide a short, actionable strategy and execution plan to optimize this user's photo for apps like Tinder/Bumble to look high-quality, warm, and highly attractive."
    elif studio == 'instagram':
        system_context = "You are a professional fashion photographer and Instagram influencer manager. Provide a short, actionable strategy to give this photo a highly aesthetic, viral, and model-like look."
    else:
        # Default Product Photo Studio
        system_context = "You are an elite e-commerce product photographer. Provide a short strategy or execution plan for enhancing a Shopify product photo based on user requirement."

    try:
        # Full dynamic prompt combination
        full_prompt = f"{system_context}\n\nUser Request: {user_prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        return jsonify({'result': response.text})
    except Exception as e:
        return jsonify({'result': f"Error: {str(e)}"}), 500