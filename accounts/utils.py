import requests
from decimal import Decimal

 

def get_data(currency):
    url = f"https://v6.exchangerate-api.com/v6/d620169727488f74311cfb51/latest/{currency}"
    response = requests.get(url)
    print(response)
    print(response.text)
    return response.json()



def get_exchange_rate(currency_input, currency_output):
    data = get_data(currency_input)
    return data["conversion_rates"][currency_output]


def convert(amount, currency_input, currency_output):
    exchange_rate = get_exchange_rate(currency_input, currency_output)
    return amount * Decimal(exchange_rate)



