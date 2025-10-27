# Academic Website Makefile

.PHONY: check install dev clean test help

# Default target
help:
	@echo "Academic Website - Available Commands:"
	@echo "======================================"
	@echo "check     - Check Python version compatibility"
	@echo "install   - Set up the development environment"
	@echo "dev       - Start the development server"
	@echo "clean     - Remove the conda environment"
	@echo "test      - Run basic functionality tests"
	@echo "upgrade   - Upgrade all dependencies"
	@echo ""
	@echo "Quick start: make check && make install && make dev"

# Check Python version
check:
	@echo "🔍 Checking Python compatibility..."
	python check_python.py

# Install environment and dependencies
install:
	@echo "📦 Setting up environment..."
	chmod +x setup.sh
	./setup.sh

# Start development server
dev:
	@echo "🚀 Starting development server..."
	chmod +x start_website.sh
	./start_website.sh

# Clean up environment
clean:
	@echo "🗑️  Removing conda environment..."
	conda env remove -n academic-website -y || true
	@echo "✅ Environment removed"

# Test basic functionality
test:
	@echo "🧪 Testing basic functionality..."
	@command -v conda >/dev/null 2>&1 || { echo "❌ Conda not found"; exit 1; }
	@conda activate academic-website && python -c "import fastapi, uvicorn; print('✅ Core modules work')" || { echo "❌ Dependencies not installed"; exit 1; }
	@echo "✅ All tests passed"

# Upgrade dependencies
upgrade:
	@echo "⬆️  Upgrading dependencies..."
	conda activate academic-website && pip install --upgrade -r requirements.txt
	@echo "✅ Dependencies upgraded"

# Install with pip (fallback)
pip-install:
	@echo "📦 Installing with pip..."
	python -m venv academic-website-env
	@echo "Activate with: source academic-website-env/bin/activate"
	@echo "Then run: pip install -r requirements.txt"