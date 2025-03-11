from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# Configure database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Instructor Model
class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomno=db.Column(db.String(20), unique=True, nullable=False)
    seatcap=db.Column(db.Integer,nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# API to Add Instructor
@app.route('/rooms', methods=['POST'])
def add_room():
    data = request.json
    roomno= data.get("roomno")
    seatcap= data.get("seatcap")

    if not roomno or not seatcap:
        return jsonify({"message": "Room No. and seat capacity are required"}), 400

    new_room = Room(roomno=roomno,seatcap=seatcap)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room added successfully"}), 201

# API to Get All Instructors
@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    result = [{"id": i.id, "roomno": i.roomno, "seatcap": i.seatcap} for i in rooms]
    return jsonify(result)


# API to Add Instructor
@app.route('/instructors', methods=['POST'])
def add_instructor():
    data = request.json
    uid = data.get("uid")
    name = data.get("name")

    if not uid or not name:
        return jsonify({"message": "Instructor ID and Name are required"}), 400

    new_instructor = Instructor(uid=uid, name=name)
    db.session.add(new_instructor)
    db.session.commit()

    return jsonify({"message": "Instructor added successfully"}), 201

# API to Get All Instructors
@app.route('/instructors', methods=['GET'])
def get_instructors():
    instructors = Instructor.query.all()
    result = [{"id": i.id, "uid": i.uid, "name": i.name} for i in instructors]
    return jsonify(result)

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        token = jwt.encode(
            {"user": username, "exp": expiration.timestamp()},  # Store expiry as timestamp
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({"access_token": token})

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(debug=True)
