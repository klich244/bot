# Author: Andrklch
# Description: Цей бот зроблений для модерації різних чатів.
# Commands:
# /unban, /ban, /unmute, /mute

import re
import asyncio
import config
import logging

from datetime import datetime, timedelta
from contextlib import suppress
from typing import Any
from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message, ChatPermissions
from aiogram.filters import CommandObject, Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

def parse_time(time_string: str | None) -> datetime | None:
  if not time_string:
    return None

  match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
  current_datetime = datetime.utcnow()
  if match_:
    value = int(match_.group(1))
    unit = match_.group(2)

    match unit:
      case "s": time_delta = timedelta(seconds=value)
      case "m": time_delta = timedelta(minutes=value)
      case "h": time_delta = timedelta(hours=value)
      case "d": time_delta = timedelta(days=value)
      case "w": time_delta = timedelta(weeks=value)
      case _: return None

  else:
    return None

  new_datetime = current_datetime + time_delta
  return new_datetime

router = Router()
router.message.filter(F.chat.type == 'supergroup', F.from_user.id == config.ADMINID) # Замість config.ADMINID пишеш свій айді

@router.message(Command('mute')) # /mute <time>
async def mute(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
  reply = message.reply_to_message
  if not reply:
    return await massege.answer('🤕 Користувача не знайдено!')

  until_date = parse_time(command.args)
  mention = reply.from_user.mention_html(reply.from_user.first_name)

  with suppress(TelegramBadRequest):
   await bot.restrict_chat_member(
      chat_id=message.chat.id,
      user_id=reply.from_user.id,
      until_date=until_date,
     permissions=ChatPermissions(can_send_messages=False)
   )
   await message.answer(f'👮‍♂️ {mention} зам\'ючено до {until_date}')

@router.message(Command('unmute')) # /unmute
async def mute(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
  reply = message.reply_to_message
  if not reply:
    return await massege.answer('🤕 Користувача не знайдено!')

  mention = reply.from_user.mention_html(reply.from_user.first_name)

  with suppress(TelegramBadRequest):
   await bot.restrict_chat_member(
      chat_id=message.chat.id,
      user_id=reply.from_user.id,
     permissions=ChatPermissions(can_send_messages=True)
   )
   await message.answer(f'👮‍♂️ {mention} розм\'ючено')
  
@router.message(Command('ban')) # /ban <time>
async def ban(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
  reply = message.reply_to_message
  if not reply:
    return await massege.answear('🤕 Користувача не знайдено!')

  until_date = parse_time(command.args)
  mention = reply.from_user.mention_html(reply.from_user.first_name)
  
  with suppress(TelegramBadRequest):
    await bot.ban_chat_member(
      chat_id=message.chat.id,
      user_id=reply.from_user.id,
      until_date=until_date
    )
    await message.answer(f'👮‍♂️ {mention} заблокований до {until_date}')

@router.message(Command('unban')) # /unban
async def ban(message: Message, bot: Bot, command: CommandObject | None=None) -> Any:
  reply = message.reply_to_message
  if not reply:
    return await massege.answear('🤕 Користувача не знайдено!')

  mention = reply.from_user.mention_html(reply.from_user.first_name)

  with suppress(TelegramBadRequest):
    await bot.unban_chat_member(
      chat_id=message.chat.id,
      user_id=reply.from_user.id,
    )
    await message.answer(f'👮‍♂️ {mention} розблокований')
                
async def main() -> None:
  bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
  dp = Dispatcher()

  dp.include_router(router)

  await bot.delete_webhook(True)
  await dp.start_polling(bot)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
