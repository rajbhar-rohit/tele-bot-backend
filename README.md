# 📸 Instagram Content Downloader

A simple tool to download all posts and reels from any public Instagram profile.

## 🚀 Quick Start

### For Beginners (No Python knowledge needed)
1. Double-click `DOWNLOAD.bat`
2. Enter the Instagram username when prompted
3. Wait for download to complete
4. Find your files in the `downloads` folder

### For Command Line Users
```cmd
DOWNLOAD.bat username
DOWNLOAD.bat username my_folder
```

## 📋 What You Get
- ✅ All photos and videos from posts
- ✅ All reels and video content  
- ✅ Carousel posts (multiple images/videos)
- ❌ No JSON metadata files (clean downloads)
- ❌ No stories (they expire anyway)

## 📁 File Structure
```
instagram-downloader/
├── DOWNLOAD.bat          # Easy-to-use launcher
├── insta_cli.py         # Main CLI program
├── requirements.txt     # Python dependencies
├── build_exe.py         # Create standalone executable
└── README.md           # This file
```

## 🛠️ Advanced Usage

### CLI Options
```cmd
python insta_cli.py username                    # Basic download
python insta_cli.py username -o my_folder       # Custom folder
python insta_cli.py username --limit 50         # Download only 50 posts
python insta_cli.py username --quiet            # Minimal output
python insta_cli.py username --help             # Show all options
```

### Create Standalone Executable
```cmd
python build_exe.py
```
This creates `dist/insta-dl.exe` that works without Python installed.

## 📦 Requirements
- Windows 10/11
- Internet connection
- Python 3.7+ (automatically installed if missing)

## ⚠️ Important Notes
- Only works with **public** Instagram profiles
- Private profiles require you to follow them first
- Respects Instagram's rate limits
- Downloads are organized by username in folders

## 🔧 Troubleshooting

### "Profile does not exist"
- Check the username spelling
- Make sure the profile is public
- Try again later (Instagram might be blocking requests)

### "Python not found"
- The batch file will try to install Python automatically
- Or download Python from: https://python.org

### Downloads are slow
- This is normal - Instagram has rate limits
- Large profiles with many posts take time
- You can use `--limit 50` to download fewer posts

## 📞 Support
If you encounter issues:
1. Make sure you have internet connection
2. Try a different username to test
3. Check if the profile is public
4. Restart the program

## 🎯 Examples
```cmd
# Download all posts from a user
DOWNLOAD.bat cristiano

# Download to a specific folder
DOWNLOAD.bat taylorswift my_music_downloads

# Download only recent 100 posts
python insta_cli.py natgeo --limit 100
```

## 📄 License
Free to use for personal purposes. Please respect Instagram's terms of service.

---
Made with ❤️ for easy Instagram content downloading