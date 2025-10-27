#!/bin/bash
# Academic Website Setup Script

echo "🎓 Academic Website Setup"
echo "========================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found"

# Remove existing environment if it exists (for clean install)
if conda env list | grep -q "academic-website"; then
    echo "🗑️  Removing existing environment for clean install..."
    conda env remove -n academic-website -y
fi

# Create conda environment from environment.yml
echo "📦 Creating conda environment with Python 3.9..."
if [ -f "environment.yml" ]; then
    conda env create -f environment.yml
    echo "✅ Environment created from environment.yml"
else
    # Fallback to manual creation
    conda create -n academic-website python=3.9 -y
    eval "$(conda shell.bash hook)"
    conda activate academic-website
    pip install -r requirements.txt
    echo "✅ Environment created from requirements.txt"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the website:"
echo "1. conda activate academic-website"
echo "2. cd new_website"
echo "3. python run_dev.py"
echo ""
echo "Or simply run: ./start_website.sh"