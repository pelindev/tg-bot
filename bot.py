import time
import requests
import json
import config
import botCommands

url = config.url
token = config.token
admin_chat = config.admin_chat
wife_chat = config.wife_chat

def getBotUpdates(update_id=""):
    """
    Checks for updates for the bot.\n
    Takes the last remembered `update_id` as parameters.\n
    If it finds a new update, it will return it. Otherwise it will return False.
    """

    time.sleep(2)
    response = requests.get(url+token+"/getUpdates")
    response = json.loads(response.text)
    errorStatus(response)
    if str(response['result'][-1]['update_id']) != str(update_id):
        print('there is a new update!')
        return response['result'][-1]
    return False

def errorStatus(response):
    """
    Сhecks the response for errors.\n
    Takes `response` as parameters.
    Killed bot if `response` status != 200
    """

    if response['ok'] == False:
        error = str(response['error_code']) + ' ' + response['description']
        exit(error)


def sendMessage(bot_update_info, text, parse_mode=""):
    """
    Sends a message to the chat.
    Takes bot update info and text for message as parameters.
    """

    chat_id = str(bot_update_info['message']['chat']['id'])
    user_name = bot_update_info['message']['from']['first_name']
    full_user_name = user_name +' '+ bot_update_info['message']['from']['last_name']
    if bot_update_info.get('message').get('text') == None:
        user_text = 'бот работает только с текстом!'
    else:
        user_text = bot_update_info['message']['text']

    message_body = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": 'True'
    }
    response = requests.post(url+token+"/sendMessage", data=message_body)
    errorStatus(json.loads(response.text))
    print('Message sent!')
    if not str(chat_id) == str(admin_chat):
        text_to_admin = """
___________
Отправитель: {}

Сообщение: {}
___________
    """.format(full_user_name, user_text)
        message_body = {
            "chat_id": admin_chat,
            "text": text_to_admin
        }
        response = requests.post(url+token+"/sendMessage", data=message_body)
        errorStatus(json.loads(response.text))
        print('Message to admin sent!')
    return response

def run():
    """
    run the PelinDev bot
    """

    # run the bot
    print('__PelinDevBot is started__')
    update_id = ""
    while True:
        bot_update_info = getBotUpdates(update_id)
        if not bot_update_info:
            continue
        print(bot_update_info)
        if str(bot_update_info['update_id']) != str(update_id):
            update_id = str(bot_update_info['update_id'])
            botCommands.commandCheck(bot_update_info)
        time.sleep(2)

if __name__ == "__main__":
    run()
