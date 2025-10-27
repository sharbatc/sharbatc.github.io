"""
Academic Website Generator
==========================

A modern Python-based academic website with multilingual support,
blog functionality, Jupyter notebook integration, and news updates.

Author: Sharbatanu Chatterjee
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import os
import yaml
from blog_manager import BlogManager
from notebook_manager import NotebookManager
from news_manager import NewsManager
from publications_manager import PublicationsManager
from talks_manager import TalksManager
from teaching_manager import TeachingManager

app = FastAPI(
    title="Sharbatanu Chatterjee - Academic Website",
    description="Personal academic website with multilingual support",
    version="2.0.0"
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Available languages
LANGUAGES = ["en", "fr", "bn"]
DEFAULT_LANGUAGE = "en"

def get_language_switch_url(current_path: str, current_lang: str, target_lang: str) -> str:
    """
    Generate URL for language switching.
    
    Args:
        current_path: Current URL path (e.g., '/en/talks')
        current_lang: Current language code (e.g., 'en')
        target_lang: Target language code (e.g., 'fr')
    
    Returns:
        New URL path (e.g., '/fr/talks')
    """
    # Remove the current language from the path
    if current_path.startswith(f"/{current_lang}/"):
        # Path like '/en/talks' -> '/talks'
        path_without_lang = current_path[len(f"/{current_lang}"):]
    elif current_path == f"/{current_lang}":
        # Path like '/en' -> ''
        path_without_lang = ""
    else:
        # Fallback for root or other paths
        path_without_lang = current_path
    
    # Build new URL with target language
    if path_without_lang and path_without_lang != "/":
        return f"/{target_lang}{path_without_lang}"
    else:
        return f"/{target_lang}/"

# Add the helper function to Jinja2 environment
templates.env.globals['get_language_switch_url'] = get_language_switch_url

# Load translations
def load_translations():
    translations = {}
    for lang in LANGUAGES:
        with open(f"locales/{lang}.yml", "r", encoding="utf-8") as f:
            translations.update(yaml.safe_load(f))
    return translations

translations = load_translations()

# Initialize managers
blog_manager = BlogManager()
notebook_manager = NotebookManager()
news_manager = NewsManager()
publications_manager = PublicationsManager()
talks_manager = TalksManager()
teaching_manager = TeachingManager()

@app.get("/", response_class=HTMLResponse)
@app.get("/{lang}/", response_class=HTMLResponse)
async def home(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Homepage with language support"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get recent content for homepage
    recent_posts = blog_manager.get_posts(lang, limit=3)
    recent_news = news_manager.get_news_items(lang, limit=3)  # Get latest 3 news items
    recent_notebooks = notebook_manager.get_notebooks(lang)[:2]
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "home",
            "translations": translations,
            "recent_posts": recent_posts,
            "recent_news": recent_news,
            "recent_notebooks": recent_notebooks
        }
    )

@app.get("/blog", response_class=HTMLResponse)
@app.get("/{lang}/blog", response_class=HTMLResponse)
async def blog(request: Request, lang: str = DEFAULT_LANGUAGE, tag: str = None):
    """Blog listing page with optional tag filtering"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get blog posts - filtered by tag if provided
    if tag:
        posts = blog_manager.get_posts_by_tag(tag, lang)
        selected_tag = tag
    else:
        posts = blog_manager.get_posts(lang, limit=10)
        selected_tag = None
    
    tags = blog_manager.get_tags(lang)
    
    return templates.TemplateResponse(
        "blog.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "blog",
            "translations": translations,
            "posts": posts,
            "tags": tags,
            "selected_tag": selected_tag
        }
    )

@app.get("/blog/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual blog post page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    post = blog_manager.get_post(slug, lang)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get related posts (same tags)
    related_posts = []
    if post.tags:
        for tag in post.tags[:2]:  # Use first 2 tags
            related = blog_manager.get_posts_by_tag(tag, lang)
            related_posts.extend([p for p in related if p.slug != slug])
        # Remove duplicates and limit
        seen = set()
        related_posts = [p for p in related_posts if p.slug not in seen and not seen.add(p.slug)][:3]
    
    return templates.TemplateResponse(
        "blog_post.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "blog",
            "translations": translations,
            "post": post,
            "related_posts": related_posts
        }
    )

