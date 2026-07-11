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
        
        # 1. Image Strategy Audit Report (Gemini 2.5 Flash)
        system_rules = (
            "You are an elite AI Photo Studio Retoucher. Analyze the uploaded photo for specific micro-aesthetic flaws. "
            "Based on the chosen studio type, generate a highly compressed action blueprint in exactly 3 bullet points using very easy English. "
            "Focus only on what was corrected (e.g., enhanced skin freshness, replaced cluttered backdrop, styled outfit). "
            "Keep it ultra-short, bold, direct, and limited to maximum 3 short lines."
        )

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=file.content_type)
        text_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, system_rules, f"User Custom Request: {user_prompt}"]
        )

        # 2. Asli Pixel Transformation Engine (Imagen 3.0 Pro)
        # Yeh aapki photo ko analyze karke naya attractive outfit, background aur fresh sharp skin texture dega.
        generation_prompt = (
            f"A premium high-fashion studio headshot, ultra-sharp details, crystal clear eyes and defined nose, "
            f"lively human skin texture with microscopic pores, fresh attractive smile. Reconstruct any blur features. "
            f"Completely remove the old blurry background, replace it with a stunning luxury golden hour outdoor environment. "
            f"Styled elegantly matching {studio} theme. 8k resolution, cinematic lighting, masterfully crafted."
        )

        image_result = client.models.generate_images(
            model='imagen-3.0-generate-002', 
            prompt=generation_prompt,
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
        # Strict Error Reporting: Agar backend API key ya limits issue karein toh real response block dikhega
        return jsonify({'success': False, 'error': f"AI Pipeline error: {str(e)}"}), 500