import bot
import newsParser

def commandCheck(update):
    """
    Сompares the command entered by the user with the commands of the bot.\n 
    Runs the user's command if it is valid.
    """
    commands = {
        "че там": newsParser.getNews(),
        "новости": newsParser.getNews(),
        "привет": 'Привет, '+update['message']['from']['first_name'],
        "default": 'Список доступных комманд:\n'+ 'че там, новости, привет'
    }
    
    if update.get('message').get('text') == None:
        bot.sendMessage(update, 'бот работает только с текстом!')
        return
    request_command = update['message']['text']
    for command in commands:
        if str(request_command).lower() == str(command):
            if command.lower() == 'че там' or command.lower() == 'новости':
                bot.sendMessage(update, commands[command], 'HTML')
                break
            bot.sendMessage(update, commands[command])
            break
    else:
        bot.sendMessage(update, commands['default'])