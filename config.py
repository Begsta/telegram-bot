from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.constants import INVEST_GRPC_API
from datetime import timedelta
import pandas as pd
import warnings
import numpy as np
from tinkoff.invest.utils import now
from ta.volume import ChaikinMoneyFlowIndicator as cmf
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
import matplotlib.pyplot as plt
from keras_visualizer import visualizer
import pandas as pd
import numpy as np
from tqdm.keras import TqdmCallback
from ta.volume import ChaikinMoneyFlowIndicator as cmf,ForceIndexIndicator as fi, MFIIndicator as MFI
from ta.momentum import RSIIndicator as rsi, StochRSIIndicator as SRSI
from ta.trend import MassIndex as MS
from tensorflow import keras


TOKEN = 't.khtwmP8Ppdm9oKaEethxsivDskRL8bUfMJGUBmWpOaNebL7iXXSYzinNYDelASRv9wnmWLLYGdcX3yoSH4nYQw'#'t.LpMsG0FJ4x0NYPKWQD71fXKzXFJqqPs888PthbgCPGGhKKazEVF5D9jk42Hh3Bu9hLOOswmdcSAgTy-8oF_yyw'

token = "1758586899:AAGxCF89bwDTQAblzNgINuYNmOJWQRIQEK4"
admins = ['765087941']
Users = []
warnings.filterwarnings("ignore")

promotion = {
    "Sberbank": "BBG004730N88",
    'Transneft': 'BBG00475KHX6',
    'Gazprom': 'BBG004730RP0'
}
