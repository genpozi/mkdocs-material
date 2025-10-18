#!/bin/bash
# MkDocs AI Assistant - Quick Test Script

echo "=========================================="
echo "MkDocs AI Assistant - Quick Test"
echo "=========================================="
echo ""

# Check if API keys are set
echo "Checking environment variables..."
echo ""

if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ] && [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "❌ No API keys found in environment"
    echo ""
    echo "Please set at least one API key:"
    echo "  export GEMINI_API_KEY=\"your-key\""
    echo "  export OPENROUTER_API_KEY=\"your-key\""
    echo "  export PERPLEXITY_API_KEY=\"your-key\""
    echo ""
    echo "Or run: source setup-env.sh"
    exit 1
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ GEMINI_API_KEY is set"
    PROVIDER="gemini"
fi

if [ -n "$PERPLEXITY_API_KEY" ]; then
    echo "✓ PERPLEXITY_API_KEY is set"
    PROVIDER="perplexity"
fi

if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "✓ OPENROUTER_API_KEY is set"
    PROVIDER="openrouter"
fi

echo ""
echo "=========================================="
echo "Running Tests"
echo "=========================================="
echo ""

# Test 1: CLI Help
echo "Test 1: CLI Help"
mkdocs-ai --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ CLI help works"
else
    echo "❌ CLI help failed"
fi
echo ""

# Test 2: Cache Stats
echo "Test 2: Cache Stats"
mkdocs-ai cache-stats > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Cache system works"
else
    echo "❌ Cache system failed"
fi
echo ""

# Test 3: Generate Test Document
echo "Test 3: Generate Test Document"
echo "Using provider: $PROVIDER"
echo ""

if [ "$PROVIDER" = "openrouter" ]; then
    mkdocs-ai generate "Write a one-sentence introduction to Docker" \
        -p openrouter \
        -m meta-llama/llama-4-maverick:free \
        -o test-output.md \
        -v
else
    mkdocs-ai generate "Write a one-sentence introduction to Docker" \
        -p $PROVIDER \
        -o test-output.md \
        -v
fi

if [ $? -eq 0 ] && [ -f "test-output.md" ]; then
    echo ""
    echo "✓ Document generation works!"
    echo ""
    echo "Generated content:"
    echo "---"
    cat test-output.md
    echo "---"
    echo ""
    rm test-output.md
else
    echo "❌ Document generation failed"
fi

echo ""
echo "=========================================="
echo "Test Complete"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Try: mkdocs-ai generate \"Your prompt here\""
echo "  2. Try: mkdocs-ai enhance docs/file.md --preview"
echo "  3. Try: mkdocs-ai build-search-index"
echo "  4. See SETUP_GUIDE.md for more examples"
echo ""
