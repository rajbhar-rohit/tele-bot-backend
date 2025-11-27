#!/usr/bin/env python3
"""
Instagram Content Downloader Telegram Bot - Rewritten for Maximum Compatibility
Handles all Instagram username formats including complex ones with underscores and periods
"""

import os
import asyncio
import logging
import tempfile
import shutil
import re
from pathlib import Path
from typing import Optional, List, Tuple
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class RobustInstagramBot:
    """
    A robust Instagram downloader bot that handles all username formats
    """
    
    def __init__(self, token: str):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.max_posts_per_request = 25
        self.max_file_size_mb = 1024  # 1GB internal processing limit
        self.telegram_upload_limit_mb = 50  # Telegram's actual upload limit
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup all bot handlers"""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("download", self.cmd_download))
        self.app.add_handler(CommandHandler("all", self.cmd_download_all))
        self.app.add_handler(CommandHandler("limit", self.cmd_download_limit))
        self.app.add_handler(CommandHandler("check", self.cmd_check))
        self.app.add_handler(CommandHandler("info", self.cmd_info))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
    # ==================== USERNAME VALIDATION ====================
    
    def normalize_username(self, raw_input: str) -> str:
        """
        Normalize any username input to clean Instagram username
        Handles @username, username, spaces, etc.
        """
        if not raw_input:
            return ""
            
        # Remove common prefixes and clean
        username = raw_input.strip()
        username = username.replace('@', '')
        username = username.replace('instagram.com/', '')
        username = username.replace('www.instagram.com/', '')
        username = username.split('/')[-1]  # Handle URLs
        username = username.split('?')[0]   # Remove query params
        
        return username.strip()
    
    def is_valid_instagram_username(self, username: str) -> bool:
        """
        Comprehensive Instagram username validation
        Based on Instagram's actual rules (as of 2024)
        """
        if not username:
            return False
            
        # Length validation (Instagram allows 1-30 characters)
        if len(username) < 1 or len(username) > 30:
            return False
            
        # Character validation - only letters, numbers, periods, underscores
        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            return False
            
        # Period rules
        if username.startswith('.') or username.endswith('.'):
            return False
        if '..' in username:  # No consecutive periods
            return False
            
        # Must contain at least one alphanumeric character
        if not re.search(r'[a-zA-Z0-9]', username):
            return False
            
        return True
    
    def get_validation_errors(self, username: str) -> List[str]:
        """Get detailed validation errors for a username"""
        errors = []
        
        if not username:
            errors.append("Username is empty")
            return errors
            
        if len(username) > 30:
            errors.append(f"Too long ({len(username)} chars, max 30)")
        if len(username) < 1:
            errors.append("Too short (minimum 1 character)")
            
        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            invalid_chars = set(re.findall(r'[^a-zA-Z0-9._]', username))
            errors.append(f"Invalid characters: {', '.join(invalid_chars)}")
            
        if username.startswith('.'):
            errors.append("Cannot start with period (.)")
        if username.endswith('.'):
            errors.append("Cannot end with period (.)")
        if '..' in username:
            errors.append("Cannot have consecutive periods (..)")
            
        if not re.search(r'[a-zA-Z0-9]', username):
            errors.append("Must contain at least one letter or number")
            
        return errors
    
    def create_safe_directory_name(self, username: str) -> str:
        """
        Create a filesystem-safe directory name from username
        Preserves uniqueness while ensuring compatibility
        """
        # Replace periods with underscores for filesystem safety
        safe_name = username.replace('.', '_')
        
        # Compress excessive consecutive underscores but preserve uniqueness
        # Replace 4+ consecutive underscores with 3 underscores
        safe_name = re.sub(r'_{4,}', '___', safe_name)
        
        # Ensure it's not empty
        if not safe_name:
            safe_name = 'instagram_user'
            
        # Limit length for filesystem compatibility
        if len(safe_name) > 50:
            safe_name = safe_name[:50].rstrip('_')
            
        return safe_name
    
    # ==================== COMMAND HANDLERS ====================
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_msg = """🤖 <b>Instagram Content Downloader Bot</b>

