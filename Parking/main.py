from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


parking_spots = []
for i in range(1,21):
    parking_spots.append({ 'id':i, 'is_available':True})

reservations = [] # 'id':1, 'name'='moshik'

checkins = []    # 'id':1, 'name'='moshik'

@app.get('/api/parking/spots/available')
def spots_available():
    all_available = []
    for spot in parking_spots:
        if spot['is_available']:
            all_available.append(spot['id'])
    return all_available

@app.get('/api/parking/all-spots')
def get_all_spots():
    detailed_spots = []
    for spot in parking_spots:
        spot_details = spot.copy()
        spot_id = spot_details['id']
        
        is_checked_in = any(c['id'] == spot_id for c in checkins)
        reservation_info = next((r for r in reservations if r['id'] == spot_id), None)

        if is_checked_in:
            spot_details['status'] = 'occupied'
            spot_details['user'] = next((c['name'] for c in checkins if c['id'] == spot_id), 'unknown')
        elif reservation_info:
            spot_details['status'] = 'reserved'
            spot_details['user'] = reservation_info['name']
        else:
            spot_details['status'] = 'available'
            spot_details['user'] = None
        detailed_spots.append(spot_details)
    return jsonify(detailed_spots)

@app.post('/api/parking/reserve')
def reserve():
    name_to_reserve_for = request.json['name']
    id_to_reserve = request.json['id']
    for spot in parking_spots:
        if spot['id'] == id_to_reserve:
            if spot['is_available']:
                spot['is_available'] = False
                reservation = {'id':id_to_reserve, 'name':name_to_reserve_for}
                reservations.append(reservation)
                return 'parking is reserved', 201
            else:
                return 'parking is not available. cannot reserve', 401
    return 'parking id does not exist', 401

#* GET /api/parking/my-reservations View my parking reservations
@app.post('/api/parking/my-reservations')
def my_reservations():
    name = request.json['name']
    all_my_reservations = []
    for reservation in reservations:
        if reservation['name'] == name:
            all_my_reservations.append(reservation['id'])
    return all_my_reservations

#* POST /api/parking/checkin Check into reserved spot
@app.post('/api/parking/checkin')
def checkin():
    name = request.json['name']
    id_to_checkin = request.json['id']

    for reservation in reservations:
        if reservation['name'] == name and reservation['id'] == id_to_checkin:
            # is already chejcked in?
            for checkin in checkins:
                if checkin['name'] == name and checkin['id'] == id_to_checkin:
                    return 'cannot checkin because you already checked-in!', 401
            checkins.append({'id': id_to_checkin, 'name':name})
            return 'checked in successfully', 201

    return 'cannot checkin because you didnt reserve', 401


#* GET /api/parking/violations Check parking violations
@app.get('/api/parking/violations')
def violations():
    all_violations = []
    for reservation in reservations:
        for other_reservation in reservations:
            if reservation['id'] == other_reservation['id']:
                if reservation['name'] != other_reservation['name']:
                    all_violations.append({'id':reservation['id'], 'violation': 'reserved by two people'})
    return all_violations

#* POST /api/parking/guest-pass Generate guest parking pass
@app.post('/api/parking/guest-pass')
def guest_pass():
    name_to_reserve_for = "guest"
    id_to_reserve = request.json['id']
    for spot in parking_spots:
        if spot['id'] == id_to_reserve:
            if spot['is_available']:
                spot['is_available'] = False
                reservation = {'id': id_to_reserve, 'name': name_to_reserve_for}
                reservations.append(reservation)
                return 'parking is reserved', 201
            else:
                return 'parking is not available. cannot reserve', 401
    return 'parking id does not exist', 401


if __name__ == '__main__':
    app.run(port=5001)
