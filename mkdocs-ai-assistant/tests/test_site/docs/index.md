# MkDocs AI Assistant Test Site

Welcome to the test site for the MkDocs AI Assistant plugin!

## What is MkDocs AI Assistant?

MkDocs AI Assistant is a powerful plugin that brings AI capabilities to your MkDocs documentation:

- **Document Generation**: Create documentation from prompts, templates, or assets
- **Content Enhancement**: Automatically improve grammar, clarity, and consistency
- **Semantic Search**: Find content using natural language queries
- **Asset Processing**: Generate docs from code, Docker Compose files, and more
- **Obelisk Integration**: Connect with Obelisk for RAG-powered chatbot

## Quick Example

Try the AI generation feature with markdown syntax:

<!-- AI-GENERATE: Write a brief introduction to Docker Compose for beginners -->

## Features

### Priority 1: Document Generation

Generate documentation using multiple methods:

```bash
# CLI generation
mkdocs ai generate "Create a guide to Kubernetes basics"

# Markdown syntax
<!-- AI-GENERATE: Explain microservices architecture -->

# Config-based batch generation
# See mkdocs.yml for examples
```

### Priority 2: Content Enhancement

Automatically improve your documentation:

- Grammar and spelling corrections
- Clarity improvements
- Consistency checking
- SEO optimization

### Priority 3: Semantic Search

Find content using natural language:

- Build-time embedding generation
- Hybrid search (keyword + semantic)
- Portable JSON index

### Priority 4: Asset Processing

Generate documentation from:

- Docker Compose files
- Source code (Python, JavaScript, etc.)
- OpenAPI specifications
- And more!

### Priority 5: Obelisk Integration

Connect with Obelisk for advanced features:

- RAG-powered chatbot
- Conversational documentation search
- FAQ generation from user questions

## Getting Started

1. [Install the plugin](getting-started/installation.md)
2. [Configure your site](getting-started/quick-start.md)
3. [Explore features](features/generation.md)
4. [See examples](examples/basic.md)

## Architecture

The plugin is built with a modular architecture:

```
mkdocs_ai/
├── providers/       # AI provider abstraction (OpenRouter, Gemini, Ollama)
├── generation/      # Document generation engine
├── enhancement/     # Content enhancement features
├── search/          # Semantic search integration
├── assets/          # Asset-to-docs processors
├── cache/           # Response caching system
└── obelisk/         # Obelisk integration layer
```

## Provider Support

- **OpenRouter**: Multi-model access (primary)
- **Gemini**: Google's models (testing)
- **Anthropic**: Claude models (direct)
- **Ollama**: Local LLM support (future)

## Development Status

This is an active development project. Current phase:

- [x] Project structure
- [x] Provider abstraction
- [x] Configuration system
- [x] Caching layer
- [ ] Document generation (in progress)
- [ ] Content enhancement
- [ ] Semantic search
- [ ] Asset processing
- [ ] Obelisk integration

## Contributing

This is a personal project but contributions are welcome! See the main README for details.

## License

MIT License - See LICENSE file for details.
