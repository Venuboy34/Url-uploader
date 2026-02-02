import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from config import ADMINS
from utils import temp, get_readable_time
from Script import script

START_TIME = time.time()

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def get_stats(client, message):
    total_users = await db.total_users_count()
    total_chats = await db.total_chat_count()
    
    # Count premium users
    premium_count = 0
    users = await db.get_all_users()
    async for user in users:
        if await db.is_premium_user(user['id']):
            premium_count += 1
    
    # Get database size (approximate)
    try:
        db_size = "N/A"
    except:
        db_size = "N/A"
    
    # Get uptime
    uptime = get_readable_time(time.time() - START_TIME)
    
    stats_text = script.STATS_TXT.format(
        total_users,
        premium_count,
        total_chats,
        db_size,
        uptime
    )
    
    buttons = [
        [
            InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")
        ],
        [
            InlineKeyboardButton("🗑️ Cʟᴏsᴇ", callback_data="close_data")
        ]
    ]
    
    await message.reply_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^refresh_stats$"))
async def refresh_stats_callback(client, callback_query):
    total_users = await db.total_users_count()
    total_chats = await db.total_chat_count()
    
    # Count premium users
    premium_count = 0
    users = await db.get_all_users()
    async for user in users:
        if await db.is_premium_user(user['id']):
            premium_count += 1
    
    # Get database size (approximate)
    try:
        db_size = "N/A"
    except:
        db_size = "N/A"
    
    # Get uptime
    uptime = get_readable_time(time.time() - START_TIME)
    
    stats_text = script.STATS_TXT.format(
        total_users,
        premium_count,
        total_chats,
        db_size,
        uptime
    )
    
    buttons = [
        [
            InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")
        ],
        [
            InlineKeyboardButton("🗑️ Cʟᴏsᴇ", callback_data="close_data")
        ]
    ]
    
    await callback_query.message.edit_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("✅ Stats refreshed!")

@Client.on_callback_query(filters.regex("^close_data$"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()
