import os
import base64
from flask import Flask, send_from_directory, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# API Key initialization using latest GenAI library
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

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    try:
        # 1. Image ko base64 bytes mein convert karna multimodal processing ke liye
        image_bytes = file.read()
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 2. Har premium studio ke liye ultra-realistic guidelines select karna
        if studio == 'linkedin':
            system_context = (
                "You are an elite corporate photographer. Analyze this user image and generate a high-end "
                "professional headshot strategy (suit-and-tie, premium office studio background, clean professional look). "
                "Output must contain: 1. Visual Audit of uploaded picture, 2. Studio Lighting Blueprint, 3. Pixel-perfect Transformation steps."
            )
        elif studio == 'dating':
            system_context = (
                "You are an expert dating photographer and profile architect. Analyze this photo to transform it "
                "into an approachable, warm, ultra-premium portrait suitable for top dating tiers. "
                "Output must contain: 1. Charm & Lighting Audit, 2. Background Atmosphere Design, 3. Profile-Boosting Actionable Enhancements."
            )
        elif studio == 'instagram':
            system_context = (
                "You are a luxury fashion and commercial model portrait photographer. Analyze this photo "
                "and craft an elite aesthetic plan to turn it into a high-fashion, high-contrast, moody model aesthetic. "
                "Output must contain: 1. Model Vibe Audit, 2. Cinematic Color & Environment Blueprint, 3. Viral Visual Transformation details."
            )
        else:
            system_context = (
                "You are an elite e-commerce commercial product catalog designer. Analyze this product photo "
                "to completely revamp its context for luxury Shopify storefronts. "
                "Output must contain: 1. Product Placement Audit, 2. High-end Studio Stage Lighting Blueprint, 3. Commercial Conversion details."
            )

        # 3. GenAI execution using Multimodal capabilities (Image + Context Text)
        full_prompt = f"{system_context}\n\nUser Transformation Requirement: {user_prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=file.content_type
                ),
                full_prompt
            ]
        )
        
        # 4. User interface par raw source render karne ke liye base64 text return karna
        src_data_url = f"data:{file.content_type};base64,{image_b64}"

        return jsonify({
            'success': True,
            'image_url': src_data_url, # Frontend par preview ke liye pass ho raha hai
            'strategy': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500