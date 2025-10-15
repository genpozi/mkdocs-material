# Installed Plugins Reference

Complete reference for all installed MkDocs Material plugins and their usage.

## 🔍 Search Plugin

**Status:** ✅ Enabled  
**Version:** Built-in

### Features
- Client-side search with instant results
- Multi-language support (60+ languages)
- Fuzzy matching and stemming
- Search highlighting
- Keyboard shortcuts

### Configuration
```yaml
plugins:
  - search:
      separator: '[\s\u200b\-_,:!=\[\]()"`/]+|\.(?!\d)|&[lg]t;|(?!\b)(?=[A-Z][a-z])'
```

### Usage
- Press `/` or `s` to focus search
- Type to search across all documentation
- Use arrow keys to navigate results
- Press `Enter` to visit page

---

## 🗜️ Minify Plugin

**Status:** ✅ Enabled  
**Version:** v0.8.0

### Features
- HTML minification
- CSS minification
- JavaScript minification
- Reduces page size by ~30%

### Configuration
```yaml
plugins:
  - minify:
      minify_html: true
```

---

## 📅 Git Revision Date Localized

**Status:** ✅ Enabled  
**Version:** v1.4.7

### Features
- Shows last update date on pages
- Multiple date formats (date, datetime, iso_date, timeago)
- Localization support
- Creation date tracking

### Configuration
```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
```

### Date Format Options
- `date` - November 28, 2022
- `datetime` - November 28, 2022 13:57:28
- `iso_date` - 2022-11-28
- `iso_datetime` - 2022-11-28 13:57:26
- `timeago` - 2 days ago

### Usage in Templates
```jinja2
{{ page.meta.git_revision_date_localized }}
{{ page.meta.git_creation_date_localized }}
```

---

## 🖼️ GLightbox

**Status:** ✅ Enabled  
**Version:** v0.5.1

### Features
- Beautiful image lightbox
- Touch navigation support
- Zoom functionality
- Keyboard navigation
- Image galleries
- Video support

### Configuration
```yaml
plugins:
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
```

### Usage

**Basic image:**
```markdown
![Image title](path/to/image.png)
```

**Image with caption:**
```markdown
![Image title](path/to/image.png "This is a caption")
```

**Disable lightbox for specific image:**
```markdown
![Image title](path/to/image.png){ .skip-lightbox }
```

**Image gallery:**
```markdown
![Image 1](image1.png)
![Image 2](image2.png)
![Image 3](image3.png)
```

### Keyboard Shortcuts
- `←` / `→` - Navigate between images
- `Esc` - Close lightbox
- `+` / `-` - Zoom in/out

---

## 🔧 Macros Plugin

**Status:** ✅ Enabled  
**Version:** v1.4.0

### Features
- Use Jinja2 variables in Markdown
- Create custom macros
- Define custom filters
- Access config variables
- Dynamic content generation

### Configuration
```yaml
plugins:
  - macros
```

### Built-in Variables

**Config access:**
```markdown
Site name: {{ config.site_name }}
Site URL: {{ config.site_url }}
```

**Date/time:**
```markdown
Current date: {{ now() }}
```

**Page metadata:**
```markdown
Page title: {{ page.title }}
Page URL: {{ page.url }}
```

### Custom Macros

Create `main.py` in your docs root:

```python
def define_env(env):
    """Define custom macros"""
    
    @env.macro
    def button(text, url):
        return f'[{text}]({url}){{ .md-button }}'
    
    @env.filter
    def uppercase(text):
        return text.upper()
```

**Usage:**
```markdown
{{ button("Click me", "/path/") }}
{{ "hello" | uppercase }}
```

### Variables in Front Matter
```yaml
---
title: My Page
version: 1.0.0
---

Version: {{ page.meta.version }}
```

---

## 📑 Section Index

**Status:** ✅ Enabled  
**Version:** v0.3.10

### Features
- Sections can have index pages
- Better navigation structure
- Automatic section landing pages

### Configuration
```yaml
plugins:
  - section-index
```

### Usage

**Directory structure:**
```
docs/
├── section/
│   ├── index.md      # Section index page
│   ├── page1.md
│   └── page2.md
```

**Navigation:**
```yaml
nav:
  - Section: section/index.md
    - Page 1: section/page1.md
    - Page 2: section/page2.md
```

Or simplified:
```yaml
nav:
  - Section: section/
