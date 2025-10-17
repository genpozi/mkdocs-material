# Content Enhancement Examples

This document demonstrates the content enhancement features of MkDocs AI Assistant.

## Overview

The enhancement system improves documentation quality through:
- Grammar and spelling corrections
- Clarity improvements
- Terminology consistency
- Readability optimization

## CLI Usage

### Basic Enhancement

Enhance a single file:

```bash
mkdocs-ai enhance docs/guide.md
```

### Enhancement Levels

**Light** - Grammar and spelling only:
```bash
mkdocs-ai enhance docs/guide.md --level light
```

**Moderate** - Grammar, spelling, and clarity (default):
```bash
mkdocs-ai enhance docs/guide.md --level moderate
```

**Aggressive** - Full enhancement including rewrites:
```bash
mkdocs-ai enhance docs/guide.md --level aggressive
```

### Preview Changes

Preview enhancements without applying:
```bash
mkdocs-ai enhance docs/guide.md --preview
```

### Save to Different File

```bash
mkdocs-ai enhance docs/guide.md -o docs/guide-enhanced.md
```

### Check Quality

Analyze documentation quality:
```bash
mkdocs-ai check-quality docs/guide.md
```

## Plugin Integration

Enable automatic enhancement during build:

```yaml
plugins:
  - ai-assistant:
      enhancement:
        enabled: true
        level: moderate
        preserve_code: true
        preserve_frontmatter: true
```

## Programmatic Usage

### Basic Enhancement

```python
from pathlib import Path
from mkdocs_ai.enhancement import EnhancementProcessor
from mkdocs_ai.providers import create_provider
from mkdocs_ai.cache import CacheManager

# Create provider
provider = create_provider("openrouter", api_key="your-key")

# Create cache manager
cache_manager = CacheManager(cache_dir=".ai-cache")

# Create processor
processor = EnhancementProcessor(
    provider=provider,
    cache_manager=cache_manager,
    enhancement_level="moderate",
)

# Enhance content
content = Path("docs/guide.md").read_text()
enhanced = await processor.enhance_content(content)

# Save result
Path("docs/guide-enhanced.md").write_text(enhanced)
```

### Grammar Only

```python
from mkdocs_ai.enhancement import GrammarEnhancer

enhancer = GrammarEnhancer(provider, cache_manager)

# Fix all grammar issues
corrected = await enhancer.fix_all(content)

# Or fix specific issues
grammar_fixed = await enhancer.fix_grammar(content)
spelling_fixed = await enhancer.fix_spelling(content)
punctuation_fixed = await enhancer.fix_punctuation(content)
```

### Clarity Improvements

```python
from mkdocs_ai.enhancement import ClarityEnhancer

enhancer = ClarityEnhancer(provider, cache_manager)

# Improve clarity
improved = await enhancer.improve_clarity(content)

# Simplify sentences
simplified = await enhancer.simplify_sentences(content)

# Improve word choice
better_words = await enhancer.improve_word_choice(content)

# Check consistency
consistency_report = await enhancer.check_consistency(content)
```

### Quality Metrics

```python
# Check quality
metrics = await processor.check_quality(content)

print(f"Grammar: {metrics['grammar_score']}/100")
print(f"Clarity: {metrics['clarity_score']}/100")
print(f"Consistency: {metrics['consistency_score']}/100")
print(f"Readability: {metrics['readability_score']}/100")

# Get improvement suggestions
suggestions = await enhancer.get_improvement_suggestions(content)
for suggestion in suggestions:
    print(f"- {suggestion}")
```

### Readability Analysis

```python
# Calculate readability metrics
readability = await enhancer.calculate_readability(content)

print(f"Flesch Reading Ease: {readability['flesch_reading_ease']}")
print(f"Grade Level: {readability['flesch_kincaid_grade']}")
print(f"Interpretation: {readability['interpretation']}")
```

## Enhancement Levels Explained

### Light Enhancement

