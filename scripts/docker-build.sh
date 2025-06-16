#!/bin/bash

# AutoGen Workflow Docker Build Script
# This script builds Docker images for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="autogen-workflow"
VERSION=${1:-"latest"}
REGISTRY=${DOCKER_REGISTRY:-""}

echo -e "${BLUE}🐳 AutoGen Workflow Docker Build Script${NC}"
echo -e "${BLUE}=======================================${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running ✓"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Copying from .env.example"
    cp .env.example .env
    print_warning "Please edit .env file with your API keys before running containers"
fi

# Build function
build_image() {
    local target=$1
    local tag_suffix=$2
    local dockerfile=${3:-"Dockerfile"}
    
    print_status "Building ${target} image..."
    
    docker build \
        --target ${target} \
        --tag ${PROJECT_NAME}:${tag_suffix}-${VERSION} \
        --tag ${PROJECT_NAME}:${tag_suffix}-latest \
        --file ${dockerfile} \
        --build-arg VERSION=${VERSION} \
        --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
        --build-arg VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
        .
    
    if [ $? -eq 0 ]; then
        print_status "✓ ${target} image built successfully"
    else
        print_error "✗ Failed to build ${target} image"
        exit 1
    fi
}

# Build all images
print_status "Building all Docker images..."

# Production image
build_image "production" "prod"

# Development image
build_image "development" "dev"

# Testing image
build_image "testing" "test"

# API Server image
build_image "api-server" "api"

# Tag images for registry if specified
if [ ! -z "$REGISTRY" ]; then
    print_status "Tagging images for registry: $REGISTRY"
    
    for suffix in "prod" "dev" "test" "api"; do
        docker tag ${PROJECT_NAME}:${suffix}-${VERSION} ${REGISTRY}/${PROJECT_NAME}:${suffix}-${VERSION}
        docker tag ${PROJECT_NAME}:${suffix}-latest ${REGISTRY}/${PROJECT_NAME}:${suffix}-latest
    done
fi

# Show built images
print_status "Built images:"
docker images | grep ${PROJECT_NAME}

# Cleanup dangling images
print_status "Cleaning up dangling images..."
docker image prune -f

print_status "🎉 All images built successfully!"

# Show usage instructions
echo -e "\n${BLUE}Usage Instructions:${NC}"
echo -e "${GREEN}Development:${NC} docker-compose -f docker-compose.dev.yml up"
echo -e "${GREEN}Production:${NC}  docker-compose up"
echo -e "${GREEN}Testing:${NC}     docker-compose -f docker-compose.test.yml up"

# Show next steps
echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "1. Edit .env file with your API keys"
echo -e "2. Run: ${GREEN}docker-compose up${NC} for production"
echo -e "3. Run: ${GREEN}docker-compose -f docker-compose.dev.yml up${NC} for development"
echo -e "4. Access the application at: ${GREEN}http://localhost:8000${NC}"

if [ ! -z "$REGISTRY" ]; then
    echo -e "\n${BLUE}Push to Registry:${NC}"
    echo -e "Run: ${GREEN}docker push ${REGISTRY}/${PROJECT_NAME}:prod-${VERSION}${NC}"
fi