# Publications routes
@app.get("/publications", response_class=HTMLResponse)
@app.get("/{lang}/publications", response_class=HTMLResponse)
async def publications(request: Request, lang: str = DEFAULT_LANGUAGE, tag: str = None):
    """Publications listing page with optional tag filtering"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get publications - filtered by tag if provided
    if tag:
        publications_list = publications_manager.get_publications_by_tag(tag, lang)
        selected_tag = tag
    else:
        publications_list = publications_manager.get_publications(lang)
        selected_tag = None
    
    tags = publications_manager.get_tags(lang)
    
    return templates.TemplateResponse(
        "publications.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "publications",
            "translations": translations,
            "publications": publications_list,
            "tags": tags,
            "selected_tag": selected_tag
        }
    )

@app.get("/publications/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/publications/{slug}", response_class=HTMLResponse)
async def publication_detail(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual publication detail page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    publication = publications_manager.get_publication(slug, lang)
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    # Get related publications (same tags)
    related_publications = []
    if publication.tags:
        for tag in publication.tags[:2]:  # Use first 2 tags
            related = publications_manager.get_publications_by_tag(tag, lang)
            related_publications.extend([p for p in related if p.slug != slug])
        # Remove duplicates and limit
        seen = set()
        related_publications = [p for p in related_publications if p.slug not in seen and not seen.add(p.slug)][:3]
    
    return templates.TemplateResponse(
        "publication_detail.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "publications",
            "translations": translations,
            "publication": publication,
            "related_publications": related_publications
        }
    )

# Talks routes
@app.get("/talks", response_class=HTMLResponse)
@app.get("/{lang}/talks", response_class=HTMLResponse)
async def talks(request: Request, lang: str = DEFAULT_LANGUAGE, tag: str = None):
    """Talks listing page with optional tag filtering"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get talks - filtered by tag if provided
    if tag:
        talks_list = talks_manager.get_talks_by_tag(tag, lang)
        selected_tag = tag
    else:
        talks_list = talks_manager.get_talks(lang)
        selected_tag = None
    
    tags = talks_manager.get_tags(lang)
    
    return templates.TemplateResponse(
        "talks.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "talks",
            "translations": translations,
            "talks": talks_list,
            "tags": tags,
            "selected_tag": selected_tag
        }
    )

@app.get("/talks/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/talks/{slug}", response_class=HTMLResponse)
async def talk_detail(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual talk detail page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    talk = talks_manager.get_talk(slug, lang)
    if not talk:
        raise HTTPException(status_code=404, detail="Talk not found")
    
    # Get related talks (same tags)
    related_talks = []
    if talk.tags:
        for tag in talk.tags[:2]:  # Use first 2 tags
            related = talks_manager.get_talks_by_tag(tag, lang)
            related_talks.extend([t for t in related if t.slug != slug])
        # Remove duplicates and limit
        seen = set()
        related_talks = [t for t in related_talks if t.slug not in seen and not seen.add(t.slug)][:3]
    
    return templates.TemplateResponse(
        "talk_detail.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "talks",
            "translations": translations,
            "talk": talk,
            "related_talks": related_talks
        }
    )

