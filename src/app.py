from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from flask_migrate import Migrate
from models import User, db
import bcrypt

app = Flask(__name__)
CORS(app)
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
    req = request.form
    
    for user in users:
        if user.username == req.get('ussername'):
            return json.dumps({ 'success': False, 'reason': 'username' })

    for user in users:
        if user.email == req.get('email'):
            return json.dumps({ 'success': False, 'reason': 'email' })

    if req['password'] != req.get('confirmPassword'):
        return json.dumps({ 'success': False, 'reason': 'password' })
    
    try:
        user = User(
            req.get('username'),
            req.get('email'),
            bcrypt.hashpw(req.get('password').encode('utf-8'), bcrypt.gensalt()),
            req.get('firstName'),
            req.get('lastName')
        )
        db.session.add(user)
        db.session.commit()
        return { 'success': True }
    except Exception as e:
        return { 'success': False, 'error': e.args }



@app.route('/login', methods=['POST'])
def login():
    username_attempt = request.form.get('username')
    password_attempt = request.form.get('password')

    user = User.query.filter_by(username=username_attempt).first_or_404()

    if (bcrypt.checkpw(password_attempt, user.password)):
        return json.dumps({'auth': True})
    else:
        return json.dumps({'auth': False})


