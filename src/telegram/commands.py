

def start(bot, chat_id: int):
    bot.send_message(chat_id, "Benvenuto in MacroBot")


def sort_commands(bot, chat_id: int, command: str):
    if command == "start":
        return start(bot, chat_id)
    
    return command