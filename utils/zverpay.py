import requests

class ZverPay:
    def __init__(self):
        super().__init__()
        self.secret = "SECRET_KEY"
        self.shop_id = "SHOP_ID"
    
    def create_pay(self, amount, direction):
        res = requests.post("https://api", data={"direction":direction, "currency":"UAH", "amount":amount, "shop_id":self.shop_id, "secret_key":self.secret})
        data = res.json()
        if not data["success"]:
            return False
        invoice = data["invoice"]
        link = data["pay_link"]
        return invoice, link
    
    def check_pay(self, invoice):
        res = requests.post("https://api", data={"invoice":invoice, "shop_id":self.shop_id, "secret_key":self.secret})
        data = res.json()
        if not data["success"]:
            return False
        status = data["status"]
        if status=="PAID":
            return True, data["amount_total"]
        else:
            return False, False