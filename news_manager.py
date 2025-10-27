"""
News Manager
============

Handles news updates and announcements with YAML frontmatter.
"""

import os
import yaml
import markdown
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class NewsItem:
    def __init__(self, filepath: str, lang: str = 'en'):
        self.filepath = filepath
        self.lang = lang
        self.content = ""
        self.html_content = ""
        self.metadata = {}
        self._load_item()
    
    def _load_item(self):
        """Load and parse the news item file"""
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
        md = markdown.Markdown(extensions=['meta', 'fenced_code'])
        self.html_content = md.convert(self.content)
    
    @property
    def title(self) -> str:
        return self.metadata.get('title', 'News Update')
    
    @property
    def date(self) -> datetime:
        date_str = self.metadata.get('date', '')
        if date_str:
            return datetime.strptime(str(date_str), '%Y-%m-%d')
        return datetime.now()
    
    @property
    def category(self) -> str:
        return self.metadata.get('category', 'general')
    
    @property
    def summary(self) -> str:
        summary = self.metadata.get('summary', '')
        if not summary:
            # Extract first sentence
            sentences = self.content.split('. ')
            summary = sentences[0] + '.' if sentences else self.content[:100] + '...'
        return summary
    
    @property
    def importance(self) -> str:
        return self.metadata.get('importance', 'normal')  # high, normal, low
    
    @property
    def tags(self) -> List[str]:
        tags = self.metadata.get('tags', [])
        if isinstance(tags, str):
            return [tag.strip() for tag in tags.split(',')]
        return tags
    
    @property
    def slug(self) -> str:
        filename = Path(self.filepath).stem
        return self.metadata.get('slug', filename)
    
    @property
    def excerpt(self) -> str:
        """Get excerpt of the content for preview"""
        excerpt_length = 200
        if len(self.content) <= excerpt_length:
            return self.html_content
        
        # Find a good breaking point
        excerpt_text = self.content[:excerpt_length]
        last_sentence = excerpt_text.rfind('.')
        if last_sentence > excerpt_length * 0.5:  # If we have at least half the content
            excerpt_text = excerpt_text[:last_sentence + 1]
        else:
            last_space = excerpt_text.rfind(' ')
            if last_space > 0:
                excerpt_text = excerpt_text[:last_space] + '...'
        
        # Convert to HTML
        md = markdown.Markdown(extensions=['meta', 'fenced_code'])
        return md.convert(excerpt_text)

class NewsManager:
    def __init__(self, content_dir: str = 'content/news'):
        self.content_dir = content_dir
    
    def get_news_items(self, lang: str = 'en', limit: Optional[int] = None, 
                      category: Optional[str] = None) -> List[NewsItem]:
        """Get news items, sorted by date (newest first)"""
        items = []
        news_dir = Path(self.content_dir)
        
        if not news_dir.exists():
            return items
        
        # Look for markdown files
        for file_path in news_dir.glob('*.md'):
            try:
                item = NewsItem(str(file_path), lang)
                # Check if item is for this language
                item_lang = item.metadata.get('lang', 'en')
                if item_lang == lang:
                    # Filter by category if specified
                    if category is None or item.category == category:
                        items.append(item)
            except Exception as e:
                print(f"Error loading news item {file_path}: {e}")
        
        # Sort by date, newest first
        items.sort(key=lambda i: i.date, reverse=True)
        
        if limit:
            items = items[:limit]
        
        return items
    
    def get_news_item(self, slug: str, lang: str = 'en') -> Optional[NewsItem]:
        """Get specific news item by slug"""
        items = self.get_news_items(lang)
        for item in items:
            if item.slug == slug:
                return item
        return None
    
    def get_categories(self, lang: str = 'en') -> List[str]:
        """Get all unique categories"""
        categories = set()
        items = self.get_news_items(lang)
        for item in items:
            categories.add(item.category)
        return sorted(list(categories))
    
    def get_recent_items(self, lang: str = 'en', days: int = 30, limit: int = 5) -> List[NewsItem]:
        """Get recent news items"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        items = self.get_news_items(lang)
        recent_items = [item for item in items if item.date >= cutoff_date]
        
        return recent_items[:limit]