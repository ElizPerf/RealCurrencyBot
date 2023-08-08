import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, target, amount):
        try:
            base_code = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            target_code = exchanges[target.lower()]
        except KeyError:
            raise APIException(f"Валюта {target} не найдена!")

        if base_code == target_code:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f"https://v6.exchangerate-api.com/v6/5a4744b8df02aa9f0d513b61/pair/{base_code}/{target_code}")
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {target} : {new_price}"
        return message
