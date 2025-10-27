#!/usr/bin/env python3
"""
Static Site Generator for FastAPI Academic Website
=================================================

This script generates a static version of the FastAPI website that can be
deployed to GitHub Pages or any static hosting service.

Author: Sharbatanu Chatterjee
"""

import os
import sys
import shutil
import requests
import time
import signal
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse
import threading

class StaticSiteGenerator:
    def __init__(self, base_url="http://localhost:8000", output_dir="dist"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.server_process = None
        
        # Pages to generate (add more as needed)
        self.pages = [
            "/",
            "/en/",
            "/fr/", 
            "/bn/",
            "/en/about",
            "/fr/about",
            "/bn/about",
            "/en/blog",
            "/fr/blog", 
            "/bn/blog",
            "/en/notebooks",
            "/fr/notebooks",
            "/bn/notebooks",
            "/en/publications",
            "/fr/publications",
            "/bn/publications",
            "/en/talks",
            "/fr/talks",
            "/bn/talks",
            "/en/teaching",
            "/fr/teaching", 
            "/bn/teaching",
            "/en/cv",
            "/fr/cv",
            "/bn/cv",
            "/en/contact",
            "/fr/contact",
            "/bn/contact",
            "/en/news",
            "/fr/news",
            "/bn/news",
        ]
    
    def start_server(self):
        """Start the FastAPI development server"""
        print("Starting FastAPI server...")
        try:
            # Use the current Python executable (works in both local conda env and GitHub Actions)
            python_path = sys.executable
                
            # Start server in background
            self.server_process = subprocess.Popen([
                python_path, "-m", "uvicorn", 
                "main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--log-level", "warning"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(10)
            
            # Test if server is responding
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully")
                return True
            else:
                print(f"❌ Server responded with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the FastAPI server"""
        if self.server_process:
            print("Stopping FastAPI server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("✅ Server stopped")
    
    def create_output_dir(self):
        """Create and clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created output directory: {self.output_dir}")
    
    def copy_static_files(self):
        """Copy static files (CSS, JS, images) to output directory"""
        static_dir = Path("static")
        if static_dir.exists():
            output_static = self.output_dir / "static"
            shutil.copytree(static_dir, output_static)
            print("✅ Copied static files")
    
    def generate_page(self, page_path):
        """Generate a single page"""
        try:
            url = urljoin(self.base_url, page_path)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Create directory structure
                if page_path.endswith('/') or '.' not in page_path.split('/')[-1]:
                    file_path = self.output_dir / page_path.strip('/') / "index.html"
                else:
                    file_path = self.output_dir / page_path.strip('/')
                
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write HTML content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"✅ Generated: {page_path} -> {file_path}")
                return True
            else:
                print(f"❌ Failed to generate {page_path}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error generating {page_path}: {e}")
            return False
    
    def discover_blog_posts(self):
        """Discover individual blog posts and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all blog post files
            blog_dir = Path("content/blog")
            if blog_dir.exists():
                blog_files = list(blog_dir.glob("*.md"))
                
                languages = ['en', 'fr', 'bn']
                for blog_file in blog_files:
                    slug = blog_file.stem  # filename without .md extension
                    for lang in languages:
                        blog_url = f"/{lang}/blog/{slug}"
                        if blog_url not in self.pages:
                            self.pages.append(blog_url)
                
                print(f"✅ Discovered {len(blog_files)} blog posts for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover blog posts: {e}")
    
    def discover_publications(self):
        """Discover individual publications and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all publication files
            pub_dir = Path("content/publications")
            if pub_dir.exists():
                pub_files = list(pub_dir.glob("*.md"))
                
                languages = ['en', 'fr', 'bn']
                for pub_file in pub_files:
                    slug = pub_file.stem  # filename without .md extension
                    for lang in languages:
                        pub_url = f"/{lang}/publications/{slug}"
                        if pub_url not in self.pages:
                            self.pages.append(pub_url)
                
                print(f"✅ Discovered {len(pub_files)} publications for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover publications: {e}")
    
    def discover_talks(self):
        """Discover individual talks and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all talk files
            talk_dir = Path("content/talks")
            if talk_dir.exists():
                talk_files = list(talk_dir.glob("*.md"))
                
                languages = ['en', 'fr', 'bn']
                for talk_file in talk_files:
                    slug = talk_file.stem  # filename without .md extension
                    for lang in languages:
                        talk_url = f"/{lang}/talks/{slug}"
                        if talk_url not in self.pages:
                            self.pages.append(talk_url)
                
                print(f"✅ Discovered {len(talk_files)} talks for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover talks: {e}")
    
    def discover_teaching(self):
        """Discover individual teaching items and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all teaching files
            teaching_dir = Path("content/teaching")
            if teaching_dir.exists():
                teaching_files = list(teaching_dir.glob("*.md"))
                
                languages = ['en', 'fr', 'bn']
                for teaching_file in teaching_files:
                    slug = teaching_file.stem  # filename without .md extension
                    for lang in languages:
                        teaching_url = f"/{lang}/teaching/{slug}"
                        if teaching_url not in self.pages:
                            self.pages.append(teaching_url)
                
                print(f"✅ Discovered {len(teaching_files)} teaching items for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover teaching items: {e}")
    
    def discover_news(self):
        """Discover individual news items and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all news files
            news_dir = Path("content/news")
            if news_dir.exists():
                news_files = list(news_dir.glob("*.md"))
                
                languages = ['en', 'fr', 'bn']
                for news_file in news_files:
                    slug = news_file.stem  # filename without .md extension
                    for lang in languages:
                        news_url = f"/{lang}/news/{slug}"
                        if news_url not in self.pages:
                            self.pages.append(news_url)
                
                print(f"✅ Discovered {len(news_files)} news items for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover news items: {e}")

    def discover_notebooks(self):
        """Discover individual notebooks and add them to pages list"""
        try:
            from pathlib import Path
            
            # Find all notebook files
            notebooks_dir = Path("content/notebooks")
            if notebooks_dir.exists():
                notebook_files = list(notebooks_dir.glob("*.ipynb"))
                
                languages = ['en', 'fr', 'bn']
                for notebook_file in notebook_files:
                    slug = notebook_file.stem  # filename without .ipynb extension
                    for lang in languages:
                        notebook_url = f"/{lang}/notebooks/{slug}"
                        if notebook_url not in self.pages:
                            self.pages.append(notebook_url)
                
                print(f"✅ Discovered {len(notebook_files)} notebooks for {len(languages)} languages")
                            
        except Exception as e:
            print(f"⚠️  Could not discover notebooks: {e}")
    
    def generate_404_page(self):
        """Generate a 404 page"""
        try:
            # Create a simple 404 page
            html_404 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - Sharbatanu Chatterjee</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container text-center mt-5">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/" class="btn btn-primary">Go Home</a>
    </div>
</body>
</html>"""
            
            with open(self.output_dir / "404.html", 'w', encoding='utf-8') as f:
                f.write(html_404)
            
            print("✅ Generated 404.html")
            
        except Exception as e:
            print(f"❌ Error generating 404 page: {e}")
    
    def generate_site(self):
        """Generate the complete static site"""
        print("🚀 Starting static site generation...")
        
        try:
            # Step 1: Create output directory
            self.create_output_dir()
            
            # Step 2: Start the FastAPI server
            if not self.start_server():
                return False
            
            # Step 3: Copy static files
            self.copy_static_files()
            
            # Step 4: Discover additional pages
            self.discover_blog_posts()
            self.discover_publications()
            self.discover_talks()
            self.discover_teaching()
            self.discover_news()
            self.discover_notebooks()
            
            # Step 5: Generate all pages
            success_count = 0
            for page in self.pages:
                if self.generate_page(page):
                    success_count += 1
            
            # Step 6: Generate 404 page
            self.generate_404_page()
            
            print(f"\n🎉 Site generation complete!")
            print(f"✅ Successfully generated {success_count}/{len(self.pages)} pages")
            print(f"📁 Output directory: {self.output_dir.absolute()}")
            
            return success_count > 0
            
        except KeyboardInterrupt:
            print("\n⚠️  Generation interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Generation failed: {e}")
            return False
        finally:
            # Always stop the server
            self.stop_server()

def main():
    """Main function"""
    print("Academic Website Static Generator")
    print("=" * 40)
    
    generator = StaticSiteGenerator()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n⚠️  Interrupted by user")
        generator.stop_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate the site
    success = generator.generate_site()
    
    if success:
        print("\n🎉 Static site generated successfully!")
        print("💡 You can now deploy the 'dist' folder to any static hosting service.")
        sys.exit(0)
    else:
        print("\n❌ Static site generation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()