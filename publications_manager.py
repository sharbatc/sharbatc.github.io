"""
Publications Manager
===================

Handles publication entries with metadata and content.
Similar to BlogManager but for academic publications.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import markdown
from markdown.extensions import meta

class Publication:
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
        return self.metadata.get('title', 'Untitled Publication')
    
    @property
    def date(self) -> datetime:
        date_str = self.metadata.get('date', '')
        if date_str:
            try:
                return datetime.strptime(str(date_str), '%Y-%m-%d')
            except:
                try:
                    return datetime.strptime(str(date_str), '%Y')
                except:
                    pass
        return datetime.now()
    
    @property
    def year(self) -> int:
        return self.date.year
    
    @property
    def authors(self) -> List[str]:
        authors = self.metadata.get('authors', 'Sharbatanu Chatterjee')
        if isinstance(authors, str):
            # Split by comma or semicolon and clean up
            return [author.strip() for author in authors.replace(';', ',').split(',')]
        return authors if isinstance(authors, list) else ['Sharbatanu Chatterjee']
    
    @property
    def journal(self) -> str:
        return self.metadata.get('journal', '')
    
    @property
    def venue(self) -> str:
        return self.metadata.get('venue', self.journal)
    
    @property
    def abstract(self) -> str:
        abstract = self.metadata.get('abstract', '')
        if not abstract:
            # Extract first paragraph as abstract
            first_para = self.content.split('\n\n')[0]
            abstract = first_para[:300] + '...' if len(first_para) > 300 else first_para
        return abstract
    
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
    def doi(self) -> str:
        return self.metadata.get('doi', '')
    
    @property
    def url(self) -> str:
        return self.metadata.get('url', '')
    
    @property
    def pdf_url(self) -> str:
        return self.metadata.get('pdf_url', '')
    
    @property
    def publication_type(self) -> str:
        return self.metadata.get('type', 'article')  # article, conference, book, etc.
    
    @property
    def citation(self) -> str:
        """Generate APA-style citation"""
        authors_str = ", ".join(self.authors) if self.authors else "Unknown"
        citation = f"{authors_str}. ({self.year}). {self.title}."
        
        if self.journal:
            citation += f" {self.journal}"
            if hasattr(self, 'volume') and self.metadata.get('volume'):
                citation += f", {self.metadata.get('volume')}"
            if hasattr(self, 'pages') and self.metadata.get('pages'):
                citation += f", {self.metadata.get('pages')}"
            citation += "."
        
        if self.doi:
            citation += f" https://doi.org/{self.doi}"
            
        return citation

class PublicationsManager:
    def __init__(self, content_dir: str = 'content/publications'):
        self.content_dir = content_dir
        self._publications_cache = {}
    
    def get_publications(self, lang: str = 'en', limit: Optional[int] = None) -> List[Publication]:
        """Get all publications for a language, sorted by date (newest first)"""
        publications = []
        pub_dir = Path(self.content_dir)
        
        if not pub_dir.exists():
            return publications
        
        # Look for markdown files
        for file_path in pub_dir.glob('*.md'):
            try:
                pub = Publication(str(file_path), lang)
                # Check if publication is for this language
                pub_lang = pub.metadata.get('lang', 'en')
                
                # Handle both string and list formats
                if isinstance(pub_lang, list):
                    # If it's a list, check if our language is in it
                    if lang in pub_lang:
                        publications.append(pub)
                elif isinstance(pub_lang, str):
                    # Strip quotes if present and compare
                    pub_lang = pub_lang.strip('"\'')
                    if pub_lang == lang:
                        publications.append(pub)
            except Exception as e:
                print(f"Error loading publication {file_path}: {e}")
        
        # Sort by date, newest first
        publications.sort(key=lambda p: p.date, reverse=True)
        
        if limit:
            publications = publications[:limit]
        
        return publications
    
    def get_publication(self, slug: str, lang: str = 'en') -> Optional[Publication]:
        """Get a specific publication by slug"""
        publications = self.get_publications(lang)
        for pub in publications:
            if pub.slug == slug:
                return pub
        return None
    
    def get_publications_by_year(self, lang: str = 'en') -> Dict[int, List[Publication]]:
        """Get publications grouped by year"""
        publications = self.get_publications(lang)
        by_year = {}
        for pub in publications:
            year = pub.year
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(pub)
        return by_year
    
    def get_publications_by_type(self, pub_type: str, lang: str = 'en') -> List[Publication]:
        """Get publications filtered by type"""
        publications = self.get_publications(lang)
        return [pub for pub in publications if pub.publication_type == pub_type]
    
    def get_publications_by_tag(self, tag: str, lang: str = 'en') -> List[Publication]:
        """Get publications filtered by tag"""
        all_publications = self.get_publications(lang)
        return [pub for pub in all_publications if tag.lower() in [t.lower() for t in pub.tags]]
    
    def get_tags(self, lang: str = 'en') -> List[str]:
        """Get all unique tags from publications"""
        all_publications = self.get_publications(lang)
        tags = set()
        for pub in all_publications:
            tags.update(pub.tags)
        return sorted(list(tags))