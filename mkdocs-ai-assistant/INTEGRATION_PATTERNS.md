# Integration Patterns

Practical patterns for integrating MkDocs AI Assistant into your daily workflows, development processes, and automation pipelines.

## Table of Contents

- [Daily Workflow Integration](#daily-workflow-integration)
- [Git Integration](#git-integration)
- [CI/CD Integration](#cicd-integration)
- [IDE Integration](#ide-integration)
- [Automation Scripts](#automation-scripts)
- [Scheduled Tasks](#scheduled-tasks)
- [Team Workflows](#team-workflows)

---

## Daily Workflow Integration

### Morning Documentation Routine

**Pattern**: Start each day by capturing overnight thoughts and planning documentation tasks.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/morning-docs.sh

DATE=$(date +%Y-%m-%d)
DOCS_DIR="$HOME/docs/daily"

# Create daily note
mkdocs-ai generate \
  --prompt "Create a daily planning document for $DATE with sections:
- Yesterday's accomplishments
- Today's priorities (top 3)
- Blockers and questions
- Notes and ideas
Format as a structured daily note with checkboxes for tasks." \
  --output "$DOCS_DIR/$DATE.md"

# Open in editor
$EDITOR "$DOCS_DIR/$DATE.md"
```

**Usage**:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias morning='~/bin/morning-docs.sh'

# Run each morning
morning
```

### End-of-Day Capture

**Pattern**: Capture learnings and progress at end of day.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/eod-capture.sh

DATE=$(date +%Y-%m-%d)
DOCS_DIR="$HOME/docs/daily"

echo "What did you work on today?"
read -r WORK

echo "What did you learn?"
read -r LEARNINGS

echo "Any blockers or questions?"
read -r BLOCKERS

mkdocs-ai generate \
  --prompt "Create an end-of-day summary for $DATE:

Work completed:
$WORK

Learnings:
$LEARNINGS

Blockers/Questions:
$BLOCKERS

Format as a structured daily log with sections for accomplishments, learnings, challenges, and tomorrow's priorities." \
  --output "$DOCS_DIR/$DATE-eod.md"

echo "Daily log saved to $DOCS_DIR/$DATE-eod.md"
```

**Usage**:
```bash
alias eod='~/bin/eod-capture.sh'
eod
```

### Quick Documentation Capture

**Pattern**: Quickly capture documentation ideas throughout the day.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/quick-doc.sh

TOPIC="$1"
NOTES="$2"
DOCS_DIR="$HOME/docs/inbox"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [ -z "$TOPIC" ]; then
  echo "Usage: quick-doc <topic> <notes>"
  exit 1
fi

mkdocs-ai generate \
  --prompt "Create documentation for: $TOPIC

Context: $NOTES

Include:
- Overview
- Key points
- Action items
- Related topics
- Tags for searchability" \
  --output "$DOCS_DIR/$TIMESTAMP-$TOPIC.md"

echo "Documentation saved to $DOCS_DIR/$TIMESTAMP-$TOPIC.md"
```

**Usage**:
```bash
quick-doc "nginx-config" "Figured out SSL redirect issue with proxy_set_header"
```

---

## Git Integration

### Pre-Commit Documentation

**Pattern**: Generate or update documentation before committing code changes.

**Implementation**:

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if any code files changed
CODE_CHANGES=$(git diff --cached --name-only | grep -E '\.(py|js|ts|go|java)$')

if [ -n "$CODE_CHANGES" ]; then
  echo "Code changes detected. Checking documentation..."
  
  # Check if corresponding docs exist
  for file in $CODE_CHANGES; do
    DOC_FILE="docs/$(dirname $file)/$(basename $file .${file##*.}).md"
    
    if [ ! -f "$DOC_FILE" ]; then
      echo "Missing documentation for $file"
      echo "Generate documentation? (y/n)"
      read -r RESPONSE
      
      if [ "$RESPONSE" = "y" ]; then
        mkdocs-ai generate \
          --prompt "Create documentation for $file based on the code changes. Include purpose, key functions/classes, usage examples, and any important notes." \
          --output "$DOC_FILE"
        
        git add "$DOC_FILE"
      fi
    fi
  done
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Post-Merge Documentation Update

**Pattern**: Update documentation after merging branches.

**Implementation**:

Create `.git/hooks/post-merge`:

```bash
#!/bin/bash
# .git/hooks/post-merge

# Get list of changed files
CHANGED_FILES=$(git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD)

# Check if any significant changes
if echo "$CHANGED_FILES" | grep -qE '\.(py|js|ts|go|java|yaml|json)$'; then
  echo "Significant changes detected. Consider updating documentation."
  echo "Run: mkdocs-ai generate --prompt 'Update documentation based on recent changes' --output docs/CHANGELOG.md"
fi
```

Make it executable:
```bash
chmod +x .git/hooks/post-merge
```

### Commit Message Enhancement

**Pattern**: Generate detailed commit messages from staged changes.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/smart-commit.sh

# Get diff of staged changes
DIFF=$(git diff --cached)

if [ -z "$DIFF" ]; then
  echo "No staged changes"
  exit 1
fi

# Generate commit message
mkdocs-ai generate \
  --prompt "Generate a conventional commit message for these changes:

$DIFF

Format:
<type>(<scope>): <subject>

<body>

<footer>

Follow conventional commits specification." \
  --output /tmp/commit-msg.txt

# Show generated message
cat /tmp/commit-msg.txt

echo ""
echo "Use this commit message? (y/n/e for edit)"
read -r RESPONSE

case $RESPONSE in
  y)
    git commit -F /tmp/commit-msg.txt
    ;;
  e)
    $EDITOR /tmp/commit-msg.txt
    git commit -F /tmp/commit-msg.txt
    ;;
  *)
    echo "Commit cancelled"
    ;;
esac

rm /tmp/commit-msg.txt
```

**Usage**:
```bash
git add .
smart-commit
```

### Pull Request Documentation

**Pattern**: Generate PR descriptions from branch changes.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/pr-description.sh

BRANCH=$(git branch --show-current)
BASE_BRANCH="${1:-main}"

# Get commits in this branch
COMMITS=$(git log $BASE_BRANCH..$BRANCH --oneline)

# Get diff summary
DIFF_STAT=$(git diff $BASE_BRANCH..$BRANCH --stat)

mkdocs-ai generate \
  --prompt "Generate a pull request description for branch '$BRANCH':

Commits:
$COMMITS

Changes:
$DIFF_STAT

Include:
- Summary of changes
- Motivation and context
- Type of change (feature/bugfix/refactor/docs)
- Testing done
- Checklist for reviewers
- Related issues

Format in GitHub markdown." \
  --output /tmp/pr-description.md

cat /tmp/pr-description.md

echo ""
echo "Copy to clipboard? (y/n)"
read -r RESPONSE

if [ "$RESPONSE" = "y" ]; then
  cat /tmp/pr-description.md | pbcopy  # macOS
  # cat /tmp/pr-description.md | xclip -selection clipboard  # Linux
  echo "Copied to clipboard"
fi
```

**Usage**:
```bash
pr-description main
```

---

## CI/CD Integration

### GitHub Actions Documentation

**Pattern**: Generate documentation as part of CI pipeline.

**Implementation**:

Create `.github/workflows/docs.yml`:

```yaml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install mkdocs-material
          pip install -e ./mkdocs-ai-assistant
      
      - name: Generate API documentation
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        run: |
          mkdocs-ai generate \
            --prompt "Generate API documentation from OpenAPI spec" \
            --output docs/api/reference.md
      
      - name: Build documentation
        run: mkdocs build
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### GitLab CI Documentation

**Pattern**: Generate and deploy documentation in GitLab CI.

**Implementation**:

Create `.gitlab-ci.yml`:

```yaml
stages:
  - generate
  - build
  - deploy

generate-docs:
  stage: generate
  image: python:3.11
  before_script:
    - pip install mkdocs-material
    - pip install -e ./mkdocs-ai-assistant
  script:
    - mkdocs-ai generate --prompt "Update API documentation" --output docs/api/reference.md
  artifacts:
    paths:
      - docs/
  only:
    - main

build-docs:
  stage: build
  image: python:3.11
  before_script:
    - pip install mkdocs-material
  script:
    - mkdocs build
  artifacts:
    paths:
      - site/
  only:
    - main

pages:
  stage: deploy
  script:
    - mv site public
  artifacts:
    paths:
      - public
  only:
    - main
```

### Documentation Validation

**Pattern**: Validate documentation completeness in CI.

**Implementation**:

```yaml
# .github/workflows/docs-validation.yml
name: Documentation Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Check for missing documentation
        run: |
          # Find code files without corresponding docs
          for file in $(find src -name "*.py"); do
            doc_file="docs/$(basename $file .py).md"
            if [ ! -f "$doc_file" ]; then
              echo "Missing documentation for $file"
              exit 1
            fi
          done
      
      - name: Validate documentation links
        run: |
          mkdocs build --strict
```

---

## IDE Integration

### VS Code Tasks

**Pattern**: Generate documentation from VS Code.

**Implementation**:

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Generate Documentation",
      "type": "shell",
      "command": "mkdocs-ai",
      "args": [
        "generate",
        "--prompt",
        "Document the current file",
        "--output",
        "docs/${fileBasenameNoExtension}.md"
      ],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Quick Doc Capture",
      "type": "shell",
      "command": "mkdocs-ai",
      "args": [
        "generate",
        "--prompt",
        "${input:docPrompt}",
        "--output",
        "docs/inbox/${input:docName}.md"
      ],
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "docPrompt",
      "type": "promptString",
      "description": "What do you want to document?"
    },
    {
      "id": "docName",
      "type": "promptString",
      "description": "Document name"
    }
  ]
}
```

**Usage**: `Cmd+Shift+P` → "Tasks: Run Task" → "Generate Documentation"

### VS Code Snippets

**Pattern**: Quick documentation generation snippets.

**Implementation**:

Create `.vscode/markdown.code-snippets`:

```json
{
  "AI Generate Section": {
    "prefix": "aigen",
    "body": [
      "<!-- AI-GENERATE: ${1:prompt} -->"
    ],
    "description": "Insert AI generation comment"
  },
  "AI Generate with Context": {
    "prefix": "aigenctx",
    "body": [
      "<!-- AI-GENERATE:",
      "Prompt: ${1:what to generate}",
      "Context: ${2:additional context}",
      "Format: ${3:format requirements}",
      "-->"
    ],
    "description": "Insert AI generation comment with context"
  }
}
```

### JetBrains IDE Integration

**Pattern**: External tools for documentation generation.

**Implementation**:

1. Go to Settings → Tools → External Tools
2. Add new tool:
   - Name: "Generate Documentation"
   - Program: `mkdocs-ai`
   - Arguments: `generate --prompt "Document $FileName$" --output docs/$FileNameWithoutExtension$.md`
   - Working directory: `$ProjectFileDir$`

**Usage**: Right-click file → External Tools → Generate Documentation

---

## Automation Scripts

### Batch Documentation Generation

**Pattern**: Generate documentation for multiple files/services.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/batch-docs.sh

SERVICES_DIR="$1"
DOCS_DIR="$2"

if [ -z "$SERVICES_DIR" ] || [ -z "$DOCS_DIR" ]; then
  echo "Usage: batch-docs.sh <services-dir> <docs-dir>"
  exit 1
fi

# Find all docker-compose files
find "$SERVICES_DIR" -name "docker-compose.yml" | while read -r compose_file; do
  service_name=$(basename $(dirname "$compose_file"))
  
  echo "Generating documentation for $service_name..."
  
  mkdocs-ai generate \
    --prompt "Document this Docker Compose service:

$(cat $compose_file)

Include:
- Service overview
- Container configuration
- Port mappings
- Volume mounts
- Environment variables
- Maintenance procedures" \
    --output "$DOCS_DIR/services/$service_name.md"
done

echo "Documentation generation complete!"
```

**Usage**:
```bash
batch-docs ~/homelab/services ~/homelab/docs
```

### Documentation Sync Script

**Pattern**: Keep documentation in sync with code changes.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/sync-docs.sh

PROJECT_DIR="$1"
DOCS_DIR="$2"

# Find recently modified code files
find "$PROJECT_DIR" -name "*.py" -mtime -7 | while read -r code_file; do
  doc_file="$DOCS_DIR/$(basename $code_file .py).md"
  
  # Check if doc is older than code
  if [ ! -f "$doc_file" ] || [ "$code_file" -nt "$doc_file" ]; then
    echo "Updating documentation for $code_file..."
    
    mkdocs-ai generate \
      --prompt "Update documentation for this code file:

$(cat $code_file)

Focus on recent changes and maintain existing structure." \
      --output "$doc_file"
  fi
done
```

**Usage**:
```bash
# Run weekly
sync-docs ~/projects/myapp ~/projects/myapp/docs
```

### Template-Based Generation

**Pattern**: Generate multiple documents from templates.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/template-docs.sh

TEMPLATE="$1"
CONTEXTS_DIR="$2"
OUTPUT_DIR="$3"

if [ -z "$TEMPLATE" ] || [ -z "$CONTEXTS_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: template-docs.sh <template> <contexts-dir> <output-dir>"
  exit 1
fi

# Process all YAML context files
find "$CONTEXTS_DIR" -name "*.yaml" | while read -r context_file; do
  output_name=$(basename "$context_file" .yaml)
  
  echo "Generating $output_name from template..."
  
  mkdocs-ai generate \
    --template "$TEMPLATE" \
    --context "$context_file" \
    --output "$OUTPUT_DIR/$output_name.md"
done

echo "Template-based generation complete!"
```

**Usage**:
```bash
template-docs templates/service.md.j2 contexts/services docs/services
```

---

## Scheduled Tasks

### Daily Documentation Digest

**Pattern**: Generate daily summary of documentation changes.

**Implementation**:

Create cron job:

```bash
# crontab -e
0 18 * * * /home/user/bin/daily-digest.sh
```

Script `~/bin/daily-digest.sh`:

```bash
#!/bin/bash

DOCS_DIR="$HOME/docs"
DATE=$(date +%Y-%m-%d)

# Find files modified today
MODIFIED=$(find "$DOCS_DIR" -name "*.md" -mtime -1)

if [ -n "$MODIFIED" ]; then
  mkdocs-ai generate \
    --prompt "Create a daily documentation digest for $DATE:

Modified files:
$MODIFIED

Include:
- Summary of changes
- Key updates
- Action items identified
- Documentation health metrics" \
    --output "$DOCS_DIR/digests/$DATE-digest.md"
  
  # Send notification
  echo "Daily documentation digest generated: $DOCS_DIR/digests/$DATE-digest.md"
fi
```

### Weekly Documentation Review

**Pattern**: Generate weekly documentation health report.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/weekly-review.sh

DOCS_DIR="$HOME/docs"
WEEK=$(date +%Y-W%U)

# Collect metrics
TOTAL_DOCS=$(find "$DOCS_DIR" -name "*.md" | wc -l)
UPDATED_THIS_WEEK=$(find "$DOCS_DIR" -name "*.md" -mtime -7 | wc -l)
STALE_DOCS=$(find "$DOCS_DIR" -name "*.md" -mtime +90 | wc -l)

mkdocs-ai generate \
  --prompt "Create a weekly documentation review for week $WEEK:

Metrics:
- Total documents: $TOTAL_DOCS
- Updated this week: $UPDATED_THIS_WEEK
- Stale documents (>90 days): $STALE_DOCS

Include:
- Documentation health summary
- Top contributors
- Most updated areas
- Areas needing attention
- Recommendations for next week" \
  --output "$DOCS_DIR/reviews/weekly-$WEEK.md"

echo "Weekly review generated: $DOCS_DIR/reviews/weekly-$WEEK.md"
```

**Cron**:
```bash
# crontab -e
0 9 * * 1 /home/user/bin/weekly-review.sh
```

### Monthly Documentation Audit

**Pattern**: Comprehensive monthly documentation audit.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/monthly-audit.sh

DOCS_DIR="$HOME/docs"
MONTH=$(date +%Y-%m)

# Comprehensive analysis
mkdocs-ai generate \
  --prompt "Create a comprehensive documentation audit for $MONTH:

Analyze:
- Documentation coverage
- Quality metrics
- Outdated content
- Missing documentation
- Usage patterns
- Improvement opportunities

Include:
- Executive summary
- Detailed findings
- Action items with priorities
- Resource requirements
- Success metrics" \
  --output "$DOCS_DIR/audits/audit-$MONTH.md"

echo "Monthly audit generated: $DOCS_DIR/audits/audit-$MONTH.md"
```

**Cron**:
```bash
# crontab -e
0 9 1 * * /home/user/bin/monthly-audit.sh
```

---

## Team Workflows

### Documentation Review Process

**Pattern**: Structured documentation review workflow.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/doc-review.sh

DOC_FILE="$1"
REVIEWER="$2"

if [ -z "$DOC_FILE" ] || [ -z "$REVIEWER" ]; then
  echo "Usage: doc-review.sh <doc-file> <reviewer>"
  exit 1
fi

# Generate review checklist
mkdocs-ai generate \
  --prompt "Create a documentation review checklist for:

$(cat $DOC_FILE)

Include:
- Accuracy check
- Completeness check
- Clarity and readability
- Technical correctness
- Examples and code samples
- Links and references
- Formatting and style
- Actionable feedback" \
  --output "/tmp/review-$(basename $DOC_FILE)"

# Send to reviewer
echo "Review checklist generated: /tmp/review-$(basename $DOC_FILE)"
echo "Assigned to: $REVIEWER"

# Create review issue/ticket
# gh issue create --title "Review: $DOC_FILE" --body "$(cat /tmp/review-$(basename $DOC_FILE))" --assignee "$REVIEWER"
```

### Documentation Sprint Planning

**Pattern**: Plan documentation sprints with AI assistance.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/doc-sprint.sh

SPRINT_GOAL="$1"
DURATION="$2"

mkdocs-ai generate \
  --prompt "Create a documentation sprint plan:

Goal: $SPRINT_GOAL
Duration: $DURATION

Include:
- Sprint objectives
- Documentation tasks breakdown
- Priority and effort estimates
- Resource allocation
- Success criteria
- Daily standup template
- Sprint retrospective template" \
  --output "docs/sprints/sprint-$(date +%Y-%m-%d).md"

echo "Sprint plan created: docs/sprints/sprint-$(date +%Y-%m-%d).md"
```

### Knowledge Transfer Sessions

**Pattern**: Generate documentation for knowledge transfer.

**Implementation**:

```bash
#!/bin/bash
# ~/bin/knowledge-transfer.sh

TOPIC="$1"
FROM_PERSON="$2"
TO_PERSON="$3"

mkdocs-ai generate \
  --prompt "Create a knowledge transfer document for: $TOPIC

From: $FROM_PERSON
To: $TO_PERSON

Include:
- Topic overview
- Key concepts and terminology
- Step-by-step procedures
- Common scenarios and solutions
- Resources and references
- Hands-on exercises
- Q&A section
- Follow-up checklist" \
  --output "docs/knowledge-transfer/$TOPIC-$(date +%Y-%m-%d).md"

echo "Knowledge transfer document created"
```

---

## Best Practices

### 1. Start Small

Begin with one integration pattern and expand gradually:
- Week 1: Daily capture scripts
- Week 2: Git hooks
- Week 3: CI/CD integration
- Week 4: Team workflows

### 2. Make It Easy

Reduce friction with aliases and shortcuts:

```bash
# ~/.bashrc or ~/.zshrc
alias doc='mkdocs-ai generate --prompt'
alias qdoc='~/bin/quick-doc.sh'
alias morning='~/bin/morning-docs.sh'
alias eod='~/bin/eod-capture.sh'
```

### 3. Automate Repetitive Tasks

Identify documentation tasks you do repeatedly and automate them.

### 4. Version Control Integration

Always integrate with your version control workflow to maintain documentation history.

### 5. Team Alignment

Ensure team members understand and adopt the integration patterns.

### 6. Monitor and Iterate

Track which integrations are used and refine based on feedback.

### 7. Documentation for Integrations

Document your integration patterns so others can adopt them.

---

## Next Steps

1. **Choose one pattern** to implement this week
2. **Test and refine** based on your workflow
3. **Share with team** and gather feedback
4. **Expand gradually** to more integration points
5. **Document your patterns** for future reference

For more examples, see:
- [PRACTICAL_EXAMPLES.md](PRACTICAL_EXAMPLES.md) - Usage examples
- [DAILY_USE_GUIDE.md](DAILY_USE_GUIDE.md) - Daily workflow patterns
- [AUTOMATION_EXAMPLES.md](AUTOMATION_EXAMPLES.md) - Advanced automation
