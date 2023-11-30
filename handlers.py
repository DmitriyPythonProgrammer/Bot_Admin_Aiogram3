from aiogram.types import *
from aiogram import Dispatcher, types
from messages import msg_texts, msg_errors
import database.__init__ as db
import main
from random import randint
from aiogram import F
from aiogram.filters import *
from functions import basic_functions as base_func
from keyboards import inline_keyboard as in_kb

dp = Dispatcher()


@dp.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def start_bot(event: ChatMemberUpdated):
    if event.new_chat_member.user.id == main.bot.id:
        await event.answer(msg_texts.start)


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):
    await event.answer(f"<b>Привет, {event.new_chat_member.user.first_name}!</b>")
    await db.request(f"DELETE FROM bans WHERE user_id = ?", False, event.new_chat_member.user.id)


@dp.callback_query(F.data.startswith("help_"))
async def callback_help(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "moder":
        await callback.message.answer(msg_texts.help_moder)
    elif action == "fun":
        await callback.message.answer(msg_texts.help_fun)
    elif action == "info":
        await callback.message.answer(msg_texts.help_info)
    elif action == "botinfo":
        await callback.message.answer(msg_texts.help_bot_info)


@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer(msg_texts.help, reply_markup=in_kb.kb_help())


@dp.message(Command("unmute"))
async def unban(message: types.Message):
    if not (await base_func.is_admin(message, True)):
        await message.reply(msg_errors.bot_not_have_permissions)
        return 0
    if not (await base_func.is_admin(message)):
        await message.reply(msg_errors.no_permission)
        return 0
    try:
        await main.bot.restrict_chat_member(chat_id=message.chat.id, user_id=id, permissions=ChatPermissions(can_send_messages=True))
        await message.reply(text=f"Пользователь с ID: {id} был размьючен")
    except:
        await message.reply(text=msg_errors.no_id)


@dp.message(Command('mute'))
async def mute(message: types.Message):
    if not (await base_func.is_admin(message, True)):
        await message.reply(msg_errors.bot_not_have_permissions)
        return 0
    if not (await base_func.is_admin(message)):
        await message.reply(msg_errors.no_permission)
        return 0
    error = await base_func.check_command(message, "mute")
    if error:
        await message.reply(id=message.chat.id, text=error)
        return 0
    idd = message.reply_to_message.from_user.id
    time, time_out, format_out = await base_func.return_time_and_format(message)
    await message.reply(f"Пользователь {message.reply_to_message.from_user.first_name} был замучен на {time_out} {format_out}")
    await main.bot.restrict_chat_member(chat_id=message.chat.id, user_id=idd, until_date=time, permissions=ChatPermissions(can_send_messages=False))
    await db.request(f"REPLACE INTO mutes (user_id, user_first_name, chat_id, until_date) VALUES (?, ?, ?, ?)", True, idd, message.reply_to_message.from_user.first_name, message.chat.id, time)


@dp.message(Command('banlist'))
async def banList(message: types.Message):
    await db.update_bans()
    data = await db.request(f"SELECT * FROM bans WHERE chat_id = ?", False, message.chat.id)
    text="Формат бан листа:\n(ИД пользователя, имя, ИД чата, время в которое будет разбанен)\nБан лист:\n"
    if len(data) == 0:
        await message.reply(text=(text + "пусто"))
        return 0
    for i in data:
        text+=f"{i}\n"
    await message.reply(text=text)


@dp.message(Command('mutelist'))
async def muteList(message: types.Message):
    await db.update_mutes()
    data = await db.request(f"SELECT * FROM mutes WHERE chat_id = ?", False, message.chat.id)
    text="Формат мут листа:\n(ИД пользователя, имя, ИД чата, время в которое будет размучен)\nМут лист:\n"
    if len(data) == 0:
        await message.reply(text=(text + "пусто"))
        return 0
    for i in data:
        text+=f"{i}\n"
    await message.reply(text=text)


@dp.message(Command("ban"))
async def ban(message: types.Message):
    if not (await base_func.is_admin(message, True)):
        await message.reply(msg_errors.bot_not_have_permissions)
        return 0
    if not (await base_func.is_admin(message)):
        await message.reply(msg_errors.no_permission)
        return 0
    error = await base_func.check_command(message, "ban")
    if error:
        await message.reply(text=error)
        return 0
    idd = message.reply_to_message.from_user.id
    time, time_out, format_out = await base_func.return_time_and_format(message)
    await message.reply(f"Пользователь {message.reply_to_message.from_user.first_name} был забанен на {time_out} {format_out}")
    await main.bot.ban_chat_member(chat_id=message.chat.id, user_id=idd, until_date=time)
    await db.request(f"REPLACE INTO bans (user_id, user_first_name, chat_id, until_date) VALUES (?, ?, ?, ?)", True, idd, message.reply_to_message.from_user.first_name, message.chat.id, time)


@dp.message(Command("unban"))
async def unban(message: types.Message):
    if not (await base_func.is_admin(message, True)):
        await message.reply(msg_errors.bot_not_have_permissions)
        return 0
    if not (await base_func.is_admin(message)):
        await message.reply(msg_errors.no_permission)
        return 0
    id = message.text.split(' ', 1)[1]
    try:
        await main.bot.unban_chat_member(user_id=id)
        await message.reply(text=f"Пользователь с ID: {id} был разбанен")
    except:
        await message.reply(text=msg_errors.no_id)


@dp.message(Command('id'))
async def idd(message: types.Message):
    if await base_func.is_reply(message):
        await message.reply(f"ID {message.reply_to_message.from_user.first_name}: {message.reply_to_message.from_user.id}")
    else:
        await message.reply(msg_errors.not_from)



@dp.message(Command('roll'))
async def any_message(message: types.Message):
    try:
        max=message.text.split(' ', 1)[1]
    except:
        await message.reply(msg_errors.not_int)
        return 0
    if len(max)>10:
        await message.reply(text=msg_errors.too_long)
        return 0
    try:
        max = int(max)
    except:
        await message.reply(text=msg_errors.not_int)
        return 0
    await message.reply(f"Вам выпало число <b>{randint(0,max)}</b>!")

