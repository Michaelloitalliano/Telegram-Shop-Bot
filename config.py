from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = 'TG_TOKEN'
bitcoin_address = "bitcoin:{address}?" \
                    "amount={amount}" \
                    "&label={message}"

admins = [
    123
]
