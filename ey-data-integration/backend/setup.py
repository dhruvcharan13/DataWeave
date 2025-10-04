#!/usr/bin/env python3
"""
Backend setup script for EY Data Integration MVP
"""

import os
import subprocess
import sys

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# Supabase Configuration\n")
            f.write("SUPABASE_URL=your_supabase_url_here\n")
            f.write("SUPABASE_KEY=your_supabase_anon_key_here\n")
            f.write("\n")
            f.write("# Backend Configuration\n")
            f.write("BACKEND_URL=http://localhost:8000\n")
        print("✅ .env file created! Please update with your Supabase credentials.")
    else:
        print("✅ .env file already exists!")

def create_temp_directory():
    """Create temp directory for file uploads"""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        print("✅ Created temp directory for file uploads")
    else:
        print("✅ Temp directory already exists")

def main():
    print("🚀 Setting up EY Data Integration Backend...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        return
    
    # Create .env file
    create_env_file()
    
    # Create temp directory
    create_temp_directory()
    
    print("=" * 50)
    print("✅ Backend setup complete!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your Supabase credentials")
    print("2. Run the Supabase schema: supabase-schema.sql")
    print("3. Start the backend: python main.py")
    print("4. API will be available at: http://localhost:8000")
    print("5. API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
