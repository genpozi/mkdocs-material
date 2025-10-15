# MkDocs Material - Complete Setup Guide

This repository contains a fully configured MkDocs Material installation with popular plugins and enhancements.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/genpozi/mkdocs-material.git
   cd mkdocs-material
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node dependencies:**
   ```bash
   npm install
   ```

4. **Build the theme:**
   ```bash
   npm run build
   ```

5. **Serve the documentation:**
   ```bash
   mkdocs serve
   ```

   The site will be available at `http://localhost:8000/mkdocs-material/`

## 📦 Installed Plugins

### Core Material Plugins
- ✅ **search** - Advanced client-side search with multi-language support
- ✅ **minify** - HTML/CSS/JS minification for production

### Git Integration
- ✅ **git-revision-date-localized** (v1.4.7)
  - Shows "Last updated" timestamps on pages
  - Supports multiple date formats and localization
  - Configuration: `type: timeago` for relative dates

### Content Enhancement
- ✅ **glightbox** (v0.5.1)
  - Beautiful image lightbox with zoom and touch navigation
  - Automatic image gallery creation
  - Responsive and mobile-friendly

- ✅ **macros** (v1.4.0)
  - Use Jinja2 variables in Markdown
  - Create custom macros and filters
  - Dynamic content generation

### Navigation
- ✅ **section-index** (v0.3.10)
  - Allows sections to have index pages
  - Better navigation structure

### Imaging Support
- ✅ **Pillow** (v11.3.0) - Image processing for social cards
- ✅ **CairoSVG** (v2.8.2) - SVG rendering for social cards

### Additional Plugins (Installed but not enabled)
These plugins are installed and ready to use when needed:

- **mkdocs-rss-plugin** (v1.17.4) - RSS feed generation
- **mkdocs-git-committers-plugin-2** (v2.5.0) - Show page contributors
- **mkdocs-awesome-pages-plugin** (v2.10.1) - Simplified navigation with `.pages` files
- **mkdocs-redirects** (v1.2.2) - URL redirects

## 🛠️ Development Workflow

### Building the Theme

The theme uses a custom TypeScript-based build system:

```bash
# Full production build
npm run build

# Build with all features
npm run build:all

# Development build with watch mode
npm run start

# Incremental build (faster)
npm run build:dirty
```

### Code Quality

```bash
# Run all checks
npm run check

# Type checking
npm run check:build

# Lint styles
npm run check:style

# Auto-fix issues
npm run fix
```

### Serving Documentation

```bash
# Development server with live reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 📁 Project Structure

```
mkdocs-material/
├── src/                          # Source code
│   ├── plugins/                  # Python MkDocs plugins
│   │   ├── blog/                 # Blog functionality
│   │   ├── search/               # Search plugin
│   │   ├── social/               # Social cards
│   │   ├── tags/                 # Tagging system
│   │   ├── privacy/              # Privacy features
│   │   ├── offline/              # Offline support
│   │   ├── meta/                 # Meta plugin
│   │   ├── group/                # Group plugin
│   │   └── info/                 # Info plugin
│   ├── templates/                # Jinja2 templates
│   │   ├── assets/
│   │   │   ├── javascripts/      # TypeScript source
│   │   │   └── stylesheets/      # SCSS source
│   │   ├── partials/             # Template partials
│   │   └── *.html                # Page templates
│   ├── extensions/               # Markdown extensions
│   └── utilities/                # Utility modules
├── material/                     # Built output (generated)
├── docs/                         # Documentation content
├── tools/                        # Build system
├── package.json                  # Node dependencies
├── pyproject.toml                # Python package config
├── requirements.txt              # Python dependencies
├── tsconfig.json                 # TypeScript config
└── mkdocs.yml                    # MkDocs configuration
```

## ⚙️ Configuration

### Plugin Configuration (mkdocs.yml)

```yaml
plugins:
  - search:
      separator: '[\s\u200b\-_,:!=\[\]()"`/]+|\.(?!\d)|&[lg]t;|(?!\b)(?=[A-Z][a-z])'
  - minify:
      minify_html: true
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
  - section-index
  - glightbox:
      touchNavigation: true
      loop: false
      effect: zoom
      slide_effect: slide
      width: 100%
      height: auto
      zoomable: true
      draggable: true
      auto_caption: false
      caption_position: bottom
  - macros
```

### Enabling Additional Plugins

To enable blog functionality, uncomment in `mkdocs.yml`:
```yaml
plugins:
  - blog  # Add this at the top of plugins list
```

To enable RSS feeds:
```yaml
plugins:
  - rss:
      match_path: blog/posts/.* 
      date_from_meta:
        as_creation: date
      categories:
        - categories
        - tags
```

To enable git committers:
```yaml
plugins:
  - git-committers:
      repository: your-username/your-repo
      branch: main
```

## 🎨 Customization

### Theme Colors
Edit `mkdocs.yml`:
```yaml
theme:
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
```

### Fonts
```yaml
theme:
  font:
    text: Roboto
    code: Roboto Mono
```

### Logo and Favicon
```yaml
theme:
  logo: assets/logo.png
  favicon: assets/favicon.png
```

## 🔧 Troubleshooting

### Build Issues

**Problem:** `material/` directory not found
```bash
# Solution: Build the theme first
npm run build
```

**Problem:** TypeScript errors
```bash
# Solution: Check TypeScript configuration
npm run check:build
```

### Plugin Issues

**Problem:** Git revision dates not showing
```bash
# Solution: Ensure you're in a git repository with commit history
git log
```

**Problem:** Images not opening in lightbox
```bash
# Solution: Ensure glightbox plugin is enabled and images use proper markdown syntax
![Alt text](image.png)
```

## 📚 Resources

- [MkDocs Material Documentation](https://squidfunk.github.io/mkdocs-material/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Plugin Documentation](https://squidfunk.github.io/mkdocs-material/plugins/)

## 🤝 Contributing

This is a fork of the official MkDocs Material theme. For contributions to the core theme, please visit:
- [squidfunk/mkdocs-material](https://github.com/squidfunk/mkdocs-material)

## 📄 License

**MIT License**

Copyright (c) 2016-2025 Martin Donath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

## 🎯 What's Next?

1. **Customize your documentation** - Edit files in `docs/`
2. **Add your content** - Create new Markdown files
3. **Configure plugins** - Enable/disable features in `mkdocs.yml`
4. **Deploy** - Use `mkdocs gh-deploy` for GitHub Pages
5. **Explore features** - Check out the [reference documentation](https://squidfunk.github.io/mkdocs-material/reference/)

---

**Version:** 9.6.21  
**Last Updated:** 2025-10-15
