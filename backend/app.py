from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with database in production)
registrations = []

@app.route('/api/register', methods=['POST'])
def register_business():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'businessName', 'businessCategory', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Create registration record
        registration = {
            'id': len(registrations) + 1,
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'businessName': data['businessName'],
            'businessCategory': data['businessCategory'],
            'location': data['location'],
            'registeredAt': datetime.now().isoformat()
        }
        
        registrations.append(registration)
        
        return jsonify({
            'success': True,
            'message': 'Business registered successfully!',
            'data': registration
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    """Get all registrations (for admin/debugging purposes)"""
    return jsonify({
        'success': True,
        'count': len(registrations),
        'data': registrations
    }), 200

@app.route('/api/registrations/count', methods=['GET'])
def get_registration_count():
    """Get the count of registrations"""
    return jsonify({
        'success': True,
        'count': len(registrations)
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

