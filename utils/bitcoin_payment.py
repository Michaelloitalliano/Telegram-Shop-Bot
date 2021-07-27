from dataclasses import dataclass
from datetime import datetime
from django_project.telegrambot.usersmanage.models import BotSettings

import blockcypher as bs
from dateutil.tz import tzutc


class AddressDetails:
    def __init__(self, address: str, total_received: int, total_sent: int, balance: int,
                 unconfirmed_balance: int, unconfirmed_txrefs: list, txrefs: list, **kwargs):
        self.address = address
        self.total_received = total_received
        self.total_sent = total_sent
        self.balance = balance
        self.unconfirmed_balance = unconfirmed_balance
        self.unconfirmed_txrefs = unconfirmed_txrefs
        self.txrefs = txrefs


class NotConfirmed(Exception):
    pass


class NotPaymentFound(Exception):
    pass


@dataclass
class Payment:
    amount: int
    rub: int
    created: datetime = None
    success: bool = False

    def create(self):
        self.created = datetime.now(tz=tzutc())

    def check_payment(self):
        settings = BotSettings.objects.first()
        details = bs.get_address_details(address=settings.address_btc, api_key=settings.token_btc)
        address_details = AddressDetails(**details)
        for transactions in address_details.unconfirmed_txrefs:
            if transactions.get('value') == self.amount:
                if transactions.get('received') >= self.created:
                    if transactions.get('confirmations') > 0:
                        return True
                    else:
                        raise NotConfirmed
        for transactions in address_details.txrefs:
            if transactions.get('value') == self.amount:
                if transactions.get('confirmed') >= self.created:
                    return True
        raise NotPaymentFound
