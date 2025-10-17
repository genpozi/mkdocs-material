# Prompt Library

A curated collection of proven prompts for the MkDocs AI Assistant, organized by category and outcome.

## Table of Contents

- [Documentation Structure](#documentation-structure)
- [Technical Documentation](#technical-documentation)
- [Homelab & Infrastructure](#homelab--infrastructure)
- [Research & Analysis](#research--analysis)
- [Development & Code](#development--code)
- [Operations & DevOps](#operations--devops)
- [Team & Process](#team--process)
- [Learning & Knowledge](#learning--knowledge)
- [Prompt Engineering Tips](#prompt-engineering-tips)

---

## Documentation Structure

### Create Documentation Outline

**Purpose**: Generate a structured outline for complex documentation.

**Prompt**:
```
Create a comprehensive documentation outline for [TOPIC] including:
- Table of contents with 3 levels
- Main sections with brief descriptions
- Suggested subsections
- Placeholders for examples and diagrams
- Cross-reference suggestions
```

**Best For**: Starting large documentation projects, ensuring complete coverage.

### Convert Notes to Documentation

**Purpose**: Transform rough notes into structured documentation.

**Prompt**:
```
Convert these rough notes into structured documentation:

[PASTE YOUR NOTES]

Organize into:
- Clear sections with headings
- Bullet points for key information
- Code blocks for technical content
- Tables for comparisons
- Action items highlighted
```

**Best For**: Daily knowledge capture, meeting notes, brainstorming sessions.

### Enhance Existing Documentation

**Purpose**: Improve clarity and completeness of existing docs.

**Prompt**:
```
Enhance this documentation by:
- Adding missing sections
- Improving clarity and structure
- Adding examples where helpful
- Including troubleshooting tips
- Suggesting related topics

Current documentation:
[PASTE EXISTING DOCS]
```

**Best For**: Documentation maintenance, improving legacy docs.

### Create Documentation Template

**Purpose**: Build reusable templates for consistent documentation.

**Prompt**:
```
Create a Jinja2 template for [DOCUMENT TYPE] documentation including:
- Standard sections with placeholders
- Variable substitution for common fields
- Optional sections with conditionals
- Example usage in comments
- Validation requirements
```

**Best For**: Standardizing documentation across projects or teams.

---

## Technical Documentation

### API Documentation

**Purpose**: Document REST APIs comprehensively.

**Prompt**:
```
Document a REST API for [SERVICE] with the following endpoints:
[LIST ENDPOINTS]

Include for each endpoint:
- HTTP method and path
- Description and purpose
- Request parameters (path, query, body)
- Request example with curl
- Response format and status codes
- Response example (success and error)
- Authentication requirements
- Rate limiting
- Common errors and solutions
```

**Best For**: Backend services, microservices, public APIs.

### Configuration Documentation

**Purpose**: Document configuration options and settings.

**Prompt**:
```
Document configuration for [TOOL/SERVICE] including:
- Configuration file format and location
- All available options with descriptions
- Default values and valid ranges
- Example configurations for common scenarios
- Environment variable alternatives
- Configuration validation
- Troubleshooting configuration issues
```

**Best For**: Tools, services, applications with complex configuration.

### Architecture Documentation

**Purpose**: Document system architecture and design.

**Prompt**:
```
Document the architecture for [SYSTEM] including:
- High-level overview with Mermaid diagram
- Component descriptions and responsibilities
- Data flow between components
- Technology stack with versions
- Design decisions and trade-offs
- Scalability considerations
- Security architecture
- Deployment architecture
```

**Best For**: System design, architectural reviews, onboarding.

### Database Schema Documentation

**Purpose**: Document database structure and relationships.

**Prompt**:
```
Document the database schema for [DATABASE] including:
- Entity-relationship diagram in Mermaid
- Table descriptions and purposes
- Column definitions with types and constraints
- Indexes and their rationale
- Foreign key relationships
- Common queries and their purposes
- Migration strategy
- Performance considerations
```

**Best For**: Database design, data modeling, team alignment.

### Integration Documentation

**Purpose**: Document integrations between systems.

**Prompt**:
```
Document the integration between [SYSTEM A] and [SYSTEM B] including:
- Integration overview and purpose
- Data flow diagram
- Authentication and authorization
- API endpoints or message formats used
- Error handling and retry logic
- Monitoring and alerting
- Troubleshooting common issues
- Testing the integration
```

**Best For**: Microservices, third-party integrations, system boundaries.

---

## Homelab & Infrastructure

### Service Documentation

**Purpose**: Document homelab services comprehensively.

**Prompt**:
```
Document my [SERVICE] homelab service including:
- Service overview and purpose
- Docker/container configuration
- Port mappings and networking
- Volume mounts and data persistence
- Environment variables
- Access URLs and credentials location
- Backup procedures
- Update procedures
- Common troubleshooting issues
- Resource requirements
```

**Best For**: Docker services, VMs, homelab applications.

### Network Documentation

**Purpose**: Document network topology and configuration.

**Prompt**:
```
Document my homelab network including:
- Network topology diagram in Mermaid
- IP address allocation table
- VLAN configuration and purposes
- Firewall rules by zone
- DNS configuration
- DHCP reservations
- Port forwarding rules
- VPN configuration
- Network security measures
```

**Best For**: Network planning, troubleshooting, security audits.

### Hardware Inventory

**Purpose**: Track hardware assets and specifications.

**Prompt**:
```
Create hardware inventory documentation for my homelab including:
- Server specifications table (CPU, RAM, storage)
- Network equipment list
- Purchase dates and warranties
- Power consumption estimates
- Rack layout diagram
- Upgrade history
- Planned upgrades
- Replacement schedule
```

**Best For**: Asset management, capacity planning, budgeting.

### Backup Strategy

**Purpose**: Document backup and recovery procedures.

**Prompt**:
```
Create comprehensive backup documentation including:
- Backup strategy overview
- What is backed up and why
- Backup schedule (daily, weekly, monthly)
- Retention policy
- Backup locations and redundancy
- Backup scripts and automation
- Restore procedures with examples
- Testing schedule and results
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
```

**Best For**: Data protection, disaster recovery, compliance.

### Maintenance Runbook

**Purpose**: Create standardized maintenance procedures.

**Prompt**:
```
Create a [FREQUENCY] maintenance runbook for my homelab including:
- Checklist of tasks to perform
- Commands to run with expected outputs
- Health checks and metrics to review
- Update procedures for services
- Log review procedures
- Backup verification
- Security checks
- Documentation updates
- Estimated time for completion
```

**Best For**: Regular maintenance, system health, preventing issues.

---

## Research & Analysis

### Literature Review

**Purpose**: Synthesize research papers on a topic.

**Prompt**:
```
Create a literature review on [TOPIC] covering:
- Overview of the research area
- Key papers and their contributions (last 2-3 years)
- Main approaches and methodologies
- Comparison of different methods
- Current state of the art
- Open challenges and limitations
- Future research directions
- Bibliography in APA format
```

**Best For**: Academic research, technology evaluation, staying current.

### Technology Comparison

**Purpose**: Compare technologies for decision-making.

**Prompt**:
```
Create a technical comparison of [OPTION A] vs [OPTION B] vs [OPTION C] for [USE CASE] including:
- Feature comparison table
- Performance characteristics
- Scalability considerations
- Operational complexity
- Cost analysis (licensing, infrastructure, maintenance)
- Community and ecosystem
- Learning curve
- Use case fit analysis
- Decision matrix with weighted criteria
- Recommendation with rationale
```

**Best For**: Technology selection, architectural decisions, vendor evaluation.

### Experiment Documentation

**Purpose**: Document technical experiments systematically.

**Prompt**:
```
Document an experiment testing [HYPOTHESIS] including:
- Research question
- Hypothesis
- Methodology and approach
- Test environment and setup
- Variables and controls
- Metrics and measurement methods
- Data collection procedures
- Results section (with placeholders for data)
- Analysis and interpretation
- Conclusions and implications
- Limitations
- Future experiments
```

**Best For**: Performance testing, proof of concepts, research validation.

### Competitive Analysis

**Purpose**: Analyze competitors or alternatives.

**Prompt**:
```
Create a competitive analysis for [PRODUCT/SERVICE] comparing:
- Feature comparison matrix
- Pricing comparison
- Target market and positioning
- Strengths and weaknesses
- Market share and trends
- Customer reviews and sentiment
- Technology stack (if known)
- Differentiation opportunities
- Threat assessment
- Strategic recommendations
```

**Best For**: Product planning, market research, strategic planning.

### Trend Analysis

**Purpose**: Analyze trends in technology or industry.

**Prompt**:
```
Create a trend analysis for [TOPIC/INDUSTRY] including:
- Current state overview
- Historical context and evolution
- Emerging trends and drivers
- Key players and innovations
- Adoption patterns
- Challenges and barriers
- Future predictions (1, 3, 5 years)
- Implications for [YOUR CONTEXT]
- Recommendations for action
```

**Best For**: Strategic planning, technology adoption, staying ahead.

---

## Development & Code

### Code Documentation

**Purpose**: Document code structure and patterns.

**Prompt**:
```
Document the codebase for [PROJECT] including:
- Project structure overview
- Key components and their responsibilities
- Design patterns used
- Code organization principles
- Important classes/functions with examples
- Configuration and environment setup
- Build and test procedures
- Deployment process
- Contributing guidelines
- Code style and conventions
```

**Best For**: Open source projects, team onboarding, code handoff.

### Migration Guide

**Purpose**: Document migration between systems or versions.

**Prompt**:
```
Create a migration guide from [OLD] to [NEW] including:
- Migration overview and rationale
- Pre-migration checklist
- Compatibility assessment
- Step-by-step migration procedure
- Data migration approach
- Code changes required
- Configuration changes
- Testing procedures
- Rollback plan
- Timeline and milestones
- Risk mitigation
- Post-migration validation
```

**Best For**: System upgrades, platform changes, refactoring.

### Troubleshooting Guide

**Purpose**: Document common issues and solutions.

**Prompt**:
```
Create a troubleshooting guide for [SYSTEM/SERVICE] covering:
- Common issues organized by category
- For each issue:
  - Symptoms and error messages
  - Root cause explanation
  - Diagnostic steps
  - Solution with commands/code
  - Prevention measures
- Debugging techniques
- Log locations and what to look for
- Performance troubleshooting
- When to escalate
```

**Best For**: Support documentation, reducing repeated issues, knowledge retention.

### Release Notes

**Purpose**: Document changes in a release.

**Prompt**:
```
Create release notes for [PROJECT] version [VERSION] including:
- Release summary and highlights
- New features with descriptions
- Improvements and enhancements
- Bug fixes
- Breaking changes and migration guide
- Deprecations
- Known issues
- Upgrade instructions
- Contributors acknowledgment
```

**Best For**: Software releases, changelog maintenance, user communication.

### Code Review Checklist

**Purpose**: Standardize code review process.

**Prompt**:
```
Create a code review checklist for [LANGUAGE/FRAMEWORK] including:
- Code quality checks
- Design and architecture review
- Security considerations
- Performance implications
- Testing requirements
- Documentation requirements
- Error handling
- Code style and conventions
- Dependency management
- Backward compatibility
```

**Best For**: Team standards, quality assurance, consistent reviews.

---

## Operations & DevOps

### Runbook Creation

**Purpose**: Create operational procedures.

**Prompt**:
```
Create an operational runbook for [TASK] including:
- Task overview and purpose
- Prerequisites and permissions needed
- Step-by-step procedure with commands
- Expected outputs at each step
- Verification steps
- Rollback procedure if needed
- Troubleshooting common issues
- Estimated time to complete
- Risk assessment
- Approval requirements
```

**Best For**: Production operations, routine tasks, delegation.

### Incident Response

**Purpose**: Document incident response procedures.

**Prompt**:
```
Create an incident response playbook for [INCIDENT TYPE] including:
- Incident detection and alerting
- Initial assessment and triage
- Severity classification
- Response team and roles
- Investigation steps
- Mitigation and resolution steps
- Communication plan (internal and external)
- Post-incident review template
- Prevention measures
- Escalation paths
```

**Best For**: Production incidents, on-call procedures, disaster recovery.

### Deployment Documentation

**Purpose**: Document deployment procedures.

**Prompt**:
```
Create deployment documentation for [SERVICE] including:
- Deployment overview and architecture
- Pre-deployment checklist
- Environment preparation
- Deployment steps with commands
- Configuration management
- Database migrations
- Smoke tests and verification
- Monitoring and alerting setup
- Rollback procedure
- Post-deployment validation
- Troubleshooting deployment issues
```

**Best For**: Production deployments, CI/CD, release management.

### Monitoring Documentation

**Purpose**: Document monitoring and alerting setup.

**Prompt**:
```
Document monitoring for [SERVICE] including:
- Monitoring architecture overview
- Metrics collected and their meaning
- Alert definitions and thresholds
- Alert routing and escalation
- Dashboard descriptions
- Log aggregation and analysis
- Performance baselines
- Capacity planning metrics
- Alert response procedures
- Monitoring tool configuration
```

**Best For**: Observability, SRE practices, on-call support.

### Disaster Recovery Plan

**Purpose**: Document disaster recovery procedures.

**Prompt**:
```
Create a disaster recovery plan for [SYSTEM] including:
- Disaster scenarios and impact assessment
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)
- Backup and restore procedures
- Failover procedures
- Communication plan
- Team roles and responsibilities
- Step-by-step recovery procedures
- Testing schedule and results
- Plan maintenance and updates
```

**Best For**: Business continuity, compliance, risk management.

---

## Team & Process

### Onboarding Documentation

**Purpose**: Create comprehensive onboarding guides.

**Prompt**:
```
Create developer onboarding documentation including:
- Welcome and team introduction
- Development environment setup (step-by-step)
- Repository structure and navigation
- Development workflow and branching strategy
- Build, test, and deployment procedures
- Code review process
- Communication channels and tools
- Team practices and conventions
- Resources and documentation links
- First week checklist
- 30-60-90 day goals
```

**Best For**: New hires, contractors, team growth.

### Process Documentation

**Purpose**: Document team processes and workflows.

**Prompt**:
```
Document the [PROCESS NAME] process including:
- Process overview and purpose
- When to use this process
- Roles and responsibilities
- Step-by-step workflow with decision points
- Tools and systems used
- Templates and examples
- Success criteria
- Common pitfalls and how to avoid them
- Process metrics and KPIs
- Process improvement suggestions
```

**Best For**: Team alignment, process improvement, scaling teams.

### Decision Record (ADR)

**Purpose**: Document architectural and technical decisions.

**Prompt**:
```
Create an Architecture Decision Record (ADR) for [DECISION] including:
- Title and status (proposed/accepted/deprecated)
- Context and problem statement
- Decision drivers and constraints
- Options considered with pros/cons
- Decision and rationale
- Consequences (positive and negative)
- Implementation notes
- Related decisions
- Date and decision makers
```

**Best For**: Architectural decisions, technical choices, team alignment.

### Meeting Template

**Purpose**: Structure recurring meetings.

**Prompt**:
```
Create a meeting template for [MEETING TYPE] including:
- Meeting purpose and goals
- Agenda with time allocations
- Pre-meeting preparation
- Discussion topics with prompts
- Decision-making framework
- Action items template
- Follow-up procedures
- Success metrics
- Meeting notes structure
```

**Best For**: Recurring meetings, team rituals, effective meetings.

### Team Charter

**Purpose**: Define team mission and ways of working.

**Prompt**:
```
Create a team charter for [TEAM NAME] including:
- Team mission and purpose
- Team goals and objectives
- Team values and principles
- Roles and responsibilities
- Communication norms
- Decision-making process
- Conflict resolution
- Meeting cadence
- Success metrics
- Team agreements
```

**Best For**: New teams, team alignment, culture building.

---

## Learning & Knowledge

### Learning Plan

**Purpose**: Create structured learning paths.

**Prompt**:
```
Create a learning plan for [TOPIC/SKILL] including:
- Learning objectives and goals
- Prerequisites and current knowledge assessment
- Learning resources (courses, books, tutorials)
- Hands-on projects and exercises
- Milestones and checkpoints
- Time estimates for each phase
- Practice and reinforcement activities
- Assessment methods
- Next steps after completion
```

**Best For**: Skill development, career growth, team training.

### Concept Explanation

**Purpose**: Explain complex concepts clearly.

**Prompt**:
```
Explain [CONCEPT] including:
- Simple definition in one sentence
- Why it matters and when to use it
- How it works (with diagrams if helpful)
- Real-world examples and use cases
- Common misconceptions
- Comparison with related concepts
- Practical applications
- Resources for deeper learning
- Key takeaways
```

**Best For**: Knowledge sharing, teaching, documentation.

### Tutorial Creation

**Purpose**: Create step-by-step tutorials.

**Prompt**:
```
Create a tutorial for [TASK/SKILL] including:
- Tutorial overview and what you'll learn
- Prerequisites and required tools
- Step-by-step instructions with screenshots/code
- Explanation of each step
- Expected outputs and verification
- Common errors and solutions
- Variations and alternatives
- Next steps and further learning
- Complete working example
```

**Best For**: Teaching, documentation, knowledge transfer.

### Book/Article Summary

**Purpose**: Summarize reading for future reference.

**Prompt**:
```
Create a summary of [BOOK/ARTICLE TITLE] including:
- Overview and main thesis
- Key concepts and ideas
- Main arguments and evidence
- Practical applications
- Critical analysis and evaluation
- Personal insights and takeaways
- Relevant quotes
- How it relates to [YOUR CONTEXT]
- Action items based on the reading
```

**Best For**: Knowledge retention, building reference library, sharing insights.

### Knowledge Base Article

**Purpose**: Create searchable knowledge base content.

**Prompt**:
```
Create a knowledge base article about [TOPIC] including:
- Clear, descriptive title
- Brief summary (2-3 sentences)
- Problem or question addressed
- Step-by-step solution or explanation
- Examples and use cases
- Related articles and topics
- Tags for searchability
- Last updated date
- Feedback mechanism
```

**Best For**: Support documentation, FAQs, self-service.

---

## Prompt Engineering Tips

### Make Prompts Specific

❌ **Vague**: "Document my server"

✅ **Specific**: "Document my Ubuntu 22.04 server running Docker with Traefik reverse proxy on port 80/443, including SSL certificate setup with Let's Encrypt, container management, and common troubleshooting"

### Provide Context

❌ **No Context**: "Create API docs"

✅ **With Context**: "Create API documentation for a Python FastAPI application with JWT authentication, PostgreSQL database, and Redis caching. Include request/response examples, error handling, and rate limiting"

### Specify Structure

❌ **Unstructured**: "Write about backups"

✅ **Structured**: "Create backup documentation with sections: Strategy Overview, Backup Schedule, Retention Policy, Backup Scripts, Restore Procedures, Testing Schedule, and Disaster Recovery"

### Include Examples

❌ **Abstract**: "Document configuration"

✅ **With Examples**: "Document Nginx configuration for reverse proxy. Here's my current config: [paste config]. Explain each directive, provide alternatives for common scenarios, and include security best practices"

### Request Format

❌ **No Format**: "Explain the process"

✅ **With Format**: "Explain the deployment process as a numbered checklist with commands, expected outputs, verification steps, and rollback procedures. Include a Mermaid flowchart"

### Specify Audience

❌ **No Audience**: "Document the system"

✅ **With Audience**: "Document the system architecture for new developers with 2-3 years experience. Include high-level overview, component descriptions, and links to detailed docs. Avoid assuming deep knowledge"

### Define Scope

❌ **Unlimited Scope**: "Document everything about Kubernetes"

✅ **Defined Scope**: "Document our Kubernetes deployment process for the production cluster, focusing on: namespace setup, deployment manifests, service configuration, and ingress rules. Exclude cluster setup and monitoring"

### Request Specific Formats

**Diagrams**:
```
Include a Mermaid diagram showing [WHAT TO SHOW]
```

**Tables**:
```
Present the comparison as a table with columns: [COLUMN NAMES]
```

**Code Blocks**:
```
Include code examples in [LANGUAGE] with comments explaining each section
```

**Checklists**:
```
Format as a checklist with checkboxes for each step
```

### Iterate and Refine

1. **Start broad**: Get initial documentation
2. **Review**: Identify gaps or unclear sections
3. **Refine**: Use more specific prompts for those sections
4. **Enhance**: Add examples, diagrams, or details as needed

### Use Templates

For recurring documentation needs, create templates with placeholders:

```
Document [SERVICE] including:
- Overview and purpose
- [SPECIFIC SECTIONS FOR THIS TYPE]
- Configuration
- Troubleshooting
```

### Combine Techniques

Best prompts combine multiple techniques:

```
Create a troubleshooting guide for [SYSTEM] targeted at [AUDIENCE] including:
- [SPECIFIC ISSUES TO COVER]
- For each issue: symptoms, diagnosis, solution, prevention
- Format as a table for quick reference
- Include code examples in [LANGUAGE]
- Add a decision tree diagram in Mermaid
```

---

## Prompt Templates

### General Documentation Template

```
Create [DOCUMENT TYPE] for [TOPIC] including:
- [SECTION 1]
- [SECTION 2]
- [SECTION 3]
Format: [FORMAT REQUIREMENTS]
Audience: [TARGET AUDIENCE]
Length: [APPROXIMATE LENGTH]
Include: [SPECIFIC ELEMENTS]
```

### Technical Documentation Template

```
Document [TECHNICAL COMPONENT] including:
- Overview and architecture
- Configuration with examples
- API/Interface reference
- Usage examples
- Troubleshooting
- Best practices
Include diagrams: [DIAGRAM TYPES]
Code examples in: [LANGUAGES]
```

### Process Documentation Template

```
Document the [PROCESS NAME] process including:
- Purpose and when to use
- Roles and responsibilities
- Step-by-step procedure
- Tools and templates
- Success criteria
- Common issues and solutions
Format as: [CHECKLIST/FLOWCHART/NARRATIVE]
```

---

## Next Steps

1. **Bookmark this library** for quick reference
2. **Copy and customize** prompts for your needs
3. **Build your own library** of prompts that work well for you
4. **Share successful prompts** with your team
5. **Iterate and improve** prompts based on results

For more examples, see:
- [PRACTICAL_EXAMPLES.md](PRACTICAL_EXAMPLES.md) - Complete examples with commands
- [USE_CASES.md](USE_CASES.md) - Use cases by domain
- [DAILY_USE_GUIDE.md](DAILY_USE_GUIDE.md) - Daily workflow integration
