from aiogram import Bot, Dispatcher, types
from aiogram import executor
from sportme import SportmeBooker
from localconfig import logindata, sportmetoken

bot = Bot(token=sportmetoken)
dp = Dispatcher(bot)

login = logindata['inbox']['username']
password = logindata['inbox']['password']


@dp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    if message.text == '/runbooker':
        text = 'booker is on'
        sp = SportmeBooker(login, password)
        sp.run('morning')
        await sp.run('morning')
        await bot.send_message(chat_id, text)
    else:
        text = "Какой-то текст"
        await bot.send_message(chat_id, text)


executor.start_polling(dp)








