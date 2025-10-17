# Quick Start

Get up and running with MkDocs AI Assistant in minutes.

## 1. Configure the Plugin

Add to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
      
      generation:
        enabled: true
      
      cache:
        enabled: true
```

## 2. Set Your API Key

```bash
export OPENROUTER_API_KEY="your-key-here"
```

## 3. Generate Your First Document

### Method 1: CLI

```bash
mkdocs ai generate "Create a comprehensive guide to Docker Compose"
```

This will create a new markdown file in `docs/generated/`.

### Method 2: Markdown Syntax

Add this to any markdown file:

```markdown
<!-- AI-GENERATE: Explain the benefits of using MkDocs for documentation -->
```

When you build your site, the AI will generate content and replace this comment.

### Method 3: Config-Based

Add generation tasks to `mkdocs.yml`:

```yaml
plugins:
  - ai-assistant:
      generation:
        tasks:
          - prompt: "Create API reference documentation"
            output: docs/api/reference.md
          - prompt: "Write a getting started guide"
            output: docs/getting-started.md
```

Run the build:

```bash
mkdocs build
```

## 4. Test the Site

Start the development server:

```bash
mkdocs serve
```

Visit [http://localhost:8000](http://localhost:8000) to see your AI-generated documentation!

## 5. Enable More Features

### Content Enhancement

Automatically improve your documentation:

```yaml
plugins:
  - ai-assistant:
      enhancement:
        enabled: true
        auto_enhance: true
        features:
          - grammar
          - clarity
          - consistency
```

### Semantic Search

Add AI-powered search:

```yaml
plugins:
  - ai-assistant:
      search:
        enabled: true
        embeddings_model: text-embedding-3-small
```

## Common Workflows

### Personal Knowledge Base

Perfect for organizing research and homelab documentation:

```yaml
plugins:
  - ai-assistant:
      generation:
        enabled: true
        output_dir: docs/research
      
      assets:
        enabled: true
        sources:
          - type: docker-compose
            path: ../homelab
            pattern: "**/*compose*.yml"
            output_dir: docs/homelab
```

### API Documentation

Generate docs from code:

```yaml
plugins:
  - ai-assistant:
      assets:
        enabled: true
        sources:
          - type: code
            path: ../src
            languages: [python, javascript]
            output_dir: docs/api
```

## Tips

1. **Use Caching**: Enable caching to save costs and speed up builds
2. **Start Simple**: Begin with document generation, add features gradually
3. **Review Output**: Always review AI-generated content before publishing
4. **Experiment**: Try different models and prompts to find what works best

## Troubleshooting

### Plugin Not Found

Make sure you installed the plugin:

```bash
pip install -e /path/to/mkdocs-ai-assistant
```

### API Key Errors

Verify your API key is set:

```bash
echo $OPENROUTER_API_KEY
```

### Generation Fails

Check the logs:

```bash
mkdocs build --verbose
```

Enable debug mode in config:

```yaml
plugins:
  - ai-assistant:
      debug: true
```

## Next Steps

- [Explore Generation Features](../features/generation.md)
- [Learn About Enhancement](../features/enhancement.md)
- [See Advanced Examples](../examples/advanced.md)
