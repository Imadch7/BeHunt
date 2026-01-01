import os
import pyotp
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.path.join(BASE_DIR, '..', 'data', 'totp_secret.txt')

def get_secret():
    if not os.path.exists(SECRET_PATH):
        new_secret = pyotp.random_base32()
        os.makedirs(os.path.dirname(SECRET_PATH), exist_ok=True)

        with open(SECRET_PATH, 'w') as file:
            file.write(new_secret)
        
        print('NEW SECRET GENRATED. Scan the QR code on the dashboard')
        os.chmod(SECRET_PATH, 0o600)

        print(f'NEW SECRET IS: {new_secret}')
        return new_secret, True
        
    with open(SECRET_PATH, 'r') as file:
        return file.read().strip(), False

@app.route('/api/auth-status', methods=['GET'])
def auth_status():
    secret, is_new = get_secret()
    totp = pyotp.totp.TOTP(secret)
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name='Admin', issuer_name='VulnerabilityTool')

    if is_new:
        return jsonify({
            'authenticated': False,
            'uri': uri,
            'now': totp.now()
        })
    
    else:
        return jsonify({
            'authenticated': False,
            'uri': uri,
            'now': totp.now()
        })

@app.route('/api/verify-2fa', methods=['POST'])
def verify_2fa():
    user_code = request.json.get('code')
    print(f'code recieved is: {user_code}')
    secret, _ = get_secret()
    totp = pyotp.totp.TOTP(secret)
    print(f'now is: {totp.now()}')

    if totp.verify(user_code):
        return jsonify({ 'authenticated': True, 'message': 'Authenticated'}), 200
    else:
        return jsonify({ 'authenticated': False, "message": "Invalid Code"}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)