# Sharbatanu Chatterjee - Personal Website

A modern, multilingual academic website built with FastAPI and deployed as a static site to GitHub Pages.

## 🌟 Features

- **Multilingual Support**: English, French, and Bengali
- **Academic Blog**: Markdown-based blog posts with syntax highlighting
- **Jupyter Notebooks**: Interactive notebook display with nbconvert
- **News Updates**: Timeline-based news and announcements
- **Responsive Design**: Mobile-friendly Bootstrap-based templates
- **Academic Focus**: Publications, talks, teaching, and CV pages
- **Static Deployment**: Automatically deployed to GitHub Pages
- **Dark/Light Theme**: Toggle between themes with persistent storage

## � System Requirements

### Python Version
- **Required**: Python 3.9 or higher
- **Recommended**: Python 3.9.20 (latest patch version)
- **Supported**: Python 3.9, 3.10, 3.11, 3.12

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

If you need to install or upgrade Python:
- **macOS**: Use Homebrew: `brew install python@3.9` or download from [python.org](https://www.python.org/downloads/)
- **Linux**: Use your package manager: `sudo apt install python3.9` (Ubuntu/Debian)
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

## �🚀 Quick Start

### Method 1: Automated Setup (Recommended)

1. **Check Python compatibility**:
   ```bash
   python check_python.py
   ```

2. **Run setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the website**:
   ```bash
   ./start_website.sh
   ```

### Method 2: Manual Setup

1. **Activate the conda environment**:
   ```bash
   conda activate academic-website
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the development server**:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

4. **Visit**: http://localhost:8000

### Static Site Generation

To generate a static version of the site:

```bash
conda activate academic-website
python generate_static_site.py
```

This creates a `dist/` folder with static HTML files that can be deployed anywhere.

## 📁 Project Structure

```
├── main.py                    # FastAPI application
├── generate_static_site.py    # Static site generator for GitHub Pages
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment configuration
├── content/                   # Markdown content files
│   ├── blog/                  # Blog posts
│   ├── notebooks/             # Jupyter notebooks
│   ├── publications.yaml      # Publications data
│   ├── talks.yaml            # Talks data
│   ├── teaching.yaml         # Teaching data
│   ├── cv.yaml               # CV data
│   └── news.yaml             # News updates
├── templates/                 # Jinja2 HTML templates
├── static/                    # CSS, JS, images
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Image assets
├── locales/                   # Translation files
├── *_manager.py              # Content management modules
├── .github/workflows/        # GitHub Actions for auto-deployment
└── backup_jekyll_site/       # Backup of original Jekyll site
```

## �️ Content Management

### Adding Blog Posts

1. **Create a new Markdown file** in `content/blog/` directory
2. **Use this format:**
   ```markdown
   ---
   title: "Your Post Title"
   date: "2024-01-15"
   author: "Your Name"
   tags: ["research", "science"]
   language: "en"  # or "fr", "bn"
   summary: "Brief description of your post"
   ---

   Your blog content here using Markdown...
   ```

3. **Blog posts are automatically detected** when you restart the server

### Adding Jupyter Notebooks

1. **Place notebook files** (`.ipynb`) in `content/notebooks/` directory
2. **The system automatically converts** them to HTML for web display
3. **Access them** via the "Notebooks" section of your website

### Managing News Updates

1. **Edit** `content/news.yaml`
2. **Add new entries** in this format:
   ```yaml
   - date: "2024-01-15"
     title:
       en: "News title in English"
       fr: "Titre en français"
       bn: "বাংলায় শিরোনাম"
     description:
       en: "Description in English"
       fr: "Description en français"
       bn: "বাংলায় বিবরণ"
     type: "research"  # or "publication", "award", "event"
   ```

### Updating Academic Pages

#### Publications
- Edit `content/publications.yaml`
- Add new publications with title, authors, venue, year, etc.

#### Talks
- Edit `content/talks.yaml`
- Include talk title, event, date, location

#### Teaching
- Edit `content/teaching.yaml`
- Add courses, institutions, terms

#### CV
- Edit `content/cv.yaml`
- Update education, experience, skills, etc.

### Adding Personal Photos

#### Step 1: Add Your Profile Photo
```bash
# Copy your main profile photo to the correct location
cp /path/to/your/photo.jpg static/images/personal/profile-photo.jpg

# Make sure it's optimized (under 500KB, 400x400px recommended)
```

#### Step 2: Test Your Photo
1. **Start the website**: `python run_dev.py`
2. **Visit**: http://localhost:8000
3. **Check direct access**: http://localhost:8000/static/images/personal/profile-photo.jpg

#### Common Image Types
- **profile-photo.jpg** - Main profile image (homepage, navbar)
- **cv-photo.jpg** - Professional headshot for CV page
- **about-photo.jpg** - More casual photo for about section

## 🎨 Design & Aesthetics

### Font System
The website uses optimized fonts for each language:

**English & French:**
- Primary: `Inter` (modern, clean sans-serif from Google Fonts)
- Fallback: `Segoe UI`, `Source Sans Pro`, sans-serif

**Bengali:**
- Primary: `Noto Sans Bengali` (Google's comprehensive Bengali font)
- Fallback: `Inter`, `Segoe UI`, sans-serif

### Theme System
- **Light/Dark toggle**: Click the theme switcher (🌙/☀️) next to the language selector
- **Persistent storage**: Your theme choice is saved in browser storage
- **Smart cards**: Content cards maintain white backgrounds for optimal readability

### Language Switcher
The language switcher correctly handles URL transitions:
- From `/en/talks` → clicking French goes to `/fr/talks`
- Maintains current page context across language switches
- Supports all three languages seamlessly

## 🔄 Automatic Deployment

This site automatically deploys to GitHub Pages when you push to the `master` branch:

1. GitHub Actions activates the conda environment
2. Runs the static site generator
3. Generates HTML files from your FastAPI app
4. Deploys to GitHub Pages
5. Site is available at: https://sharbatc.github.io

## 🌐 Languages

The site supports three languages:
- English (`/en/`)
- French (`/fr/`)
- Bengali (`/bn/`)

Language switching is automatic based on browser preferences, with manual override available.

## ⚙️ Environment Setup

The project uses a conda environment named `academic-website`. Always activate it before development:

```bash
conda activate academic-website
```

### Alternative Installation Methods

#### Using environment.yml
```bash
# Create environment from environment.yml
conda env create -f environment.yml
conda activate academic-website
```

#### Using pip (if conda not available)
```bash
# Create virtual environment
python -m venv academic-website
source academic-website/bin/activate  # On Windows: academic-website\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Troubleshooting

### Common Issues

1. **Server won't start**: Make sure conda environment is activated
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Font rendering issues**: Clear browser cache
4. **Language switcher not working**: Check URL patterns in browser developer tools

### Development Commands

```bash
# Check Python compatibility
python check_python.py

# Start development server with auto-reload
python -m uvicorn main:app --reload --port 8000

# Generate static site for deployment
python generate_static_site.py

# Test specific language
curl http://localhost:8000/en/
curl http://localhost:8000/fr/
curl http://localhost:8000/bn/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
