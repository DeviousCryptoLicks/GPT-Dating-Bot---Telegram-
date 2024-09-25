from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from TOKEN import token, token_AI

from gpt import *
from util import *


async def start(update, context):
    dialog.mode = 'main'
    text = load_message('main')
    await send_photo(update, context, 'main')
    await send_text(update, context, text)
    # await send_text(update, context, '*Command START*')

    await show_main_menu(update, context, {
        "start": "main bot menu",
        "profile": "Tinder profile generation 😎",
        "opener": "message to start a conversation 🥰",
        "message": "conversation on your behalf 😈",
        "date": "conversation with celebrities 🔥",
        "gpt": "ask a question to GPT chat 🧠",
    })


async def gpt(update, context):
    dialog.mode = 'gpt'
    text = load_message('gpt')
    await send_photo(update, context, 'gpt')
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt('gpt')
    answer = await chatgpt.send_question(prompt, text)
    # answer = await chatgpt.send_question("Give a clear and concise answer to the following question:", text)
    await send_text(update, context, answer)
    # await send_text(update, context, '*Communicating with GPT chat*')


async def date(update, context):
    dialog.mode = 'date'
    text = load_message('date')
    await send_photo(update, context, 'date')
    # await send_text(update, context, text)
    await send_text_buttons(update, context, text, {
        'date_grande': 'Ariana Grande',
        'date_robbie': 'Margot Robbie',
        'date_zendaya': 'Zendaya',
        'date_gosling': 'Ryan Gosling',
        'date_hardy': 'Tom Hardy',
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "The other person is typing a message...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)
    # await send_text(update, context, answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_photo(update, context, query)
    await send_text(update, context, 'Great choice! Invite them on a date in 5 messages.')
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = 'message'
    text = load_message('message')
    await send_photo(update, context, 'message')
    await send_text_buttons(update, context, text, {
        'message_next': 'Next message',
        'message_date': 'Invite on a date',
    })
    dialog.list.clear()


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_history = '\n\n'.join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT is formulating a response...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'date':
        await date_dialog(update, context)
    elif dialog.mode == 'message':
        await message_dialog(update, context)
    else:
        await send_text(update, context, '*Hello*')
        await send_text(update, context, '_How are you?_')
        await send_text(update, context, 'You wrote ' + update.message.text)
        await send_photo(update, context, 'avatar_main')
        await send_text_buttons(update, context, 'Start something?', {
            'start': 'Start',
            'stop': 'Stop',
        })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, '*Process started*')
    else:
        await send_text(update, context, '*Process stopped*')


dialog = Dialog()
dialog.mode = None
dialog.list = []

chatgpt = ChatGptService(token=token_AI)

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern='^date_.*'))
app.add_handler(CallbackQueryHandler(message_button, pattern='^message_.*'))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
