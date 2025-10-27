#!/usr/bin/env python3
"""
Check Python version compatibility for the Academic Website.
"""
import sys
import platform

def check_python_version():
    """Check if the current Python version meets requirements."""
    required_version = (3, 9)
    current_version = sys.version_info[:2]
    
    print("🐍 Python Version Check")
    print("=" * 30)
    print(f"Current Python: {platform.python_version()}")
    print(f"Required: Python {required_version[0]}.{required_version[1]}+")
    
    if current_version >= required_version:
        print("✅ Python version is compatible!")
        return True
    else:
        print("❌ Python version is too old!")
        print(f"   Please upgrade to Python {required_version[0]}.{required_version[1]} or higher")
        print("   Download from: https://www.python.org/downloads/")
        return False

if __name__ == "__main__":
    if not check_python_version():
        sys.exit(1)
    
    print("\n🎉 Your Python installation is ready for the Academic Website!")
    print("📋 Next steps:")
    print("   1. Run: ./setup.sh")
    print("   2. Run: ./start_website.sh")