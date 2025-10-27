#!/usr/bin/env python3
"""
Static Site Generator for Academic Website
==========================================

This script generates static HTML files from the FastAPI website
for deployment to GitHub Pages.
"""

import os
import requests
import shutil
from pathlib import Path
from urllib.parse import urljoin
import time
import sys

class StaticSiteGenerator:
    def __init__(self, base_url="http://localhost:8000", output_dir="docs"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        
        # Pages to generate
        self.pages = [
            "/",
            "/en/",
            "/en/publications",
            "/en/talks", 
            "/en/teaching",
            "/en/notebooks",
            "/en/blog",
            "/en/news",
            "/fr/",
            "/bn/",
        ]
        
        # Static assets
        self.static_dirs = [
            "static/css",
            "static/js", 
            "static/fonts",
            "static/images",
            "files"
        ]
    
    def fetch_page(self, url):
        """Fetch a single page"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Error fetching {url}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def save_page(self, path, content):
        """Save page content to file"""
        if not content:
            return
            
        file_path = self.output_dir / path.lstrip("/")
        
        # Create directory structure
        if path.endswith("/"):
            file_path = file_path / "index.html"
        elif not path.endswith(".html") and "." not in path.split("/")[-1]:
            file_path = file_path / "index.html"
            
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved: {file_path}")
    
    def copy_static_files(self):
        """Copy static files to output directory"""
        source_dir = Path("new_website")
        
        for static_dir in self.static_dirs:
            src = source_dir / static_dir
            dst = self.output_dir / static_dir
            
            if src.exists():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"Copied: {src} -> {dst}")
    
    def discover_dynamic_pages(self):
        """Discover publication, talk, and other dynamic pages"""
        additional_pages = []
        
        # Add current working directory to Python path
        sys.path.insert(0, str(Path.cwd() / "new_website"))
        
        # Get publications
        try:
            from publications_manager import PublicationsManager
            pm = PublicationsManager("content/publications")
            pubs = pm.get_publications("en")
            for pub in pubs:
                additional_pages.append(f"/en/publications/{pub.slug}")
        except Exception as e:
            print(f"Error discovering publications: {e}")
        
        # Get talks
        try:
            from talks_manager import TalksManager
            tm = TalksManager("content/talks")
            talks = tm.get_talks("en")
            for talk in talks:
                additional_pages.append(f"/en/talks/{talk.slug}")
        except Exception as e:
            print(f"Error discovering talks: {e}")
            
        # Get teaching
        try:
            from teaching_manager import TeachingManager
            teach_m = TeachingManager("content/teaching")
            teaching = teach_m.get_teaching_items("en")
            for item in teaching:
                additional_pages.append(f"/en/teaching/{item.slug}")
        except Exception as e:
            print(f"Error discovering teaching: {e}")
        
        # Get blog posts
        try:
            from blog_manager import BlogManager
            bm = BlogManager("content/blog")
            posts = bm.get_posts("en")
            for post in posts:
                additional_pages.append(f"/en/blog/{post.slug}")
        except Exception as e:
            print(f"Error discovering blog posts: {e}")
        
        return additional_pages
    
    def generate(self):
        """Generate the static site"""
        print("Starting static site generation...")
        
        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Discover dynamic pages
        dynamic_pages = self.discover_dynamic_pages()
        all_pages = self.pages + dynamic_pages
        
        # Generate pages
        print(f"Generating {len(all_pages)} pages...")
        for page in all_pages:
            url = urljoin(self.base_url, page)
            print(f"Fetching: {url}")
            content = self.fetch_page(url)
            self.save_page(page, content)
            time.sleep(0.1)  # Small delay to avoid overwhelming the server
        
        # Copy static files
        print("Copying static files...")
        self.copy_static_files()
        
        # Create .nojekyll to disable Jekyll processing
        nojekyll_path = self.output_dir / ".nojekyll"
        with open(nojekyll_path, 'w') as f:
            f.write('')
        
        print("Static site generation complete!")
        print(f"Files saved to: {self.output_dir}")

def main():
    generator = StaticSiteGenerator()
    generator.generate()

if __name__ == "__main__":
    main()