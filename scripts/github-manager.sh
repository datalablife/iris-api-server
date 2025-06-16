#!/bin/bash

# GitHub Management Script for AutoGen Workflow
# This script helps manage GitHub operations using the GitHub CLI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
REPO_OWNER="datalablife"
REPO_NAME="iris-api-server"
REPO_FULL_NAME="$REPO_OWNER/$REPO_NAME"

echo -e "${BLUE}"
cat << "EOF"
   _____ _ _   _    _       _       __  __                                   
  / ____(_) | | |  | |     | |     |  \/  |                                  
 | |  __ _| |_| |__| |_   _| |__   | \  / | __ _ _ __   __ _  __ _  ___ _ __   
 | | |_ | | __|  __  | | | | '_ \  | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|  
 | |__| | | |_| |  | | |_| | |_) | | |  | | (_| | | | | (_| | (_| |  __/ |     
  \_____|_|\__|_|  |_|\__,_|_.__/  |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|     
                                                             __/ |            
                                                            |___/             
EOF
echo -e "${NC}"

# Function to print colored output
print_header() {
    echo -e "\n${PURPLE}=== $1 ===${NC}"
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to check GitHub CLI installation
check_gh_cli() {
    print_header "Checking GitHub CLI"
    
    if command -v gh &> /dev/null; then
        GH_VERSION=$(gh --version | head -n1)
        print_status "GitHub CLI is installed: $GH_VERSION"
        return 0
    else
        print_error "GitHub CLI is not installed"
        print_status "Please install GitHub CLI: https://cli.github.com/"
        return 1
    fi
}

# Function to authenticate with GitHub
authenticate_github() {
    print_header "GitHub Authentication"
    
    if gh auth status &> /dev/null; then
        print_status "Already authenticated with GitHub"
        CURRENT_USER=$(gh api user --jq .login)
        print_status "Logged in as: $CURRENT_USER"
        return 0
    else
        print_status "Not authenticated. Starting authentication..."
        gh auth login
        return $?
    fi
}

# Function to check repository status
check_repository() {
    print_header "Repository Status"
    
    if gh repo view "$REPO_FULL_NAME" &> /dev/null; then
        print_status "Repository exists: $REPO_FULL_NAME"
        
        # Get repository info
        REPO_INFO=$(gh repo view "$REPO_FULL_NAME" --json name,description,visibility,defaultBranch,url)
        REPO_URL=$(echo "$REPO_INFO" | jq -r .url)
        VISIBILITY=$(echo "$REPO_INFO" | jq -r .visibility)
        DEFAULT_BRANCH=$(echo "$REPO_INFO" | jq -r .defaultBranch)
        
        print_status "Repository URL: $REPO_URL"
        print_status "Visibility: $VISIBILITY"
        print_status "Default Branch: $DEFAULT_BRANCH"
        
        return 0
    else
        print_warning "Repository does not exist: $REPO_FULL_NAME"
        return 1
    fi
}

# Function to create repository
create_repository() {
    print_header "Creating Repository"
    
    print_status "Creating repository: $REPO_FULL_NAME"
    
    gh repo create "$REPO_FULL_NAME" \
        --description "AutoGen Programming Workflow - Multi-Agent Development System with Docker containerization" \
        --public \
        --clone=false \
        --add-readme=false
    
    if [ $? -eq 0 ]; then
        print_success "Repository created successfully"
        return 0
    else
        print_error "Failed to create repository"
        return 1
    fi
}

# Function to setup repository secrets
setup_secrets() {
    print_header "Setting Up Repository Secrets"
    
    print_status "Setting up GitHub Actions secrets..."
    
    # Note: In a real scenario, you would prompt for these values or read from a secure source
    print_warning "Please set up the following secrets manually in GitHub:"
    echo "  - GOOGLE_API_KEY: Your Google Gemini API key"
    echo "  - DOCKER_USERNAME: Your Docker Hub username"
    echo "  - DOCKER_PASSWORD: Your Docker Hub password"
    echo ""
    echo "Go to: https://github.com/$REPO_FULL_NAME/settings/secrets/actions"
}

# Function to enable GitHub features
enable_github_features() {
    print_header "Enabling GitHub Features"
    
    print_status "Enabling GitHub features for the repository..."
    
    # Enable issues
    gh repo edit "$REPO_FULL_NAME" --enable-issues
    print_status "✓ Issues enabled"
    
    # Enable projects
    gh repo edit "$REPO_FULL_NAME" --enable-projects
    print_status "✓ Projects enabled"
    
    # Enable wiki
    gh repo edit "$REPO_FULL_NAME" --enable-wiki
    print_status "✓ Wiki enabled"
    
    # Enable discussions
    gh repo edit "$REPO_FULL_NAME" --enable-discussions
    print_status "✓ Discussions enabled"
    
    print_success "GitHub features enabled"
}

# Function to create labels
create_labels() {
    print_header "Creating Issue Labels"
    
    # Define labels
    declare -A LABELS=(
        ["bug"]="#d73a4a"
        ["enhancement"]="#a2eeef"
        ["documentation"]="#0075ca"
        ["good first issue"]="#7057ff"
        ["help wanted"]="#008672"
        ["question"]="#d876e3"
        ["wontfix"]="#ffffff"
        ["duplicate"]="#cfd3d7"
        ["invalid"]="#e4e669"
        ["priority:high"]="#ff0000"
        ["priority:medium"]="#ff9900"
        ["priority:low"]="#00ff00"
        ["type:feature"]="#84b6eb"
        ["type:bugfix"]="#fc2929"
        ["type:refactor"]="#fbca04"
        ["status:in-progress"]="#0e8a16"
        ["status:review"]="#f9d0c4"
        ["status:blocked"]="#b60205"
        ["docker"]="#2496ed"
        ["autogen"]="#6f42c1"
        ["gemini-api"]="#4285f4"
        ["testing"]="#c5def5"
        ["ci/cd"]="#28a745"
    )
    
    print_status "Creating issue labels..."
    
    for label in "${!LABELS[@]}"; do
        color="${LABELS[$label]}"
        if gh label create "$label" --color "$color" --repo "$REPO_FULL_NAME" 2>/dev/null; then
            print_status "✓ Created label: $label"
        else
            print_warning "Label already exists or failed to create: $label"
        fi
    done
    
    print_success "Labels setup completed"
}

# Function to create milestones
create_milestones() {
    print_header "Creating Project Milestones"
    
    # Define milestones
    declare -A MILESTONES=(
        ["v1.0.0 - Initial Release"]="Complete AutoGen workflow with Docker containerization"
        ["v1.1.0 - Enhanced Features"]="Additional features and improvements"
        ["v1.2.0 - Performance Optimization"]="Performance improvements and optimizations"
        ["v2.0.0 - Major Update"]="Major feature updates and breaking changes"
    )
    
    print_status "Creating project milestones..."
    
    for milestone in "${!MILESTONES[@]}"; do
        description="${MILESTONES[$milestone]}"
        if gh api repos/"$REPO_FULL_NAME"/milestones -f title="$milestone" -f description="$description" &>/dev/null; then
            print_status "✓ Created milestone: $milestone"
        else
            print_warning "Milestone already exists or failed to create: $milestone"
        fi
    done
    
    print_success "Milestones setup completed"
}

# Function to show repository information
show_repo_info() {
    print_header "Repository Information"
    
    if gh repo view "$REPO_FULL_NAME" &> /dev/null; then
        gh repo view "$REPO_FULL_NAME"
    else
        print_error "Repository not found or not accessible"
    fi
}

# Function to show help
show_help() {
    echo -e "${BLUE}GitHub Manager for AutoGen Workflow${NC}"
    echo -e "Manage GitHub repository operations"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  $0 <command>"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}setup${NC}        Complete repository setup"
    echo -e "  ${GREEN}create${NC}       Create repository"
    echo -e "  ${GREEN}check${NC}        Check repository status"
    echo -e "  ${GREEN}auth${NC}         Authenticate with GitHub"
    echo -e "  ${GREEN}secrets${NC}      Setup repository secrets"
    echo -e "  ${GREEN}features${NC}     Enable GitHub features"
    echo -e "  ${GREEN}labels${NC}       Create issue labels"
    echo -e "  ${GREEN}milestones${NC}   Create project milestones"
    echo -e "  ${GREEN}info${NC}         Show repository information"
    echo -e "  ${GREEN}help${NC}         Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  $0 setup         # Complete setup"
    echo -e "  $0 check         # Check repository status"
    echo -e "  $0 info          # Show repository info"
}

# Main command processing
COMMAND=${1:-"help"}

case $COMMAND in
    "setup")
        print_status "Starting complete GitHub setup..."
        if check_gh_cli && authenticate_github; then
            if ! check_repository; then
                create_repository
            fi
            setup_secrets
            enable_github_features
            create_labels
            create_milestones
            show_repo_info
            print_success "🎉 GitHub setup completed!"
        fi
        ;;
    "create")
        if check_gh_cli && authenticate_github; then
            create_repository
        fi
        ;;
    "check")
        if check_gh_cli && authenticate_github; then
            check_repository
        fi
        ;;
    "auth")
        if check_gh_cli; then
            authenticate_github
        fi
        ;;
    "secrets")
        if check_gh_cli && authenticate_github; then
            setup_secrets
        fi
        ;;
    "features")
        if check_gh_cli && authenticate_github; then
            enable_github_features
        fi
        ;;
    "labels")
        if check_gh_cli && authenticate_github; then
            create_labels
        fi
        ;;
    "milestones")
        if check_gh_cli && authenticate_github; then
            create_milestones
        fi
        ;;
    "info")
        if check_gh_cli && authenticate_github; then
            show_repo_info
        fi
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
