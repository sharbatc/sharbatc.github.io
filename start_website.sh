#!/bin/bash
# Quick start script for the academic website

echo "🚀 Starting Academic Website..."

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate academic-website

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "📁 Navigating to website directory..."
    cd new_website
fi

# Start the development server
python run_dev.py