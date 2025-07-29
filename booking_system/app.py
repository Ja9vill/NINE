from datetime import datetime
from flask import Flask, request, jsonify

from .models import db, Room, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json() or request.form
    if 'name' not in data:
        return jsonify({'error': 'name required'}), 400
    room = Room(name=data['name'])
    db.session.add(room)
    db.session.commit()
    return jsonify({'id': room.id, 'name': room.name})


@app.route('/rooms', methods=['GET'])
def list_rooms():
    rooms = Room.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in rooms])


@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json() or request.form
    required = ['room_id', 'user_name', 'start_time', 'end_time']
    if not all(key in data for key in required):
        return jsonify({'error': 'room_id, user_name, start_time, end_time required'}), 400
    room = Room.query.get_or_404(int(data['room_id']))
    start = datetime.fromisoformat(data['start_time'])
    end = datetime.fromisoformat(data['end_time'])
    booking = Booking(room=room, user_name=data['user_name'], start_time=start, end_time=end)
    db.session.add(booking)
    db.session.commit()
    return jsonify({'id': booking.id})


@app.route('/bookings', methods=['GET'])
def list_bookings():
    bookings = Booking.query.all()
    result = []
    for b in bookings:
        result.append({
            'id': b.id,
            'room_id': b.room_id,
            'user_name': b.user_name,
            'start_time': b.start_time.isoformat(),
            'end_time': b.end_time.isoformat(),
        })
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
