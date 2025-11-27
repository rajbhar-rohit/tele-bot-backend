"""
Build Script for Instagram Downloader
Creates a standalone executable that doesn't require Python
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller!")
            return False

def build_executable():
    """Build standalone executable"""
    print("🔨 Building standalone executable...")
    
    # Install requirements first
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=insta-dl",
        "--console",
        "--clean",
        "--distpath=.",
        "insta_cli.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build completed!")
        print("📁 Executable created: insta-dl.exe")
        
        # Create batch file for the executable
        with open("RUN-EXE.bat", "w") as f:
            f.write('@echo off\n')
            f.write('title Instagram Downloader (Standalone)\n')
            f.write('echo Instagram Content Downloader (Standalone Version)\n')
            f.write('echo ================================================\n')
            f.write('echo.\n')
            f.write('if "%1"=="" (\n')
            f.write('    set /p username="Enter Instagram username: "\n')
            f.write('    set /p folder="Enter output folder (or press Enter for \'downloads\'): "\n')
            f.write('    if "%folder%"=="" set folder=downloads\n')
            f.write('    insta-dl.exe %username% -o %folder%\n')
            f.write(') else (\n')
            f.write('    insta-dl.exe %*\n')
            f.write(')\n')
            f.write('pause\n')
        
        print("📝 Created RUN-EXE.bat for standalone version")
        print("\n🚀 Usage:")
        print("  insta-dl.exe username")
        print("  insta-dl.exe username -o my_folder")
        print("  RUN-EXE.bat  (interactive mode)")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Build failed!")
        return False

def main():
    print("Instagram Downloader - Executable Builder")
    print("=" * 45)
    print("This will create a standalone .exe file that works")
    print("without Python installed on other computers.")
    print()
    
    if not install_pyinstaller():
        return
    
    if not build_executable():
        return
    
    print("\n🎉 Success! You now have:")
    print("  • insta-dl.exe - Standalone executable")
    print("  • RUN-EXE.bat - Easy launcher for the exe")
    print("\nYou can share these files with others who don't have Python!")

if __name__ == "__main__":
    main()