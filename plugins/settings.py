from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.users_chats_db import db
from Script import script

@Client.on_callback_query(filters.regex("^settings$"))
async def settings_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    settings = await db.get_user_settings(user_id)
    
    buttons = [
        [
            InlineKeyboardButton("🕒 Sᴇᴛ Tɪᴍᴇᴢᴏɴᴇ", callback_data="set_timezone")
        ],
        [
            InlineKeyboardButton("🖼️ Sᴇᴇ Tʜᴜᴍʙɴᴀɪʟ", callback_data="view_thumbnail"),
            InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ Tʜᴜᴍʙɴᴀɪʟ", callback_data="delete_thumbnail")
        ],
        [
            InlineKeyboardButton(
                f"💥 Sᴘᴏɪʟᴇʀ: {'ON ✅' if settings['spoiler'] else 'OFF ❌'}",
                callback_data="toggle_spoiler"
            )
        ],
        [
            InlineKeyboardButton(
                f"✏️ Rᴇɴᴀᴍᴇ Oᴘᴛɪᴏɴ: {'ON ✅' if settings['show_rename'] else 'OFF ❌'}",
                callback_data="toggle_rename"
            )
        ],
        [
            InlineKeyboardButton(
                f"📄 Uᴘʟᴏᴀᴅ ᴀs Dᴏᴄ: {'ON ✅' if settings['upload_as_doc'] else 'OFF ❌'}",
                callback_data="toggle_upload_doc"
            )
        ],
        [
            InlineKeyboardButton(
                f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs: {'ON ✅' if settings['screenshots'] else 'OFF ❌'}",
                callback_data="toggle_screenshots"
            )
        ],
        [
            InlineKeyboardButton(
                f"🤖 Bᴏᴛ Uᴘᴅᴀᴛᴇs: {'ON ✅' if settings['bot_updates'] else 'OFF ❌'}",
                callback_data="toggle_bot_updates"
            )
        ],
        [
            InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="start")
        ]
    ]
    
    await callback_query.message.edit_text(
        script.SETTINGS_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^toggle_spoiler$"))
async def toggle_spoiler(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    new_status = await db.toggle_spoiler(user_id)
    await callback_query.answer(f"Spoiler effect is now {'ON ✅' if new_status else 'OFF ❌'}", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^toggle_rename$"))
async def toggle_rename(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    new_status = await db.toggle_rename(user_id)
    await callback_query.answer(f"Rename option is now {'ON ✅' if new_status else 'OFF ❌'}", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^toggle_upload_doc$"))
async def toggle_upload_doc(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    new_status = await db.toggle_upload_as_doc(user_id)
    await callback_query.answer(f"Upload as document is now {'ON ✅' if new_status else 'OFF ❌'}", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^toggle_screenshots$"))
async def toggle_screenshots(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    new_status = await db.toggle_screenshots(user_id)
    await callback_query.answer(f"Screenshots are now {'ON ✅' if new_status else 'OFF ❌'}", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^toggle_bot_updates$"))
async def toggle_bot_updates(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    new_status = await db.toggle_bot_updates(user_id)
    await callback_query.answer(f"Bot updates are now {'ON ✅' if new_status else 'OFF ❌'}", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^view_thumbnail$"))
async def view_thumbnail(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    thumbnail = await db.get_thumbnail(user_id)
    
    if thumbnail:
        await callback_query.message.reply_photo(
            photo=thumbnail,
            caption="📸 <b>Your current thumbnail</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ", callback_data="delete_thumbnail")],
                [InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="settings")]
            ])
        )
        await callback_query.answer()
    else:
        await callback_query.answer("❌ No thumbnail set!", show_alert=True)

@Client.on_callback_query(filters.regex("^delete_thumbnail$"))
async def delete_thumbnail(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await db.delete_thumbnail(user_id)
    await callback_query.answer("✅ Thumbnail deleted successfully!", show_alert=True)
    await settings_callback(client, callback_query)

@Client.on_callback_query(filters.regex("^set_timezone$"))
async def set_timezone(client, callback_query: CallbackQuery):
    await callback_query.answer(
        "⏰ To set your timezone, send it in format:\n/settimezone Asia/Kolkata",
        show_alert=True
    )

@Client.on_message(filters.command("settimezone") & filters.private)
async def set_timezone_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a timezone!\n\nExample: /settimezone Asia/Kolkata")
        return
    
    timezone = message.command[1]
    user_id = message.from_user.id
    
    try:
        import pytz
        pytz.timezone(timezone)
        await db.set_timezone(user_id, timezone)
        await message.reply(f"✅ Timezone set to: {timezone}")
    except:
        await message.reply("❌ Invalid timezone! Please use a valid timezone like Asia/Kolkata")

# Thumbnail handler
@Client.on_message(filters.private & filters.photo)
async def save_thumbnail(client, message):
    user_id = message.from_user.id
    
    # Check if user wants to set this as thumbnail
    if message.caption and "thumbnail" in message.caption.lower():
        file_id = message.photo.file_id
        await db.set_thumbnail(user_id, file_id)
        await message.reply("✅ Thumbnail saved successfully!")
