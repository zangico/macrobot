

async def start(bot, chat_id: int):
    await bot.send_message(chat_id, "Welcome to MacroBot")


async def sort_commands(bot, chat_id: int, command: str):
    if command == "start":
        return await start(bot, chat_id)
    
    return command