- ✅ Fix grammar errors
- ✅ Correct spelling mistakes
- ❌ No clarity improvements
- ❌ No consistency checking
- ❌ No sentence rewrites

**Use when**: You want minimal changes, just error corrections.

### Moderate Enhancement (Default)

- ✅ Fix grammar errors
- ✅ Correct spelling mistakes
- ✅ Improve clarity
- ✅ Check consistency
- ❌ No sentence rewrites

**Use when**: You want quality improvements while preserving your writing style.

### Aggressive Enhancement

- ✅ Fix grammar errors
- ✅ Correct spelling mistakes
- ✅ Improve clarity
- ✅ Check consistency
- ✅ Rewrite unclear sentences

**Use when**: You want maximum quality improvements and don't mind rewrites.

## What Gets Preserved

The enhancement system automatically preserves:

- **Code blocks** - Fenced code blocks (```) and inline code (`)
- **Frontmatter** - YAML frontmatter at the top of files
- **Markdown formatting** - Headers, lists, links, etc.
- **Technical terms** - Programming terms, API names, etc.
- **Proper nouns** - Product names, company names, etc.

## Example: Before and After

### Before Enhancement

```markdown
# Docker Setup

Docker is a tool that lets you run applications in containers. Its really useful
for development because you can have consistent environments across different machines.

To install docker, you need to download it from the website and then run the installer.
After that you can start using it by running docker commands in your terminal.
```

### After Enhancement (Moderate Level)

```markdown
# Docker Setup

Docker is a tool that allows you to run applications in containers. It's really useful
for development because you can maintain consistent environments across different machines.

To install Docker, download it from the official website and run the installer.
After installation, you can start using it by running Docker commands in your terminal.
```

**Changes made**:
- Fixed "Its" → "It's"
- Improved "lets you" → "allows you to"
- Improved "you can have" → "you can maintain"
- Fixed "docker" → "Docker" (proper noun)
- Improved sentence structure

## Best Practices

### 1. Start with Preview

Always preview changes before applying:
```bash
mkdocs-ai enhance docs/guide.md --preview
```

### 2. Use Appropriate Level

- **Light**: For well-written docs that just need error fixes
- **Moderate**: For most documentation
- **Aggressive**: For drafts or low-quality content

### 3. Review Changes

Always review enhanced content before committing:
```bash
git diff docs/guide.md
```

### 4. Enable Caching

Caching saves time and API costs:
```yaml
cache:
  enabled: true
  ttl: 86400  # 24 hours
```

### 5. Exclude Certain Files

Exclude files that shouldn't be enhanced:
```yaml
enhancement:
  enabled: true
  exclude_patterns:
    - "docs/api/*"
    - "docs/reference/*"
```

## Troubleshooting

### Enhancement Changes Too Much

Use a lighter level:
```bash
mkdocs-ai enhance docs/guide.md --level light
```

### Technical Terms Changed

The AI should preserve technical terms, but if it doesn't, you can:
1. Use inline code formatting: \`technical_term\`
2. Add to custom dictionary (future feature)
3. Use lighter enhancement level

### Slow Performance

Enable caching to speed up repeated enhancements:
```yaml
cache:
  enabled: true
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Enhance Documentation

on:
  pull_request:
    paths:
      - 'docs/**'

jobs:
  enhance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: pip install mkdocs-ai-assistant
      
      - name: Enhance documentation
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        run: |
          mkdocs-ai enhance docs/guide.md
      
      - name: Commit changes
        run: |
          git config user.name "AI Assistant"
          git config user.email "ai@example.com"
          git add docs/
          git commit -m "docs: AI-enhanced documentation"
          git push
```

## Next Steps

- Try enhancing your documentation: `mkdocs-ai enhance docs/index.md --preview`
- Check quality metrics: `mkdocs-ai check-quality docs/index.md`
- Enable automatic enhancement in your MkDocs config
- Explore other features: generation, search, asset processing