# Teaching routes
@app.get("/teaching", response_class=HTMLResponse)
@app.get("/{lang}/teaching", response_class=HTMLResponse)
async def teaching(request: Request, lang: str = DEFAULT_LANGUAGE, tag: str = None):
    """Teaching listing page with optional tag filtering"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get teaching items - filtered by tag if provided
    if tag:
        teaching_list = []  # Temporarily disable tag filtering
        selected_tag = tag
    else:
        teaching_list = teaching_manager.get_teaching_items(lang)
        selected_tag = None
    
    tags = []  # Temporarily disable tags until we fix the teaching manager
    
    return templates.TemplateResponse(
        "teaching.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "teaching",
            "translations": translations,
            "teaching": teaching_list,
            "tags": tags,
            "selected_tag": selected_tag
        }
    )

@app.get("/teaching/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/teaching/{slug}", response_class=HTMLResponse)
async def teaching_detail(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual teaching item detail page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    teaching_item = teaching_manager.get_teaching_item(slug, lang)
    if not teaching_item:
        raise HTTPException(status_code=404, detail="Teaching item not found")
    
    # Get related teaching items (same tags)
    related_teaching = []
    if teaching_item.tags:
        for tag in teaching_item.tags[:2]:  # Use first 2 tags
            related = teaching_manager.get_teaching_by_tag(tag, lang)
            related_teaching.extend([t for t in related if t.slug != slug])
        # Remove duplicates and limit
        seen = set()
        related_teaching = [t for t in related_teaching if t.slug not in seen and not seen.add(t.slug)][:3]
    
    return templates.TemplateResponse(
        "teaching_detail.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "teaching",
            "translations": translations,
            "teaching_item": teaching_item,
            "related_teaching": related_teaching
        }
    )

@app.get("/notebooks", response_class=HTMLResponse)
@app.get("/{lang}/notebooks", response_class=HTMLResponse)
async def notebooks(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Jupyter notebooks page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get notebooks
    notebooks_list = notebook_manager.get_notebooks(lang)
    
    return templates.TemplateResponse(
        "notebooks.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "notebooks",
            "translations": translations,
            "notebooks": notebooks_list
        }
    )

@app.get("/notebooks/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/notebooks/{slug}", response_class=HTMLResponse)
async def notebook_view(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual notebook view"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get notebook info
    notebook_info = notebook_manager.get_notebook(slug, lang)
    if not notebook_info:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    # Convert to HTML
    notebook_html = notebook_manager.convert_to_html(slug, lang)
    if not notebook_html:
        raise HTTPException(status_code=500, detail="Failed to convert notebook")
    
    # Check if it's an error message (fallback)
    if "Notebook Conversion Error" in notebook_html:
        # Still show the page but with error content
        pass
    
    return templates.TemplateResponse(
        "notebook_view.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "notebooks",
            "translations": translations,
            "notebook": notebook_info,
            "notebook_html": notebook_html
        }
    )

@app.get("/news", response_class=HTMLResponse)
@app.get("/{lang}/news", response_class=HTMLResponse)
async def news(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Latest news and updates page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # Get news items
    news_items = news_manager.get_news_items(lang, limit=20)
    categories = news_manager.get_categories(lang)
    
    return templates.TemplateResponse(
        "news.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "news",
            "translations": translations,
            "news_items": news_items,
            "categories": categories
        }
    )

@app.get("/news/{slug}", response_class=HTMLResponse)
@app.get("/{lang}/news/{slug}", response_class=HTMLResponse)
async def news_item(request: Request, slug: str, lang: str = DEFAULT_LANGUAGE):
    """Individual news item page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    news_item = news_manager.get_news_item(slug, lang)
    if not news_item:
        raise HTTPException(status_code=404, detail="News item not found")
    
    # Get additional data for sidebar
    recent_news = news_manager.get_news_items(lang, limit=10)
    categories = news_manager.get_categories(lang)
    
    return templates.TemplateResponse(
        "news_item.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "news",
            "translations": translations,
            "news_item": news_item,
            "recent_news": recent_news,
            "categories": categories
        }
    )

@app.get("/publications", response_class=HTMLResponse)
@app.get("/{lang}/publications", response_class=HTMLResponse)
async def publications(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Publications page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    return templates.TemplateResponse(
        "publications.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "publications",
            "translations": translations
        }
    )

@app.get("/talks", response_class=HTMLResponse)
@app.get("/{lang}/talks", response_class=HTMLResponse)
async def talks(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Talks and presentations page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    return templates.TemplateResponse(
        "talks.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "talks",
            "translations": translations
        }
    )

@app.get("/teaching", response_class=HTMLResponse)
@app.get("/{lang}/teaching", response_class=HTMLResponse)
async def teaching(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Teaching page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    return templates.TemplateResponse(
        "teaching.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "teaching",
            "translations": translations
        }
    )

@app.get("/cv", response_class=HTMLResponse)
@app.get("/{lang}/cv", response_class=HTMLResponse)
async def cv(request: Request, lang: str = DEFAULT_LANGUAGE):
    """CV/Resume page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    return templates.TemplateResponse(
        "cv.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "cv",
            "translations": translations
        }
    )

@app.get("/contact", response_class=HTMLResponse)
@app.get("/{lang}/contact", response_class=HTMLResponse)
async def contact(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Contact page"""
    if lang not in LANGUAGES:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    return templates.TemplateResponse(
        "contact.html", 
        {
            "request": request, 
            "lang": lang, 
            "available_languages": LANGUAGES,
            "page": "contact",
            "translations": translations
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)