from flask import Flask
import json
from flask_migrate import Migrate
from models import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/coined_db?user=postgres&password=11292000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/users')
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

@app.route('/users/<user_id>')
def getUserById(user_id):
    result = User.query.filter_by(id=user_id)[0]
    user = {
            'id': result.id,
            'username': result.username,
            'email': result.email,
            'password': result.password,
            'firstName': result.first_name,
            'lastName': result.last_name
    }
    return json.dumps({'user': user})