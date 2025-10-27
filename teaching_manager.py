"""
Teaching Manager
================

Handles teaching entries with metadata and content.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import markdown
from markdown.extensions import meta

class TeachingItem:
    def __init__(self, filepath: str, lang: str = 'en'):
        self.filepath = filepath
        self.lang = lang
        self.metadata = {}
        self.content = ""
        self.html_content = ""
        
        self._parse_file()
    
    def _parse_file(self):
        """Parse markdown file with frontmatter"""
        try:
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
            
        except Exception as e:
            print(f"Error parsing {self.filepath}: {e}")
    
    @property
    def title(self) -> str:
        return self.metadata.get('title', 'Untitled Teaching')
    
    @property
    def date(self) -> datetime:
        date_str = self.metadata.get('date', '2024-01-01')
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return datetime.now()
        return date_str
    
    @property
    def semester(self) -> str:
        return self.metadata.get('semester', '')
    
    @property
    def institution(self) -> str:
        return self.metadata.get('institution', '')
    
    @property
    def course_code(self) -> str:
        return self.metadata.get('course_code', '')
    
    @property
    def role(self) -> str:
        return self.metadata.get('role', '')
    
    @property
    def students(self) -> str:
        return self.metadata.get('students', '')
    
    @property
    def description(self) -> str:
        return self.metadata.get('description', '')
    
    @property
    def materials_url(self) -> str:
        return self.metadata.get('materials_url', '')
    
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

class TeachingManager:
    def __init__(self, content_dir: str = 'content/teaching'):
        self.content_dir = content_dir
        self._teaching_cache = {}
    
    def get_teaching(self, lang: str = 'en', limit: Optional[int] = None) -> List[TeachingItem]:
        """Get all teaching items for a language, sorted by date (newest first)"""
        teaching = []
        teaching_dir = Path(self.content_dir)
        
        if not teaching_dir.exists():
            return teaching
        
        # Look for markdown files
        for file_path in teaching_dir.glob('*.md'):
            try:
                item = TeachingItem(str(file_path), lang)
                # Check if teaching item is for this language
                item_lang = item.metadata.get('lang', 'en')
                # Strip quotes if present
                if isinstance(item_lang, str):
                    item_lang = item_lang.strip('"\'')
                if item_lang == lang:
                    teaching.append(item)
            except Exception as e:
                print(f"Error loading teaching item {file_path}: {e}")
        
        # Sort by date, newest first
        teaching.sort(key=lambda t: t.date, reverse=True)
        
        if limit:
            teaching = teaching[:limit]
        
        return teaching
    
    def get_teaching_item(self, slug: str, lang: str = 'en') -> Optional[TeachingItem]:
        """Get a specific teaching item by slug"""
        teaching_items = self.get_teaching(lang)
        for item in teaching_items:
            if item.slug == slug:
                return item
        return None
    
    def get_teaching_by_tag(self, tag: str, lang: str = 'en') -> List[TeachingItem]:
        """Get teaching items filtered by tag"""
        all_teaching = self.get_teaching(lang)
        return [item for item in all_teaching if tag.lower() in [t.lower() for t in item.tags]]
    
    def get_tags(self, lang: str = 'en') -> List[str]:
        """Get all unique tags from teaching items"""
        all_teaching = self.get_teaching(lang)
        tags = set()
        for item in all_teaching:
            tags.update(item.tags)
        return sorted(list(tags))
        self._load_content()
    
    def _load_content(self):
        """Load and parse the markdown file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown with metadata
        md = markdown.Markdown(extensions=['meta'])
        self.html_content = md.convert(content)
        self.content = content
        
        # Extract metadata
        if hasattr(md, 'Meta'):
            for key, value in md.Meta.items():
                if key not in self.metadata:
                    self.metadata[key] = value[0] if isinstance(value, list) and len(value) == 1 else value
    
    @property
    def title(self) -> str:
        return self.metadata.get('title', 'Untitled Course')
    
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
    def semester(self) -> str:
        return self.metadata.get('semester', '')
    
    @property
    def institution(self) -> str:
        return self.metadata.get('institution', '')
    
    @property
    def course_code(self) -> str:
        return self.metadata.get('course_code', '')
    
    @property
    def description(self) -> str:
        description = self.metadata.get('description', '')
        if not description:
            # Extract first paragraph as description
            first_para = self.content.split('\n\n')[0]
            description = first_para[:300] + '...' if len(first_para) > 300 else first_para
        return description
    
    @property
    def role(self) -> str:
        return self.metadata.get('role', 'instructor')  # instructor, TA, guest lecturer, etc.
    
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
    def students(self) -> str:
        return self.metadata.get('students', '')
    
    @property
    def materials_url(self) -> str:
        return self.metadata.get('materials_url', '')

class TeachingManager:
    def __init__(self, content_dir: str = 'content/teaching'):
        self.content_dir = content_dir
        self._teaching_cache = {}
    
    def get_teaching_items(self, lang: str = 'en', limit: Optional[int] = None) -> List[TeachingItem]:
        """Get all teaching items for a language, sorted by date (newest first)"""
        items = []
        teaching_dir = Path(self.content_dir)
        
        if not teaching_dir.exists():
            return items
        
        # Look for markdown files
        for file_path in teaching_dir.glob('*.md'):
            try:
                item = TeachingItem(str(file_path), lang)
                # Check if item is for this language
                item_lang = item.metadata.get('lang', 'en')
                if item_lang == lang:
                    items.append(item)
            except Exception as e:
                print(f"Error loading teaching item {file_path}: {e}")
        
        # Sort by date, newest first
        items.sort(key=lambda i: i.date, reverse=True)
        
        if limit:
            items = items[:limit]
        
        return items
    
    def get_teaching_item(self, slug: str, lang: str = 'en') -> Optional[TeachingItem]:
        """Get a specific teaching item by slug"""
        items = self.get_teaching_items(lang)
        for item in items:
            if item.slug == slug:
                return item
        return None
    
    def get_teaching_by_role(self, role: str, lang: str = 'en') -> List[TeachingItem]:
        """Get teaching items filtered by role"""
        items = self.get_teaching_items(lang)
        return [item for item in items if item.role == role]
    
    def get_teaching_by_tag(self, tag: str, lang: str = 'en') -> List[TeachingItem]:
        """Get teaching items filtered by tag"""
        items = self.get_teaching_items(lang)
        return [item for item in items if tag.lower() in [t.lower() for t in item.tags]]