import requests
import concurrent.futures


class DataSource:
    supported_symbols: dict
    endpoint: str

    def fetch_latest_price(self) -> dict:
        pass


class Binance(DataSource):
    def __init__(self):
        self.supported_symbols = {
            "BTC": "BTCUSDT",
            "ETH": "ETHUSDT",
            "LUNA": "LUNAUSDT",
        }
        self.endpoint = "https://api.binance.com/api/v3/ticker/price"

    def _get_single_price(self, symbol: str) -> float:
        response = requests.get(self.endpoint, params={"symbol": symbol})
        return float(response.json()["price"])

    def fetch_latest_price(self) -> dict:
        results = dict.fromkeys(self.supported_symbols)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.supported_symbols)) as executor:
            future_to_symbol = {executor.submit(self._get_single_price, self.supported_symbols[symbol]): symbol for symbol in self.supported_symbols}
            for future in concurrent.futures.as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except Exception as e:
                    raise e
        return results


class CoinGecko(DataSource):
    def __init__(self):
        self.supported_symbols = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "LUNA": "terra-luna",
        }
        self.endpoint = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,terra-luna&vs_currencies=USD"

    def fetch_latest_price(self) -> dict:
        response = requests.get(self.endpoint).json()
        results = {symbol: float(response[self.supported_symbols[symbol]]["usd"]) for symbol in self.supported_symbols}
        return results


binance_source = Binance()
coingecko_source = CoinGecko()
