#!/bin/bash

# AutoGen Workflow Docker Deployment Script
# This script deploys the application using Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-"production"}
ACTION=${2:-"up"}

echo -e "${BLUE}🚀 AutoGen Workflow Docker Deployment${NC}"
echo -e "${BLUE}====================================${NC}"

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

# Check if Docker and Docker Compose are available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Copying from .env.example"
    cp .env.example .env
    print_warning "Please edit .env file with your API keys before continuing"
    read -p "Press Enter to continue after editing .env file..."
fi

# Function to deploy based on environment
deploy_environment() {
    local env=$1
    local compose_file=""
    
    case $env in
        "production"|"prod")
            compose_file="docker-compose.yml"
            print_status "Deploying to PRODUCTION environment"
            ;;
        "development"|"dev")
            compose_file="docker-compose.dev.yml"
            print_status "Deploying to DEVELOPMENT environment"
            ;;
        "testing"|"test")
            compose_file="docker-compose.test.yml"
            print_status "Running TESTING environment"
            ;;
        *)
            print_error "Unknown environment: $env"
            print_error "Available environments: production, development, testing"
            exit 1
            ;;
    esac
    
    # Execute Docker Compose command
    case $ACTION in
        "up")
            print_status "Starting services..."
            docker-compose -f $compose_file up -d
            ;;
        "down")
            print_status "Stopping services..."
            docker-compose -f $compose_file down
            ;;
        "restart")
            print_status "Restarting services..."
            docker-compose -f $compose_file restart
            ;;
        "logs")
            print_status "Showing logs..."
            docker-compose -f $compose_file logs -f
            ;;
        "status")
            print_status "Showing service status..."
            docker-compose -f $compose_file ps
            ;;
        "build")
            print_status "Building and starting services..."
            docker-compose -f $compose_file up --build -d
            ;;
        *)
            print_error "Unknown action: $ACTION"
            print_error "Available actions: up, down, restart, logs, status, build"
            exit 1
            ;;
    esac
}

# Pre-deployment checks
print_status "Running pre-deployment checks..."

# Check if required directories exist
mkdir -p logs output data test-results coverage

# Check if API key is set
if grep -q "your_google_api_key_here" .env; then
    print_warning "Google API key not set in .env file"
fi

# Deploy
deploy_environment $ENVIRONMENT

# Post-deployment actions
if [ "$ACTION" = "up" ] || [ "$ACTION" = "build" ]; then
    print_status "Waiting for services to start..."
    sleep 10
    
    # Check service health
    print_status "Checking service health..."
    
    case $ENVIRONMENT in
        "production"|"prod")
            # Check main application
            if curl -f http://localhost:8000/health > /dev/null 2>&1; then
                print_status "✓ Main application is healthy"
            else
                print_warning "✗ Main application health check failed"
            fi
            
            # Check Nginx
            if curl -f http://localhost/health > /dev/null 2>&1; then
                print_status "✓ Nginx is healthy"
            else
                print_warning "✗ Nginx health check failed"
            fi
            ;;
        "development"|"dev")
            print_status "Development environment started"
            print_status "Access the application at: http://localhost:8000"
            print_status "Access Jupyter notebook at: http://localhost:8889"
            ;;
        "testing"|"test")
            print_status "Test environment started"
            print_status "Check test results in ./test-results/"
            ;;
    esac
    
    # Show running containers
    print_status "Running containers:"
    docker ps --filter "name=autogen"
    
    # Show useful commands
    echo -e "\n${BLUE}Useful Commands:${NC}"
    echo -e "${GREEN}View logs:${NC}     ./scripts/docker-deploy.sh $ENVIRONMENT logs"
    echo -e "${GREEN}Check status:${NC}  ./scripts/docker-deploy.sh $ENVIRONMENT status"
    echo -e "${GREEN}Stop services:${NC} ./scripts/docker-deploy.sh $ENVIRONMENT down"
    echo -e "${GREEN}Restart:${NC}       ./scripts/docker-deploy.sh $ENVIRONMENT restart"
fi

print_status "🎉 Deployment completed successfully!"
