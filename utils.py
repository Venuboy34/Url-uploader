import time
import asyncio
import math
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message
from config import *

class temp:
    ME = None
    B_NAME = None
    U_NAME = None
    B_LINK = None
    BANNED_USERS = []
    BANNED_CHATS = []
    B_USERS_CANCEL = False
    B_GROUPS_CANCEL = False

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {Dic_powerN[n]}B"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    """Progress callback for upload/download"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))])
        )

        tmp = progress + """
📁 <b>Total Size :</b> {1}
📥 <b>{3} :</b> {2}
📊 <b>Progress :</b> {0}%
⚡ <b>Speed :</b> {4}/s
⏳ <b>Remaining :</b> {5}
""".format(
            round(percentage, 2),
            humanbytes(total),
            humanbytes(current),
            "Downloaded" if ud_type == "⬇️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴" else "Uploaded",
            humanbytes(speed),
            time_formatter(estimated_total_time - elapsed_time)
        )
        try:
            await message.edit_text(
                text=f"{ud_type}...\n\n{tmp}",
                parse_mode=enums.ParseMode.HTML
            )
        except:
            pass

def TimeFormatter(milliseconds: int) -> str:
    """Format time from milliseconds"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

def time_formatter(milliseconds: int) -> str:
    """Format remaining time"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d ") if days else "") + \
        ((str(hours) + "h ") if hours else "") + \
        ((str(minutes) + "m ") if minutes else "") + \
        ((str(seconds) + "s") if seconds else "")
    return tmp

async def get_seconds(time_string):
    """Convert time string to seconds"""
    parts = time_string.split()
    if len(parts) != 2:
        return 0
    
    value = int(parts[0])
    unit = parts[1].lower()
    
    if unit in ["second", "seconds", "sec", "s"]:
        return value
    elif unit in ["minute", "minutes", "min", "m"]:
        return value * 60
    elif unit in ["hour", "hours", "h"]:
        return value * 3600
    elif unit in ["day", "days", "d"]:
        return value * 86400
    elif unit in ["week", "weeks", "w"]:
        return value * 604800
    elif unit in ["month", "months", "mon"]:
        return value * 2592000
    elif unit in ["year", "years", "y"]:
        return value * 31536000
    else:
        return 0

async def users_broadcast(user_id, message: Message, is_pin):
    """Broadcast message to users"""
    try:
        if is_pin:
            await message.copy(chat_id=user_id)
            try:
                await bot.pin_chat_message(user_id, message.id)
            except:
                pass
        else:
            await message.copy(chat_id=user_id)
        return 200, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await users_broadcast(user_id, message, is_pin)
    except Exception as e:
        if "blocked" in str(e).lower():
            await db.delete_user(user_id)
            return 400, "Blocked"
        elif "deleted" in str(e).lower():
            await db.delete_user(user_id)
            return 400, "Deleted"
        else:
            return 400, "Error"

async def groups_broadcast(chat_id, message: Message, is_pin):
    """Broadcast message to groups"""
    try:
        if is_pin:
            await message.copy(chat_id=chat_id)
            try:
                await bot.pin_chat_message(chat_id, message.id)
            except:
                pass
        else:
            await message.copy(chat_id=chat_id)
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await groups_broadcast(chat_id, message, is_pin)
    except Exception:
        await db.delete_chat(chat_id)
        return "Error"

async def clear_junk(user_id, message: Message):
    """Check if user is valid"""
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except Exception as e:
        if "blocked" in str(e).lower():
            await db.delete_user(user_id)
            return False, "Blocked"
        elif "deleted" in str(e).lower():
            await db.delete_user(user_id)
            return False, "Deleted"
        else:
            return False, "Error"

async def junk_group(chat_id, message: Message):
    """Check if group is valid"""
    try:
        await message.copy(chat_id=chat_id)
        return True, "Success", ""
    except Exception as e:
        await db.delete_chat(chat_id)
        return False, "deleted", str(e)
