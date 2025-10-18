# Quick Start Guide - Get Testing in 5 Minutes!

This guide gets you up and running with MkDocs AI Assistant quickly.

## Step 1: Install (30 seconds)

```bash
cd mkdocs-ai-assistant
pip install -e .
```

## Step 2: Set API Keys (1 minute)

Choose ONE of these methods:

### Method A: Environment Variables (Recommended)

```bash
# Set for current session
export GEMINI_API_KEY="your-gemini-key-here"
export OPENROUTER_API_KEY="your-openrouter-key-here"
export PERPLEXITY_API_KEY="your-perplexity-key-here"
```

### Method B: Use Setup Script

```bash
source setup-env.sh
# Follow the prompts to enter your keys
```

### Method C: Pass Keys Directly (Testing Only)

```bash
# You can pass keys directly to commands
mkdocs-ai generate "test" --api-key "your-key" -p gemini
```

## Step 3: Test It Works (30 seconds)

```bash
# Quick test
./test-setup.sh
```

Or manually:

```bash
# Test with Gemini (best quality)
mkdocs-ai generate "Write one sentence about Docker" -p gemini -v

# Test with OpenRouter (free models)
mkdocs-ai generate "Write one sentence about Docker" \
  -p openrouter \
  -m meta-llama/llama-4-maverick:free \
  -v
```

## Step 4: Try All Features (3 minutes)

### Document Generation

```bash
# Generate a document
mkdocs-ai generate "Create a brief Docker introduction" -p gemini

# Check the output
ls docs/generated/
cat docs/generated/*.md
```

### Content Enhancement

```bash
# Create a test file
echo "# Test
Docker is a tool that lets you run apps in containers. Its really useful." > test.md

# Preview enhancement
mkdocs-ai enhance test.md --preview -p gemini

# Apply enhancement
mkdocs-ai enhance test.md -p gemini
cat test.md
```

### Semantic Search

```bash
# Build search index (if you have docs)
mkdocs-ai build-search-index -p gemini

# Search
mkdocs-ai search "Docker" -p gemini
```

### Asset Processing

```bash
# Discover assets
mkdocs-ai discover-assets

# Process if you have Docker Compose or Python files
mkdocs-ai process-assets -t python_modules -p gemini -v
```

## Provider-Specific Examples

### Using Gemini (Best Quality)

```bash
export GEMINI_API_KEY="your-key"

# Generate
mkdocs-ai generate "Docker guide" -p gemini

# Enhance
mkdocs-ai enhance docs/file.md -p gemini

# Search
mkdocs-ai build-search-index -p gemini
mkdocs-ai search "query" -p gemini
```

### Using OpenRouter (Free Models)

```bash
export OPENROUTER_API_KEY="your-key"

# With Llama (free)
mkdocs-ai generate "Docker guide" \
  -p openrouter \
  -m meta-llama/llama-4-maverick:free

# With DeepSeek (free)
mkdocs-ai generate "Docker guide" \
  -p openrouter \
  -m deepseek/deepseek-chat-v3.1:free
```

### Using Perplexity (Online Search)

```bash
export PERPLEXITY_API_KEY="your-key"

# Generate with online search
mkdocs-ai generate "Latest Docker features" -p perplexity
```

## Common Commands Reference

```bash
# Help
mkdocs-ai --help
mkdocs-ai generate --help

# Generate
mkdocs-ai generate "prompt" -p gemini
mkdocs-ai generate "prompt" -o output.md -p gemini

# Enhance
mkdocs-ai enhance file.md --preview -p gemini
mkdocs-ai enhance file.md --level light -p gemini
mkdocs-ai check-quality file.md -p gemini

# Search
mkdocs-ai build-search-index -p gemini
mkdocs-ai search "query" -k 10 -p gemini

# Assets
mkdocs-ai discover-assets
mkdocs-ai process-assets -t docker_compose -p gemini

# Cache
mkdocs-ai cache-stats
mkdocs-ai cache-clear
```

## Troubleshooting

### "API key not found"

```bash
# Check if set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your-key"

# Or pass directly
mkdocs-ai generate "test" --api-key "your-key" -p gemini
```

### "Provider error"

```bash
# Try with verbose flag
mkdocs-ai generate "test" -p gemini -v

# Try different provider
mkdocs-ai generate "test" -p openrouter -m meta-llama/llama-4-maverick:free
```

### "Command not found"

```bash
# Reinstall
pip install -e .

# Check installation
which mkdocs-ai
mkdocs-ai --version
```

## Next Steps

1. ✅ You've tested the CLI
2. 📖 Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed configuration
3. 🔧 Configure MkDocs plugin in `mkdocs.yml`
4. 📝 Generate documentation for your project
5. 🎨 Customize settings for your needs

## Security Reminder

- ✅ Use environment variables for API keys
- ✅ Add `.env` to `.gitignore` (already done)
- ❌ Never commit API keys to git
- ❌ Never share API keys in chat/email
- 🔄 Rotate keys regularly

## Getting Help

- **Setup issues**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Feature docs**: See `PRIORITY_*_COMPLETE.md` files
- **Examples**: Check `examples/` directory
- **Verbose mode**: Add `-v` to any command

---

**Ready to build amazing documentation!** 🚀

Start with: `mkdocs-ai generate "Your first prompt" -p gemini -v`
