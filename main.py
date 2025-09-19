from flask import Flask, jsonify
from flask_cors import CORS
import logging
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from climate import climate_bp
from database import db
from parking import parking_bp
from automation import automation_bp, process_event
from auth import auth_bp
from meeting_rooms import meeting_rooms_bp

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
            {
                'id': 1, 
                'trigger': {'type': 'motion', 'condition': {'area': 'main_office'}}, 
                'action': {'type': 'lights_on'}, 
                'active': True, 
                'description': "When motion is detected in the Main Office, turn the lights on."
            },
            {
                'id': 2, 
                'trigger': {'type': 'motion', 'condition': {'area': 'meeting_room_empty'}}, 
                'action': {'type': 'lights_off'}, 
                'active': True, 
                'description': "When meeting room is empty (simulated via motion trigger), turn lights off."
            },
            {
                'id': 3, 'trigger': {'type': 'time', 'condition': {'time': '19:00'}}, 
                'action': {'type': 'hvac_off'}, 'active': False, 'description': "Turn off HVAC after business hours (7 PM)."
            }
        ]
        db.automation_rules.insert_many(default_rules)

    # Initialize Meeting Rooms
    if db.meeting_rooms.count_documents({}) == 0:
        logging.info("Application: Initializing meeting rooms...")
        default_rooms = [
            {'id': 1, 'name': 'Neo', 'capacity': 4, 'equipment': ['55" Display', 'Whiteboard']},
            {'id': 2, 'name': 'Trinity', 'capacity': 8, 'equipment': ['75" Display', 'Whiteboard', 'Video Conferencing']},
            {'id': 3, 'name': 'Morpheus', 'capacity': 12, 'equipment': ['Projector', 'Whiteboard', 'Conference Phone']},
            {'id': 4, 'name': 'Smith', 'capacity': 4, 'equipment': ['55" Display', 'Whiteboard']},
        ]
        db.meeting_rooms.insert_many(default_rooms)
        # Bookings collection will be created on first insert.

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

# Timer job to trigger automation events
def time_trigger_job():
    with app.app_context():
        current_time = datetime.now().strftime("%H:%M")
        process_event('time', {'time': current_time})

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
    app.register_blueprint(meeting_rooms_bp)

    # Routes the root app to index.html
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    # Respods to health checks from index.html
    @app.route('/health')
    def health_check():
        logging.warning("Application: Health check successful.")
        logging.info("Application: Health check successful.")
        return jsonify({"status": "OK"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        initialize_database()

    # Initialize and start the scheduler
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(time_trigger_job, 'cron', minute='*')
    scheduler.start()
    
    logging.warning("Application: Starting Officer application on port 5000...")    
    # Use debug=False to prevent the app from running twice (which duplicates scheduler jobs)
    app.run(host='0.0.0.0', port=5000, debug=False)