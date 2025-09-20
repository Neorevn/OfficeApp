from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)


data = []


# 1. Daily employee check-in
@app.route('/api/wellness/checkin', methods=['POST'])
def checkin():
    info = request.json

    name = info['name']
    mood = info['mood']
    energy = info['energy']
    stress = info['stress']

    record = {
        'name': name,
        'mood': mood,
        'energy': energy,
        'stress': stress,
        'time': str(datetime.now())
    }
    data.append(record)

    # Give advice
    advice = []
    if stress > 7:
        advice.append("Take a break!")
    if energy < 4:
        advice.append("Drink coffee or go for a walk")
    if mood < 5:
        advice.append("Talk to a friend")

    return jsonify({
        'message': 'Thank you! I received your check-in',
        'advice': advice
    })


# 2. Check office air quality
@app.route('/api/wellness/air-quality', methods=['GET'])
def air_quality():
    # Generate random numbers (instead of real sensors)
    co2 = random.randint(400, 1000)
    temp = random.randint(20, 26)
    humidity = random.randint(40, 70)

    status = "Good"
    if co2 > 800:
        status = "Bad - High CO2 levels"
    if temp > 25:
        status = "Too hot"

    return jsonify({
        'co2': co2,
        'temperature': temp,
        'humidity': humidity,
        'status': status
    })


# 3. Check office noise levels
@app.route('/api/wellness/noise-levels', methods=['GET'])
def noise():
    noise_level = random.randint(30, 80)

    if noise_level < 50:
        status = "Quiet - Good for work"
    elif noise_level < 70:
        status = "Moderate"
    else:
        status = "Too noisy!"

    return jsonify({
        'noise_db': noise_level,
        'status': status
    })


# 4. Break reminder
@app.route('/api/wellness/break-reminder', methods=['POST'])
def break_reminder():
    info = request.json
    name = info['name']
    minutes = info.get('minutes', 60)  # How many minutes between breaks

    return jsonify({
        'message': f"Hi {name}! I'll remind you to take a break every {minutes} minutes",
        'tips': [
            "Stand up and walk around",
            "Drink water",
            "Do some stretches"
        ]
    })


# 5. Check chair and desk ergonomics
@app.route('/api/wellness/ergonomics/check', methods=['GET'])
def ergonomics():
    chair_ok = random.choice([True, False])
    desk_height_ok = random.choice([True, False])
    screen_distance_ok = random.choice([True, False])

    problems = []
    if not chair_ok:
        problems.append("Chair is not at the right height")
    if not desk_height_ok:
        problems.append("Desk is too high or too low")
    if not screen_distance_ok:
        problems.append("Screen is too close or too far")

    if not problems:
        problems.append("Everything looks good!")

    return jsonify({
        'problems': problems,
        'tips': [
            "Sit with straight back",
            "Keep feet on floor",
            "Screen at eye level"
        ]
    })


# 6. Mental health support
@app.route('/api/wellness/mental-health/support', methods=['POST'])
def mental_health():
    info = request.json
    name = info['name']
    problem = info.get('problem', 'general')

    resources = {
        'stress': [
            "Breathing exercises",
            "5-minute meditation",
            "Meeting with counselor"
        ],
        'tired': [
            "Take a break",
            "Go outside for fresh air",
            "Drink water"
        ],
        'sad': [
            "Talk to a friend",
            "Call emergency line: 1201",
            "Request meeting with psychologist"
        ]
    }

    help_options = resources.get(problem, [
        "We are here for you",
        "Talk to us anytime",
        "Help line: 1201"
    ])

    return jsonify({
        'message': f"Hi {name}, we are here to help!",
        'help': help_options,
        'emergency': "In emergency: 100 or 1201"
    })




if __name__ == '__main__':
    print("The system is starting to work! 🚀")
    app.run(port=5003)

