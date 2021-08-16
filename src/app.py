import time
import bcrypt
import requests
import schedule
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

import keys
from models import User, db
from btc_svc_reader import get_sample_btc_data

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://localhost:5432/coined_db?user={keys.DB_USERNAME}&password={keys.DB_PASSWORD}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#scheduled job that will get the coin data in intervals rather than making api call
#for every page load
coins = []
def get_crypto_data():
    r = requests.get(f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={keys.API_KEY}&limit=100')
    data = r.json()['data']
    
    print("getting some data")

    global coins
    coins = []

    for coin in data:
        coins.append({
            'name': coin['name'],
            'price': coin['quote']['USD']['price'],
            'percentChange24hr': coin['quote']['USD']['percent_change_24h'],
            'volume24hr': coin['quote']['USD']['volume_24h'],
            'marketCap': coin['quote']['USD']['market_cap']
        })
get_crypto_data()
schedule.every(2).hours.do(get_crypto_data)
def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading._start_new_thread(run_scheduled_jobs, ())

#routes, need to restructure these into separate packages instead of one big file later
@app.route('/users', methods=['GET'])
def get_all_users():
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
    return { 'users': users }


@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    result = User.query.filter_by(id=user_id).first_or_404()
    user = {
        'id': result.id,
        'username': result.username,
        'email': result.email,
        'password': result.password,
        'firstName': result.first_name,
        'lastName': result.last_name
    }
    return { 'user': user }


@app.route('/users', methods=['POST'])
def create_user():
    users = User.query.all()
    req = request.form

    for user in users:
        if user.username == req.get('username'):
            return { 'success': False, 'reason': 'username' }

    for user in users:
        if user.email == req.get('email'):
            return { 'success': False, 'reason': 'email' }

    if req['password'] != req.get('confirmPassword'):
        return { 'success': False, 'reason': 'password' }

    try:
        user = User(
            req.get('username'),
            req.get('email'),
            bcrypt.hashpw(req.get('password').encode(
                'utf-8'), bcrypt.gensalt()).decode('utf8'),
            req.get('firstName'),
            req.get('lastName')
        )
        db.session.add(user)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e.args}


@app.route('/login', methods=['POST'])
def login():
    req = request.form

    user = User.query.filter_by(username=req.get('username')).first()

    if user is None:
        return {'success': False}

    if (bcrypt.checkpw(req.get('password').encode(
                'utf-8'), user.password.encode(
                'utf-8'))):
        return {
            'success': True, 
            'userInfo': {
                'id': user.id,
                'username': user.username,
                'password': user.password
            }
        }
    else:
        return { 'success': False }

@app.route('/auth', methods=['POST'])
def auth():
    req = request.form
    user = User.query.filter_by(username=req.get('username')).first()

    if user is None:
        return {'success': False}
    
    if (req.get('password') == user.password):
        return {'success': True}
    else:
        return {'success': False}

@app.route('/coins', methods=['GET'])
def get_all_coins():
    args = request.args.get('coins')
    global coins

    #get every coin
    if args is None:

        biggest_movers = coins.copy()
        biggest_movers.sort(key=lambda coin : abs(float(coin['percentChange24hr'])), reverse=True)
        
        biggest_winners = coins.copy()
        biggest_winners.sort(key=lambda coin : float(coin['percentChange24hr']), reverse=True)
        
        biggest_losers = coins.copy()
        biggest_losers.sort(key=lambda coin : float(coin['percentChange24hr']), reverse=False)
        
        biggest_market_cap = coins.copy()
        biggest_market_cap.sort(key=lambda coin : float(coin['marketCap']), reverse=True)

        biggest_volume = coins.copy()
        biggest_volume.sort(key=lambda coin : float(coin['volume24hr']), reverse=True)

        return { 'coins': coins[:24], 
                'biggestMovers': biggest_movers[:24],
                'biggestWinners': biggest_winners[:24],
                'biggestLosers': biggest_losers[:24],
                'biggestMarketCap': biggest_market_cap[:24],
                'biggestVolume': biggest_volume[:24]
                }

    names = args.split(',')
    filtered_coins = list(filter(lambda coin : coin['name'].lower() in names, coins))
    for coin in filtered_coins:
        # coin['history'] = get_sample_btc_data()
        coin['history'] = get_sample_btc_data()
    return { 'coins': list(filtered_coins) }


    

@app.route('/coins/historical', methods=['GET'])
def get_coin_history():
    coin_names = request.args.get('coinNames')
    pass
    
    """
    TODO:
        Setup API call for coin historical data once we have it.
        Take query string with the names of coins data is needed for.
    """