I can download posts and reels from any public Instagram profile!

<b>🚀 Quick Start:</b>
Just send me any Instagram username:
• cristiano
• nat.geo
• @username (I'll remove the @)

<b>📋 Commands:</b>
• /download username - Download posts (default: 25 posts)
• /all username - Download ALL posts from profile
• /limit username 10 - Download specific number of posts
• /check username - Validate username format
• /info username - Get profile information
• /help - Show detailed help

<b>⚡ Features:</b>
✅ Supports ALL username formats
✅ Handles underscores, periods, numbers
✅ Downloads images and videos
✅ Flexible download limits
✅ Real-time progress updates
✅ Works with public profiles only

Try it now! Send me any Instagram username."""
        await update.message.reply_text(welcome_msg, parse_mode='HTML')
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_msg = """📖 <b>Detailed Help &amp; Examples</b>

<b>🎯 Supported Username Formats:</b>
• Simple: cristiano, elonmusk
• With underscores: user_name_123
• With periods: nat.geo, tech.insider
• Complex: __user__name__, a.b.c_d_e_f
• Numbers: user123, test_user_2024

<b>📱 Download Commands:</b>
1. <b>Default download:</b> /download username (25 posts)
   /download user_name_123

2. <b>Download ALL posts:</b> /all username
   /all cristiano

3. <b>Limited download:</b> /limit username number
   /limit nat.geo 50
   /limit user_name_123 10

4. <b>Direct message:</b> Just type the username (25 posts)
   user_name_123

<b>🔧 Utility Commands:</b>
• /check username - Validate username format
• /info username - Get profile details
• /help - Show this help

<b>📊 Download Limits:</b>
• Default: 25 posts
• /all command: ALL posts (can be hundreds!)
• /limit command: 1-500 posts
• Large downloads may take time

<b>⚠️ Important Notes:</b>
• Only public profiles work
• Private profiles will show an error
• Files over 50MB can't be sent via Telegram (Telegram's limit)
• ALL downloads can take very long for large profiles

<b>🔧 Troubleshooting:</b>
• If username fails, try /check username first
• Use /info to verify profile exists
• For large profiles, use /limit instead of /all
• Wait between downloads to avoid rate limits

