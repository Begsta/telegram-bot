from trade_bot.config import *



bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


def normalisation(column):
    column = (column - min(column))
    column /= max(column)
    return column

async def send_promotion(promotion1, bull):
    photo = open('to.png', 'rb')
    if bull:
        for user in Users:
            await bot.send_message(user, f"Покупай акцию {promotion1}")
            await bot.send_photo(user, photo)
    elif not bull:
        for user in Users:
            await bot.send_message(user, f"Покупай акцию {promotion1}")
            photo = open('to.png', 'rb')
            await bot.send_photo(user, photo)



async def scan():
    while True:


        with Client(TOKEN) as client:
            for names, figis in promotion.items():
                df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
                # indicators = pd.DataFrame(columns=['cmf', 'date'])
                for candle in client.get_all_candles(
                    figi= figis,
                    from_=now() - timedelta(days=5),
                    interval=CandleInterval.CANDLE_INTERVAL_HOUR,
                ):
                    df = df.append({'Open': np.float64(candle.open.units), 'High': np.float64(candle.high.units),
                                    'Low': np.float64(candle.low.units), 'Close': np.float64(candle.close.units),
                                    'Volume': np.float64(candle.volume),  'Date': candle.time}, ignore_index=True)

                W = 14
                df['cmf'] = cmf(high=df['High'], low=df['Low'], volume=df['Volume'], close=df['Close'],
                                fillna=False, window=W).chaikin_money_flow()
                df['fi'] = fi(volume=df['Volume'], close=df['Close'], fillna=False, window=W).force_index()
                df['rsi'] = rsi(close=df['Close'], fillna=False, window=W).rsi()
                df["MFI"] = MFI(high=df['High'], low=df['Low'], volume=df['Volume'], close=df['Close'],
                                fillna=False, window=W).money_flow_index()
                df['SRSI'] = SRSI(close=df['Close'], fillna=False, window=W).stochrsi()
                df['MS'] = MS(high=df["High"], low=df['Low'], fillna=False).mass_index()
                df = df.dropna().reset_index().drop(columns=['index'])[:-1]
                df_normal = df.copy()
                for i in df_normal.columns[:-1]:
                    df_normal[i] = normalisation(df_normal[i])

                answer = neural_network.predict(df_normal[['cmf', 'rsi', 'MFI', 'SRSI', 'MS']]).T
                up, low = answer
                date = [i.strftime('%dth, %X')[:-3] for i in df['Date']]
                if up[-1] > 0.8:
                    fig, ax = plt.subplots(nrows=1, ncols=1)
                    ax.plot(date, df['Close'][:])
                    ax.set_xticks([d for d in date[::5]])
                    ax.grid()
                    ax.set_title(names)
                    ax.set_ylabel('Цена акции')
                    ax.set_xlabel('Время')
                    fig.savefig('to.png')
                    plt.close(fig)
                    await send_promotion(names, True)
                elif low[-1] > 0.8:
                    fig, ax = plt.subplots(nrows=1, ncols=1)
                    ax.plot(date, df['Close'][:])
                    ax.set_xticks([d for d in date[::5]])
                    ax.grid()
                    ax.set_title(names)
                    ax.set_ylabel('Цена акции')
                    ax.set_xlabel('Время')
                    fig.savefig('to.png')
                    plt.close(fig)
                    await send_promotion(names, False)
            await asyncio.sleep(100)


async def void_for_admin():
    for i in admins:
        await bot.send_message(i, "Бот запущен")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.id not in Users:
        Users.append(message.from_user.id)
    await bot.send_message(message.from_user.id, "Вы стали нашим новым пользователем\n"
                                                 "Если хотите узнать, что я умею, введите команду /help")



@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я бот для трейдинга\n"
                        "Я сканирую биржу и высылаю вам отчёт, какую акцию следует продовать или покупать\n"
                        "При команде /start мы вас добовляем в базу дванных бота\n"
                        "Каждый час бот вам будет присылать сообщения с советом\n"
                        "Совет будет вам помогать с покупками и продажами акций\n")


"""@dp.message_handler(commands=['stop'])
async def stop_parsing(message: types.Message, state: FSMContext):
    # просто обновляем данные
    await bot.send_message(chat_id=message.from_user.id, text="парсинг остановлен")
    await loop.run_in_executor(None, input)
    dp.stop_polling()
    await dp.wait_closed()
    await bot.close()
    sys.exit()"""

if __name__ == '__main__':
    global neural_network
    neural_network = keras.models.load_model('trade_bot/neural')
    loop = asyncio.get_event_loop()
    loop.create_task(void_for_admin())
    loop.create_task(scan())
    loop.run_until_complete(dp.start_polling())