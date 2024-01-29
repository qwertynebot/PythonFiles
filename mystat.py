import requests
from bs4 import BeautifulSoup

def login_to_mystat(username, password):
    login_url = 'https://mystat.itstep.org/login/'

    session = requests.Session()

    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, 'html.parser')

    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': password,
    }

    login_response = session.post(login_url, data=login_data)

    if login_response.status_code == 200:
        return session  
    else:
        print(f'Помилка при вході на сайт: {login_response.status_code}')
        return None

def parse_diamond_balance(session):
    balance_url = 'https://mystat.itstep.org/balance/'

    balance_page = session.get(balance_url)

    if balance_page.status_code == 200:
        soup = BeautifulSoup(balance_page.text, 'html.parser')
        diamond_balance_element = soup.find('div', class_='diamond-balance')
        diamond_balance = diamond_balance_element.text.strip()
        return diamond_balance
    else:
        print(f'Помилка при отриманні сторінки балансу: {balance_page.status_code}')
        return None

username = '###'
password = '###'

session = login_to_mystat(username, password)

if session:
    diamond_balance = parse_diamond_balance(session)
    if diamond_balance:
        print(f'Кількість діамантів на балансі: {diamond_balance}')


