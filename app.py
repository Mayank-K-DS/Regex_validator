from flask import Flask, render_template, request, jsonify, redirect, url_for
import re
import os
import uuid
from datetime import datetime
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Create necessary directories
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('history', exist_ok=True)

# Phone number regex patterns by country
phone_patterns = {
    'US': r'^\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$',
    'UK': r'^\+?44\s?(\d{2,5})\s?(\d{3,4})\s?(\d{3,4})$',
    'India': r'^\+?91?\s?(\d{3,5})\s?(\d{3,5})\s?(\d{4})$',
    'Australia': r'^\+?61\s?(\d{1})\s?(\d{4})\s?(\d{4})$',
    'Germany': r'^\+?49\s?(\d{2,4})\s?(\d{3,7})\s?(\d{2,8})$',
    'China': r'^\+?86\s?(\d{2,3})\s?(\d{4})\s?(\d{4})$',
    'France': r'^\+?33\s?(\d{1})\s?(\d{2})\s?(\d{2})\s?(\d{2})\s?(\d{2})$',
    'Canada': r'^\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$',
}

# Email regex pattern
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Date regex patterns
date_patterns = {
    'MM/DD/YYYY': r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$',
    'DD/MM/YYYY': r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d\d$',
    'YYYY-MM-DD': r'^(19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$',
    'Month DD, YYYY': r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s(0[1-9]|[12][0-9]|3[01]),\s(19|20)\d\d$'
}

# IP-based history file handlers
def get_client_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip.replace(":", "_")  # sanitize for filename

def get_history_path():
    ip = get_client_ip()
    return os.path.join('history', f'{ip}.json')

def load_history():
    path = get_history_path()
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return []

def save_history(history):
    path = get_history_path()
    with open(path, 'w') as file:
        json.dump(history, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/phone')
def phone():
    return render_template('phone.html', countries=sorted(phone_patterns.keys()))

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/date')
def date():
    return render_template('date.html', formats=list(date_patterns.keys()))

@app.route('/history')
def history():
    history_data = load_history()
    return render_template('history.html', history=history_data)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    save_history([])
    return redirect(url_for('history'))

def add_to_history(validator_type, input_value, additional_info, is_valid, message):
    history = load_history()
    history_item = {
        'id': len(history) + 1,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': validator_type,
        'input': input_value,
        'additional_info': additional_info,
        'valid': is_valid,
        'message': message
    }
    history.insert(0, history_item)
    history = history[:50]  # keep last 50
    save_history(history)

@app.route('/validate/phone', methods=['POST'])
def validate_phone():
    phone_number = request.form.get('phone')
    country = request.form.get('country')

    if not phone_number or not country:
        return jsonify({'valid': False, 'message': 'Please provide a phone number and country'})

    if country not in phone_patterns:
        return jsonify({'valid': False, 'message': 'Country not supported'})

    pattern = phone_patterns[country]
    valid = bool(re.match(pattern, phone_number))

    message = f'Valid {country} phone number format' if valid else f'Invalid {country} phone number format'
    add_to_history('Phone', phone_number, country, valid, message)

    return jsonify({'valid': valid, 'message': message})

@app.route('/validate/email', methods=['POST'])
def validate_email():
    email_address = request.form.get('email')

    if not email_address:
        return jsonify({'valid': False, 'message': 'Please provide an email address'})

    valid = bool(re.match(email_pattern, email_address))
    message = 'Valid email format' if valid else 'Invalid email format'
    add_to_history('Email', email_address, None, valid, message)

    return jsonify({'valid': valid, 'message': message})

@app.route('/validate/date', methods=['POST'])
def validate_date():
    date_string = request.form.get('date')
    format_type = request.form.get('format')

    if not date_string or not format_type:
        return jsonify({'valid': False, 'message': 'Please provide a date and format'})

    if format_type not in date_patterns:
        return jsonify({'valid': False, 'message': 'Format not supported'})

    pattern = date_patterns[format_type]
    valid = bool(re.match(pattern, date_string))

    message = f'Valid date in {format_type} format' if valid else f'Invalid date in {format_type} format'
    add_to_history('Date', date_string, format_type, valid, message)

    return jsonify({'valid': valid, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)
