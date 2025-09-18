from flask import Flask, jsonify
from flask_cors import CORS
import logging
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from climate import climate_bp
from database import db
from parking import parking_bp
from automation import automation_bp
from auth import auth_bp

# Load environment variables from .env file at the very beginning
load_dotenv()


# Initializes the entire database for first startup
def initialize_database():
    logging.info("Application: Checking database initialization...")

    # Initialize Office State
    if db.state.count_documents({}) == 0:
        logging.info("Application: Initializing office state...")
        db.state.insert_one({
            '_id': 'office',
            'temperature': 21,
            'hvac_mode': 'off',
            'lights_on': False
        })

    # Initialize Parking Spots
    if db.parking_spots.count_documents({}) == 0:
        logging.info("Application: Initializing 20 parking spots...")
        db.parking_spots.insert_many([{'id': i, 'is_available': True} for i in range(1, 21)])

    # Initialize default Automation Rules
    if db.automation_rules.count_documents({}) == 0:
        logging.info("Application: Initializing default automation rules...")
        default_rules = [
            {'id': 1, 'trigger': 'motion', 'action': 'lights_on', 'area': 'main_office', 'active': True, 'description': "When motion is detected in the Main Office, turn the lights on."},
            {'id': 2, 'trigger': 'motion', 'action': 'lights_off', 'area': 'meeting_room_empty', 'active': True, 'description': "When meeting room is empty (simulated via motion trigger), turn lights off."},
            {'id': 3, 'trigger': 'time', 'action': 'hvac_off', 'area': 'after_hours', 'active': False, 'description': "Turn off HVAC after business hours (7 PM) (simulated via trigger)."}
        ]
        db.automation_rules.insert_many(default_rules)

    # Initialize default Users
    if db.users.count_documents({}) == 0:
        logging.info("Application: Initializing users...")
        users_to_create = [
            # Admins
            {'username': 'admin1', 'password': generate_password_hash('adminpass1'), 'role': 'admin'},
            # Users
            {'username': 'user1', 'password': generate_password_hash('userpass1'), 'role': 'user'}
        ]
        db.users.insert_many(users_to_create)

    logging.info("Application: Database initialization check complete.")

def create_app():
    app = Flask(__name__, static_folder='.', static_url_path='')
    CORS(app)

    # Serverside logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Register Blueprints
    app.register_blueprint(climate_bp)
    app.register_blueprint(parking_bp)
    app.register_blueprint(automation_bp)
    app.register_blueprint(auth_bp)

    # Routes the root app to index.html
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    # Respods to health checks from index.html
    @app.route('/health')
    def health_check():
        logging.warning("Application: Health check successful.")
        return jsonify({"status": "OK"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    initialize_database()
    logging.warning("Application: Starting Officer application on port 5000...")
    app.run(port=5000, debug=True)