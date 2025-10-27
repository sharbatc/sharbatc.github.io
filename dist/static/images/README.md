# Images Directory Structure

This directory contains all static images for your academic website.

## Directory Organization

### `static/images/personal/`
**Purpose**: Personal photographs and profile images
**Examples**:
- `profile-photo.jpg` - Main profile photo for homepage
- `about-photo.jpg` - Additional photo for about section
- `cv-photo.jpg` - Professional headshot for CV
- `headshot-square.jpg` - Square format for social media
- `conference-photos/` - Photos from conferences and events

**Recommended formats**: JPG, PNG, WebP
**Recommended sizes**: 
- Profile photos: 400x400px (square) or 300x400px (portrait)
- Banner photos: 1200x400px

### `static/images/research/`
**Purpose**: Research-related images, figures, and diagrams
**Examples**:
- `project1-diagram.png` - Research project diagrams
- `results-graph.jpg` - Data visualization images
- `lab-equipment.jpg` - Laboratory photos
- `fieldwork/` - Field research photos
- `publications/` - Figures from publications

### `static/images/blog/`
**Purpose**: Images for blog posts and articles
**Examples**:
- `2024-01-15-post-image.jpg` - Blog post featured images
- `tutorials/` - Tutorial screenshots and diagrams
- `conferences/` - Conference photos and presentations

### `static/images/icons/`
**Purpose**: Website icons and small graphics (auto-created when needed)
**Examples**:
- `favicon.ico` - Website favicon
- `logo.png` - Website logo
- `social-icons/` - Social media icons

## Usage in Templates

### In HTML templates:
```html
<!-- Profile photo -->
<img src="{{ url_for('static', path='images/personal/profile-photo.jpg') }}" 
     alt="Your Name" 
     class="img-fluid rounded-circle">

<!-- Research image -->
<img src="{{ url_for('static', path='images/research/project1-diagram.png') }}" 
     alt="Research Project Diagram" 
     class="img-fluid">
```

### In Markdown blog posts:
```markdown
![Research Results](/static/images/research/results-graph.jpg)
![Profile Photo](/static/images/personal/profile-photo.jpg)
```

### In YAML content files:
```yaml
# In cv.yaml or similar
photo: "/static/images/personal/cv-photo.jpg"

# In publications.yaml
publications:
  - title: "My Research Paper"
    image: "/static/images/research/publication-figure.png"
```

## Image Optimization Tips

### File Formats
- **JPG**: Best for photographs with many colors
- **PNG**: Best for images with transparency or few colors
- **WebP**: Modern format, smaller file sizes (recommended when supported)
- **SVG**: Best for logos and simple graphics

### File Sizes
- Keep images under 500KB when possible
- Use compression tools like TinyPNG or ImageOptim
- Consider creating multiple sizes for responsive design

### Naming Convention
- Use lowercase letters and hyphens
- Be descriptive: `conference-presentation-2024.jpg`
- Include dates for time-sensitive content: `2024-01-15-workshop.jpg`
- Use consistent naming for profile photos: `profile-photo.jpg`

## Responsive Images

For better performance, consider creating multiple sizes:

```
static/images/personal/
├── profile-photo.jpg          (400x400px - default)
├── profile-photo-large.jpg    (800x800px - high DPI)
├── profile-photo-small.jpg    (200x200px - thumbnails)
└── profile-photo-banner.jpg   (1200x400px - hero section)
```

## Quick Start

1. **Add your profile photo**:
   ```bash
   cp your-photo.jpg static/images/personal/profile-photo.jpg
   ```

2. **Update templates to use your photo**:
   Edit `templates/index.html` and `templates/base.html`

3. **Test the image**:
   Visit: `http://localhost:8000/static/images/personal/profile-photo.jpg`

## Security Notes

- Never commit sensitive or private images to public repositories
- Consider image metadata (EXIF data) - strip personal information if needed
- Use appropriate file permissions for sensitive research images
- Consider using a CDN for better performance in production