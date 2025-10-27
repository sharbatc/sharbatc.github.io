"""
Blog Management Module
=====================

Handles markdown blog posts with frontmatter support.
"""

import os
import re
import yaml
import markdown
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class BlogPost:
    def __init__(self, filepath: str, lang: str = 'en'):
        self.filepath = filepath
        self.lang = lang
        self.content = ""
        self.html_content = ""
        self.metadata = {}
        self._load_post()
    
    def _load_post(self):
        """Load and parse the markdown file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Parse frontmatter
                self.metadata = yaml.safe_load(parts[1])
                self.content = parts[2].strip()
            else:
                self.content = content
        else:
            self.content = content
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=[
            'meta', 'codehilite', 'fenced_code', 'tables', 'toc'
        ])
        self.html_content = md.convert(self.content)
        
        # Extract metadata if not in frontmatter
        if hasattr(md, 'Meta'):
            for key, value in md.Meta.items():
                if key not in self.metadata:
                    self.metadata[key] = value[0] if isinstance(value, list) and len(value) == 1 else value
    
    @property
    def title(self) -> str:
        return self.metadata.get('title', 'Untitled')
    
    @property
    def date(self) -> datetime:
        date_str = self.metadata.get('date', '')
        if date_str:
            # Handle both string dates and datetime.date objects
            if isinstance(date_str, datetime):
                return date_str
            elif hasattr(date_str, 'strftime'):  # datetime.date object
                return datetime.combine(date_str, datetime.min.time())
            else:
                # String date
                return datetime.strptime(str(date_str).strip(), '%Y-%m-%d')
        return datetime.now()
    
    @property
    def excerpt(self) -> str:
        excerpt = self.metadata.get('excerpt', '')
        if not excerpt:
            # Extract first paragraph
            first_para = self.content.split('\n\n')[0]
            excerpt = first_para[:200] + '...' if len(first_para) > 200 else first_para
        return excerpt
    
    @property
    def tags(self) -> List[str]:
        tags = self.metadata.get('tags', [])
        if isinstance(tags, str):
            return [tag.strip() for tag in tags.split(',')]
        return tags
    
    @property
    def author(self) -> str:
        return self.metadata.get('author', 'Sharbatanu Chatterjee')
    
    @property
    def slug(self) -> str:
        filename = Path(self.filepath).stem
        return self.metadata.get('slug', filename)
    
    @property
    def reading_time(self) -> int:
        """Estimate reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Average 200 words per minute

class BlogManager:
    def __init__(self, content_dir: str = 'content/blog'):
        self.content_dir = content_dir
        self._posts_cache = {}
    
    def get_posts(self, lang: str = 'en', limit: Optional[int] = None) -> List[BlogPost]:
        """Get all blog posts for a language, sorted by date (newest first)"""
        posts = []
        blog_dir = Path(self.content_dir)
        
        if not blog_dir.exists():
            return posts
        
        # Look for markdown files
        for file_path in blog_dir.glob('*.md'):
            try:
                post = BlogPost(str(file_path), lang)
                # Check if post is for this language
                post_lang = post.metadata.get('lang', 'en')
                if post_lang == lang:
                    posts.append(post)
            except Exception as e:
                print(f"Error loading post {file_path}: {e}")
        
        # Sort by date, newest first
        posts.sort(key=lambda p: p.date, reverse=True)
        
        if limit:
            posts = posts[:limit]
        
        return posts
    
    def get_post(self, slug: str, lang: str = 'en') -> Optional[BlogPost]:
        """Get a specific post by slug"""
        posts = self.get_posts(lang)
        for post in posts:
            if post.slug == slug:
                return post
        return None
    
    def get_tags(self, lang: str = 'en') -> List[str]:
        """Get all unique tags"""
        all_tags = set()
        posts = self.get_posts(lang)
        for post in posts:
            all_tags.update(post.tags)
        return sorted(list(all_tags))
    
    def get_posts_by_tag(self, tag: str, lang: str = 'en') -> List[BlogPost]:
        """Get posts filtered by tag"""
        posts = self.get_posts(lang)
        return [post for post in posts if tag in post.tags]