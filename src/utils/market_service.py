from pycoingecko import CoinGeckoAPI


class MarketService:
    def __init__(self):
        self.coingecko = CoinGeckoAPI()
        self.coingecko.request_timeout = 15
        self.currency = 'usd'

    def get_price(self, coin_id):
        market_info = self.coingecko.get_coins_markets(vs_currency=self.currency, ids=[coin_id])
        price = market_info[0]['current_price'] if market_info else 0
        return price

    def get_tokens_price_coingecko(self, coin_ids):
        market_infos = self.coingecko.get_coins_markets(vs_currency=self.currency, ids=coin_ids)
        prices = {}
        for market_info in market_infos:
            prices[market_info['id']] = market_info['current_price']
        return prices
