# Quick Start Guide

## Installation

```bash
cd /workspaces/mkdocs-material/mkdocs-ai-assistant
pip install -e .
```

## Test the Plugin

```bash
cd tests/test_site
mkdocs build
```

**Expected Output**:
```
INFO - Cache initialized at .ai-cache
ERROR - Failed to initialize AI provider: API key required
WARNING - AI features will be disabled
INFO - Documentation built in 0.19 seconds
```

This is correct! The plugin works, it just needs an API key.

## Add API Key

```bash
export OPENROUTER_API_KEY="your-key-here"
# or
export GEMINI_API_KEY="your-key-here"
```

## Use in Your Project

Add to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - ai-assistant:
      provider:
        name: openrouter  # or gemini, anthropic, ollama
        api_key: !ENV OPENROUTER_API_KEY
        model: anthropic/claude-3.5-sonnet
      
      cache:
        enabled: true
        dir: .ai-cache
      
      generation:
        enabled: true
```

## What Works Now

✅ Plugin installation  
✅ Configuration loading  
✅ Provider initialization  
✅ Caching system  
✅ MkDocs integration  
✅ Graceful error handling  

## What's Coming Next

🚧 Document generation (Priority 1)  
🚧 Content enhancement (Priority 2)  
🚧 Semantic search (Priority 3)  
🚧 Asset processing (Priority 4)  
🚧 Obelisk integration (Priority 5)  

## File Structure

```
mkdocs-ai-assistant/
├── mkdocs_ai/              # Main package
│   ├── plugin.py          # Main plugin
│   ├── config.py          # Configuration
│   ├── providers/         # AI providers (4 implemented)
│   └── cache/             # Caching system
│
├── tests/test_site/       # Test site
│   ├── mkdocs.yml        # Example config
│   └── docs/             # Documentation
│
├── README.md              # Full documentation
├── IMPLEMENTATION_STATUS.md  # Detailed status
├── SESSION_SUMMARY.md     # What we built
└── QUICK_START.md         # This file
```

## Key Files to Read

1. **README.md** - Complete overview
2. **IMPLEMENTATION_STATUS.md** - Current status
3. **SESSION_SUMMARY.md** - Session recap
4. **mkdocs_ai/plugin.py** - Main code
5. **tests/test_site/mkdocs.yml** - Config example

## Supported Providers

| Provider | Status | Use Case |
|----------|--------|----------|
| OpenRouter | ✅ Ready | Production (recommended) |
| Gemini | ✅ Ready | Testing/development |
| Anthropic | ✅ Ready | Direct Claude access |
| Ollama | ✅ Ready | Local LLM (future) |

## Configuration Options

See `mkdocs_ai/config.py` for all options.

Key settings:
- `provider.name` - Which AI service to use
- `provider.model` - Which model to use
- `cache.enabled` - Enable caching (recommended)
- `generation.enabled` - Enable document generation
- `debug` - Enable debug logging

## Next Steps

1. Review the documentation files
2. Test with your API keys
3. Wait for Priority 1 implementation (document generation)
4. Start using for your research and homelab docs

## Questions?

See the comprehensive documentation in:
- README.md
- IMPLEMENTATION_STATUS.md
- SESSION_SUMMARY.md

## Status

**Foundation**: ✅ Complete  
**Features**: 🚧 Coming soon  
**Ready to use**: Yes (with API key)  
**Production ready**: Not yet (features pending)  

---

**Last Updated**: October 17, 2025
