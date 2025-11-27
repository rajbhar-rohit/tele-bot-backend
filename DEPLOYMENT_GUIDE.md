# 🚀 24/7 Free Hosting Guide for Instagram Telegram Bot

This guide shows you how to deploy your Instagram Telegram Bot for free 24/7 hosting.

## 🆓 Free Hosting Options (Ranked by Ease)

### 1. 🥇 **Railway** (Recommended - Easiest)
- **Free Tier**: 500 hours/month (enough for 24/7)
- **Pros**: Easy setup, GitHub integration, automatic deployments
- **Cons**: Credit card required (but free tier)

### 2. 🥈 **Render** 
- **Free Tier**: 750 hours/month
- **Pros**: No credit card needed, simple deployment
- **Cons**: Sleeps after 15 minutes of inactivity

### 3. 🥉 **Heroku** (Limited Free)
- **Free Tier**: 550-1000 hours/month
- **Pros**: Popular, well-documented
- **Cons**: Sleeps after 30 minutes, requires credit card

### 4. 🔧 **PythonAnywhere**
- **Free Tier**: Always-on tasks (1 task)
- **Pros**: Python-focused, no sleep
- **Cons**: Limited resources

### 5. 🐙 **GitHub Codespaces** (Advanced)
- **Free Tier**: 120 hours/month
- **Pros**: Full development environment
- **Cons**: Limited hours, complex setup

---

## 🚀 Quick Setup Instructions

### Option 1: Railway (Recommended)

1. **Prepare your code**:
   ```bash
   # Make sure all files are ready
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy

3. **Set environment variables**:
   - Go to your project → Variables
   - Add: `TELEGRAM_BOT_TOKEN=your_bot_token_here`

### Option 2: Render

1. **Create account**: Go to [render.com](https://render.com)
2. **New Web Service**: Connect your GitHub repo
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python telegram_bot.py`
4. **Environment Variables**: Add `TELEGRAM_BOT_TOKEN`

### Option 3: PythonAnywhere

