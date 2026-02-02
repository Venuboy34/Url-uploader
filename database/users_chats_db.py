import pymongo
import datetime
from config import DATABASE_URI, DATABASE_NAME
from utils import temp

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

class Database:
    
    def __init__(self):
        self.col = mydb['users']
        self.grp = mydb['groups']

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            thumbnail=None,
            timezone="Asia/Kolkata",
            spoiler=False,
            show_rename=True,
            upload_as_doc=False,
            screenshots=True,
            bot_updates=True
        )

    def new_group(self, id, title):
        return dict(
            id=id,
            title=title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            )
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
    
    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    
    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id': int(chat)})
        return False if not chat else chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status = dict(
            is_disabled=False,
            reason=""
        )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
    
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status = dict(
            is_disabled=True,
            reason=reason
        )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    
    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    
    async def get_all_chats(self):
        return self.grp.find({})

    async def delete_chat(self, chat):
        await self.grp.delete_many({'id': int(chat)})
    
    # User Settings
    async def set_thumbnail(self, user_id, file_id):
        await self.col.update_one({'id': user_id}, {'$set': {'thumbnail': file_id}})
    
    async def get_thumbnail(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('thumbnail') if user else None
    
    async def delete_thumbnail(self, user_id):
        await self.col.update_one({'id': user_id}, {'$set': {'thumbnail': None}})
    
    async def set_timezone(self, user_id, timezone):
        await self.col.update_one({'id': user_id}, {'$set': {'timezone': timezone}})
    
    async def get_timezone(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('timezone', 'Asia/Kolkata') if user else 'Asia/Kolkata'
    
    async def toggle_spoiler(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        current = user.get('spoiler', False) if user else False
        await self.col.update_one({'id': user_id}, {'$set': {'spoiler': not current}})
        return not current
    
    async def toggle_rename(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        current = user.get('show_rename', True) if user else True
        await self.col.update_one({'id': user_id}, {'$set': {'show_rename': not current}})
        return not current
    
    async def toggle_upload_as_doc(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        current = user.get('upload_as_doc', False) if user else False
        await self.col.update_one({'id': user_id}, {'$set': {'upload_as_doc': not current}})
        return not current
    
    async def toggle_screenshots(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        current = user.get('screenshots', True) if user else True
        await self.col.update_one({'id': user_id}, {'$set': {'screenshots': not current}})
        return not current
    
    async def toggle_bot_updates(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        current = user.get('bot_updates', True) if user else True
        await self.col.update_one({'id': user_id}, {'$set': {'bot_updates': not current}})
        return not current
    
    async def get_user_settings(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if not user:
            return {
                'timezone': 'Asia/Kolkata',
                'spoiler': False,
                'show_rename': True,
                'upload_as_doc': False,
                'screenshots': True,
                'bot_updates': True
            }
        return {
            'timezone': user.get('timezone', 'Asia/Kolkata'),
            'spoiler': user.get('spoiler', False),
            'show_rename': user.get('show_rename', True),
            'upload_as_doc': user.get('upload_as_doc', False),
            'screenshots': user.get('screenshots', True),
            'bot_updates': user.get('bot_updates', True)
        }
    
    # Premium Features
    async def update_user(self, user_data):
        await self.col.update_one(
            {'id': user_data['id']},
            {'$set': user_data},
            upsert=True
        )
    
    async def get_user(self, user_id):
        return await self.col.find_one({'id': int(user_id)})
    
    async def remove_premium_access(self, user_id):
        await self.col.update_one(
            {'id': user_id},
            {'$unset': {'expiry_time': ""}}
        )
        return True
    
    async def is_premium_user(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get('expiry_time'):
            if user['expiry_time'] > datetime.datetime.now():
                return True
            else:
                await self.remove_premium_access(user_id)
                return False
        return False

db = Database()
