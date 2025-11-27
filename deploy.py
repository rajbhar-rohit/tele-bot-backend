#!/usr/bin/env python3
"""
Deployment Helper Script for Instagram Telegram Bot
Helps you deploy to various free hosting platforms
"""

import os
import sys
import subprocess
import json

def print_banner():
    print("🚀" + "="*60 + "🚀")
    print("   Instagram Telegram Bot - Deployment Helper")
    print("🚀" + "="*60 + "🚀")
    print()

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'telegram_bot.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def check_git():
    """Check if git is initialized and has commits"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git repository not initialized!")
            print("   Run: git init && git add . && git commit -m 'Initial commit'")
            return False
        
        # Check if there are commits
        result = subprocess.run(['git', 'log', '--oneline'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("❌ No git commits found!")
            print("   Run: git add . && git commit -m 'Initial commit'")
            return False
            
        print("✅ Git repository ready!")
        return True
    except FileNotFoundError:
        print("❌ Git not installed!")
        return False

def get_bot_token():
    """Get bot token from user"""
    token = input("🔑 Enter your Telegram Bot Token: ").strip()
    if not token:
        print("❌ Bot token is required!")
        return None
    
    if not token.startswith(('1', '2', '5', '6', '7')):
        print("⚠️  Warning: Bot token format looks unusual")
    
    return token

def create_env_file(token):
    """Create .env file with bot token"""
    with open('.env', 'w') as f:
        f.write(f"TELEGRAM_BOT_TOKEN={token}\n")
        f.write("LOG_LEVEL=INFO\n")
    print("✅ Created .env file")

def show_deployment_options():
    """Show available deployment options"""
    print("\n🌐 Choose your deployment platform:")
    print("1. 🚂 Railway (Recommended - Easy setup)")
    print("2. 🎨 Render (No credit card needed)")
    print("3. 🟣 Heroku (Popular choice)")
    print("4. 🐍 PythonAnywhere (Python-focused)")
    print("5. 🐳 Docker (Self-hosted)")
    print("6. 📋 Show all instructions")
    print()

def railway_instructions():
    """Show Railway deployment instructions"""
    print("\n🚂 Railway Deployment:")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your repository")
    print("5. Add environment variable:")
    print("   - Key: TELEGRAM_BOT_TOKEN")
    print("   - Value: [your bot token]")
    print("6. Deploy automatically!")
    print("\n✅ Your bot will be live 24/7!")

def render_instructions():
    """Show Render deployment instructions"""
    print("\n🎨 Render Deployment:")
    print("1. Go to https://render.com")
    print("2. Sign up (no credit card needed)")
    print("3. New → Web Service")
    print("4. Connect GitHub repository")
    print("5. Configure:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python telegram_bot.py")
    print("6. Add environment variable: TELEGRAM_BOT_TOKEN")
    print("7. Deploy!")
    print("\n⚠️  Note: Free tier sleeps after 15 minutes of inactivity")

def heroku_instructions():
    """Show Heroku deployment instructions"""
    print("\n🟣 Heroku Deployment:")
    print("1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. Login: heroku login")
    print("3. Create app: heroku create your-bot-name")
    print("4. Set token: heroku config:set TELEGRAM_BOT_TOKEN=your_token")
    print("5. Deploy: git push heroku main")
    print("6. Scale worker: heroku ps:scale worker=1")
    print("\n⚠️  Note: Requires credit card for verification")

def pythonanywhere_instructions():
    """Show PythonAnywhere deployment instructions"""
    print("\n🐍 PythonAnywhere Deployment:")
    print("1. Go to https://pythonanywhere.com")
    print("2. Create free account")
    print("3. Upload your code via Files tab")
    print("4. Go to Tasks → Create scheduled task")
    print("5. Command: python3.10 /home/yourusername/telegram_bot.py")
    print("6. Set to run every minute: * * * * *")
    print("\n✅ Always-on task (no sleeping)")

def docker_instructions():
    """Show Docker deployment instructions"""
    print("\n🐳 Docker Deployment:")
    print("1. Install Docker: https://docs.docker.com/get-docker/")
    print("2. Build image: docker build -t instagram-bot .")
    print("3. Run container:")
    print("   docker run -d --name instagram-bot \\")
    print("     -e TELEGRAM_BOT_TOKEN=your_token \\")
    print("     --restart unless-stopped \\")
    print("     instagram-bot")
    print("\n🔧 Or use docker-compose:")
    print("   docker-compose up -d")

def show_all_instructions():
    """Show all deployment instructions"""
    railway_instructions()
    render_instructions()
    heroku_instructions()
    pythonanywhere_instructions()
    docker_instructions()

def main():
    print_banner()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    if not check_git():
        sys.exit(1)
    
    # Get bot token
    token = get_bot_token()
    if not token:
        sys.exit(1)
    
    # Create .env file
    create_env_file(token)
    
    # Show deployment options
    show_deployment_options()
    
    try:
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            railway_instructions()
        elif choice == '2':
            render_instructions()
        elif choice == '3':
            heroku_instructions()
        elif choice == '4':
            pythonanywhere_instructions()
        elif choice == '5':
            docker_instructions()
        elif choice == '6':
            show_all_instructions()
        else:
            print("❌ Invalid choice!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Deployment cancelled by user")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("🎉 Deployment instructions complete!")
    print("📚 Check DEPLOYMENT_GUIDE.md for detailed information")
    print("🔧 All deployment files are ready in your repository")
    print("="*60)

if __name__ == "__main__":
    main()