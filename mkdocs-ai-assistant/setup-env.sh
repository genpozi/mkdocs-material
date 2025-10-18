#!/bin/bash
# MkDocs AI Assistant - Environment Setup Script
# This script helps you set up environment variables for testing

echo "=========================================="
echo "MkDocs AI Assistant - Environment Setup"
echo "=========================================="
echo ""

# Function to set environment variable
set_env_var() {
    local var_name=$1
    local var_value=$2
    
    if [ -n "$var_value" ]; then
        export $var_name="$var_value"
        echo "✓ $var_name set"
    else
        echo "✗ $var_name not set (skipped)"
    fi
}

# Prompt for API keys
echo "Enter your API keys (press Enter to skip):"
echo ""

read -p "Gemini API Key: " GEMINI_KEY
read -p "Perplexity API Key: " PERPLEXITY_KEY
read -p "OpenRouter API Key: " OPENROUTER_KEY

echo ""
echo "Setting environment variables..."
echo ""

# Set environment variables
set_env_var "GEMINI_API_KEY" "$GEMINI_KEY"
set_env_var "PERPLEXITY_API_KEY" "$PERPLEXITY_KEY"
set_env_var "OPENROUTER_API_KEY" "$OPENROUTER_KEY"

echo ""
echo "=========================================="
echo "Environment variables set for this session"
echo "=========================================="
echo ""
echo "To make these permanent, add to your shell config:"
echo ""
echo "  # For bash (~/.bashrc)"
if [ -n "$GEMINI_KEY" ]; then
    echo "  export GEMINI_API_KEY=\"$GEMINI_KEY\""
fi
if [ -n "$PERPLEXITY_KEY" ]; then
    echo "  export PERPLEXITY_API_KEY=\"$PERPLEXITY_KEY\""
fi
if [ -n "$OPENROUTER_KEY" ]; then
    echo "  export OPENROUTER_API_KEY=\"$OPENROUTER_KEY\""
fi
echo ""
echo "Or run: source setup-env.sh"
echo ""
echo "Test with: mkdocs-ai generate \"Test prompt\" -p gemini -v"
echo ""
