#!/usr/bin/env python3
"""
Telegram Bot Setup Script
Helps configure and run the Instagram Downloader Telegram Bot
"""

import os
import sys
from pathlib import Path

def main():
    print("🤖 Instagram Downloader Telegram Bot Setup")
    print("=" * 50)
    
    # Check if token is already set
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("\n📝 Bot Token Setup Required")
        print("\nTo create your Telegram bot:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot command")
        print("3. Follow the instructions to create your bot")
        print("4. Copy the bot token you receive")
        print("\n" + "="*50)
        
        # Get token from user
        token = input("\n🔑 Enter your bot token: ").strip()
        
        if not token:
            print("❌ No token provided. Exiting...")
            return
            
        # Set environment variable for current session
        os.environ['TELEGRAM_BOT_TOKEN'] = token
        
        print(f"\n✅ Token set for current session!")
        print(f"\n💡 To make this permanent, add this to your system:")
        
        if os.name == 'nt':  # Windows
            print(f"   set TELEGRAM_BOT_TOKEN={token}")
            print(f"   Or add it to your system environment variables")
        else:  # Unix/Linux/Mac
            print(f"   export TELEGRAM_BOT_TOKEN={token}")
            print(f"   Add this line to your ~/.bashrc or ~/.zshrc")
    else:
        print(f"✅ Bot token found: {token[:10]}...")
    
    print("\n" + "="*50)
    print("🚀 Starting bot...")
    print("📱 Your bot is now ready to receive messages!")
    print("💬 Send /start to your bot to begin")
    print("\n⏹️  Press Ctrl+C to stop the bot")
    print("="*50)
    
    # Import and run the bot
    try:
        from telegram_bot import RobustInstagramBot
        bot = RobustInstagramBot(token)
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()