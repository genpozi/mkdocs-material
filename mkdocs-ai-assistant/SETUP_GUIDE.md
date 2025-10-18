# MkDocs AI Assistant - Setup Guide

This guide will help you set up and test MkDocs AI Assistant with your API keys.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- API keys from at least one provider

## Step 1: Installation

```bash
cd mkdocs-ai-assistant
pip install -e .
```

## Step 2: Configure API Keys

### Option A: Environment Variables (Recommended)

Set environment variables in your shell:

```bash
# For Gemini (recommended for quality)
export GEMINI_API_KEY="your-gemini-key"

# For Perplexity
export PERPLEXITY_API_KEY="your-perplexity-key"

# For OpenRouter (free models available)
export OPENROUTER_API_KEY="your-openrouter-key"
```

To make these permanent, add them to your shell configuration:

```bash
# For bash
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export GEMINI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### Option B: .env File (Alternative)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```bash
   nano .env  # or use your preferred editor
   ```

3. The `.env` file is automatically ignored by git (see `.gitignore`)

## Step 3: Test the Installation

### Test CLI Help

```bash
mkdocs-ai --help
```

You should see all available commands.

### Test with Gemini (Best Quality)

```bash
# Generate a test document
mkdocs-ai generate "Write a brief introduction to Docker" -p gemini -v

# Check if it works
ls docs/generated/
```

### Test with OpenRouter (Free Models)

```bash
# Using free Llama model
mkdocs-ai generate "Write a brief introduction to Docker" \
  -p openrouter \
  -m meta-llama/llama-4-maverick:free \
  -v

# Using free DeepSeek model
mkdocs-ai generate "Write a brief introduction to Docker" \
  -p openrouter \
  -m deepseek/deepseek-chat-v3.1:free \
  -v
```

## Step 4: Test All Features

### 1. Document Generation

```bash
# Basic generation
mkdocs-ai generate "Create a guide to Kubernetes basics"

# With custom output
mkdocs-ai generate "API documentation" -o docs/api.md

# With specific provider and model
mkdocs-ai generate "Docker tutorial" -p gemini -v
```

### 2. Content Enhancement

```bash
# Create a test file
echo "# Test Document

Docker is a tool that lets you run applications in containers. Its really useful for development." > test.md

# Preview enhancement
mkdocs-ai enhance test.md --preview

# Apply enhancement
mkdocs-ai enhance test.md -v

# Check quality
mkdocs-ai check-quality test.md
```

### 3. Semantic Search

```bash
# Build search index (requires docs directory)
mkdocs-ai build-search-index

# Search documentation
mkdocs-ai search "Docker configuration"

# Search with more results
mkdocs-ai search "API reference" -k 10
```

### 4. Asset Processing

```bash
# Discover assets in project
mkdocs-ai discover-assets

# Process Docker Compose files
mkdocs-ai process-assets -t docker_compose -v

# Process Python modules
mkdocs-ai process-assets -t python_modules -v
```

### 5. Cache Management

```bash
# View cache statistics
mkdocs-ai cache-stats

# Clear cache if needed
mkdocs-ai cache-clear
```

## Step 5: Configure MkDocs Plugin

Create or update `mkdocs.yml`:

```yaml
site_name: My Documentation
site_url: https://example.com

plugins:
  - search
  - ai-assistant:
      enabled: true
      debug: false
      
      provider:
        name: gemini  # or openrouter, perplexity
        api_key: !ENV GEMINI_API_KEY
        model: gemini-2.0-flash-exp
        temperature: 0.7
        max_tokens: 4000
      
      cache:
        enabled: true
        dir: .ai-cache
        ttl: 86400  # 24 hours
      
      generation:
        enabled: true
        output_dir: docs/generated
        markdown_syntax: true
      
      enhancement:
        enabled: false  # Enable for automatic enhancement
        level: moderate
      
      search:
        enabled: true
        index_file: .ai-cache/search_index.json
        chunk_size: 1000
        chunk_overlap: 200
      
      assets:
        enabled: false  # Enable for automatic asset processing

theme:
  name: material
```

## Step 6: Build Your Site

```bash
# Build the site
mkdocs build

# Serve locally
mkdocs serve
```

Visit http://localhost:8000 to see your documentation.

## Provider-Specific Configuration

### Gemini (Recommended for Quality)

```yaml
provider:
  name: gemini
  api_key: !ENV GEMINI_API_KEY
  model: gemini-2.0-flash-exp  # Fast and capable
  # Alternative: gemini-1.5-pro  # More capable, slower
```

**Best for**: High-quality generation, content enhancement

### OpenRouter (Free Models Available)

```yaml
provider:
  name: openrouter
  api_key: !ENV OPENROUTER_API_KEY
  model: meta-llama/llama-4-maverick:free
  # Alternative: deepseek/deepseek-chat-v3.1:free
```

**Best for**: Testing, cost-conscious usage

### Perplexity (Online Search Capabilities)

```yaml
provider:
  name: perplexity
  api_key: !ENV PERPLEXITY_API_KEY
  model: llama-3.1-sonar-large-128k-online
```

**Best for**: Research-based content, current information

## Troubleshooting

### API Key Not Found

**Error**: `API key not found`

**Solution**: 
```bash
# Check if environment variable is set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your-key"
```

### Provider Not Working

**Error**: `Provider error` or `Failed to generate`

**Solution**:
1. Check API key is valid
2. Try with verbose flag: `-v`
3. Check provider status
4. Try a different provider

### Cache Issues

**Error**: Cache-related errors

**Solution**:
```bash
# Clear cache
mkdocs-ai cache-clear

# Check cache stats
mkdocs-ai cache-stats
```

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
# Reinstall in development mode
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

## Testing Checklist

- [ ] Installation successful
- [ ] API keys configured
- [ ] CLI help works
- [ ] Document generation works
- [ ] Content enhancement works
- [ ] Search index builds
- [ ] Search works
- [ ] Asset discovery works
- [ ] Cache works
- [ ] MkDocs build works

## Example Workflow

Here's a complete workflow to test all features:

```bash
# 1. Set up environment
export GEMINI_API_KEY="your-key"

# 2. Generate some documentation
mkdocs-ai generate "Introduction to Docker" -o docs/docker-intro.md
mkdocs-ai generate "Kubernetes basics" -o docs/k8s-basics.md

# 3. Enhance existing content
mkdocs-ai enhance docs/docker-intro.md --preview
mkdocs-ai enhance docs/docker-intro.md

# 4. Build search index
mkdocs-ai build-search-index

# 5. Search documentation
mkdocs-ai search "Docker containers"

# 6. Process assets (if you have Docker Compose files)
mkdocs-ai discover-assets
mkdocs-ai process-assets -t docker_compose

# 7. Check cache
mkdocs-ai cache-stats

# 8. Build MkDocs site
mkdocs build
mkdocs serve
```

## Security Best Practices

1. **Never commit API keys** to git
2. **Use environment variables** for keys
3. **Add .env to .gitignore** (already done)
4. **Rotate keys regularly**
5. **Use different keys** for development and production
6. **Monitor API usage** to detect unauthorized use

## Getting Help

- **Documentation**: See markdown files in project root
- **Examples**: Check `examples/` directory
- **Issues**: Report bugs via GitHub issues
- **Verbose mode**: Add `-v` flag to any command for detailed output

## Next Steps

1. Test all features with your API keys
2. Configure MkDocs plugin for your project
3. Generate documentation for your project
4. Enable automatic enhancement and search
5. Provide feedback on the alpha release

---

**Ready to start?** Follow the steps above and you'll be generating AI-powered documentation in minutes!
