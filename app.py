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
        
        # Studio wise strict text contexts - Gagar mein Sagar (Easy Grammar)
        if studio == 'linkedin':
            text_context = (
                "You are a luxury branding expert. Provide a highly compressed 3-bullet-point strategy "
                "in plain, super easy English explaining how we fixed the flat lighting, replaced the messy background "
                "with an elite corporate office blur, and enhanced the attire to a premium look. Keep it ultra short."
            )
            image_generation_prompt = f"A premium corporate LinkedIn headshot of a person, high-end professional business attire, luxury modern blurred office background, professional studio lighting, depth of field, 8k resolution, crisp details. User requirement: {user_prompt}"
        
        elif studio == 'dating':
            text_context = (
                "You are a dating profile consultant. Provide a highly compressed 3-bullet-point strategy "
                "in plain, super easy English explaining how we fixed the flat expressions, added golden hour lighting, "
                "and created a warm high-status lifestyle atmosphere. Keep it ultra short."
            )
            image_generation_prompt = f"An attractive, high-quality profile portrait for Tinder, warm golden hour natural lighting, cinematic bokeh background of a high-end rooftop cafe, smiling naturally, photorealistic, 8k. User requirement: {user_prompt}"
        
        elif studio == 'instagram':
            text_context = (
                "You are a fashion shoot manager. Provide a highly compressed 3-bullet-point strategy "
                "in plain, super easy English explaining how we created high-contrast moody colors, enhanced model physics, "
                "and added a cinematic viral travel aesthetic. Keep it ultra short."
            )
            image_generation_prompt = f"A cinematic aesthetic fashion model shoot, high contrast dramatic lighting, moody editorial color grading, highly fashionable streetwear, cinematic premium city background, hyper-realistic portrait. User requirement: {user_prompt}"
        
        else:
            text_context = (
                "You are an e-commerce designer. Provide a highly compressed 3-bullet-point strategy "
                "in plain, super easy English explaining how we fixed shadows, added high-end commercial placement, "
                "and enhanced colors for high Shopify sales conversions. Keep it ultra short."
            )
            image_generation_prompt = f"A high-end commercial studio product photography shot, luxury marble tabletop, clean minimalistic studio backdrop, perfect soft diffused lighting, ultra-premium commercial quality. User requirement: {user_prompt}"

        # 1. Strategy Generation via Gemini 2.5 Flash
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=file.content_type)
        text_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, text_context]
        )
        
        # 2. IMAGE PIPELINE MODEL FIX: Using production model mapping string bypass handler
        image_result = client.models.generate_images(
            model='imagen-3.0-generate-002', 
            prompt=image_generation_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/jpeg",
                aspect_ratio="3:4" if studio != 'product' else "1:1",
                person_generation="ALLOW_ADULT"
            )
        )
        
        generated_bytes = image_result.generated_images[0].image.image_bytes
        generated_b64 = base64.b64encode(generated_bytes).decode('utf-8')
        output_data_url = f"data:image/jpeg;base64,{generated_b64}"

        return jsonify({
            'success': True,
            'image_url': output_data_url,
            'strategy': text_response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500