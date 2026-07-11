import os
import base64
from flask import Flask, send_from_directory, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Gemini Client
client = genai.Client(api_key=os.environ.get("API_KEY"))

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file uploaded'}), 400
        
    file = request.files['image']
    user_prompt = request.form.get('prompt', '')
    studio = request.form.get('studio', 'product')

    try:
        image_bytes = file.read()
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Hyper-Strict Aesthetic Framework (Gagar mein Sagar Prompt Logic)
        system_rules = (
            "You are an elite AI Photo Studio Retoucher. Analyze the uploaded photo for specific micro-aesthetic flaws: "
            "sweat reflection, oil shine, skin blemishes, acne, asymmetrical eyes/nose/ears proportions, weak jawline, hair density/receding hairline/baldness, and lens bloating/body posture issues. "
            "Based on the chosen studio type, generate a highly compressed action blueprint in exactly 3 bullet points using very easy English. "
            "Focus only on what was corrected (e.g., eliminated sweat shine and blemishes, chiseled the jawline structure, filled hairline density, or streamlined lens bloat). "
            "Keep it ultra-short, bold, direct, and limited to maximum 3 short lines."
        )

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=file.content_type)
        
        # Strategy Analysis Pipeline via stable Gemini 2.5 Flash
        text_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, system_rules, f"User Custom Request: {user_prompt}"]
        )

        # Base64 response routing setup
        src_data_url = f"data:{file.content_type};base64,{image_b64}"

        return jsonify({
            'success': True,
            'image_url': src_data_url,
            'strategy': text_response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500