1. **Create account**: Go to [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload code**: Use Files tab or git clone
3. **Create task**: Go to Tasks → Create scheduled task
4. **Set command**: `python3.10 /home/yourusername/telegram_bot.py`

---

## 📁 Required Files for Deployment

All hosting platforms need these files in your repository:

### Core Files ✅
- `telegram_bot.py` - Your main bot code
- `requirements.txt` - Python dependencies
- `Procfile` - Process definition for Heroku/Railway
- `runtime.txt` - Python version specification

### Platform-Specific Files
- `railway.json` - Railway configuration
- `render.yaml` - Render configuration  
- `Dockerfile` - Docker container setup
- `docker-compose.yml` - Docker Compose setup
- `.env.example` - Environment variables template

---

## 🛠️ Step-by-Step Setup

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**:
   ```bash
   # Create repository on GitHub first
   git remote add origin https://github.com/yourusername/instagram-telegram-bot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Get Your Bot Token

1. **Create Bot**:
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Follow instructions
   - Copy the bot token

2. **Test Locally** (optional):
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token_here"
   python telegram_bot.py
   ```

### Step 3: Choose Hosting Platform

Run the deployment helper:
```bash
python deploy.py
```

---

## 🚀 Detailed Platform Instructions

### 🥇 Railway (Recommended)

**Why Railway?**
- ✅ 500 hours/month free (20+ days)
- ✅ Automatic deployments from GitHub
- ✅ Easy environment variable management
- ✅ No sleeping (unlike Heroku/Render)

**Setup Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Add environment variable:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: Your bot token
7. Deploy automatically!

**Pro Tips:**
- Railway auto-detects Python projects
- Uses `Procfile` for process definition
- Supports custom domains (paid plans)
- Great logging and monitoring

---

### 🥈 Render

**Why Render?**
- ✅ No credit card required
- ✅ 750 hours/month free
- ✅ GitHub integration
- ❌ Sleeps after 15 minutes inactivity

**Setup Steps:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. New → Web Service
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python telegram_bot.py`
6. Add environment variable: `TELEGRAM_BOT_TOKEN`
7. Deploy!

**Keep-Alive Solution:**
```python
# Add to your bot (optional)
import requests
import threading
import time

def keep_alive():
    while True:
        try:
            requests.get("https://your-app-name.onrender.com")
            time.sleep(300)  # Ping every 5 minutes
        except:
            pass

# Start keep-alive thread
threading.Thread(target=keep_alive, daemon=True).start()
```

---

### 🥉 Heroku

**Why Heroku?**
- ✅ Popular and well-documented
- ✅ 550-1000 hours/month free
- ❌ Requires credit card verification
- ❌ Sleeps after 30 minutes

**Setup Steps:**
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Create app: `heroku create your-bot-name`
4. Set environment variable:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```
6. Scale worker process:
   ```bash
   heroku ps:scale worker=1
   ```

**Heroku-Specific Files:**
- `Procfile`: Defines worker process
- `runtime.txt`: Specifies Python version

---

### 🐍 PythonAnywhere

**Why PythonAnywhere?**
- ✅ Python-focused hosting
- ✅ Always-on tasks (no sleeping)
- ✅ Free tier includes 1 scheduled task
- ❌ Limited resources on free tier

**Setup Steps:**
1. Create account at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your code:
   - Use Files tab to upload
   - Or clone from GitHub: `git clone https://github.com/yourusername/repo.git`
3. Install dependencies:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. Create scheduled task:
   - Go to Tasks tab
   - Create new task
   - Command: `python3.10 /home/yourusername/telegram_bot.py`
   - Schedule: Leave blank for always-on

**Environment Variables:**
Create a `.env` file in your project directory:
```bash
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
```

---

### 🐳 Docker (Self-Hosted)

**Why Docker?**
- ✅ Complete control
- ✅ Consistent environment
- ✅ Easy scaling
- ❌ Requires your own server

**Quick Start:**
```bash
# Build and run
docker build -t instagram-bot .
docker run -d --name instagram-bot \
  -e TELEGRAM_BOT_TOKEN=your_token \
  --restart unless-stopped \
  instagram-bot
```

**Docker Compose:**
```bash
# Create .env file first
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env

# Start with docker-compose
docker-compose up -d
```

**Free VPS Options:**
- Oracle Cloud (Always Free tier)
- Google Cloud (Free tier)
- AWS (Free tier - 12 months)
- DigitalOcean (Student pack)

---

## 🔧 Troubleshooting

### Common Issues

**Bot Not Responding:**
```bash
# Check logs
heroku logs --tail  # Heroku
# Or check platform-specific logs
```

**Import Errors:**
- Ensure `requirements.txt` is complete
- Check Python version compatibility

**Token Issues:**
- Verify token is correct
- Check environment variable name
- Ensure no extra spaces

**Memory Issues:**
- Reduce `max_posts_per_request` in bot
- Optimize file processing

### Monitoring Your Bot

**Health Checks:**
```python
# Add to your bot
import requests

def health_check():
    try:
        # Test Telegram API
        requests.get(f"https://api.telegram.org/bot{token}/getMe")
        return True
    except:
        return False
```

**Logging:**
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## 💡 Pro Tips for 24/7 Operation

### 1. **Error Handling**
```python
# Robust error handling
try:
    bot.run()
except Exception as e:
    logging.error(f"Bot crashed: {e}")
    # Restart logic here
```

### 2. **Resource Management**
- Set reasonable limits on file sizes
- Clean up temporary files
- Monitor memory usage

### 3. **Rate Limiting**
- Respect Instagram's API limits
- Add delays between requests
- Handle rate limit errors gracefully

### 4. **Monitoring**
- Set up uptime monitoring (UptimeRobot)
- Configure error notifications
- Monitor resource usage

### 5. **Backup Strategy**
- Keep code in version control
- Document configuration
- Have deployment scripts ready

---

## 🎯 Recommended Setup

**For Beginners:** Railway
- Easiest setup
- Good free tier
- No sleeping issues

**For Advanced Users:** Docker + VPS
- Full control
- Better performance
- Scalable

**For Testing:** Render
- No credit card needed
- Quick setup
- Good for development

---

## 📞 Support

If you encounter issues:

1. **Check the logs** on your hosting platform
2. **Verify environment variables** are set correctly
3. **Test locally** first with `python telegram_bot.py`
4. **Check bot token** with @BotFather
5. **Review platform documentation** for specific issues

---

## 🎉 Success!

Once deployed, your bot will be available 24/7! Users can:
- Send Instagram usernames to download content
- Use `/all` for complete profile downloads
- Use `/limit` for specific number of posts
- Get real-time progress updates

**Test your deployment:**
1. Send `/start` to your bot
2. Try downloading from a public Instagram profile
3. Monitor logs for any issues

Your Instagram Telegram Bot is now live! 🚀