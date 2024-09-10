import requests

# URL для получения всех монет с CoinMarketCap API
COINMARKETCAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
API_KEY = 'CMC_API_KEY'

def fetch_all_symbols():
    symbols = []
    start = 1  # Начинаем с первой монеты
    limit = 500  # Максимальное количество монет за один запрос
    while True:
        params = {
            'start': start,
            'limit': limit,
            'convert': 'USDT'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY
        }
        try:
            response = requests.get(COINMARKETCAP_URL, params=params, headers=headers)
            response.raise_for_status()  # Проверяем на наличие HTTP ошибок
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            break

        data = response.json().get('data', [])
        if not data:  # Если данные пусты, значит, больше нет монет для загрузки
            break

        for coin in data:
            symbol = f"{coin['symbol']}/USDT"
            symbols.append(symbol)

        start += limit  # Увеличиваем стартовый индекс для следующего запроса

    return symbols

def save_symbols_to_file(symbols):
    try:
        with open('config.py', 'w') as f:
            f.write("symbolsData = [\n")
            f.write(",\n".join(f"    '{symbol}'" for symbol in symbols))
            f.write("\n]\n")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

# Получаем все монеты и их символы
symbolsData = fetch_all_symbols()

# Сохраняем торговые пары в файл config.py
save_symbols_to_file(symbolsData)
print("Торговые пары успешно сохранены в файл config.py")
