import openai
from aiogram import Bot, Dispatcher, executor, types
import config

openai.api_key = config.TOKENGPT
messages = []

hstr = open('h.txt', 'a')

CHANNEL_ID = "-1001902525507"

bot = Bot(token=config.TOKENTG)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)

    if user_channel_status['status'] != 'left':
        await bot.send_message(message.from_user.id, "Спасибо за подписку на канал! ChatGPT 3.5 готов к работе!")
    else:
        button = types.InlineKeyboardButton("Я подписался", callback_data="Я подписался")
        markup = types.InlineKeyboardMarkup(row_width=1).add(button)

        await bot.send_message(message.from_user.id, "Сначала подпишись на канал! https://t.me/shinkarukdev", reply_markup=markup)


@dispatcher.callback_query_handler(lambda call: True)
async def callback(call: types.CallbackQuery):
    if call.message:
        user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=call.from_user.id)

        if user_channel_status["status"] != "left":
            await bot.send_message(call.from_user.id, "Спасибо за подписку!")
        else:
            await bot.send_message(call.from_user.id, "Вы не подписались :(")


def chatgpt(message):
    messages.append({"role": "user", "content": message})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply



@dispatcher.message_handler()
async def f(message):
    user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)

    if message.text[0] != '/' and user_channel_status["status"] != "left":
        hstr.write(message.text)
        hstr.write('\n')
        await bot.send_message(message.chat.id, 'ChatGPT набирает сообщение...')
        await bot.send_message(message.chat.id, chatgpt(message.text))
    else:
        await bot.send_message(message.chat.id, 'ChatGPT ждет подписки на канал https://t.me/shinkarukdev')


#hstr.close()


if __name__ == '__main__':
    executor.start_polling(dispatcher)
