#!/bin/bash

# Deploy script for GitHub Pages
# This script generates static files from the FastAPI website

set -e

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -d "new_website" ]; then
    echo "❌ Error: new_website directory not found. Please run this script from the repository root."
    exit 1
fi

# Check if docs directory exists, if so, remove it
if [ -d "docs" ]; then
    echo "🧹 Cleaning existing docs directory..."
    rm -rf docs
fi

# Create docs directory
mkdir -p docs

echo "📋 Starting FastAPI server..."
cd new_website

# Start the server in background
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Check if server is running
if ! curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "❌ Error: Server failed to start"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Server started successfully"

cd ..

echo "📄 Generating static pages..."

# Create basic static pages
pages=(
    ""
    "en/"
    "en/publications"
    "en/talks"
    "en/teaching"
    "en/notebooks"
    "en/blog"
    "en/news"
    "fr/"
    "bn/"
)

# Download main pages
for page in "${pages[@]}"; do
    echo "Fetching: $page"
    
    if [ -z "$page" ]; then
        # Root page
        curl -s "http://localhost:8000/" > docs/index.html
    else
        # Create directory structure
        mkdir -p "docs/$page"
        curl -s "http://localhost:8000/$page" > "docs/$page/index.html"
    fi
done

# Copy static assets
echo "📁 Copying static assets..."
if [ -d "new_website/static" ]; then
    cp -r new_website/static docs/
fi

if [ -d "files" ]; then
    cp -r files docs/
fi

# Create .nojekyll file to disable Jekyll
touch docs/.nojekyll

# Stop the server
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null || true

echo "✅ Static site generated successfully in docs/ directory"
echo "📝 Next steps:"
echo "   1. Commit and push changes to GitHub"
echo "   2. Go to repository Settings > Pages"
echo "   3. Set source to 'Deploy from a branch'"
echo "   4. Select 'master' branch and '/docs' folder"
echo "   5. Your site will be available at https://sharbatc.github.io"