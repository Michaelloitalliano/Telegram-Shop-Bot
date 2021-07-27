from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .username import UpdateUsername


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(UpdateUsername())
