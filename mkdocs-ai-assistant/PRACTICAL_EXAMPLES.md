# Practical Examples for Daily Use

This guide provides copy-paste-ready examples for your most common documentation tasks.

## Table of Contents

- [Homelab Documentation](#homelab-documentation)
- [Research Reports](#research-reports)
- [Quick Documentation Tasks](#quick-documentation-tasks)
- [Daily Workflows](#daily-workflows)

---

## Homelab Documentation

### Example 1: Document a New Service

**Scenario**: You just set up Plex Media Server and need documentation.

**Using the Template**:

```bash
# Generate from template with context file
mkdocs-ai generate \
  --template templates/homelab-service.md.j2 \
  --context examples/homelab-plex.yaml \
  --output docs/services/plex.md
```

**Result**: Complete service documentation with configuration, maintenance commands, and troubleshooting.

### Example 2: Quick Service Overview

**Scenario**: Need a quick overview of a service without a full template.

**Command**:

```bash
mkdocs-ai generate \
  --prompt "Document my Jellyfin media server running on port 8096 with Docker. Include setup, configuration, and common issues." \
  --output docs/services/jellyfin.md
```

### Example 3: Network Diagram Documentation

**Scenario**: Document your homelab network topology.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create documentation for my homelab network with the following:
- pfSense firewall (192.168.1.1)
- Proxmox host (192.168.1.10)
- TrueNAS storage (192.168.1.20)
- Docker host (192.168.1.30)
- VLAN 10 for IoT devices
- VLAN 20 for guest network
Include network diagram in Mermaid format, firewall rules, and VLAN configuration." \
  --output docs/network/topology.md
```

### Example 4: Backup Strategy Documentation

**Scenario**: Document your backup procedures.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a comprehensive backup strategy document for my homelab:
- Daily: Docker volumes to NAS
- Weekly: VM snapshots
- Monthly: Full system backup to cloud
- Retention: 7 daily, 4 weekly, 12 monthly
Include scripts, restore procedures, and testing schedule." \
  --output docs/operations/backup-strategy.md
```

### Example 5: Maintenance Runbook

**Scenario**: Create a monthly maintenance checklist.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a monthly homelab maintenance runbook including:
- Update all Docker containers
- Check disk health on NAS
- Review firewall logs
- Test backups
- Update documentation
- Security audit
Include commands and expected outputs." \
  --output docs/operations/monthly-maintenance.md
```

---

## Research Reports

### Example 1: Full Research Report from Template

**Scenario**: Starting a new research project on AI agents.

**Using the Template**:

```bash
# Generate from template with context
mkdocs-ai generate \
  --template templates/research-report.md.j2 \
  --context examples/research-ai-agents.yaml \
  --output research/ai-agents-comparison.md
```

**Result**: Complete research report structure with AI-generated sections for methodology, findings, and analysis.

### Example 2: Literature Review

**Scenario**: Need to review recent papers on a topic.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a literature review on 'Retrieval-Augmented Generation (RAG) systems' covering:
- Key papers from 2023-2024
- Main approaches and techniques
- Comparison of methods
- Current limitations
- Future directions
Format with proper citations." \
  --output research/rag-literature-review.md
```

### Example 3: Technology Evaluation

**Scenario**: Evaluating different database options for a project.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a technical evaluation comparing PostgreSQL, MongoDB, and Cassandra for a high-traffic web application:
- Performance characteristics
- Scalability options
- Operational complexity
- Cost analysis
- Use case fit
Include decision matrix and recommendation." \
  --output research/database-evaluation.md
```

### Example 4: Experiment Documentation

**Scenario**: Document a technical experiment you ran.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Document an experiment testing LLM performance on code generation:
- Hypothesis: Larger context windows improve code quality
- Method: Test GPT-4, Claude, and Llama on 50 coding tasks
- Metrics: Correctness, efficiency, maintainability
- Results: [I'll fill in actual data]
- Analysis and conclusions
Create structure with placeholders for data." \
  --output research/experiments/llm-context-experiment.md
```

### Example 5: Weekly Research Notes

**Scenario**: Capture weekly research progress.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a weekly research log template for tracking:
- Papers read this week
- Key insights and takeaways
- Experiments conducted
- Questions raised
- Next steps
Format as a structured weekly entry." \
  --output research/logs/week-$(date +%Y-%U).md
```

---

## Quick Documentation Tasks

### Example 1: API Documentation

**Scenario**: Document a REST API you built.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Document a REST API for a task management system with endpoints:
- GET /tasks - List all tasks
- POST /tasks - Create task
- GET /tasks/{id} - Get task details
- PUT /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task
Include request/response examples, authentication, and error codes." \
  --output docs/api/tasks-api.md
```

### Example 2: Configuration Guide

**Scenario**: Document configuration options for a tool.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a configuration guide for Nginx reverse proxy setup:
- SSL/TLS configuration
- Proxy headers
- Rate limiting
- Caching
- Security headers
Include example configs and explanations." \
  --output docs/guides/nginx-config.md
```

### Example 3: Troubleshooting Guide

**Scenario**: Create a troubleshooting guide for common issues.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a troubleshooting guide for Docker networking issues:
- Container can't reach internet
- Containers can't communicate
- Port mapping not working
- DNS resolution failures
- Bridge network issues
Include symptoms, diagnosis steps, and solutions." \
  --output docs/troubleshooting/docker-networking.md
```

### Example 4: Migration Guide

**Scenario**: Document a migration process.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create a migration guide from MySQL to PostgreSQL:
- Pre-migration checklist
- Schema conversion
- Data migration steps
- Application changes needed
- Testing procedures
- Rollback plan
Include scripts and timelines." \
  --output docs/guides/mysql-to-postgres-migration.md
```

### Example 5: Onboarding Documentation

**Scenario**: Create onboarding docs for a new team member.

**Prompt**:

```bash
mkdocs-ai generate \
  --prompt "Create developer onboarding documentation covering:
- Development environment setup
- Repository structure
- Build and test procedures
- Deployment process
- Code review guidelines
- Team communication channels
Include checklists and links." \
  --output docs/team/onboarding.md
```

---

## Daily Workflows

### Morning Documentation Routine

**Capture overnight thoughts**:

```bash
# Quick brain dump to documentation
mkdocs-ai generate \
  --prompt "Organize these thoughts into structured documentation: [paste your notes]" \
  --output docs/notes/$(date +%Y-%m-%d)-morning.md
```

### End-of-Day Capture

**Document what you learned today**:

```bash
# Create daily log
mkdocs-ai generate \
  --prompt "Create a daily log entry for $(date +%Y-%m-%d) covering:
- What I worked on
- Problems solved
- Lessons learned
- Tomorrow's priorities
Format as a structured daily note." \
  --output docs/logs/daily/$(date +%Y-%m-%d).md
```

### Weekly Review

**Generate weekly summary**:

```bash
# Summarize the week
mkdocs-ai generate \
  --prompt "Create a weekly review for week $(date +%U) of $(date +%Y):
- Major accomplishments
- Challenges faced
- Key decisions made
- Metrics and progress
- Next week's focus
Include sections for personal and professional growth." \
  --output docs/reviews/weekly/$(date +%Y-W%U).md
```

### Project Kickoff

**Start a new project with documentation**:

```bash
# Generate project structure
mkdocs-ai generate \
  --prompt "Create project documentation structure for [PROJECT_NAME]:
- Project overview and goals
- Technical architecture
- Development roadmap
- Team roles
- Success metrics
Include placeholders for detailed sections." \
  --output projects/[PROJECT_NAME]/README.md
```

### Meeting Notes Enhancement

**Turn rough notes into documentation**:

```bash
# Enhance meeting notes
mkdocs-ai generate \
  --prompt "Convert these meeting notes into structured documentation:
[paste your rough notes]

Include:
- Meeting summary
- Key decisions
- Action items with owners
- Follow-up questions
- Next steps" \
  --output docs/meetings/$(date +%Y-%m-%d)-[MEETING_NAME].md
```

---

## Advanced Patterns

### Batch Documentation Generation

**Document multiple services at once**:

```bash
# Create a script for batch generation
for service in plex jellyfin sonarr radarr; do
  mkdocs-ai generate \
    --prompt "Document my $service homelab service with Docker setup, configuration, and maintenance" \
    --output docs/services/$service.md
done
```

### Documentation with Context

**Use existing docs as context**:

```bash
# Generate related documentation
mkdocs-ai generate \
  --prompt "Based on my existing network documentation, create a security hardening guide for my homelab" \
  --output docs/security/hardening.md
```

### Template Customization

**Create your own templates**:

```bash
# Copy and customize existing template
cp templates/homelab-service.md.j2 templates/my-custom-service.md.j2

# Edit to match your needs
# Then use it:
mkdocs-ai generate \
  --template templates/my-custom-service.md.j2 \
  --context my-context.yaml \
  --output docs/my-service.md
```

### Incremental Documentation

**Add to existing docs with AI-GENERATE comments**:

```markdown
# My Existing Documentation

## Current Section
This is already documented.

## New Section
<!-- AI-GENERATE: Add a section about monitoring and alerting for this service -->

## Another Section
Already documented.
```

Then build:

```bash
cd docs && mkdocs build
```

---

## Tips for Better Results

### 1. Be Specific

❌ **Vague**: "Document my server"

✅ **Specific**: "Document my Ubuntu 22.04 server running Docker with Traefik reverse proxy, including SSL setup and container management"

### 2. Provide Context

❌ **No Context**: "Create API docs"

✅ **With Context**: "Create API documentation for a Python FastAPI application with JWT authentication, including request/response examples and error handling"

### 3. Specify Format

❌ **No Format**: "Document the process"

✅ **With Format**: "Document the deployment process as a step-by-step checklist with commands, expected outputs, and rollback procedures"

### 4. Include Examples

❌ **Abstract**: "Document configuration"

✅ **With Examples**: "Document Nginx configuration including this example: [paste your config], explain each directive and provide alternatives"

### 5. Request Structure

❌ **Unstructured**: "Write about backups"

✅ **Structured**: "Create backup documentation with sections: Strategy, Schedule, Retention, Restore Procedures, Testing, and Automation"

---

## Next Steps

1. **Try the examples** - Copy and adapt these commands for your needs
2. **Create your templates** - Build templates for your recurring documentation tasks
3. **Build your prompt library** - Save prompts that work well for you
4. **Automate** - Add documentation generation to your workflows
5. **Iterate** - Refine prompts based on results

For more examples, see:
- [DAILY_USE_GUIDE.md](DAILY_USE_GUIDE.md) - Comprehensive daily use patterns
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Technical reference
- [templates/](templates/) - Template examples
- [examples/](examples/) - Context file examples
