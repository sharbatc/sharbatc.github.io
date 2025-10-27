"""
Jupyter Notebook Manager
========================

Handles Jupyter notebook conversion and display using nbconvert.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from nbconvert import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor
import yaml

class NotebookManager:
    def __init__(self, content_dir: str = 'content/notebooks'):
        self.content_dir = content_dir
        # Use a very basic configuration to avoid MathBlockParser issues
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_name = 'classic'
        self.html_exporter.exclude_input_prompt = True
        self.html_exporter.exclude_output_prompt = True
        
        # Minimal configuration to avoid markdown parsing conflicts
        self.html_exporter.anchor_link_text = ''
    
    def get_notebooks(self, lang: str = 'en') -> List[Dict]:
        """Get all notebooks with metadata"""
        notebooks = []
        notebook_dir = Path(self.content_dir)
        
        if not notebook_dir.exists():
            return notebooks
        
        for file_path in notebook_dir.glob('*.ipynb'):
            try:
                notebook_info = self._get_notebook_info(file_path, lang)
                if notebook_info:
                    notebooks.append(notebook_info)
            except Exception as e:
                print(f"Error processing notebook {file_path}: {e}")
        
        # Sort by date or title
        notebooks.sort(key=lambda x: x.get('date', ''), reverse=True)
        return notebooks
    
    def _get_notebook_info(self, file_path: Path, lang: str) -> Optional[Dict]:
        """Extract metadata from notebook"""
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Get metadata from notebook
        metadata = notebook.get('metadata', {})
        custom_meta = metadata.get('custom', {})
        
        # Check if notebook is for this language
        notebook_lang = custom_meta.get('lang', 'en')
        if notebook_lang != lang:
            return None
        
        # Extract title from first markdown cell or filename
        title = custom_meta.get('title')
        if not title:
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    lines = source.split('\n')
                    for line in lines:
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
                    if title:
                        break
        
        if not title:
            title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
        
        return {
            'title': title,
            'filename': file_path.name,
            'slug': file_path.stem,
            'description': custom_meta.get('description', ''),
            'date': custom_meta.get('date', ''),
            'author': custom_meta.get('author', 'Sharbatanu Chatterjee'),
            'tags': custom_meta.get('tags', []),
            'category': custom_meta.get('category', 'analysis'),
            'lang': notebook_lang
        }
    
    def get_notebook(self, slug: str, lang: str = 'en') -> Optional[Dict]:
        """Get specific notebook by slug"""
        notebooks = self.get_notebooks(lang)
        for notebook in notebooks:
            if notebook['slug'] == slug:
                return notebook
        return None
    
    def convert_to_html(self, slug: str, lang: str = 'en') -> Optional[str]:
        """Convert notebook to HTML"""
        notebook_file = Path(self.content_dir) / f"{slug}.ipynb"
        
        if not notebook_file.exists():
            return None
        
        try:
            # Try the simplest possible conversion first
            try:
                # Create a fresh, minimal exporter for each conversion
                exporter = HTMLExporter()
                exporter.template_name = 'basic'
                exporter.exclude_input_prompt = True
                exporter.exclude_output_prompt = True
                
                # Disable any problematic features
                exporter.anchor_link_text = ''
                
                (body, resources) = exporter.from_filename(str(notebook_file))
                
            except Exception as e:
                print(f"Basic template failed: {e}")
                # Fallback: try without any template customization
                try:
                    fallback_exporter = HTMLExporter()
                    (body, resources) = fallback_exporter.from_filename(str(notebook_file))
                except Exception as e2:
                    print(f"Fallback conversion also failed: {e2}")
                    # Last resort: manual conversion
                    return self._manual_conversion(notebook_file)
            
            # Clean up the HTML (remove nbconvert boilerplate)
            body = self._clean_html(body)
            
            return body
        
        except Exception as e:
            print(f"Error converting notebook {slug}: {e}")
            # Return a fallback error message instead of None
            return f'''
            <div class="alert alert-warning">
                <h5>Notebook Conversion Error</h5>
                <p>Sorry, we encountered an issue converting this notebook for web display.</p>
                <p><strong>Error details:</strong> {str(e)}</p>
                <p>You can try downloading the notebook file directly or viewing it in a Jupyter environment.</p>
                <a href="/static/notebooks/{slug}.ipynb" class="btn btn-primary" download>
                    <i class="fas fa-download me-2"></i>Download Notebook
                </a>
            </div>
            '''
    
    def _clean_html(self, html: str) -> str:
        """Clean up nbconvert HTML output"""
        import re
        
        # Simple cleaning - just remove some problematic elements
        # Remove style tags that might conflict
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # Remove script tags for security
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        
        # Extract main content if possible, otherwise return as-is
        content_match = re.search(r'<div[^>]*class="[^"]*jp-Notebook[^"]*"[^>]*>(.*?)</div>\s*$', html, re.DOTALL)
        if content_match:
            return f'<div class="notebook-content">{content_match.group(1)}</div>'
        
        # Fallback: try to find any div with notebook content
        content_match = re.search(r'<div[^>]*class="[^"]*cell[^"]*"[^>]*>.*?</div>', html, re.DOTALL)
        if content_match:
            # Find all cell divs and wrap them
            cell_matches = re.findall(r'<div[^>]*class="[^"]*cell[^"]*"[^>]*>.*?</div>', html, re.DOTALL)
            return f'<div class="notebook-content">{"".join(cell_matches)}</div>'
        
        # Last resort: return simplified HTML
        return f'<div class="notebook-content">{html}</div>'
    
    def _manual_conversion(self, notebook_file: Path) -> str:
        """Manual notebook conversion as fallback when nbconvert fails"""
        try:
            with open(notebook_file, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            html = '<div class="notebook-content manual-conversion">'
            
            for cell in notebook.get('cells', []):
                cell_type = cell.get('cell_type', 'code')
                source = ''.join(cell.get('source', []))
                
                if cell_type == 'markdown':
                    # Simple markdown to HTML conversion
                    import markdown
                    md = markdown.Markdown(extensions=['fenced_code'])
                    html += f'<div class="cell markdown-cell">{md.convert(source)}</div>'
                    
                elif cell_type == 'code':
                    # Simple code cell display
                    html += f'''
                    <div class="cell code-cell">
                        <div class="input">
                            <pre><code class="language-python">{source}</code></pre>
                        </div>
                    '''
                    
                    # Add outputs if any
                    outputs = cell.get('outputs', [])
                    if outputs:
                        html += '<div class="output">'
                        for output in outputs:
                            if output.get('output_type') == 'stream':
                                text = ''.join(output.get('text', []))
                                html += f'<pre class="output-text">{text}</pre>'
                            elif output.get('output_type') == 'execute_result' or output.get('output_type') == 'display_data':
                                # Handle text output
                                data = output.get('data', {})
                                if 'text/plain' in data:
                                    text = ''.join(data['text/plain'])
                                    html += f'<pre class="output-result">{text}</pre>'
                        html += '</div>'
                    
                    html += '</div>'
            
            html += '</div>'
            return html
            
        except Exception as e:
            print(f"Manual conversion failed: {e}")
            return f'''
            <div class="alert alert-danger">
                <h5>Conversion Failed</h5>
                <p>Unable to display this notebook. Error: {str(e)}</p>
                <a href="/static/notebooks/{notebook_file.stem}.ipynb" class="btn btn-primary" download>
                    <i class="fas fa-download me-2"></i>Download Notebook
                </a>
            </div>
            '''
    
    def get_notebook_preview(self, slug: str, lang: str = 'en', cells: int = 3) -> Optional[str]:
        """Get preview of first few cells"""
        notebook_file = Path(self.content_dir) / f"{slug}.ipynb"
        
        if not notebook_file.exists():
            return None
        
        try:
            with open(notebook_file, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            preview_cells = []
            cell_count = 0
            
            for cell in notebook.get('cells', []):
                if cell_count >= cells:
                    break
                
                # Skip empty cells
                if not cell.get('source'):
                    continue
                
                preview_cells.append(cell)
                cell_count += 1
            
            # Create minimal notebook for preview
            preview_notebook = {
                'cells': preview_cells,
                'metadata': notebook.get('metadata', {}),
                'nbformat': notebook.get('nbformat', 4),
                'nbformat_minor': notebook.get('nbformat_minor', 2)
            }
            
            # Convert to HTML
            (body, resources) = self.html_exporter.from_notebook_node(preview_notebook)
            return self._clean_html(body)
        
        except Exception as e:
            print(f"Error creating preview for {slug}: {e}")
            return None