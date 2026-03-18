import json
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from decrypt_problem import Decrypt_problem

app = Flask(__name__)
CORS(app)

decryptor = Decrypt_problem(header={"User-Agent": "Mozilla/5.0"})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ttf_url = data.get('ttf_url')
    encrypted_text = data.get('text')
    
    if not ttf_url or not encrypted_text:
        return jsonify({"error": "Missing params"}), 400
        
    fake_json_str = json.dumps({"text": encrypted_text})
    decrypted_json_str = decryptor.get_encrypt_string(fake_json_str, ttf_url)
    
    decrypted_text = json.loads(decrypted_json_str)["text"]
    return jsonify({"decrypted_text": decrypted_text})

if __name__ == '__main__':
    app.run(port=5000)