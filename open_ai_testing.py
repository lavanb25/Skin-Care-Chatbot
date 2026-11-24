#This is the Final working code

# import requests
# import json

# API_KEY = "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"
# API_URL = "https://openrouter.ai/api/v1/chat/completions"

# # Using OpenAI model (gpt-3.5-turbo)
# payload = {
#     "model": "openai/gpt-3.5-turbo",
#     "messages": [
#         {
#             "role": "system", 
#             "content": "You are a cosmetic skincare assistant. Give a short answer of about 20 words. No explanations or reasoning."
#         },
#         {
#             "role": "user",
#             "content": "I have dark circles. what should I use?. iam dark skined person and i have sensitive skin"
#         }
#     ],
#     "temperature": 0.7,
#     "max_tokens": 100
# }

# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json",
#     "HTTP-Referer": "http://localhost:3000",  # Optional
#     "X-Title": "Cosmetic Chatbot"  # Optional
# }

# response = requests.post(API_URL, json=payload, headers=headers)
# data = response.json()

# print(data['choices'][0]['message']['content'])

#Code along with Frontend
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Route to serve the HTML file
@app.route('/')
def index():
    try:
        return send_file('index.html')
    except:
        return "index.html not found. Make sure it's in the same directory as app.py", 404

# Route for the chat API
@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'success': False,
                'response': 'Please provide a message.'
            })
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a cosmetic skincare assistant. Give helpful, concise answers about skincare and cosmetics. Keep responses brief and informative."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'response': f'API error: {response.status_code}'
            })
            
        ai_response = response.json()
        
        # Check if the response has the expected structure
        if 'choices' in ai_response and len(ai_response['choices']) > 0:
            message_content = ai_response['choices'][0]['message']['content']
        else:
            message_content = "Sorry, I couldn't process that request. Please try again."
        
        return jsonify({
            'success': True,
            'response': message_content
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'success': False,
            'response': f'Sorry, an error occurred: {str(e)}'
        })

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'skincare-assistant'})

if __name__ == '__main__':
    print("Starting Skincare Assistant Server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, port=5000, host='0.0.0.0')