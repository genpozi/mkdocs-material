# MkDocs AI Assistant

AI-powered document generation, enhancement, and semantic search for MkDocs.

## Features

### Priority 1: Document Generation
- **CLI Generation**: `mkdocs ai generate "Create Docker Compose guide"`
- **Markdown Syntax**: `<!-- AI-GENERATE: Explain Kubernetes concepts -->`
- **Template-Based**: Use Jinja2 templates with AI filling
- **Batch Generation**: Define generation tasks in config

### Priority 2: Content Enhancement
- **Automatic Enhancement**: Improve grammar, clarity, and consistency
- **Preserve Code**: Never modifies code blocks or frontmatter
- **Configurable**: Choose enhancement features per project

### Priority 3: Semantic Search
- **Build-Time Embeddings**: Generate embeddings during build
- **Hybrid Search**: Combines with Material's keyword search
- **Portable**: JSON-based index, no external dependencies

### Priority 4: Asset Processing
- **Docker Compose → Docs**: Automatic documentation from compose files
- **Code → Docs**: Generate API documentation from source code
- **Auto-Discovery**: Finds and processes assets automatically

### Priority 5: Obelisk Integration
- **RAG Chatbot**: Integrate with Obelisk for powerful Q&A
- **Export Format**: Compatible with Obelisk's document format
- **Optional**: Works standalone or with Obelisk

## Installation

```bash
cd mkdocs-ai-assistant
pip install -e .
```

## Quick Start

### 1. Set Up API Keys

**IMPORTANT**: Never commit API keys to git! Use environment variables.

```bash
# Set environment variables (recommended)
export GEMINI_API_KEY="your-gemini-key"
export OPENROUTER_API_KEY="your-openrouter-key"
export PERPLEXITY_API_KEY="your-perplexity-key"

# Or use the setup script
source setup-env.sh

# Test the setup
./test-setup.sh
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

### 2. Configure Plugin

```yaml
# mkdocs.yml
plugins:
  - ai-assistant:
      provider:
        name: gemini  # or openrouter, perplexity
        api_key: !ENV GEMINI_API_KEY  # Use environment variable!
        model: anthropic/claude-3.5-sonnet
      
      generation:
        enabled: true
      
      enhancement:
        enabled: true
        auto_enhance: true
```

### 2. Generate Documents

**CLI:**
```bash
mkdocs ai generate "Create a comprehensive guide to Docker Compose"
```

**Markdown:**
```markdown
<!-- AI-GENERATE: Explain the benefits of using MkDocs for documentation -->
```

**Config:**
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

### 3. Enhance Content

Content is automatically enhanced during build when `auto_enhance: true`.

## Configuration

### Provider Options

**OpenRouter (Recommended):**
```yaml
provider:
  name: openrouter
  api_key: !ENV OPENROUTER_API_KEY
  model: anthropic/claude-3.5-sonnet
  fallback: google/gemini-pro
```

**Gemini (Testing):**
```yaml
provider:
  name: gemini
  api_key: !ENV GEMINI_API_KEY
  model: gemini-pro
```

**Ollama (Local):**
```yaml
provider:
  name: ollama
  base_url: http://localhost:11434
  model: llama3.2
```

### Caching

```yaml
cache:
  enabled: true
  dir: .ai-cache
  ttl: 86400  # 24 hours
```

### Enhancement Features

```yaml
enhancement:
  enabled: true
  auto_enhance: true
  features:
    - grammar      # Fix grammar and spelling
    - clarity      # Improve readability
    - consistency  # Ensure consistent terminology
  preserve_code: true
  preserve_frontmatter: true
```

### Asset Processing

```yaml
assets:
  enabled: true
  sources:
    - type: docker-compose
      path: ../homelab
      pattern: "**/*compose*.yml"
      output_dir: docs/homelab
    
    - type: code
      path: ../src
      languages: [python, javascript]
      output_dir: docs/api
```

## Architecture

### Modular Design

```
mkdocs_ai/
├── providers/       # AI provider abstraction
├── generation/      # Document generation
├── enhancement/     # Content enhancement
├── search/          # Semantic search
├── assets/          # Asset processing
├── cache/           # Caching system
└── obelisk/         # Obelisk integration
```

### Provider Abstraction

All AI providers implement a common interface:

```python
class AIProvider(ABC):
    async def generate(self, prompt: str, **kwargs) -> str
    async def embed(self, text: str) -> list[float]
    def supports_streaming(self) -> bool
```

Supported providers:
- **OpenRouter**: Multi-model access (primary)
- **Gemini**: Google's models (testing)
- **Anthropic**: Claude models
- **Ollama**: Local LLM support (future)

### Extension Points

The plugin is designed for future expansion:

1. **Custom Providers**: Add new AI providers by subclassing `AIProvider`
2. **Enhancement Plugins**: Add custom enhancement features
3. **Asset Processors**: Support new asset types
4. **Search Backends**: Integrate different vector databases

## Development

### Setup

```bash
cd mkdocs-ai-assistant
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

### Code Quality

```bash
black mkdocs_ai/
ruff check mkdocs_ai/
mypy mkdocs_ai/
```

## Roadmap

### Phase 1: MVP (Current)
- [x] Project structure
- [x] Provider abstraction
- [ ] Document generation (CLI + markdown)
- [ ] Basic caching
- [ ] Test site

### Phase 2: Enhancement
- [ ] Content enhancement engine
- [ ] Grammar and clarity improvements
- [ ] Consistency checking

### Phase 3: Search
- [ ] Semantic search integration
- [ ] Embedding generation
- [ ] Hybrid search with Material

### Phase 4: Assets
- [ ] Docker Compose processor
- [ ] Code documentation generator
- [ ] Auto-discovery system

### Phase 5: Obelisk
- [ ] Export format compatibility
- [ ] API client integration
- [ ] Chatbot backend

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! This is a personal project but open to improvements.

## Future Opportunities

Areas identified for future development:

1. **Streaming Generation**: Real-time document generation with progress
2. **Interactive Mode**: Review and approve AI changes before applying
3. **Batch Processing**: Parallel generation for multiple documents
4. **Template Library**: Pre-built templates for common documentation types
5. **Quality Scoring**: AI-powered documentation quality assessment
6. **Translation**: Multi-language documentation generation
7. **Version Control Integration**: Git-aware enhancement and generation
8. **Analytics**: Track AI usage and cost optimization
9. **Custom Models**: Fine-tuned models for specific documentation styles
10. **Collaborative Features**: Team-based AI assistance workflows
