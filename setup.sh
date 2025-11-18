#!/bin/bash
# Reliable Setup Script for AI Pattern Detector
# This script ensures all dependencies are installed and the environment is ready

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup
main() {
    print_header "🛡️  AI Pattern Detector Setup"
    
    # Check Python
    print_info "Checking Python installation..."
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
    print_success "Python $PYTHON_VERSION detected"
    
    # Check pip
    print_info "Checking pip installation..."
    if ! command_exists pip3 && ! command_exists pip; then
        print_error "pip is not installed. Please install pip."
        exit 1
    fi
    
    PIP_CMD="pip3"
    if ! command_exists pip3; then
        PIP_CMD="pip"
    fi
    print_success "pip found"
    
    # Virtual environment (optional but recommended)
    if [ -z "$VIRTUAL_ENV" ]; then
        print_info "Virtual environment not detected"
        read -p "Create virtual environment? (recommended) [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            print_info "Creating virtual environment..."
            python3 -m venv venv
            print_success "Virtual environment created"
            print_info "Activating virtual environment..."
            source venv/bin/activate
            print_success "Virtual environment activated"
            print_warning "Remember to activate it in the future: source venv/bin/activate"
        fi
    else
        print_success "Virtual environment already active: $VIRTUAL_ENV"
    fi
    
    # Upgrade pip
    print_info "Upgrading pip..."
    $PIP_CMD install --upgrade pip --quiet
    print_success "pip upgraded"
    
    # Install dependencies
    print_info "Installing dependencies..."
    if [ ! -f "ai_tools/requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    $PIP_CMD install -r ai_tools/requirements.txt
    print_success "Dependencies installed"
    
    # Verify installation
    print_info "Verifying installation..."
    python3 scripts/check_environment.py
    VERIFY_EXIT=$?
    
    if [ $VERIFY_EXIT -eq 0 ]; then
        print_success "Installation verified successfully!"
    else
        print_warning "Some optional components may not be available (this is OK)"
    fi
    
    # Optional: Ollama setup
    print_info "Ollama setup (optional - for AI features)..."
    if command_exists ollama; then
        print_success "Ollama is installed"
        read -p "Pull default model (llama3.2:3b)? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Pulling llama3.2:3b model (this may take a few minutes)..."
            ollama pull llama3.2:3b || print_warning "Failed to pull model (you can do this later)"
        fi
    else
        print_warning "Ollama not installed. AI features will use fallback mode."
        print_info "To install Ollama: https://ollama.ai"
    fi
    
    # Optional: ChromaDB setup
    print_info "Checking ChromaDB (optional - for vector database)..."
    python3 -c "import chromadb" 2>/dev/null && print_success "ChromaDB installed" || print_warning "ChromaDB not installed (vector DB features disabled)"
    
    # Success message
    print_header "✅ Setup Complete!"
    
    echo ""
    echo "Next steps:"
    echo "  1. Start the dashboard:"
    echo "     ${GREEN}streamlit run dashboard/app.py${NC}"
    echo ""
    echo "  2. Or run tests:"
    echo "     ${GREEN}python3 tools/demo_dashboard.py${NC}"
    echo ""
    echo "  3. Check environment:"
    echo "     ${GREEN}python3 scripts/check_environment.py${NC}"
    echo ""
    
    if [ -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
        print_warning "Remember to activate virtual environment:"
        echo "     ${YELLOW}source venv/bin/activate${NC}"
        echo ""
    fi
    
    echo "For more information, see:"
    echo "  - Quick Start: ${BLUE}QUICKSTART.md${NC}"
    echo "  - Documentation: ${BLUE}docs/README.md${NC}"
    echo ""
}

# Run main function
main
