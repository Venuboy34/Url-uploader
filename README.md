# Telegram URL Uploader Bot 🤖

A powerful Telegram bot for uploading files from URLs with premium features, user management, and advanced settings.

## Features ✨

- 📥 **URL Upload**: Download and upload files from direct URLs, social media, YouTube, torrents
- 💎 **Premium System**: Free (2GB) and Premium (4GB) upload limits with Telegram Stars payment
- ⚡ **High Speed**: Up to 50 MB/s download/upload speed
- 🔄 **File Management**: Rename files, custom thumbnails, screenshots
- ⚙️ **User Settings**: Timezone, spoiler effect, upload as document, bot updates
- 👥 **Admin Tools**: Broadcast, ban system, stats, user management
- 🚀 **Force Subscribe**: Support for 2 channels
- 📊 **MongoDB**: User and chat database management
- 🎯 **Worker Support**: Up to 500 concurrent workers

## Setup Instructions 🛠️

### Prerequisites

- Python 3.10+
- MongoDB Database
- Telegram Bot Token
- Telegram API ID and API Hash

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd telegram_url_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file or set these environment variables:

   ```env
   # Bot Configuration
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token

   # Database
   DATABASE_URI=your_mongodb_uri
   DATABASE_NAME=UrlUploaderBot

   # Channels & Groups
   LOG_CHANNEL=-100xxxxxxxxxx
   SUPPORT_CHAT=https://t.me/your_support_chat
   FORCE_SUB_CHANNEL=-100xxxxxxxxxx
   FORCE_SUB_CHANNEL2=-100xxxxxxxxxx

   # Admin
   ADMINS=123456789 987654321
   OWNER_ID=123456789

   # Premium Logs
   PREMIUM_LOGS=-100xxxxxxxxxx

   # Bot Settings
   WORKERS=500
   MAX_CONCURRENT=500

   # File Size Limits (in GB)
   FREE_USER_LIMIT=2
   PREMIUM_USER_LIMIT=4

   # Speed (MB/s)
   MAX_SPEED=50

   # Subscription Image
   SUBSCRIPTION=https://graph.org/file/86da2027469565b5873d6.jpg
   ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Bot Commands 📋

### User Commands
- `/start` - Start the bot
- `/help` - Get help information
- `/info` - Get your user information
- `/myplan` - Check your premium plan
- `/plan` - View premium plans
- `/settings` - Configure bot settings

### Admin Commands
- `/stats` - View bot statistics
- `/broadcast` - Broadcast message to users
- `/grp_broadcast` - Broadcast message to groups
- `/add_premium <user_id> <time>` - Add premium access (e.g., `/add_premium 123456 1 month`)
- `/remove_premium <user_id>` - Remove premium access
- `/get_premium <user_id>` - Get premium user details
- `/premium_users` - List all premium users
- `/banned` - List banned users
- `/clear_junk` - Remove inactive users
- `/junk_group` - Remove inactive groups

## Premium Features 💎

### Payment Options (Telegram Stars)
- 50⭐ - 7 Days
- 100⭐ - 1 Month
- 200⭐ - 2 Months
- 500⭐ - 6 Months
- 1000⭐ - 1 Year

### Premium Benefits
- 4GB upload limit (vs 2GB free)
- 50 MB/s speed
- Priority support
- All features unlocked

## Settings ⚙️

Users can customize:
- 🕒 **Timezone**: Set local timezone
- 🖼️ **Thumbnail**: Custom thumbnail for uploads
- 💥 **Spoiler Effect**: Enable/disable spoiler
- ✏️ **Rename Option**: Toggle file rename
- 📄 **Upload as Document**: Toggle document mode
- 📸 **Screenshots**: Toggle video screenshots
- 🤖 **Bot Updates**: Toggle update notifications

## Project Structure 📁

```
telegram_url_bot/
├── bot.py                  # Main bot file
├── config.py              # Configuration
├── Script.py              # Bot messages and scripts
├── utils.py               # Utility functions
├── info.py                # Backward compatibility
├── requirements.txt       # Dependencies
├── database/
│   └── users_chats_db.py # Database management
└── plugins/
    ├── start.py          # Start command
    ├── info.py           # User info command
    ├── settings.py       # Settings management
    ├── premium.py        # Premium features
    ├── broadcast.py      # Broadcasting
    ├── ban_system.py     # Ban management
    └── admin.py          # Admin commands
```

## Developer Info 👨‍💻

- **Developer**: Zerodev (@Venuboyy)
- **Library**: Pyrogram
- **Language**: Python 3
- **Database**: MongoDB
- **Version**: v1.0 [Stable]

## Features To Implement 🚧

The following features are mentioned in requirements but need additional implementation:

1. **URL Downloading**:
   - Direct URL download
   - Social media downloaders (YouTube, Instagram, etc.)
   - Torrent/magnet link support
   - Quality selection for videos

2. **File Processing**:
   - File rename interface
   - Custom thumbnail application
   - Video screenshot generation
   - Format conversion

3. **Progress Tracking**:
   - Real-time download progress
   - Upload progress with speed
   - ETA calculation

These will require additional plugins and external libraries like yt-dlp, aria2, etc.

## Notes 📝

- Make sure MongoDB is properly configured and accessible
- Set up proper admin IDs in environment variables
- Configure force subscribe channels if needed
- Premium logs channel should be set for payment tracking
- Welcome sticker ID needs to be from your bot's accessible stickers

## Support 💬

For issues or questions, contact:
- Developer: @Venuboyy
- Support Chat: [Your Support Chat Link]

## License 📄

This project is provided as-is for educational purposes.

---

**Built with ❤️ by Zerodev**
