import os
import sys
import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from database.users_chats_db import db
from utils import temp
from Script import script

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="urluploader",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=WORKERS,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = f"https://t.me/{me.username}"
        
        logger.info(f"{me.first_name} Started ⚡")
        logger.info(f"Username: @{me.username}")
        
        # Send startup message to log channel
        try:
            await self.send_message(
                chat_id=LOG_CHANNEL,
                text=f"<b>🤖 Bot Started Successfully!</b>\n\n"
                     f"<b>Bot Name:</b> {me.first_name}\n"
                     f"<b>Username:</b> @{me.username}\n"
                     f"<b>Bot ID:</b> <code>{me.id}</code>"
            )
        except Exception as e:
            logger.error(f"Error sending startup message: {e}")

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot stopped. Bye!")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
