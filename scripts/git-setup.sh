#!/bin/bash

# Git Setup and Configuration Script for AutoGen Workflow
# This script configures Git for the iris-api-server repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="git@github.com:datalablife/iris-api-server.git"
USER_NAME="Jack Chan"
USER_EMAIL="163439565+datalablife@users.noreply.github.com"
DEFAULT_BRANCH="main"

echo -e "${BLUE}"
cat << "EOF"
   _____ _ _     _____      _               
  / ____(_) |   / ____|    | |              
 | |  __ _| |_ | (___   ___| |_ _   _ _ __   
 | | |_ | | __|  \___ \ / _ \ __| | | | '_ \  
 | |__| | | |_   ____) |  __/ |_| |_| | |_) | 
  \_____|_|\__| |_____/ \___|\__|\__,_| .__/  
                                     | |     
                                     |_|     
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

# Function to check if Git is installed
check_git_installation() {
    print_header "Checking Git Installation"
    
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        print_status "Git is installed: $GIT_VERSION"
        return 0
    else
        print_error "Git is not installed. Please install Git first."
        return 1
    fi
}

# Function to initialize Git repository
initialize_git_repo() {
    print_header "Initializing Git Repository"
    
    if [ -d ".git" ]; then
        print_status "Git repository already exists"
    else
        print_status "Initializing new Git repository..."
        git init
        print_success "Git repository initialized"
    fi
}

# Function to configure Git user
configure_git_user() {
    print_header "Configuring Git User"
    
    print_status "Setting user name: $USER_NAME"
    git config user.name "$USER_NAME"
    
    print_status "Setting user email: $USER_EMAIL"
    git config user.email "$USER_EMAIL"
    
    # Set default branch
    print_status "Setting default branch: $DEFAULT_BRANCH"
    git config init.defaultBranch "$DEFAULT_BRANCH"
    
    # Configure other useful settings
    git config core.autocrlf input
    git config core.safecrlf true
    git config pull.rebase false
    git config push.default simple
    
    print_success "Git user configuration completed"
}

# Function to configure remote repository
configure_remote() {
    print_header "Configuring Remote Repository"
    
    # Check if remote already exists
    if git remote get-url origin &> /dev/null; then
        CURRENT_URL=$(git remote get-url origin)
        print_status "Remote 'origin' already exists: $CURRENT_URL"
        
        if [ "$CURRENT_URL" != "$REPO_URL" ]; then
            print_warning "Remote URL differs from expected. Updating..."
            git remote set-url origin "$REPO_URL"
            print_success "Remote URL updated to: $REPO_URL"
        fi
    else
        print_status "Adding remote 'origin': $REPO_URL"
        git remote add origin "$REPO_URL"
        print_success "Remote 'origin' added"
    fi
}

# Function to set up branch
setup_branch() {
    print_header "Setting Up Branch"
    
    # Check current branch
    if git rev-parse --verify HEAD &> /dev/null; then
        CURRENT_BRANCH=$(git branch --show-current)
        print_status "Current branch: $CURRENT_BRANCH"
        
        if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
            print_status "Renaming branch to $DEFAULT_BRANCH"
            git branch -M "$DEFAULT_BRANCH"
        fi
    else
        print_status "No commits yet. Branch will be created on first commit."
    fi
}

# Function to create initial commit
create_initial_commit() {
    print_header "Creating Initial Commit"
    
    # Check if there are any commits
    if git rev-parse --verify HEAD &> /dev/null; then
        print_status "Repository already has commits"
        return 0
    fi
    
    # Add all files
    print_status "Adding all files to staging area..."
    git add .
    
    # Check if there are files to commit
    if git diff --staged --quiet; then
        print_warning "No files to commit"
        return 0
    fi
    
    # Create initial commit
    print_status "Creating initial commit..."
    git commit -m "🎉 Initial commit: AutoGen Workflow with Docker containerization

- Complete AutoGen multi-agent programming workflow
- Docker containerization with multi-environment support
- CI/CD pipeline with GitHub Actions
- Comprehensive testing suite
- Monitoring and logging integration
- Complete documentation

Features:
- 5-agent workflow (Architect, PM, Programmer, Reviewer, Optimizer)
- Google Gemini API integration
- Docker multi-stage builds
- Development, testing, and production environments
- Nginx reverse proxy and load balancing
- PostgreSQL and Redis integration
- Prometheus and Grafana monitoring
- Automated testing and deployment"
    
    print_success "Initial commit created"
}

