# Document Generation

AI-powered document generation from prompts, templates, and inline comments.

## Overview

Generate comprehensive documentation using:

- **CLI Commands**: Quick one-liners for instant docs
- **Markdown Syntax**: Inline `<!-- AI-GENERATE: ... -->` comments
- **Templates**: Jinja2-based templates for consistent structure
- **Batch Generation**: Define multiple generation tasks in config

## Quick Start

### CLI Generation

```bash
# Generate from prompt
mkdocs-ai generate "Create a comprehensive guide to Docker Compose"

# Specify output file
mkdocs-ai generate "Write API documentation" -o docs/api/reference.md

# Use specific provider
mkdocs-ai generate "Setup guide" --provider gemini

# Verbose output
mkdocs-ai generate "Tutorial" -v
```

### Markdown Syntax

Add generation comments directly in your markdown:

```markdown
# Getting Started

<!-- AI-GENERATE: Explain the benefits of using MkDocs for documentation -->

## Installation

<!-- AI-GENERATE: Provide step-by-step installation instructions for MkDocs -->
```

When you build your site, the AI will replace these comments with generated content.

### Template-Based Generation

Create reusable templates:

```jinja2
{# templates/api-endpoint.md.j2 #}
# {{ endpoint_name }}

<!-- AI-GENERATE: Document the {{ endpoint_name }} API endpoint including parameters, responses, and examples -->

## Parameters

<!-- AI-GENERATE: List and describe all parameters for {{ endpoint_name }} -->

## Examples

<!-- AI-GENERATE: Provide code examples for {{ endpoint_name }} in Python and JavaScript -->
```

Use the template:

```bash
mkdocs-ai generate --template api-endpoint.md.j2 \
  --context '{"endpoint_name": "User Authentication"}' \
  -o docs/api/auth.md
```

## Plugin Integration

Enable generation in your MkDocs configuration:

```yaml
# mkdocs.yml
plugins:
  - ai-assistant:
      provider:
        name: openrouter
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
      
      generation:
        enabled: true
        output_dir: docs/generated
        templates_dir: .ai-templates
        cli_enabled: true
        markdown_syntax: true
        
        # Batch generation tasks
        tasks:
          - prompt: "Create API reference documentation"
            output: docs/api/reference.md
          - prompt: "Write a getting started guide"
            output: docs/getting-started.md
```

## Features

### Prompt-Based Generation
Generate documentation from natural language prompts:

```bash
mkdocs-ai generate "Create a troubleshooting guide for common Docker issues"
```

### Context-Aware Generation
Provide context for better results:

```bash
mkdocs-ai generate "Document this API" \
  --context-file api-spec.yaml \
  -o docs/api.md
```

### Template System
Use Jinja2 templates for consistent documentation:

```jinja2
# {{ title }}

{{ description }}

<!-- AI-GENERATE: Provide detailed explanation of {{ topic }} -->

## Usage

<!-- AI-GENERATE: Show practical examples of {{ topic }} -->
```

### Batch Processing
Generate multiple documents at once:

```yaml
generation:
  tasks:
    - prompt: "API documentation"
      output: docs/api.md
    - prompt: "User guide"
      output: docs/guide.md
    - prompt: "FAQ"
      output: docs/faq.md
```

## CLI Commands

### generate

Generate documentation from a prompt:

```bash
mkdocs-ai generate [OPTIONS] PROMPT
```

**Options**:
- `-o, --output PATH`: Output file path
- `-p, --provider`: AI provider (openrouter, gemini, anthropic, ollama)
- `--api-key TEXT`: API key for provider
- `--template PATH`: Template file to use
- `--context TEXT`: JSON context for template
- `--context-file PATH`: YAML/JSON context file
- `-v, --verbose`: Verbose output

**Examples**:

```bash
# Basic generation
mkdocs-ai generate "Create Docker guide"

# With output file
mkdocs-ai generate "API docs" -o docs/api.md

# Using template
mkdocs-ai generate --template guide.md.j2 \
  --context '{"topic": "Docker"}' \
  -o docs/docker.md

# With context file
mkdocs-ai generate "Document API" \
  --context-file openapi.yaml \
  -o docs/api.md
```

### batch

Generate multiple documents from config:

```bash
mkdocs-ai batch [OPTIONS]
```

**Options**:
- `-c, --config PATH`: Config file path (default: mkdocs.yml)
- `-v, --verbose`: Verbose output

**Example**:

```bash
mkdocs-ai batch -c mkdocs.yml -v
```

## Markdown Syntax

### Basic Syntax

```markdown
<!-- AI-GENERATE: Your prompt here -->
```

### With Context

```markdown
<!-- AI-GENERATE: Document the {{ feature }} feature -->
```

### Multi-line Prompts

```markdown
<!--
AI-GENERATE:
Create a comprehensive guide covering:
- Installation steps
- Configuration options
- Usage examples
- Troubleshooting tips
-->
```

## Templates

### Template Structure

```jinja2
{# Header #}
# {{ title }}

{# AI-generated content #}
<!-- AI-GENERATE: {{ prompt }} -->

{# Variables #}
{{ content }}

{# Loops #}
{% for item in items %}
## {{ item.name }}
<!-- AI-GENERATE: Document {{ item.name }} -->
{% endfor %}
```

### Template Variables

Pass variables via context:

```bash
mkdocs-ai generate \
  --template doc.md.j2 \
  --context '{"title": "Guide", "version": "1.0"}' \
  -o docs/guide.md
```

### Template Directory

Configure template directory:

```yaml
generation:
  templates_dir: .ai-templates
```

Place templates in `.ai-templates/`:

```
.ai-templates/
├── api-endpoint.md.j2
├── guide.md.j2
└── tutorial.md.j2
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable generation |
| `output_dir` | string | `docs/generated` | Output directory |
| `templates_dir` | string | `.ai-templates` | Template directory |
| `cli_enabled` | boolean | `true` | Enable CLI commands |
| `markdown_syntax` | boolean | `true` | Process AI-GENERATE comments |

## Best Practices

1. **Clear Prompts**: Be specific about what you want
2. **Use Templates**: Maintain consistency across documents
3. **Provide Context**: Include relevant information for better results
4. **Review Output**: Always review AI-generated content
5. **Iterate**: Refine prompts based on results

## Examples

### API Documentation

```bash
mkdocs-ai generate \
  "Create comprehensive API documentation including authentication, endpoints, and examples" \
  -o docs/api.md
```

### Tutorial

```bash
mkdocs-ai generate \
  "Write a step-by-step tutorial for beginners covering installation, basic usage, and first project" \
  -o docs/tutorial.md
```

### Troubleshooting Guide

```bash
mkdocs-ai generate \
  "Create a troubleshooting guide with common issues, solutions, and debugging tips" \
  -o docs/troubleshooting.md
```

## Status

✅ **COMPLETE** - Fully implemented and production-ready

- [x] CLI generation
- [x] Markdown syntax processing
- [x] Template system
- [x] Batch generation
- [x] Plugin integration
- [x] Context support
- [x] Cache integration
