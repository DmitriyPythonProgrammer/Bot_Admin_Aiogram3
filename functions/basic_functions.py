from aiogram import types
from aiogram.types import *
from messages import msg_errors
from datetime import datetime, timedelta
import main


async def is_reply(message: types.Message):
    if  message.reply_to_message == None:
        return False
    else:
        if message.reply_to_message.forum_topic_created != None:
            return False
        else:
            return True

async def is_bot(message: types.Message):
    if message.reply_to_message.from_user.id == main.bot.id:
        return False
    else:
        return True

async def check_command(message: types.Message, type: str):
    if await is_reply(message):
        idd = message.reply_to_message.from_user.id
        if idd == message.from_user.id:
            return msg_errors.not_for_myself
        user_status = await main.bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        if await is_bot(message):
            if isinstance(user_status, ChatMemberOwner) or isinstance(user_status, ChatMemberAdministrator):
                return msg_errors.not_for_admin_up
        else:
            return msg_errors.not_for_bots
    else:
        return msg_errors.not_from
    if message.text.count(' ')!=1:
        return msg_errors.incorrect_format_time
    try:
        time = message.text.split(' ', 1)[1]
    except:
        return msg_errors.incorrect_format_time
    format = time[-1]
    if not (time == '0' or format in ['m', 'h', 'd']):
        return msg_errors.incorrect_format_time
    time = time[0:-1]
    try:
        time = int(time)
    except:
        return msg_errors.incorrect_format_time
    return None

async def return_time_and_format(message: types.Message):
    time = message.text.split(' ', 1)[1]
    format = time[-1]
    format_out = None
    if time == '0':
        time_out = ''
        format_out = 'вечно'
    else:
        time = time[0:-1]
        time = int(time)
        time_out = time
        if format == 'm':
            format_out = 'минут'
            time = datetime.now() + timedelta(minutes=time)
        if format == 'h':
            format_out = 'часов'
            time = datetime.now() + timedelta(hours=time)
        if format == 'd':
            format_out = 'дней'
            time = datetime.now() + timedelta(days=time)
    return time, time_out, format_out


async def return_id(message: types.Message):
    if message.text.count(' ') != 1:
        return msg_errors.incorrect_format_id
    id = message.text.split(' ', 1)[1]


async def is_admin(message: types.Message, bot=False):
    if not(bot):
        member = await main.bot.get_chat_member(message.chat.id, message.from_user.id)
    else:
        member = await main.bot.get_chat_member(message.chat.id, main.bot.id)
    return (isinstance(member, ChatMemberAdministrator) or isinstance(member, ChatMemberOwner))


