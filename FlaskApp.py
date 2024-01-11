pip install Flask
python -m venv venv
venv\Scripts\activate
pip install flask-restful flask-sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions_sent = db.relationship('Transaction', backref='sender', lazy=True, foreign_keys='Transaction.sender_id')
    transactions_received = db.relationship('Transaction', backref='receiver', lazy=True, foreign_keys='Transaction.receiver_id')
    contacts = db.relationship('Contact', backref='user', lazy=True)

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify(username=user.username, balance=user.balance), 200

def send_money():
    current_user = get_jwt_identity()
    data = request.get_json()

    amount = data.get('amount')
    receiver_username = data.get('receiver_username')

    sender = User.query.get(current_user)
    receiver = User.query.filter_by(username=receiver_username).first()

    if not receiver:
        return jsonify({'message': 'Receiver not found'}), 404

    if sender.balance < amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Deduct amount from sender's balance
    sender.balance -= amount

    # Add amount to receiver's balance
    receiver.balance += amount

    # Create a new transaction record
    transaction = Transaction(amount=amount, sender_id=sender.id, receiver_id=receiver.id)
    db.session.add(transaction)

    db.session.commit()

    return jsonify({'message': 'Money sent successfully'}), 200

def transaction_history():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    # Fetch transaction history for the user
    sent_transactions = [{'id': t.id, 'amount': t.amount, 'receiver': t.receiver.username, 'timestamp': t.timestamp}
                         for t in user.transactions_sent]

    received_transactions = [{'id': t.id, 'amount': t.amount, 'sender': t.sender.username, 'timestamp': t.timestamp}
                             for t in user.transactions_received]

    # Combine sent and received transactions
    all_transactions = sent_transactions + received_transactions

    # Sort transactions by timestamp in descending order
    all_transactions.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify({'transactions': all_transactions}), 200

def add_contact():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    data = request.get_json()

    new_contact = Contact(name=data['name'], phone=data['phone'], email=data['email'], user=user)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({'message': 'Contact added successfully'}), 201

@app.route('/get-contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    contacts = [{'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}
                for contact in user.contacts]

    return jsonify({'contacts': contacts}), 200

@app.route('/delete-contact/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    if contact.user_id != current_user:
        return jsonify({'message': 'Unauthorized to delete this contact'}), 403

    db.session.delete(contact)
    db.session.commit()

    return jsonify({'message': 'Contact deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
