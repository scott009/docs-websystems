#!/bin/bash
# new-project.sh - Create new web system project documentation
# Usage: ./new-project.sh <project-name>

set -e  # Exit on any error

PROJECT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$REPO_ROOT/templates"
PROJECTS_DIR="$REPO_ROOT/projects"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Validate input
if [ -z "$PROJECT_NAME" ]; then
    print_error "Usage: $0 <project-name>"
    echo
    echo "Examples:"
    echo "  $0 my-ecommerce-site"
    echo "  $0 task-management-app"
    echo "  $0 blog-platform"
    exit 1
fi

# Validate project name (alphanumeric, hyphens, underscores only)
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    print_error "Project name must contain only letters, numbers, hyphens, and underscores"
    exit 1
fi

# Check if project already exists
PROJECT_DIR="$PROJECTS_DIR/$PROJECT_NAME"
if [ -d "$PROJECT_DIR" ]; then
    print_error "Project '$PROJECT_NAME' already exists at: $PROJECT_DIR"
    exit 1
fi

print_info "Creating new web system project: $PROJECT_NAME"
print_info "Repository root: $REPO_ROOT"

# Create project directory
mkdir -p "$PROJECT_DIR"
print_status "Created project directory: $PROJECT_DIR"

# Get current date and timestamp
CURRENT_DATE=$(date +'%m/%d/%Y')
CURRENT_TIMESTAMP=$(date +'%m/%d/%Y at %I:%M %p %Z')

print_info "Using timestamp: $CURRENT_TIMESTAMP"

# Copy and customize each template file
for template_file in "$TEMPLATES_DIR"/*.md; do
    if [ -f "$template_file" ]; then
        filename=$(basename "$template_file")
        target_file="$PROJECT_DIR/$filename"
        
        print_info "Processing template: $filename"
        
        # Copy template and replace placeholders
        sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
            -e "s/{{DATE}}/$CURRENT_DATE/g" \
            -e "s/{{TIMESTAMP}}/$CURRENT_TIMESTAMP/g" \
            "$template_file" > "$target_file"
        
        print_status "Created: $filename"
    fi
done

# Create README.md for the project
cat > "$PROJECT_DIR/README.md" << EOF
# $PROJECT_NAME

Documentation for the $PROJECT_NAME web system project.

## Documentation Files

- [**project-specification.md**](./project-specification.md) - Project scope, architecture, and constraints
- [**current-status.md**](./current-status.md) - Current progress and session context
- [**operations-guide.md**](./operations-guide.md) - Commands, procedures, and troubleshooting
- [**infrastructure.md**](./infrastructure.md) - Environment setup and deployment architecture
- [**changelog.md**](./changelog.md) - Documentation evolution tracking

## Quick Start

1. Review and customize the project specification
2. Update the current status with your initial setup
3. Follow the operations guide for development setup
4. Configure your infrastructure as documented

## AI Assistant Integration

This documentation is optimized for use with Claude Code and other AI assistants:

- **Model hints** guide appropriate AI model selection (Haiku ✨ for simple tasks, Sonnet 🧠 for complex analysis)
- **Evidence requirements** ensure proper command output documentation
- **Health checks** provide system verification procedures
- **Rollback procedures** enable safe deployment practices

Created: $CURRENT_DATE using docs-websystems template
EOF

print_status "Created: README.md"

# Summary
echo
print_status "Project '$PROJECT_NAME' created successfully!"
echo
print_info "📁 Project location: $PROJECT_DIR"
print_info "📝 Next steps:"
echo "   1. Edit project-specification.md to define your project"
echo "   2. Update current-status.md with your current progress"
echo "   3. Customize infrastructure.md for your environment"
echo "   4. Follow operations-guide.md for development setup"
echo
print_info "🤖 AI Integration:"
echo "   • Load project context: cat $PROJECT_DIR/*.md"
echo "   • Use model hints: Haiku ✨ for simple tasks, Sonnet 🧠 for complex analysis"
echo "   • Follow evidence requirements in operations-guide.md"
echo
print_status "Happy building! 🚀"