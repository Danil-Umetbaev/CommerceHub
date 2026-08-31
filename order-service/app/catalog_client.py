import requests
class CatalogClient:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_product(self, product_id: str):
            url = f'{self.base_url}/{product_id}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
            print(f"Requesting: {url}")  # <-- добавить
            response = requests.get(url, headers=headers, timeout=10)
            print("Status:", response.status_code)
            print("Headers:", response.headers)   # <-- добавить
            print("Body:", response.text)
            response.raise_for_status()
            return response.json()