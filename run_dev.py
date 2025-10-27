#!/usr/bin/env python3
"""
Development server startup script with port conflict handling
"""

import os
import sys
import socket
import subprocess
import signal
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for development
os.environ['DEVELOPMENT'] = '1'

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill any process running on the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"🔄 Killing existing process {pid} on port {port}")
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                    except ProcessLookupError:
                        pass  # Process already gone
            return True
    except Exception as e:
        print(f"⚠️  Could not kill process on port {port}: {e}")
    return False

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return None

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Academic Website Development Server")
    print("=" * 50)
    
    port = 8000
    
    # Check if port is in use and handle accordingly
    if is_port_in_use(port):
        print(f"⚠️  Port {port} is already in use")
        
        # Try to kill existing process
        if kill_process_on_port(port):
            print(f"✅ Freed up port {port}")
            # Wait a moment for the port to be released
            import time
            time.sleep(1)
        
        # If port is still in use, find alternative
        if is_port_in_use(port):
            alt_port = find_available_port(8001)
            if alt_port:
                port = alt_port
                print(f"🔄 Using alternative port {port}")
            else:
                print("❌ No available ports found")
                sys.exit(1)
    
    print(f"📍 URL: http://localhost:{port}")
    print("🌍 Languages: English, French, Bengali")
    print("📝 Features: Blog, Notebooks, News, Multilingual")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            reload_dirs=[str(current_dir)],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)