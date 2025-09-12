# Environmental Controls - DevSecOps Project
# << Neorevn >> version 1.8

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging

app = Flask(__name__)

CORS(app)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

office_state = {
    'temperature': 21,
    'hvac_mode': 'off',  # 'off', 'heat', 'cool'
    'lights_on': False
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    if not data:
        logging.warning("No data provided in request.")
        return jsonify({'error': 'No data provided'}), 400

    action = data.get('action')
    value = data.get('value')

    if not action:
        logging.warning("No action specified in request.")
        return jsonify({'error': 'No action specified'}), 400

    if action == 'set_temperature':
        try:
            temp_value = int(value)
            office_state['temperature'] = temp_value
            logging.info(f"Temperature set to: {temp_value}°C")
            return jsonify({'status': 'success', 'message': f"Temperature set to {temp_value}°C"})
        except (ValueError, TypeError):
            logging.warning(f"Invalid temperature value provided: {value}")
            return jsonify({'error': 'Invalid temperature value, must be an integer.'}), 400

    elif action == 'set_hvac_mode':
        if value in ['heat', 'cool', 'off']:
            office_state['hvac_mode'] = value
            logging.info(f"HVAC mode set to: {value}")
            if value == 'heat':
                message = "Heating is now active."
            elif value == 'cool':
                message = "Cooling is now active."
            else:
                message = "HVAC is now off."
            return jsonify({'status': 'success', 'message': message})
        else:
            logging.warning(f"Invalid HVAC mode specified: {value}")
            return jsonify({'error': 'Invalid HVAC mode. Use "heat", "cool", or "off".'}), 400

    elif action == 'set_lights':
        if value not in ['on', 'off']:
            logging.warning(f"Invalid light setting specified: {value}")
            return jsonify({'error': 'Invalid light setting. Use "on" or "off".'}), 400
        
        office_state['lights_on'] = (value == 'on')
        message = f"Lights turned {value}."
        logging.info(message)
        return jsonify({'status': 'success', 'message': message})

    else:
        logging.warning(f"Invalid action specified: {action}")
        return jsonify({'error': 'Invalid action specified'}), 400

@app.route('/status', methods=['GET'])
def status():
    logging.info(f"Status requested. Current state: {office_state}")
    return jsonify(office_state)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    logging.info("Starting the Flask application for local testing...")
    app.run(debug=True)