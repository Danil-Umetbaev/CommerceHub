import requests

class PaymentClient:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def create_payment(self, order_id: str, user_id, amount: int):
            json_data = {
                "order_id": order_id,
                "user_id": user_id,
                "amount": amount
            }
            print(f'json_data: {json_data}')
            url = f'{self.base_url}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
            print(f"Requesting: {url}")  # <-- добавить
            response = requests.post(url, headers=headers, json=json_data)
            print("Status:", response.status_code)# <-- добавить
            print("Body:", response.text)
            response.raise_for_status()
            return response.json()
