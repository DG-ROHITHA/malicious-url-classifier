from flask import Flask, request, jsonify 
from flask_cors import CORS
import joblib
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load model with error handling
try:
    model = joblib.load("url_classifier.pkl")
    print("✅ ML model loaded successfully")
except FileNotFoundError:
    print("⚠️  Model file not found. Using rule-based mode only.")
    model = None

def extract_features(url):
    """Extract features from URL with improved logic"""
    try:
        domain_part = url.split('/')[2]
    except IndexError:
        domain_part = ''

    # Regex for IPv4 detection
    ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    lower_url = url.lower()
    
    # Fixed protocol detection
    has_https = 1 if lower_url.startswith('https://') else 0
    has_http = 1 if lower_url.startswith('http://') and not has_https else 0

    # Improved suspicious words detection with word boundaries
    suspicious_words = ['login', 'verify', 'secure', 'update', 'account', 'banking']
    has_suspicious = 0
    
    # Check for whole words only (not substrings)
    for word in suspicious_words:
        if re.search(r'(^|[^a-zA-Z0-9])' + word + r'([^a-zA-Z0-9]|$)', lower_url):
            has_suspicious = 1
            break

    return {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'has_https': has_https,
        'has_http': has_http,
        'has_ip': int(bool(ip_pattern.match(domain_part))),
        'has_at_symbol': int('@' in url),
        'num_slashes': url.count('/'),
        'num_hyphens': url.count('-'),
        'is_shortened': int(any(s in domain_part for s in ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly'])),
        'num_digits': sum(char.isdigit() for char in url),
        'has_suspicious_words': has_suspicious
    }

def is_definitely_safe(url):
    """Rule-based check for known safe domains"""
    safe_domains = [
        'google.', 'youtube.', 'github.', 'wikipedia.', 'stackoverflow.',
        'linkedin.', 'microsoft.', 'apple.', 'python.', 'ubuntu.', 'docker.',
        'nginx.', 'apache.', 'mongodb.', 'postgresql.', 'amazon.', 'facebook.',
        'twitter.', 'instagram.', 'netflix.', 'reddit.', 'gitlab.', 'bitbucket.',
        'medium.', 'quora.', 'spotify.', 'discord.', 'whatsapp.', 'telegram.'
    ]
    return any(domain in url for domain in safe_domains)

def is_definitely_malicious(url):
    """Rule-based check for obvious malicious patterns"""
    malicious_patterns = [
        'login@', 'verify@', 'secure@', 'banking@', 'account@',
        'http://192.168.', 'http://10.0.', 'http://172.16.',
        'http://localhost', 'http://127.0.0.1',
        '//fake-bank', '//phishing-login', '//secure-verify',
        '.exe?', '.zip?', '.scr?', '.bat?', '.cmd?',
        'user@evil.com', 'admin@malicious'
    ]
    return any(pattern in url.lower() for pattern in malicious_patterns)

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint with hybrid approach"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL parameter required"}), 400
            
        url = data['url'].strip()
        if not url:
            return jsonify({"error": "URL cannot be empty"}), 400

        print(f"🔍 Analyzing URL: {url}")

        # PHASE 1: Rule-based safety check
        if is_definitely_safe(url):
            return jsonify({
                "prediction": 0,
                "confidence": 99.0,
                "method": "rule_based_safe",
                "message": "Known safe domain",
                "url": url
            })

        # PHASE 2: Rule-based danger check
        if is_definitely_malicious(url):
            return jsonify({
                "prediction": 1,
                "confidence": 99.0,
                "method": "rule_based_malicious", 
                "message": "Known malicious pattern",
                "url": url
            })

        # PHASE 3: ML model prediction (if available)
        if model:
            features = extract_features(url)
            feature_list = [
                features['url_length'],
                features['num_dots'],
                features['has_https'],
                features['has_http'],
                features['has_ip'],
                features['has_at_symbol'],
                features['num_slashes'],
                features['num_hyphens'],
                features['is_shortened'],
                features['num_digits'],
                features['has_suspicious_words']
            ]

            prediction = model.predict([feature_list])[0]
            confidence = model.predict_proba([feature_list]).max() * 100

            # Only trust high-confidence predictions
            if confidence >= 75:
                return jsonify({
                    "prediction": int(prediction),
                    "confidence": round(confidence, 2),
                    "method": "ml_high_confidence",
                    "message": "ML model prediction",
                    "url": url,
                    "features": features  # For transparency
                })

        # PHASE 4: Default safe when uncertain or no model
        return jsonify({
            "prediction": 0,
            "confidence": 60.0,
            "method": "default_safe",
            "message": "Low confidence or no model - defaulting to safe",
            "url": url
        })

    except Exception as e:
        print(f"❌ Error in prediction: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    """Collect user feedback for model improvement"""
    try:
        data = request.get_json()
        feedback_data = {
            'url': data.get('url'),
            'expected_class': data.get('expected_class'),
            'timestamp': datetime.now().isoformat(),
            'user_agent': request.headers.get('User-Agent')
        }
        
        # Save feedback to file for future model training
        with open('feedback_data.json', 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')
            
        return jsonify({
            "status": "success",
            "message": "Feedback received for model improvement"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Malicious URL Detector API...")
    print("📊 Endpoints:")
    print("   POST /predict     - Analyze a URL")
    print("   POST /feedback    - Provide classification feedback")
    print("   GET  /health      - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)