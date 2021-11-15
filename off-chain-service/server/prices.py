from statistics import median

from sources import binance_source, coingecko_source


class CryptoPrice:
    latest: dict
    supported_symbols: list

    def __init__(self):
        self.latest = dict()
        self.supported_symbols = ["BTC", "ETH", "LUNA"]

    def save_latest_price(self) -> None:
        binance_latest = binance_source.fetch_latest_price()
        coingecko_latest = coingecko_source.fetch_latest_price()
        for symbol in self.supported_symbols:
            self.latest[symbol] = round(median([binance_latest[symbol], coingecko_latest[symbol]]), 2)

    def get_latest_price(self) -> dict:
        return self.latest


crypto_price = CryptoPrice()
