from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Script import script

@Client.on_message(filters.command("info"))
async def user_info(client, message):
    user = message.from_user
    
    # Get user's profile photos
    try:
        photos = await client.get_chat_photos(user.id, limit=1)
        if photos:
            photo = photos[0].file_id
        else:
            photo = None
    except:
        photo = None
    
    # Get data centre
    dc_id = user.dc_id if user.dc_id else "Unknown"
    
    # Format info text
    info_text = script.INFO_TXT.format(
        user.first_name or "None",
        user.last_name or "None",
        user.id,
        dc_id,
        user.username or "None",
        user.id
    )
    
    buttons = [
        [InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="start")]
    ]
    
    if photo:
        await message.reply_photo(
            photo=photo,
            caption=info_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            info_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