<b>💡 Pro Tips:</b>
• Start with /info to see how many posts a profile has
• Use /limit for testing with new profiles
• /all command works best with smaller profiles (&lt;100 posts)
• Complex usernames with underscores work perfectly"""
        await update.message.reply_text(help_msg, parse_mode='HTML')
    
    async def cmd_download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /download command"""
        if not context.args:
            await update.message.reply_text(
                "❌ <b>Missing Username</b>\n\n"
                "Usage: /download username\n\n"
                "Examples:\n"
                "• /download cristiano\n"
                "• /download user_name_123\n"
                "• /download nat.geo",
                parse_mode='HTML'
            )
            return
            
        raw_username = ' '.join(context.args)
        await self.process_download_request(update, raw_username)
        
    async def cmd_download_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /all command - download ALL posts"""
        if not context.args:
            await update.message.reply_text(
                "❌ <b>Missing Username</b>\n\n"
                "Usage: /all username\n\n"
                "Examples:\n"
                "• /all cristiano\n"
                "• /all user_name_123\n"
                "• /all nat.geo\n\n"
                "⚠️ <b>Warning:</b> This downloads ALL posts from the profile!\n"
                "Large profiles may have hundreds of posts and take a long time.",
                parse_mode='HTML'
            )
            return
            
        raw_username = ' '.join(context.args)
        
        # Send warning for /all command
        warning_msg = await update.message.reply_text(
            f"⚠️ <b>ALL Posts Download</b>\n\n"
            f"👤 Username: {self.escape_html(raw_username)}\n"
            f"📥 Mode: Download ALL posts\n\n"
            f"🔍 Checking profile size first...",
            parse_mode='HTML'
        )
        
        # Quick profile check to warn about large profiles
        username = self.normalize_username(raw_username)
        if self.is_valid_instagram_username(username):
            try:
                loader = instaloader.Instaloader(quiet=True)
                profile = instaloader.Profile.from_username(loader.context, username)
                
                if profile.mediacount > 100:
                    await warning_msg.edit_text(
                        f"⚠️ <b>Large Profile Warning</b>\n\n"
                        f"👤 Username: {self.escape_html(username)}\n"
                        f"📊 Total posts: {self.format_number(profile.mediacount)}\n\n"
                        f"🚨 <b>This is a large profile!</b>\n"
                        f"Downloading ALL posts may take a very long time.\n\n"
                        f"💡 <b>Recommendations:</b>\n"
                        f"• Use /limit {self.escape_html(username)} 50 instead\n"
                        f"• Or continue with /all if you really want everything\n\n"
                        f"⏳ Starting download in 3 seconds...",
                        parse_mode='HTML'
                    )
                    await asyncio.sleep(3)
                else:
                    await warning_msg.edit_text(
                        f"✅ <b>Profile Size OK</b>\n\n"
                        f"👤 Username: {self.escape_html(username)}\n"
                        f"📊 Total posts: {self.format_number(profile.mediacount)}\n\n"
                        f"⬇️ Starting download of all posts...",
                        parse_mode='HTML'
                    )
                    await asyncio.sleep(1)
            except:
                # If profile check fails, just proceed
                pass
        
        await self.process_download_request(update, raw_username, download_all=True)
        
    async def cmd_download_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /limit command - download specific number of posts"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ <b>Missing Username or Number</b>\n\n"
                "Usage: /limit username number\n\n"
                "Examples:\n"
                "• /limit cristiano 10\n"
                "• /limit user_name_123 50\n"
                "• /limit nat.geo 5\n\n"
                "📊 <b>Limits:</b>\n"
                "• Minimum: 1 post\n"
                "• Maximum: 500 posts\n"
                "• Recommended: 10-50 posts for testing",
                parse_mode='HTML'
            )
            return
            
        try:
            # Get username and limit
            raw_username = context.args[0]
            limit = int(context.args[1])
            
            # Validate limit
            if limit < 1:
                await update.message.reply_text(
                    "❌ <b>Invalid Limit</b>\n\n"
                    "Minimum limit is 1 post.\n"
                    "Example: /limit username 5",
                    parse_mode='HTML'
                )
                return
            elif limit > 500:
                await update.message.reply_text(
                    "❌ <b>Limit Too High</b>\n\n"
                    "Maximum limit is 500 posts.\n"
                    "For downloading all posts, use: /all username",
                    parse_mode='HTML'
                )
                return
                
            await self.process_download_request(update, raw_username, post_limit=limit)
            
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Invalid Number</b>\n\n"
                "Please provide a valid number.\n\n"
                "Usage: /limit username number\n"
                "Example: /limit cristiano 10",
                parse_mode='HTML'
            )
    
    async def cmd_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command - validate username"""
        if not context.args:
            await update.message.reply_text(
                "❓ <b>Username Validator</b>\n\n"
                "Check if a username is valid before downloading.\n\n"
                "Usage: /check username\n\n"
                "Examples:\n"
                "• /check nat.geo\n"
                "• /check user__name__123",
                parse_mode='HTML'
            )
            return
            
        raw_username = ' '.join(context.args)
        username = self.normalize_username(raw_username)
        
        if self.is_valid_instagram_username(username):
            safe_name = self.create_safe_directory_name(username)
            await update.message.reply_text(
                f"✅ <b>Username Valid!</b>\n\n"
                f"👤 <b>Original:</b> {self.escape_html(raw_username)}\n"
                f"🧹 <b>Cleaned:</b> {self.escape_html(username)}\n"
                f"📁 <b>Directory:</b> {self.escape_html(safe_name)}\n"
                f"📏 <b>Length:</b> {len(username)} characters\n\n"
                f"Ready to download! Use:\n"
                f"• /download {self.escape_html(username)}\n"
                f"• Or just send: {self.escape_html(username)}",
                parse_mode='HTML'
            )
        else:
            errors = self.get_validation_errors(username)
            error_list = '\n'.join([f"• {error}" for error in errors])
            await update.message.reply_text(
                f"❌ <b>Username Invalid</b>\n\n"
                f"👤 <b>Input:</b> {self.escape_html(raw_username)}\n"
                f"🧹 <b>Cleaned:</b> {self.escape_html(username)}\n"
                f"📏 <b>Length:</b> {len(username)} characters\n\n"
                f"<b>Issues Found:</b>\n{error_list}\n\n"
                f"<b>Valid Format Rules:</b>\n"
                f"• 1-30 characters\n"
                f"• Letters, numbers, periods, underscores only\n"
                f"• Cannot start/end with periods\n"
                f"• No consecutive periods\n"
                f"• Must have at least one letter/number",
                parse_mode='HTML'
            )
    
    async def cmd_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command - get profile info without downloading"""
        if not context.args:
            await update.message.reply_text(
                "ℹ️ <b>Profile Information</b>\n\n"
                "Get profile details without downloading.\n\n"
                "Usage: /info username\n\n"
                "Examples:\n"
                "• /info cristiano\n"
                "• /info user_name_123",
                parse_mode='HTML'
            )
            return
            
        raw_username = ' '.join(context.args)
        await self.get_profile_info(update, raw_username)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle direct username messages"""
        raw_username = update.message.text.strip()
        
        # Skip if it looks like a command or random text
        if raw_username.startswith('/') or len(raw_username) > 50 or ' ' in raw_username:
            await update.message.reply_text(
                "🤔 That doesn't look like an Instagram username.\n\n"
                "Send a username like:\n"
                "• `cristiano`\n"
                "• `nat.geo`\n\n"
                "Or use `/help` for more information."
            )
            return
            
        await self.process_download_request(update, raw_username)
    
    # ==================== CORE FUNCTIONALITY ====================
    
    async def process_download_request(self, update: Update, raw_username: str, download_all: bool = False, post_limit: Optional[int] = None):
        """Process a download request with comprehensive error handling"""
        # Normalize and validate username
        username = self.normalize_username(raw_username)
        
        if not self.is_valid_instagram_username(username):
            errors = self.get_validation_errors(username)
            error_text = '\n'.join([f"• {error}" for error in errors])
            await update.message.reply_text(
                f"❌ <b>Invalid Username Format</b>\n\n"
                f"Input: {self.escape_html(raw_username)}\n"
                f"Cleaned: {self.escape_html(username)}\n\n"
                f"Issues:\n{error_text}\n\n"
                f"Use /check {self.escape_html(raw_username)} for detailed validation.",
                parse_mode='HTML'
            )
            return
        
        # Send initial status
        status_msg = await update.message.reply_text(
            f"🔍 <b>Checking Profile</b>\n\n"
            f"👤 Username: {self.escape_html(username)}\n"
            f"⏳ Connecting to Instagram...",
            parse_mode='HTML'
        )
        
        try:
            await self.download_instagram_content(update, status_msg, username, download_all, post_limit)
        except Exception as e:
            logger.error(f"Download failed for {username}: {e}")
            await status_msg.edit_text(
                f"💥 <b>Download Failed</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n"
                f"❌ Error: {self.escape_html(str(e)[:200])}...\n\n"
                f"Try:\n"
                f"• Check if profile is public\n"
                f"• Wait a few minutes and retry\n"
                f"• Use /info {self.escape_html(username)} to test connection",
                parse_mode='HTML'
            )
    
    async def get_profile_info(self, update: Update, raw_username: str):
        """Get profile information without downloading"""
        username = self.normalize_username(raw_username)
        
        if not self.is_valid_instagram_username(username):
            await update.message.reply_text(
                f"❌ Invalid username format: {self.escape_html(username)}\n\n"
                f"Use /check {self.escape_html(username)} for validation details.",
                parse_mode='HTML'
            )
            return
        
        status_msg = await update.message.reply_text(
            f"ℹ️ <b>Getting Profile Info</b>\n\n"
            f"👤 Username: {self.escape_html(username)}\n"
            f"⏳ Fetching data...",
            parse_mode='HTML'
        )
        
        try:
            loader = instaloader.Instaloader(quiet=True)
            profile = instaloader.Profile.from_username(loader.context, username)
            
            # Format follower counts
            followers = self.format_number(profile.followers)
            following = self.format_number(profile.followees)
            posts = self.format_number(profile.mediacount)
            
            bio_text = profile.biography[:100] + '...' if len(profile.biography) > 100 else profile.biography
            info_text = f"""ℹ️ <b>Profile Information</b>

👤 <b>Name:</b> {self.escape_html(profile.full_name or 'Not set')}
🔗 <b>Username:</b> @{self.escape_html(profile.username)}
📝 <b>Bio:</b> {self.escape_html(bio_text)}

📊 <b>Statistics:</b>
• Posts: {posts}
• Followers: {followers}
• Following: {following}

🔒 <b>Status:</b> {'Private' if profile.is_private else 'Public'}
✅ <b>Verified:</b> {'Yes' if profile.is_verified else 'No'}
🏢 <b>Business:</b> {'Yes' if profile.is_business_account else 'No'}

Ready to download? Send /download {self.escape_html(username)}"""
            
            await status_msg.edit_text(info_text, parse_mode='HTML')
            
        except instaloader.exceptions.ProfileNotExistsException:
            await status_msg.edit_text(
                f"❌ <b>Profile Not Found</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n\n"
                f"The profile doesn't exist or has been deleted.\n"
                f"Please check the spelling and try again.",
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Profile info failed for {username}: {e}")
            await status_msg.edit_text(
                f"❌ <b>Error Getting Profile Info</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n"
                f"❌ Error: {self.escape_html(str(e)[:100])}...\n\n"
                f"This might be a temporary issue. Try again later.",
                parse_mode='HTML'
            )
    
    async def download_instagram_content(self, update: Update, status_msg, username: str, download_all: bool = False, post_limit: Optional[int] = None):
        """Download Instagram content with robust error handling"""
        temp_dir = None
        
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix=f"instagram_{username}_")
            safe_dirname = self.create_safe_directory_name(username)
            
            # Setup instaloader with optimal settings
            loader = instaloader.Instaloader(
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                post_metadata_txt_pattern="",
                storyitem_metadata_txt_pattern="",
                compress_json=False,
                dirname_pattern=temp_dir + "/{profile}",
                quiet=True,
                request_timeout=30
            )
            
            # Get profile
            logger.info(f"Fetching profile: {username}")
            profile = instaloader.Profile.from_username(loader.context, username)
            
            # Initialize download parameters early to avoid scope issues
            if download_all:
                total_to_download = profile.mediacount
                max_posts = profile.mediacount
                download_type = "ALL"
            elif post_limit is not None:
                total_to_download = min(profile.mediacount, post_limit)
                max_posts = post_limit
                download_type = f"LIMITED ({post_limit})"
            else:
                total_to_download = min(profile.mediacount, self.max_posts_per_request)
                max_posts = self.max_posts_per_request
                download_type = f"DEFAULT ({self.max_posts_per_request})"
            
            # Update status with profile info
            await status_msg.edit_text(
                f"👤 <b>{self.escape_html(profile.full_name or profile.username)}</b>\n\n"
                f"🔗 @{self.escape_html(profile.username)}\n"
                f"📊 {self.format_number(profile.mediacount)} posts total\n"
                f"� Dtownload type: {download_type}\n"
                f"🎯 Target: {total_to_download} posts\n"
                f"🔒 Status: {'Private' if profile.is_private else 'Public'}\n\n"
                f"⬇️ Starting download...",
                parse_mode='HTML'
            )
            
            # Check if private
            if profile.is_private:
                await status_msg.edit_text(
                    f"🔒 <b>Private Profile</b>\n\n"
                    f"👤 @{self.escape_html(profile.username)}\n\n"
                    f"This profile is private and cannot be downloaded.\n"
                    f"Only public profiles are supported by this bot.",
                    parse_mode='HTML'
                )
                return
            

            
            # Download posts
            downloaded_count = 0
            
            logger.info(f"Starting {download_type} download of up to {total_to_download} posts for {username}")
            
            for i, post in enumerate(profile.get_posts()):
                if downloaded_count >= max_posts:
                    break
                
                try:
                    # Download post
                    loader.download_post(post, target=safe_dirname)
                    downloaded_count += 1
                    
                    # Update progress every 3 posts
                    if downloaded_count % 3 == 0 or downloaded_count == 1:
                        await status_msg.edit_text(
                            f"👤 <b>{self.escape_html(profile.full_name or profile.username)}</b>\n\n"
                            f"📊 {self.format_number(profile.mediacount)} posts total\n"
                            f"📥 Type: {download_type}\n"
                            f"⬇️ Downloaded: {downloaded_count}/{total_to_download}\n"
                            f"📁 Processing files...",
                            parse_mode='HTML'
                        )
                    
                    # Small delay to prevent rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.warning(f"Failed to download post {post.shortcode}: {e}")
                    continue
            
            # Send downloaded files
            await self.send_downloaded_files(update, status_msg, temp_dir, safe_dirname, username, downloaded_count)
            
        except instaloader.exceptions.ProfileNotExistsException:
            await status_msg.edit_text(
                f"❌ <b>Profile Not Found</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n\n"
                f"This profile doesn't exist or has been deleted.\n"
                f"Please check the spelling and try again.",
                parse_mode='HTML'
            )
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            await status_msg.edit_text(
                f"🔒 <b>Private Profile</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n\n"
                f"This profile is private and cannot be accessed.\n"
                f"Only public profiles are supported.",
                parse_mode='HTML'
            )
        except instaloader.exceptions.ConnectionException as e:
            await status_msg.edit_text(
                f"🌐 <b>Connection Error</b>\n\n"
                f"👤 Username: {self.escape_html(username)}\n\n"
                f"Instagram connection failed. This might be due to:\n"
                f"• Rate limiting\n"
                f"• Network issues\n"
                f"• Instagram server problems\n\n"
                f"Please try again in a few minutes.",
                parse_mode='HTML'
            )
        finally:
            # Cleanup
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    async def send_downloaded_files(self, update: Update, status_msg, temp_dir: str, 
                                  safe_dirname: str, original_username: str, downloaded_count: int):
        """Send downloaded files to user"""
        profile_dir = Path(temp_dir) / safe_dirname
        
        if not profile_dir.exists():
            await status_msg.edit_text(
                f"❌ <b>No Files Downloaded</b>\n\n"
                f"👤 Username: {self.escape_html(original_username)}\n\n"
                f"No files were successfully downloaded.\n"
                f"This might be due to:\n"
                f"• All posts failed to download\n"
                f"• Network issues\n"
                f"• Profile has no posts",
                parse_mode='HTML'
            )
            return
        
        # Get all files
        all_files = list(profile_dir.glob("*"))
        image_files = [f for f in all_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        video_files = [f for f in all_files if f.suffix.lower() in ['.mp4', '.mov', '.avi']]
        
        total_files = len(image_files) + len(video_files)
        
        if total_files == 0:
            await status_msg.edit_text(
                f"❌ <b>No Media Files Found</b>\n\n"
                f"👤 Username: {self.escape_html(original_username)}\n"
                f"📥 Posts processed: {downloaded_count}\n\n"
                f"No image or video files were found.",
                parse_mode='HTML'
            )
            return
        
        # Update status
        await status_msg.edit_text(
            f"✅ <b>Download Complete!</b>\n\n"
            f"👤 Username: {self.escape_html(original_username)}\n"
            f"📥 Posts downloaded: {downloaded_count}\n"
            f"🖼️ Images: {len(image_files)}\n"
            f"🎥 Videos: {len(video_files)}\n\n"
            f"📤 Sending files to Telegram...",
            parse_mode='HTML'
        )
        
        # Send files
        sent_count = 0
        max_files_to_send = 15  # Reasonable limit for Telegram
        
        # Send images first
        for img_file in image_files[:max_files_to_send]:
            try:
                file_size_mb = img_file.stat().st_size / (1024 * 1024)
                if file_size_mb < self.telegram_upload_limit_mb:
                    with open(img_file, 'rb') as f:
                        await update.message.reply_photo(f)
                    sent_count += 1
                    await asyncio.sleep(0.5)  # Rate limiting
                else:
                    logger.info(f"Skipping large image: {img_file.name} ({file_size_mb:.1f}MB) - exceeds Telegram's 50MB limit")
            except Exception as e:
                logger.error(f"Failed to send image {img_file}: {e}")
        
        # Send videos
        remaining_slots = max_files_to_send - sent_count
        for vid_file in video_files[:remaining_slots]:
            try:
                file_size_mb = vid_file.stat().st_size / (1024 * 1024)
                if file_size_mb < self.telegram_upload_limit_mb:
                    with open(vid_file, 'rb') as f:
                        await update.message.reply_video(f)
                    sent_count += 1
                    await asyncio.sleep(1)  # Longer delay for videos
                else:
                    logger.info(f"Skipping large video: {vid_file.name} ({file_size_mb:.1f}MB) - exceeds Telegram's 50MB limit")
            except Exception as e:
                logger.error(f"Failed to send video {vid_file}: {e}")
        
        # Final summary
        if sent_count < total_files:
            await update.message.reply_text(
                f"📤 <b>Files Sent: {sent_count}/{total_files}</b>\n\n"
                f"Some files were skipped due to:\n"
                f"• File size &gt; 50MB (Telegram's limit)\n"
                f"• Telegram sending limits\n"
                f"• Network issues\n\n"
                f"💡 For complete downloads, use the CLI version!",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                f"🎉 <b>All {sent_count} files sent successfully!</b>\n\n"
                f"👤 Profile: {self.escape_html(original_username)}\n"
                f"📥 Posts: {downloaded_count}\n"
                f"📤 Files: {sent_count}",
                parse_mode='HTML'
            )
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def escape_html(self, text: str) -> str:
        """Escape HTML special characters for safe display"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def format_number(self, num: int) -> str:
        """Format large numbers with K, M suffixes"""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)
    
    def run(self):
        """Start the bot"""
        logger.info("🤖 Starting Robust Instagram Downloader Bot...")
        logger.info(f"📊 Max posts per request: {self.max_posts_per_request}")
        logger.info(f"📁 Max processing size: {self.max_file_size_mb}MB, Telegram upload limit: {self.telegram_upload_limit_mb}MB")
        self.app.run_polling(drop_pending_updates=True)

# ==================== MAIN FUNCTION ====================

def main():
    """Main function to start the bot"""
    # Get bot token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ **Error: Missing Bot Token**")
        print("\n📝 Setup Instructions:")
        print("1. Create a bot with @BotFather on Telegram")
        print("2. Get your bot token")
        print("3. Set environment variable:")
        print("   Windows: set TELEGRAM_BOT_TOKEN=your_token_here")
        print("   Linux/Mac: export TELEGRAM_BOT_TOKEN=your_token_here")
        print("4. Run this script again")
        return
    
    try:
        # Create and start bot
        bot = RobustInstagramBot(token)
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        logger.error(f"Bot startup failed: {e}")

if __name__ == "__main__":
    main()