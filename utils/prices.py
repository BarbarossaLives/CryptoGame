import requests

def get_prices(coins):
    api_key = "YOUR_API_KEY"  # Replace with your real CryptoCompare API key
    url = "https://min-api.cryptocompare.com/data/pricemulti"
    params = {
        "fsyms": ",".join(coins),
        "tsyms": "USD",
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()