```

---

## 📰 RSS Plugin

**Status:** ⚠️ Installed (not enabled)  
**Version:** v1.17.4

### Features
- Generate RSS feeds
- Blog post feeds
- Custom feed configuration
- Category/tag support

### Enable
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

### Usage
Add metadata to blog posts:
```yaml
---
date: 2024-01-15
categories:
  - News
  - Updates
tags:
  - release
  - features
---
```

---

## 👥 Git Committers

**Status:** ⚠️ Installed (not enabled)  
**Version:** v2.5.0

### Features
- Show page contributors
- GitHub integration
- Contributor avatars
- Commit statistics

### Enable
```yaml
plugins:
  - git-committers:
      repository: username/repository
      branch: main
```

### Requirements
- GitHub personal access token
- Set `MKDOCS_GIT_COMMITTERS_APIKEY` environment variable

### Usage in Templates
```jinja2
{% for author in committers %}
  {{ author.name }} ({{ author.contribution }}%)
{% endfor %}
```

---

## 📄 Awesome Pages

**Status:** ⚠️ Installed (not enabled)  
**Version:** v2.10.1

### Features
- Simplified navigation configuration
- `.pages` files for structure
- Automatic page ordering
- Hide pages from navigation

### Enable
```yaml
plugins:
  - awesome-pages
```

### Usage

Create `.pages` file in directory:
```yaml
title: Section Title
nav:
  - index.md
  - page1.md
  - page2.md
  - ...
```

**Automatic ordering:**
```yaml
nav:
  - ... | *.md
```

**Hide pages:**
```yaml
hide: true
```

**Custom order:**
```yaml
order: asc  # or desc
order_by: title  # or filename
```

---

## 🔀 Redirects

**Status:** ⚠️ Installed (not enabled)  
**Version:** v1.2.2

### Features
- URL redirects
- Maintain old URLs
- SEO-friendly redirects

### Enable
```yaml
plugins:
  - redirects:
      redirect_maps:
        'old-page.md': 'new-page.md'
        'old-section/page.md': 'new-section/page.md'
```

---

## 🎨 Social Cards (Imaging)

**Status:** ✅ Dependencies installed  
**Pillow:** v11.3.0  
**CairoSVG:** v2.8.2

### Features
- Automatic social card generation
- Custom layouts
- Brand colors
- Logo integration

### Enable
```yaml
plugins:
  - social:
      cards: true
      cards_layout_options:
        background_color: "#4051b5"
        color: "#ffffff"
```

### Requirements
- Pillow (installed)
- CairoSVG (installed)

### Custom Cards
Override in page metadata:
```yaml
---
social:
  cards_layout_options:
    title: Custom Title
    description: Custom description
---
```

---

## 🔧 Plugin Combinations

### Blog Setup
```yaml
plugins:
  - blog
  - rss:
      match_path: blog/posts/.*
  - git-revision-date-localized
  - social
```

### Documentation Site
```yaml
plugins:
  - search
  - git-revision-date-localized
  - git-committers
  - section-index
  - glightbox
  - macros
```

### Minimal Setup
```yaml
plugins:
  - search
  - minify
```

---

## 📊 Performance Impact

| Plugin | Build Time Impact | Page Size Impact |
|--------|------------------|------------------|
| search | Low | +50KB |
| minify | Medium | -30% |
| git-revision-date | Low | Minimal |
| glightbox | Low | +20KB |
| macros | Low-Medium | Varies |
| social | High | Minimal |
| git-committers | Medium | Minimal |

---

## 🐛 Troubleshooting

### Plugin Not Working

1. Check plugin is enabled in `mkdocs.yml`
2. Verify plugin is installed: `pip list | grep mkdocs`
3. Check for error messages: `mkdocs build --verbose`

### Build Errors

**Git plugins:**
- Ensure you're in a git repository
- Check git history exists: `git log`

**Social cards:**
- Verify Pillow and CairoSVG are installed
- Check font files are available

**Macros:**
- Check `main.py` syntax
- Verify macro names don't conflict

### Performance Issues

- Disable unused plugins
- Use `mkdocs build --dirty` for incremental builds
- Consider caching for git plugins

---

## 📚 Additional Resources

- [MkDocs Material Plugins](https://squidfunk.github.io/mkdocs-material/plugins/)
- [Plugin Development](https://www.mkdocs.org/dev-guide/plugins/)
- [Community Plugins](https://github.com/mkdocs/catalog)

---

**Last Updated:** 2025-10-15
