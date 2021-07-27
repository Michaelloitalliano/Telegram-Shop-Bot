import requests as rs, json

class Price():
    def rub_btc(self, rub: int):
        try:
            r = rs.get("https://api.cryptonator.com/api/ticker/rub-btc", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.60 YaBrowser/20.12.0.963 Yowser/2.5 Safari/537.36"})
            data = json.loads(r.text)
            price = float(data["ticker"]["price"])
            return rub*price
        except Exception as ex:
            print(ex)
            return False
    def rub_sat(self, rub: int):
        try:
            r = rs.get("https://api.cryptonator.com/api/ticker/rub-btc", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.60 YaBrowser/20.12.0.963 Yowser/2.5 Safari/537.36"})
            data = json.loads(r.text)
            price = float(data["ticker"]["price"])*(100000000)
            return rub*price
        except Exception as ex:
            print(ex)
            return False
    def btc_rub(self, btc: int):
        try:
            r = rs.get("https://api.cryptonator.com/api/ticker/btc-rub", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.60 YaBrowser/20.12.0.963 Yowser/2.5 Safari/537.36"})
            data = json.loads(r.text)
            price = float(data["ticker"]["price"])
            return btc*price
        except Exception as ex:
            print(ex)
            return False
p = Price()