import requests
import logging
import datetime

url = 'https://api.qiwi.com/partner/bill/v1/bills/'

class QSystem:
    """Инициализируем модуль"""

    def __init__(self, token):
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def create_bill(self, count, comment, bill_ids, lifetime):
        date, microsecond = str(datetime.datetime.now()).split('.')
        if microsecond == 6:
            exp_datetime = (str(datetime.datetime.now() + datetime.timedelta(hours=5)))
        else:
            exp_datetime = (str(datetime.datetime.now() + datetime.timedelta(hours=5)))
            exp_datetime = exp_datetime[0:19]
        am = {'currency': 'RUB', 'value': '{}'.format(count)}
        exp = exp_datetime.replace(' ', 'T') + '+03:00'

        rdata = {'amount': am, 'expirationDateTime': exp,
                 'comment': comment}
        rurl = url + bill_ids

        try:
            response = requests.put(rurl, json=rdata, headers=self.headers, timeout=5)
            cod = response.status_code
            res = response.json()
            if cod == 200:
                return res.get('payUrl')
            else:
                levent = 'qiwi server error (create bill). code - ' + str(cod) + ', response - ' + str(res)
                logging.error(levent)
                return 'error'

        except Exception as e:
            levent = 'protocol error (create bill): ' + str(e)
            logging.error(levent)
            return 'error'

    def cancel_bill(self, bill_num):
        rurl = url + bill_num + '/reject'

        try:
            response = requests.post(rurl, headers=self.headers, timeout=5)
            cod = response.status_code
            res = response.json()
            if cod == 200:
                status = res.get('status')
                return status.get('value')
            else:
                levent = 'qiwi server error (cancel bill). code - ' + str(cod) + ', response - ' + str(res)
                logging.error(levent)
                return 'error'

        except Exception as e:
            levent = 'protocol error (cancel bill): ' + str(e)
            logging.error(levent)
            return 'error'

    def bill_status(self, bill_num):
        rurl = url + bill_num

        try:
            response = requests.get(rurl, headers=self.headers, timeout=5)
            cod = response.status_code
            res = response.json()
            if cod == 200:
                return res
            else:
                if "Invoice not found" in str(res):
                    return True
                levent = 'qiwi server error (bill status). code - ' + str(cod) + ', response - ' + str(res)
                logging.error(levent)
                return 'error'

        except Exception as e:
            levent = 'protocol error (bill status): ' + str(e)
            logging.error(levent)
            return 'error'

class FuckingCard:
    """Инициализируем модуль"""

    def __init__(self, token, number, card_num):
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'  # ваш токен из личного кабинета
        }
        self.number = number
        self.card_num = card_num
    
    def payment_history_last(self, rows_num=10):
        parameters = {'rows': rows_num, 'operation': 'IN'}
        h = requests.get(f'https://edge.qiwi.com/payment-history/v2/persons/{self.number}/payments', params=parameters, headers=self.headers)
        return h.json()["data"]
    
    def check_pay(self, amount):
        payments = self.payment_history_last()
        for payment in payments:
            sum = payment["sum"]["amount"]
            if float(sum)==float(amount):
                return True
        return False