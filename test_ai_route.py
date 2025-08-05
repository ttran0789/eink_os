from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'status': 'error', 'message': 'Please provide an image prompt'})
        
        # For now, just return success without actually generating
        return jsonify({'status': 'success', 'message': f'Would generate image for: {prompt}'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
