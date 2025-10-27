"""
Talks Manager
=============

Handles talk/presentation entries with metadata and content.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import markdown
from markdown.extensions import meta

class Talk:
    def __init__(self, filepath: str, lang: str = 'en'):
        self.filepath = filepath
        self.lang = lang
        self.metadata = {}
        self.content = ""
        self.html_content = ""
        
        self._load_content()
    
    def _load_content(self):
        """Load and parse the markdown file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Parse YAML frontmatter
                import yaml
                self.metadata = yaml.safe_load(parts[1]) or {}
                self.content = parts[2].strip()
            else:
                self.content = content
        else:
            self.content = content
        
        # Convert markdown to HTML (without frontmatter)
        md = markdown.Markdown(extensions=['fenced_code', 'tables'])
        self.html_content = md.convert(self.content)
    
    @property
    def title(self) -> str:
        return self.metadata.get('title', 'Untitled Talk')
    
    @property
    def date(self) -> datetime:
        date_str = self.metadata.get('date', '')
        if date_str:
            try:
                return datetime.strptime(str(date_str), '%Y-%m-%d')
            except:
                pass
        return datetime.now()
    
    @property
    def venue(self) -> str:
        return self.metadata.get('venue', '')
    
    @property
    def location(self) -> str:
        return self.metadata.get('location', '')
    
    @property
    def abstract(self) -> str:
        abstract = self.metadata.get('abstract', '')
        if not abstract:
            # Extract first paragraph as abstract
            first_para = self.content.split('\n\n')[0]
            abstract = first_para[:300] + '...' if len(first_para) > 300 else first_para
        return abstract
    
    @property
    def talk_type(self) -> str:
        return self.metadata.get('type', 'presentation')  # invited, contributed, poster, etc.
    
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
    def slides_url(self) -> str:
        return self.metadata.get('slides_url', '')
    
    @property
    def video_url(self) -> str:
        return self.metadata.get('video_url', '')

class TalksManager:
    def __init__(self, content_dir: str = 'content/talks'):
        self.content_dir = content_dir
        self._talks_cache = {}
    
    def get_talks(self, lang: str = 'en', limit: Optional[int] = None) -> List[Talk]:
        """Get all talks for a language, sorted by date (newest first)"""
        talks = []
        talks_dir = Path(self.content_dir)
        
        if not talks_dir.exists():
            return talks
        
        # Look for markdown files
        for file_path in talks_dir.glob('*.md'):
            try:
                talk = Talk(str(file_path), lang)
                # Check if talk is for this language
                talk_lang = talk.metadata.get('lang', 'en')
                # Strip quotes if present
                if isinstance(talk_lang, str):
                    talk_lang = talk_lang.strip('"\'')
                if talk_lang == lang:
                    talks.append(talk)
            except Exception as e:
                print(f"Error loading talk {file_path}: {e}")
        
        # Sort by date, newest first
        talks.sort(key=lambda t: t.date, reverse=True)
        
        if limit:
            talks = talks[:limit]
        
        return talks
    
    def get_talk(self, slug: str, lang: str = 'en') -> Optional[Talk]:
        """Get a specific talk by slug"""
        talks = self.get_talks(lang)
        for talk in talks:
            if talk.slug == slug:
                return talk
        return None
    
    def get_talks_by_type(self, talk_type: str, lang: str = 'en') -> List[Talk]:
        """Get talks filtered by type"""
        talks = self.get_talks(lang)
        return [talk for talk in talks if talk.talk_type == talk_type]
    
    def get_talks_by_tag(self, tag: str, lang: str = 'en') -> List[Talk]:
        """Get talks filtered by tag"""
        all_talks = self.get_talks(lang)
        return [talk for talk in all_talks if tag.lower() in [t.lower() for t in talk.tags]]
    
    def get_tags(self, lang: str = 'en') -> List[str]:
        """Get all unique tags from talks"""
        all_talks = self.get_talks(lang)
        tags = set()
        for talk in all_talks:
            tags.update(talk.tags)
        return sorted(list(tags))