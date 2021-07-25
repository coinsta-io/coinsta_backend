from flask import Flask, request, jsonify
import json
from flask_migrate import Migrate
from models import User, db
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/coined_db?user=postgres&password=11292000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/users', methods=['GET'])
def getAllUsers():
    results = User.query.all()
    users = []
    for user in results:
        users.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'firstName': user.first_name,
            'lastName': user.last_name
        })
    return json.dumps({'users': users})


@app.route('/users/<user_id>', methods=['GET'])
def getUserById(user_id):
    result = User.query.filter_by(id=user_id).first_or_404()
    user = {
            'id': result.id,
            'username': result.username,
            'email': result.email,
            'password': result.password,
            'firstName': result.first_name,
            'lastName': result.last_name
    }
    return json.dumps({ 'user': user })


@app.route('/users', methods=['POST'])
def createUser():
    users = User.query.all()
    req = request.get_json(force=True)
    for user in users:
        if user.username == req['username']:
            return json.dumps({ 'success': False, 'reason': 'username' })

    for user in users:
        if user.email == req['email']:
            return json.dumps({ 'success': False, 'reason': 'email' })

    if req['password'] != req['confirmPassword']:
        return json.dumps({ 'success': False, 'reason': 'password' })
    
    try:
        user = User(
            req['username'],
            req['email'],
            bcrypt.hashpw(req['password'].encode('utf-8'), bcrypt.gensalt()),
            req['firstName'],
            req['lastName']
        )
        db.session.add(user)
        db.session.commit()
        return json.dumps({ 'success': True })
    except Exception as e:
        return json.dumps({ 'success': False, 'error': e.args })



@app.route('/login', methods=['POST'])
def login():
    username_attempt = request.form.get('username')
    password_attempt = request.form.get('password')

    user = User.query.filter_by(username=username_attempt).first_or_404()

    if (bcrypt.checkpw(password_attempt, user.password)):
        return json.dumps({'auth': True})
    else:
        return json.dumps({'auth': False})


