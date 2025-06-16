#!/bin/bash
# AutoGen Workflow Environment Activation Script
# This script sets up the UV virtual environment and loads environment variables

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AutoGen Programming Workflow Environment Setup${NC}"
echo "=================================================="

# Add UV to PATH
export PATH="$HOME/.local/bin:$PATH"

# Get the project directory (where this script is located)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${YELLOW}📁 Project Directory: $PROJECT_DIR${NC}"

# Activate UV virtual environment
if [ -d "autogen-env" ]; then
    echo -e "${GREEN}🔧 Activating UV virtual environment...${NC}"
    source autogen-env/bin/activate
    
    # Load environment variables from .env file
    if [ -f ".env" ]; then
        echo -e "${GREEN}📋 Loading environment variables from .env...${NC}"
        export $(grep -v '^#' .env | xargs)
        echo -e "${GREEN}✅ Environment variables loaded${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file not found. Using default configuration.${NC}"
    fi
    
    # Verify Python and packages
    echo -e "${BLUE}🐍 Python version: $(python --version)${NC}"
    echo -e "${BLUE}📦 Virtual environment: $(which python)${NC}"
    
    # Check if AutoGen is installed
    if python -c "import autogen_agentchat" 2>/dev/null; then
        echo -e "${GREEN}✅ AutoGen packages are installed${NC}"
    else
        echo -e "${YELLOW}⚠️  AutoGen packages not found. Installing...${NC}"
        uv pip install -r requirements.txt
    fi
    
    # Check API key
    if [ -n "$GOOGLE_API_KEY" ]; then
        echo -e "${GREEN}✅ Google Gemini API key is configured${NC}"
    elif [ -n "$OPENAI_API_KEY" ]; then
        echo -e "${GREEN}✅ OpenAI API key is configured${NC}"
    else
        echo -e "${YELLOW}⚠️  No API keys found. Please configure GOOGLE_API_KEY or OPENAI_API_KEY${NC}"
    fi
    
    echo "=================================================="
    echo -e "${GREEN}🎉 Environment is ready! You can now run:${NC}"
    echo -e "${BLUE}  • python demo.py                    ${NC}# Quick demo"
    echo -e "${BLUE}  • python test_installation.py      ${NC}# Test installation"
    echo -e "${BLUE}  • python autogen_workflow/main.py  ${NC}# Full workflow"
    echo "=================================================="
    
else
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    uv venv autogen-env
    source autogen-env/bin/activate
    echo -e "${GREEN}📦 Installing dependencies...${NC}"
    uv pip install -r requirements.txt
    echo -e "${GREEN}✅ Environment created and dependencies installed${NC}"
fi

# Export function to easily reactivate
activate_autogen() {
    cd "$PROJECT_DIR"
    source autogen-env/bin/activate
    export $(grep -v '^#' .env | xargs) 2>/dev/null
    echo -e "${GREEN}✅ AutoGen environment activated${NC}"
}

export -f activate_autogen

# Start a new shell with the environment activated
exec bash --rcfile <(echo "
source ~/.bashrc
cd '$PROJECT_DIR'
source autogen-env/bin/activate
export \$(grep -v '^#' .env | xargs) 2>/dev/null
echo -e '${GREEN}✅ AutoGen environment is active${NC}'
echo -e '${BLUE}💡 Tip: Use \"activate_autogen\" to reactivate if needed${NC}'
")
