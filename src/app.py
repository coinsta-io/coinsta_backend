from flask import Flask
from flask_migrate import Migrate
from models import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/coined_db?user=postgres&password=11292000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    user = User('username', 'email@email.com', 'password', 'first', 'last')
    db.session.add(user)
    db.session.commit()
    return "Done!"

