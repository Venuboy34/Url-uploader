import asyncio
import requests
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from database.users_chats_db import db
from Script import script
from config import *
from utils import temp

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Check force subscribe
    if FORCE_SUB_CHANNEL or FORCE_SUB_CHANNEL2:
        try:
            channels_to_check = []
            if FORCE_SUB_CHANNEL:
                channels_to_check.append(FORCE_SUB_CHANNEL)
            if FORCE_SUB_CHANNEL2:
                channels_to_check.append(FORCE_SUB_CHANNEL2)
            
            not_subscribed = []
            for channel in channels_to_check:
                try:
                    member = await client.get_chat_member(channel, user_id)
                    if member.status in ["left", "kicked"]:
                        not_subscribed.append(channel)
                except UserNotParticipant:
                    not_subscribed.append(channel)
            
            if not_subscribed:
                buttons = []
                for i, channel in enumerate(not_subscribed, 1):
                    try:
                        chat = await client.get_chat(channel)
                        invite_link = chat.invite_link or f"https://t.me/{chat.username}"
                        buttons.append([InlineKeyboardButton(f"Join Channel {i}", url=invite_link)])
                    except:
                        pass
                buttons.append([InlineKeyboardButton("🔄 Try Again", callback_data="check_subscribe")])
                
                # Send force subscribe message with image
                await message.reply_photo(
                    photo=WELCOME_IMAGE,
                    caption="<b>⚠️ You must join our channel(s) to use this bot!\n\nClick the button(s) below to join and then click 'Try Again'.</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        except Exception as e:
            print(f"Force subscribe error: {e}")
    
    # Send welcome sticker
    sticker_msg = await message.reply_sticker(WELCOME_STICKER)
    
    # Delete sticker after 2 seconds
    await asyncio.sleep(2)
    await sticker_msg.delete()
    
    # Add user to database
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user_name)
    
    # Get random welcome image
    try:
        response = requests.get(RANDOM_IMAGE_API)
        random_image = response.json().get('url', WELCOME_IMAGE)
    except:
        random_image = WELCOME_IMAGE
    
    # Send welcome message
    buttons = [
        [
            InlineKeyboardButton("🆘 Hᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Pʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ Sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{DEVELOPER.replace('@', '')}")
        ]
    ]
    
    await message.reply_photo(
        photo=random_image,
        caption=script.START_TXT.format(message.from_user.mention, "👋"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("start") & filters.group)
async def group_start(client, message):
    buttons = [
        [
            InlineKeyboardButton("🤖 Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ", url=f"https://t.me/{temp.U_NAME}?startgroup=true")
        ]
    ]
    
    await message.reply_text(
        script.GSTART_TXT.format(message.from_user.mention, "👋"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )
    
    # Add group to database
    if not await db.get_chat(message.chat.id):
        await db.add_chat(message.chat.id, message.chat.title)

@Client.on_callback_query(filters.regex("^check_subscribe"))
async def check_subscribe_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    channels_to_check = []
    if FORCE_SUB_CHANNEL:
        channels_to_check.append(FORCE_SUB_CHANNEL)
    if FORCE_SUB_CHANNEL2:
        channels_to_check.append(FORCE_SUB_CHANNEL2)
    
    not_subscribed = []
    for channel in channels_to_check:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                not_subscribed.append(channel)
        except UserNotParticipant:
            not_subscribed.append(channel)
    
    if not_subscribed:
        await callback_query.answer("❌ You haven't joined all channels yet!", show_alert=True)
        return
    
    await callback_query.message.delete()
    
    # Add user to database
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, callback_query.from_user.first_name)
    
    # Send welcome message
    try:
        response = requests.get(RANDOM_IMAGE_API)
        random_image = response.json().get('url', WELCOME_IMAGE)
    except:
        random_image = WELCOME_IMAGE
    
    buttons = [
        [
            InlineKeyboardButton("🆘 Hᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Pʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ Sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{DEVELOPER.replace('@', '')}")
        ]
    ]
    
    await callback_query.message.reply_photo(
        photo=random_image,
        caption=script.START_TXT.format(callback_query.from_user.mention, "👋"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query):
    buttons = [
        [InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")]
    ]
    await callback_query.message.edit_text(
        script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback_query):
    buttons = [
        [InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")]
    ]
    await callback_query.message.edit_text(
        script.ABOUT_TXT.format(temp.U_NAME, temp.B_NAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client, callback_query):
    buttons = [
        [
            InlineKeyboardButton("🆘 Hᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Pʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("⚙️ Sᴇᴛᴛɪɴɢs", callback_data="settings")
        ],
        [
            InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{DEVELOPER.replace('@', '')}")
        ]
    ]
    await callback_query.message.edit_text(
        script.START_TXT.format(callback_query.from_user.mention, "👋"),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )
