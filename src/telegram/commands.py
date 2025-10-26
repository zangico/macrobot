

async def start(bot, chat_id: int):
    await bot.send_message(chat_id, "Welcome to MacroBot")

async def get_chat_id(bot, chat_id:int):
    await bot.send_message(chat_id, f"Your chat id is: {chat_id}")


async def sort_commands(bot, chat_id: int, command: str):
    if command == "start":
        return await start(bot, chat_id)
    elif command == "chat_id":
        return await get_chat_id(bot, chat_id)
    
    return command