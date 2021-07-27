from aiogram import Dispatcher

import logging

from .has_active import IsWork
from .is_admin import IsAdmin


def setup(dp: Dispatcher):
    logging.info('Подключаю filters...')
    dp.filters_factory.bind(IsWork)
    dp.filters_factory.bind(IsAdmin)
