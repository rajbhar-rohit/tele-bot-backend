# Instagram Downloader Telegram Bot 🤖

A **completely rewritten** Telegram bot that downloads Instagram posts and reels from public profiles. Now supports **ALL** Instagram username formats including complex ones with underscores and periods.

## ✨ Key Features

- 📥 **Universal Username Support** - Handles ANY valid Instagram username format
- 🔧 **Robust Error Handling** - Comprehensive validation and error messages  
- 🤖 **Smart Normalization** - Automatically cleans and validates usernames
- 📱 **Direct File Delivery** - Images and videos sent straight to your chat
- ⚡ **Real-time Updates** - Progress tracking during downloads
- 🛡️ **Bulletproof Validation** - Prevents errors before they happen

## 🎯 Supported Username Formats

The bot now handles **ALL** these formats perfectly:

### ✅ Simple Usernames
- `cristiano`
- `elonmusk` 
- `user123`

### ✅ Complex Underscores (Main Focus)
- `_s_o_n_a_l_i__1ok` ⭐ **Your specific case!**
- `__user__name__`
- `_cristiano_ronaldo_`
- `user____name` (gets optimized to `user___name`)
- `a_b_c_d_e_f_g`

### ✅ Periods & Mixed Formats
- `nat.geo`
- `tech.insider`
- `user_name.test`
- `_user.name_`
- `a.b.c.d`

### ✅ Auto-Normalization
- `@username` → `username`
- `@_s_o_n_a_l_i__1ok` → `_s_o_n_a_l_i__1ok`
- URLs and extra characters are automatically cleaned

## Quick Start 🚀

### 1. Create Your Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token you receive

### 2. Run the Bot
**Windows:**
```bash
# Double-click RUN_TELEGRAM_BOT.bat
# OR run manually:
python setup_telegram_bot.py
```

**Linux/Mac:**
```bash
# Install requirements
pip install -r requirements.txt

# Set your bot token
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Run the bot
python telegram_bot.py
```

### 3. Use Your Bot
1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send an Instagram username like `cristiano` or `@natgeo`
4. Wait for the bot to download and send the files!

## 🤖 Bot Commands

### Download Commands
- `/download username` - Download posts (default: 25 posts)
- `/all username` - Download ALL posts from profile ⚠️
- `/limit username number` - Download specific number of posts (1-500)

### Utility Commands
- `/start` - Welcome message and quick start guide
- `/help` - Comprehensive help with all username examples
- `/check username` - Validate username format before downloading
- `/info username` - Get profile information without downloading

### Direct Usage
Just send any username directly (downloads 25 posts):
- `_s_o_n_a_l_i__1ok`
- `cristiano`
- `nat.geo`

## 💡 Usage Examples

### Complex Usernames (Now Fully Supported!)
```
_s_o_n_a_l_i__1ok
__real__madrid__
user___name___test
_cristiano_ronaldo_
tech.news.daily
```

### Download Commands
```
/download _s_o_n_a_l_i__1ok     # Default: 25 posts
/all cristiano                  # ALL posts (can be hundreds!)
/limit nat.geo 50              # Exactly 50 posts
/limit _s_o_n_a_l_i__1ok 10    # Exactly 10 posts
```

### Utility Commands
```
/check __user__name__          # Validate username
/info nat.geo                  # Profile information
/download user_123.test        # Standard download
```

### Auto-Normalization
```
@_s_o_n_a_l_i__1ok    → _s_o_n_a_l_i__1ok
@cristiano            → cristiano
user@name             → username (removes @)
```

## 📊 Download Options

### 🎯 Three Ways to Download

**1. Default Download (25 posts)**
```
/download username
username                    # Direct message
```

**2. Limited Download (1-500 posts)**
```
/limit username 10          # Download exactly 10 posts
/limit username 50          # Download exactly 50 posts
/limit username 100         # Download exactly 100 posts
```

**3. Complete Download (ALL posts)**
```
/all username               # Downloads every single post
```

### ⚠️ Important Notes

**Default Download:**
- ✅ Fast and reliable
- ✅ Good for testing new profiles
- ✅ 25 posts is usually enough for most users

**Limited Download:**
- ✅ Perfect for specific needs
- ✅ You control exactly how many posts
- ✅ Range: 1-500 posts
- ⚡ Recommended for large profiles

**ALL Download:**
- ⚠️ Can take a VERY long time for large profiles
- ⚠️ Some profiles have 1000+ posts
- ⚠️ Use with caution on popular accounts
- ✅ Perfect for smaller profiles (<100 posts)
- 🔍 Bot warns you about large profiles first

## Limitations ⚠️

- Only public Instagram profiles are supported
- Files larger than 50MB cannot be sent via Telegram (Telegram's limit)
- Bot can process files up to 1GB internally
- Limited to 20 posts per request (to prevent timeouts)
- Rate limited to prevent spam

## Troubleshooting 🔧

### Bot Token Issues
```bash
# Make sure your token is set correctly
echo $TELEGRAM_BOT_TOKEN  # Linux/Mac
echo %TELEGRAM_BOT_TOKEN%  # Windows
```

### Installation Issues
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Profile Not Found
- Make sure the username is correct
- Check if the profile is public
- Try without the @ symbol

## Development 🛠️

The bot is built with:
- `python-telegram-bot` - Telegram Bot API wrapper
- `instaloader` - Instagram content downloading
- `asyncio` - Asynchronous operations

### File Structure
```
telegram_bot.py          # Main bot code
setup_telegram_bot.py    # Setup and configuration script
RUN_TELEGRAM_BOT.bat    # Windows batch file
requirements.txt         # Python dependencies
```

### Key Features in Code
- Async/await for non-blocking operations
- Temporary file handling with cleanup
- Progress updates during downloads
- Error handling for various Instagram exceptions
- File size validation for Telegram limits

## Security Notes 🔒

- Keep your bot token private
- Don't commit tokens to version control
- Use environment variables for configuration
- The bot only downloads public content

## Support 💬

If you encounter issues:
1. Check the console output for error messages
2. Verify your bot token is correct
3. Ensure the Instagram profile is public
4. Try with a different username

---

**Note:** This bot respects Instagram's terms of service and only downloads publicly available content.