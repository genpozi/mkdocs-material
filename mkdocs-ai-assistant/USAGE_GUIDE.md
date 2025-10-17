# MkDocs AI Assistant - Usage Guide

Complete guide to using the document generation features.

## Table of Contents

- [CLI Generation](#cli-generation)
- [Markdown Syntax](#markdown-syntax)
- [Template-Based Generation](#template-based-generation)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## CLI Generation

### Basic Usage

Generate a document from a prompt:

```bash
mkdocs-ai generate "Create a comprehensive guide to Docker Compose"
```

This will:
1. Generate content using AI
2. Save to `docs/generated/create-a-comprehensive-guide-to-docker-compose.md`
3. Show progress and statistics

### Specify Output File

```bash
mkdocs-ai generate "Kubernetes basics" -o docs/k8s/basics.md
```

### Use Specific Provider

```bash
# Use Gemini
mkdocs-ai generate "API documentation" -p gemini

# Use Anthropic
mkdocs-ai generate "Tutorial" -p anthropic --api-key $ANTHROPIC_API_KEY

# Use local Ollama
mkdocs-ai generate "Guide" -p ollama
```

### Use Specific Model

```bash
mkdocs-ai generate "Advanced topic" -m anthropic/claude-3-opus
```

### Disable Caching

```bash
mkdocs-ai generate "Fresh content" --no-cache
```

### Verbose Output

```bash
mkdocs-ai generate "Documentation" -v
```

Shows:
- Provider and model being used
- Cache status
- Output path
- Content preview
- Detailed statistics

## Markdown Syntax

### Simple Generation

Add AI-GENERATE comments to your markdown files:

```markdown
# My Page

## Introduction

<!-- AI-GENERATE: Write a brief introduction to Docker for beginners -->

## Next Section

Regular content here...
```

When you build your site (`mkdocs build`), the comment will be replaced with AI-generated content.

### Block Generation

For larger sections:

```markdown
## Docker Compose Guide

<!-- AI-GENERATE-START: Comprehensive guide to Docker Compose -->

This placeholder content will be replaced.

<!-- AI-GENERATE-END -->
```

The entire block (including existing content) will be replaced with AI-generated content.

### With Options

```markdown
<!-- AI-GENERATE: Explain microservices | model=anthropic/claude-3-opus -->
```

Options format: `prompt | option1=value1 option2=value2`

## Template-Based Generation

### Create a Template

Create `.ai-templates/api-reference.md.j2`:

```jinja2
# {{ name }} API Reference

**Version**: {{ version }}

## Overview

{{ ai.overview }}

## Endpoints

{{ ai.endpoints }}

## Authentication

{{ ai.authentication }}

## Examples

{{ ai.examples }}
```

### Use the Template

```bash
mkdocs-ai generate "API documentation" \
  -t .ai-templates/api-reference.md.j2 \
  -c name="My API" \
  -c version="2.0"
```

The AI will:
1. Generate content for each `{{ ai.field }}` placeholder
2. Render the template with both context variables and AI-generated content

### Template Syntax

- `{{ variable }}` - Regular Jinja2 variable
- `{{ ai.field_name }}` - AI-generated content
- Context variables: `-c key=value`

## Configuration

### In mkdocs.yml

```yaml
plugins:
  - ai-assistant:
      # Provider configuration
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
        fallback: google/gemini-pro
        temperature: 0.7
        max_tokens: 4000
      
      # Caching
      cache:
        enabled: true
        dir: .ai-cache
        ttl: 86400  # 24 hours
      
      # Generation
      generation:
        enabled: true
        output_dir: docs/generated
        templates_dir: .ai-templates
        cli_enabled: true
        markdown_syntax: true
```

### Environment Variables

Set API keys as environment variables:

```bash
# OpenRouter (recommended)
export OPENROUTER_API_KEY="your-key"

# Gemini
export GEMINI_API_KEY="your-key"

# Anthropic
export ANTHROPIC_API_KEY="your-key"
```

## Examples

### Example 1: Research Report

```bash
mkdocs-ai generate \
  "Create a comprehensive research report on Kubernetes networking, \
   including CNI plugins, service mesh, and network policies. \
   Include diagrams descriptions and practical examples." \
  -o docs/research/k8s-networking.md \
  -v
```

### Example 2: Homelab Documentation

```bash
mkdocs-ai generate \
  "Document my homelab Docker Compose stack including Traefik, \
   Portainer, and monitoring services. Include setup instructions, \
   configuration details, and troubleshooting tips." \
  -o docs/homelab/docker-stack.md
```

### Example 3: API Documentation

```bash
mkdocs-ai generate \
  "Create REST API documentation for an authentication service" \
  -t .ai-templates/api-reference.md.j2 \
  -c name="Auth Service" \
  -c version="1.0" \
  -o docs/api/auth.md
```

### Example 4: Tutorial Series

```bash
# Part 1
mkdocs-ai generate \
  "Create part 1 of a Docker tutorial series: Introduction and Installation" \
  -o docs/tutorials/docker-01-intro.md

# Part 2
mkdocs-ai generate \
  "Create part 2 of a Docker tutorial series: Containers and Images" \
  -o docs/tutorials/docker-02-containers.md

# Part 3
mkdocs-ai generate \
  "Create part 3 of a Docker tutorial series: Docker Compose" \
  -o docs/tutorials/docker-03-compose.md
```

### Example 5: Inline Generation

Create `docs/guides/docker.md`:

```markdown
# Docker Guide

## What is Docker?

<!-- AI-GENERATE: Explain Docker in simple terms for beginners (2-3 paragraphs) -->

## Installation

<!-- AI-GENERATE-START: Step-by-step Docker installation guide for Ubuntu -->
<!-- AI-GENERATE-END -->

## Basic Commands

<!-- AI-GENERATE: List and explain the 10 most important Docker commands -->

## Best Practices

<!-- AI-GENERATE: Docker best practices for production deployments -->
```

Then build:

```bash
mkdocs build
```

All AI-GENERATE comments will be replaced with generated content.

## Cache Management

### View Cache Statistics

```bash
mkdocs-ai cache-stats
```

Shows:
- Number of cached entries
- Total cache size
- Hit/miss statistics
- Hit rate percentage

### Clear Cache

```bash
mkdocs-ai cache-clear
```

Removes all cached responses. Useful when:
- You want fresh content
- Models have been updated
- Cache is too large

## Troubleshooting

### API Key Errors

**Error**: `API key required for OpenRouterProvider`

**Solution**:
```bash
export OPENROUTER_API_KEY="your-key-here"
```

Or specify in command:
```bash
mkdocs-ai generate "prompt" --api-key your-key
```

### Generation Fails

**Error**: `Generation failed: HTTP error 429`

**Solution**: Rate limited. Wait a moment and try again, or enable caching.

**Error**: `Generation failed: HTTP error 401`

**Solution**: Invalid API key. Check your key is correct.

### Markdown Comments Not Processing

**Check**:
1. Is `generation.markdown_syntax` enabled in config?
2. Is the plugin enabled?
3. Are there any errors in build output?

Run with verbose:
```bash
mkdocs build --verbose
```

### Cache Not Working

**Check**:
1. Is `cache.enabled` set to `true`?
2. Does the cache directory exist and have write permissions?
3. Check cache stats: `mkdocs-ai cache-stats`

### Template Errors

**Error**: `Template not found`

**Solution**: Check template path is correct and file exists.

**Error**: `Invalid template`

**Solution**: Check Jinja2 syntax in template file.

## Tips & Best Practices

### 1. Use Caching

Enable caching to save money and speed up builds:

```yaml
cache:
  enabled: true
  ttl: 86400  # 24 hours
```

### 2. Be Specific in Prompts

**Bad**: "Write about Docker"

**Good**: "Create a beginner-friendly guide to Docker Compose, including installation, basic concepts, and a practical example with a web application and database"

### 3. Use Templates for Consistency

Create templates for common documentation types:
- API references
- Service documentation
- Tutorial structure
- Troubleshooting guides

### 4. Review AI Output

Always review AI-generated content before publishing:
- Check for accuracy
- Verify code examples
- Ensure consistency with your style
- Add project-specific details

### 5. Iterate on Prompts

If output isn't what you want:
1. Clear cache: `mkdocs-ai cache-clear`
2. Refine your prompt
3. Try again

### 6. Use Verbose Mode for Debugging

```bash
mkdocs-ai generate "prompt" -v
```

Shows detailed information about what's happening.

### 7. Organize Generated Content

Use subdirectories:
```bash
mkdocs-ai generate "API docs" -o docs/api/reference.md
mkdocs-ai generate "Tutorial" -o docs/tutorials/getting-started.md
mkdocs-ai generate "Research" -o docs/research/kubernetes.md
```

### 8. Combine Manual and AI Content

Use AI for:
- Initial drafts
- Boilerplate content
- Examples and explanations
- Comprehensive overviews

Write manually for:
- Project-specific details
- Personal insights
- Unique configurations
- Critical information

### 9. Use Different Models

Experiment with different models for different tasks:
- **Claude (Anthropic)**: Best for technical accuracy
- **GPT-4 (OpenRouter)**: Great for creative content
- **Gemini**: Fast and cost-effective for testing
- **Local (Ollama)**: Privacy-focused, no API costs

### 10. Monitor Costs

If using paid APIs:
- Enable caching
- Use cheaper models for drafts
- Review generated content length
- Check provider pricing

## Advanced Usage

### Custom System Prompts

Modify `mkdocs_ai/generation/prompt.py` to customize the system prompt for your needs.

### Provider-Specific Options

Each provider supports different options. Check provider documentation:
- OpenRouter: Multiple models, fallback support
- Gemini: Safety settings, temperature control
- Anthropic: Claude-specific parameters
- Ollama: Local model selection

### Integration with CI/CD

Generate documentation in CI:

```yaml
# .github/workflows/docs.yml
- name: Generate AI Documentation
  env:
    OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
  run: |
    mkdocs-ai generate "API Reference" -o docs/api/reference.md
    mkdocs build
```

### Batch Generation (Coming Soon)

Future feature for config-based batch generation:

```yaml
plugins:
  - ai-assistant:
      generation:
        tasks:
          - prompt: "API documentation"
            output: docs/api.md
          - prompt: "Tutorial"
            output: docs/tutorial.md
```

## Getting Help

1. Check this guide
2. Review [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)
3. Check [README.md](README.md)
4. Enable verbose mode: `-v`
5. Check logs: `mkdocs build --verbose`

## Next Steps

- Try the examples above
- Create your own templates
- Experiment with different prompts
- Integrate into your workflow
- Share feedback and improvements

---

**Happy Documenting!** 🚀
