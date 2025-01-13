import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ensure the "img" folder exists
IMG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(IMG_FOLDER, exist_ok=True)

@app.route('/proxy', methods=['GET'])
def proxy_request():
    # Récupérer les paramètres de la requête
    url = request.args.get('url')
    cookie = request.args.get('cookie')

    if not url or not cookie:
        return jsonify({'error': 'URL and cookie are required'}), 400

    # Effectuer la requête GET à l'API externe
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'identity',
        'accept-language': 'fr',
        'cookie': f'access_token_web={cookie}',
        'referer': 'https://www.vinted.fr',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    try:
        # Faire l'appel GET à l'URL cible
        response = requests.get(url, headers=headers)

        # Vérifier si la réponse est valide
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch data from the external API'}), 500

        # Retourner la réponse JSON à l'utilisateur
        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_image', methods=['POST'])
def save_image():
    try:
        # Get the image URL and ID from the request
        image_url = request.json.get('url')
        image_id = request.json.get('id')

        if not image_url or not image_id:
            return jsonify({"error": "Missing 'url' or 'id' in the request"}), 400

        # Fetch the image
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch the image"}), 500

        # Save the image to the "img" folder with the name "A_{id}"
        filename = f"A_{image_id}.jpg"
        file_path = os.path.join(IMG_FOLDER, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return jsonify({"message": f"Image saved as {filename}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