# Function to check SSH key
check_ssh_key() {
    print_header "Checking SSH Configuration"
    
    if [ -f ~/.ssh/id_rsa.pub ] || [ -f ~/.ssh/id_ed25519.pub ]; then
        print_status "SSH key found"
        
        # Test SSH connection to GitHub
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
            print_success "SSH connection to GitHub is working"
            return 0
        else
            print_warning "SSH connection to GitHub failed"
            print_status "Please ensure your SSH key is added to GitHub"
            return 1
        fi
    else
        print_warning "No SSH key found"
        print_status "Please generate an SSH key and add it to GitHub"
        print_status "Run: ssh-keygen -t ed25519 -C \"$USER_EMAIL\""
        return 1
    fi
}

# Function to sync with remote
sync_with_remote() {
    print_header "Syncing with Remote Repository"
    
    # Check if remote repository exists and is accessible
    if git ls-remote origin &> /dev/null; then
        print_status "Remote repository is accessible"
        
        # Fetch remote branches
        print_status "Fetching remote branches..."
        git fetch origin
        
        # Check if remote has main branch
        if git ls-remote --heads origin main | grep -q main; then
            print_status "Remote has main branch"
            
            # Check if we have commits
            if git rev-parse --verify HEAD &> /dev/null; then
                print_status "Local repository has commits"
                
                # Check if we're ahead, behind, or diverged
                LOCAL=$(git rev-parse HEAD)
                REMOTE=$(git rev-parse origin/main)
                
                if [ "$LOCAL" = "$REMOTE" ]; then
                    print_success "Local and remote are in sync"
                else
                    print_warning "Local and remote have diverged"
                    print_status "You may need to merge or rebase manually"
                fi
            else
                print_status "No local commits. Setting up tracking branch..."
                git branch --set-upstream-to=origin/main main
            fi
        else
            print_status "Remote repository is empty. Ready to push initial commit."
        fi
    else
        print_warning "Cannot access remote repository"
        print_status "This might be due to SSH key issues or repository permissions"
    fi
}

# Function to display Git status
show_git_status() {
    print_header "Git Repository Status"
    
    echo -e "${YELLOW}Repository Information:${NC}"
    echo "  Working Directory: $(pwd)"
    echo "  Git Directory: $(git rev-parse --git-dir 2>/dev/null || echo 'Not a git repository')"
    
    if git rev-parse --git-dir &> /dev/null; then
        echo "  Current Branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"
        echo "  Remote URL: $(git remote get-url origin 2>/dev/null || echo 'No remote')"
        echo "  Last Commit: $(git log -1 --format='%h - %s (%cr)' 2>/dev/null || echo 'No commits')"
        
        echo -e "\n${YELLOW}Git Status:${NC}"
        git status --short
        
        echo -e "\n${YELLOW}Remote Branches:${NC}"
        git branch -r 2>/dev/null || echo "  No remote branches"
    fi
}

# Function to show next steps
show_next_steps() {
    print_header "Next Steps"
    
    echo -e "${BLUE}Git Setup Complete! Here's what you can do next:${NC}"
    echo ""
    echo -e "${GREEN}1. Push to GitHub:${NC}"
    echo "   git push -u origin main"
    echo ""
    echo -e "${GREEN}2. Create a new branch for development:${NC}"
    echo "   git checkout -b feature/your-feature-name"
    echo ""
    echo -e "${GREEN}3. Make changes and commit:${NC}"
    echo "   git add ."
    echo "   git commit -m \"Your commit message\""
    echo "   git push origin feature/your-feature-name"
    echo ""
    echo -e "${GREEN}4. Create a Pull Request on GitHub${NC}"
    echo ""
    echo -e "${GREEN}5. Useful Git commands:${NC}"
    echo "   git status              # Check repository status"
    echo "   git log --oneline       # View commit history"
    echo "   git branch -a           # List all branches"
    echo "   git pull origin main    # Pull latest changes"
    echo ""
    echo -e "${BLUE}Repository URL:${NC} https://github.com/datalablife/iris-api-server"
}

# Main execution
main() {
    print_status "Starting Git setup for AutoGen Workflow..."
    
    # Run setup steps
    if check_git_installation; then
        initialize_git_repo
        configure_git_user
        configure_remote
        setup_branch
        create_initial_commit
        check_ssh_key
        sync_with_remote
        show_git_status
        show_next_steps
        
        print_success "🎉 Git setup completed successfully!"
    else
        print_error "Git setup failed. Please install Git and try again."
        exit 1
    fi
}

# Run main function
main "$@"
