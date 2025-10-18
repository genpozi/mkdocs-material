# Content Enhancement

AI-powered content enhancement for improving documentation quality.

## Overview

The Content Enhancement feature automatically improves your documentation by:

- **Fixing Grammar**: Corrects grammar and spelling errors
- **Improving Clarity**: Simplifies complex sentences and improves readability
- **Ensuring Consistency**: Maintains consistent terminology throughout
- **Preserving Code**: Never modifies code blocks or frontmatter

## Enhancement Levels

### Light
Grammar and spelling corrections only. Minimal changes to preserve your writing style.

```bash
mkdocs-ai enhance docs/guide.md --level light
```

### Moderate (Default)
Grammar, spelling, and clarity improvements. Balances quality with style preservation.

```bash
mkdocs-ai enhance docs/guide.md --level moderate
```

### Aggressive
Full enhancement including sentence rewrites. Maximum quality improvements.

```bash
mkdocs-ai enhance docs/guide.md --level aggressive
```

## CLI Usage

### Enhance a Document

```bash
# Basic enhancement
mkdocs-ai enhance docs/guide.md

# Preview changes without applying
mkdocs-ai enhance docs/guide.md --preview

# Save to different file
mkdocs-ai enhance docs/guide.md -o docs/guide-enhanced.md

# Verbose output with quality metrics
mkdocs-ai enhance docs/guide.md -v
```

### Check Quality

Check documentation quality without making changes:

```bash
mkdocs-ai check-quality docs/guide.md
```

Shows:
- Grammar score (0-100)
- Clarity score (0-100)
- Consistency score (0-100)
- Readability score (0-100)
- Specific issues found
- Improvement suggestions

## Plugin Integration

Enable automatic enhancement during MkDocs build:

```yaml
# mkdocs.yml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
      
      enhancement:
        enabled: true
        level: moderate
        preserve_code: true
        preserve_frontmatter: true
        exclude_patterns:
          - "docs/api/*"
          - "docs/generated/*"
```

## Features

### Grammar Correction
- Detects and fixes grammar errors
- Corrects spelling mistakes
- Fixes punctuation issues
- Preserves technical terms

### Clarity Improvement
- Simplifies complex sentences
- Improves word choice
- Enhances readability
- Calculates Flesch Reading Ease scores

### Consistency Checking
- Ensures consistent terminology
- Maintains style consistency
- Checks for contradictions

### Code Preservation
- Never modifies code blocks
- Preserves frontmatter
- Maintains markdown formatting
- Respects inline code

## Examples

### Before Enhancement

```markdown
The API endpoint can be used for getting the user data and it returns
a JSON response which contains the user information including their name,
email, and other details that might be relevant.
```

### After Enhancement (Moderate)

```markdown
The API endpoint retrieves user data and returns a JSON response containing
the user's name, email, and other relevant information.
```

## Quality Metrics

The enhancement system provides quality scores:

- **Grammar Score**: Percentage of text without grammar errors
- **Clarity Score**: Readability and sentence complexity
- **Consistency Score**: Terminology and style consistency
- **Readability Score**: Flesch Reading Ease (0-100)

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable enhancement |
| `level` | string | `moderate` | Enhancement level |
| `preserve_code` | boolean | `true` | Preserve code blocks |
| `preserve_frontmatter` | boolean | `true` | Preserve frontmatter |
| `exclude_patterns` | list | `[]` | Patterns to exclude |

## Best Practices

1. **Start with Preview**: Always preview changes before applying
2. **Use Light Level First**: Test with light enhancement before aggressive
3. **Exclude Generated Content**: Don't enhance auto-generated API docs
4. **Check Quality First**: Run quality checks to identify issues
5. **Review Changes**: Always review AI-enhanced content

## Status

✅ **COMPLETE** - Fully implemented and production-ready
