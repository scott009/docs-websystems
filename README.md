# docs-websystems

Cross-platform documentation templates for web system projects

## Overview

This repository provides a standardized documentation template system for web development projects, optimized for AI assistant integration and cross-platform development workflows.

## Repository Structure

```
docs-websystems/
├── templates/              # Reusable documentation templates
│   ├── project-specification.md
│   ├── current-status.md
│   ├── operations-guide.md
│   ├── infrastructure.md
│   └── changelog.md
├── projects/               # Individual project documentation
│   └── inquirycircle/     # Example: InquiryCircle web system
└── scripts/               # Project initialization tools
    ├── new-project.sh     # Bash version (Linux/Mac)
    └── new-project.bat    # Windows batch version
```

## Quick Start

### Create New Project Documentation

**Linux/Mac/WSL:**
```bash
./scripts/new-project.sh my-project-name
```

**Windows:**
```batch
scripts\new-project.bat my-project-name
```

### AI Assistant Integration

These templates are optimized for use with Claude Code and other AI assistants:

- **Model hints** guide appropriate AI model selection (Haiku ✨ for simple tasks, Sonnet 🧠 for complex analysis)
- **Evidence requirements** ensure proper command output documentation
- **Health checks** provide system verification procedures
- **Rollback procedures** enable safe deployment practices

### Load Project Context for AI

```bash
# Example: Load InquiryCircle context
cat projects/inquirycircle/Documentation/{project-spec,STATUS,operations-guide,infrastructure,CHANGELOG}.md
```

## Template Features

- **Cross-platform support** - Works on Windows, Mac, and Linux
- **AI-friendly structure** - Optimized for AI assistant workflows
- **Version control ready** - Git-friendly documentation lifecycle
- **Technology agnostic** - Supports any web framework combination
- **Scalable** - Easy to add new projects without restructuring

## Example Projects

- **inquirycircle** - Full-stack web application with Vue 3 frontend, Django backend, and Docker deployment

## Contributing

This template system is designed to evolve with your project needs. Feel free to:

- Customize templates for your specific tech stack
- Add new project examples
- Enhance the AI integration features
- Improve the cross-platform scripts

## License

Open source - use freely for your projects

---

**Generated with Claude Code**  
**Co-Authored-By: Claude <noreply@anthropic.com>**