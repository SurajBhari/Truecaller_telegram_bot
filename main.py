import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
from random import choice 
from json import load 

with open("config.json", "r") as f:
    data = load(f)
    api = data["bot_token"]


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def truecaller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = update.message.text
    content = content[-10:]
    try:
        content = int(content)
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a valid number")
        return
    info = search(content)
    print(content)
    print(info)
    if not info:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No info found or server too busy")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=info)


def search(num):
    with open("config.json", "r") as f:
        bearers = load(f)["bearers"]
    bearer = choice(bearers)
    head={
        "Host": "search5-noneu.truecaller.com",
        "authorization": f"{bearer}",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/13.23.9 (Android;11)"
    } 
    url = f"https://search5-noneu.truecaller.com/v2/search?q={num}&countryCode=IN&type=4&locAddr=&encoding=json"
    req=requests.get(url,headers=head)
    print(req)
    print(req.text)
    if req.status_code != 200:
        return False
    try:
        data=req.json()
        print(data)
        if data:
            # write to a json file for debugging
            from json import dump
            with open('data.json', 'w') as f:
                dump(data, f, indent=4)
            to_send = ""
            try:
                to_send += f"Name: {data['data'][0]['name']}\n"
            except:
                pass
            try:
                to_send += f"Carrier: {data['data'][0]['phones'][0]['carrier']}\n"
            except:
                pass
            try:
                to_send += f"Email: {data['data'][0]['internetAddresses'][0]['id']}\n"
            except:
                pass
            try:
                to_send += f"Address: {data['data'][0]['addresses'][0]['city']}\n"
            except:
                pass
            try:
                to_send += f"Score: {data['data'][0]['score']}\n"
            except:
                pass
            try:
                to_send += f"Badges: {', '.join(data['data'][0]['badges'])}\n"
            except:
                pass
            try:
                to_send += f"About: {data['data'][0]['about']}\n"
            except:
                pass
            try:
                to_send += f"Job: {data['data'][0]['jobTitle']}\n"
            except:
                pass
            try:
                to_send += f"Number type: {data['data'][0]['phones'][0]['numberType']}\n"
            except:
                pass
            try:
                to_send += f"Spam score: {data['data'][0]['spamScore']}\n"
            except:
                pass
            try:
                to_send+= f"Image: {data['data'][0]['image']}\n"
            except:
                pass
            test = to_send
            to_send = ""
            for line in test.split("\n"):
                if line.split(":")[-1].strip():
                    to_send += line + "\n"
            return to_send        
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    application = ApplicationBuilder().token(api).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    tf = MessageHandler(None, truecaller)
    application.add_handler(tf)
    application.run_polling()
