import requests
from keys import API_KEY

r = requests.get(f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={API_KEY}&limit=5000')
print(r.json()['data'][0])
data = r.json()['data']
lines = ''
for coin in data:
    lines += coin['name'] + ' ' + str(coin['quote']['USD']['price']) + '\n'

with open('crypto.txt', mode='w', encoding='utf-8') as file_object:
        print(lines, file=file_object)