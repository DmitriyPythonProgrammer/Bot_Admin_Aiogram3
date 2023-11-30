from aiogram import types


def kb_help():
    buttons = [

        [types.InlineKeyboardButton(text="Команды для модерации чата", callback_data="help_moder")],
        [types.InlineKeyboardButton(text="Развлекательные команды", callback_data="help_fun")],
        [types.InlineKeyboardButton(text="Информационные команды", callback_data="help_info")],
        [types.InlineKeyboardButton(text="Информация о боте", callback_data="help_botinfo")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
