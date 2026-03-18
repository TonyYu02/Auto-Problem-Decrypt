from flask import Flask, request, jsonify
import json
import requests
import urllib.parse
from decrypt_problem import Decrypt_problem

app = Flask(__name__)
decryptor = Decrypt_problem(header={"User-Agent": "Mozilla/5.0"})

def is_safe_url(url):
    if not url:
        return False
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https":
            return False
        allowed_domains = ["yuketang.cn", "xuetangx.com"]
        if not any(domain in parsed.netloc for domain in allowed_domains):
            return False
        if not parsed.path.endswith(".ttf"):
            return False
        return True
    except Exception:
        return False

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ttf_url = data.get('ttf_url')
    encrypted_text = data.get('text')

    if not ttf_url or not encrypted_text:
        return jsonify({"error": "Missing params"}), 400
    if not is_safe_url(ttf_url):
        return jsonify({"error": "Dangerous or invalid TTF URL"}), 403
        
    try:
        fake_json_str = json.dumps({"text": encrypted_text})
        decrypted_json_str = decryptor.get_encrypt_string(fake_json_str, ttf_url)
        decrypted_text = json.loads(decrypted_json_str)["text"]
        
        return jsonify({"decrypted_text": decrypted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
