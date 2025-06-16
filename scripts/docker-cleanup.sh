#!/bin/bash

# AutoGen Workflow Docker Cleanup Script
# This script cleans up Docker resources for the AutoGen project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 AutoGen Workflow Docker Cleanup${NC}"
echo -e "${BLUE}==================================${NC}"

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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Configuration
PROJECT_NAME="autogen-workflow"
CLEANUP_TYPE=${1:-"basic"}

# Function to show disk usage
show_disk_usage() {
    print_status "Current Docker disk usage:"
    docker system df
}

# Function to clean up containers
cleanup_containers() {
    print_status "Stopping and removing AutoGen containers..."
    
    # Stop all compose services
    docker-compose down --remove-orphans 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down --remove-orphans 2>/dev/null || true
    docker-compose -f docker-compose.test.yml down --remove-orphans 2>/dev/null || true
    
    # Remove AutoGen containers
    docker ps -a --filter "name=autogen" --format "{{.ID}}" | xargs -r docker rm -f
    
    print_success "✓ Containers cleaned up"
}

# Function to clean up images
cleanup_images() {
    print_status "Removing AutoGen images..."
    
    # Remove AutoGen images
    docker images --filter "reference=${PROJECT_NAME}*" --format "{{.ID}}" | xargs -r docker rmi -f
    
    # Remove dangling images
    docker image prune -f
    
    print_success "✓ Images cleaned up"
}

# Function to clean up volumes
cleanup_volumes() {
    print_status "Removing AutoGen volumes..."
    
    # Remove named volumes
    docker volume ls --filter "name=autogen" --format "{{.Name}}" | xargs -r docker volume rm
    
    # Remove dangling volumes
    docker volume prune -f
    
    print_success "✓ Volumes cleaned up"
}

# Function to clean up networks
cleanup_networks() {
    print_status "Removing AutoGen networks..."
    
    # Remove AutoGen networks
    docker network ls --filter "name=autogen" --format "{{.ID}}" | xargs -r docker network rm
    
    # Remove dangling networks
    docker network prune -f
    
    print_success "✓ Networks cleaned up"
}

# Function to clean up build cache
cleanup_build_cache() {
    print_status "Cleaning up Docker build cache..."
    
    docker builder prune -f
    
    print_success "✓ Build cache cleaned up"
}

# Function to clean up test artifacts
cleanup_test_artifacts() {
    print_status "Cleaning up test artifacts..."
    
    rm -rf test-results/* 2>/dev/null || true
    rm -rf coverage/* 2>/dev/null || true
    rm -rf logs/* 2>/dev/null || true
    
    print_success "✓ Test artifacts cleaned up"
}

# Function to perform system cleanup
cleanup_system() {
    print_status "Performing Docker system cleanup..."
    
    docker system prune -f --volumes
    
    print_success "✓ System cleanup completed"
}

# Show current usage
show_disk_usage

# Perform cleanup based on type
case $CLEANUP_TYPE in
    "basic")
        print_status "Performing basic cleanup..."
        cleanup_containers
        cleanup_test_artifacts
        docker image prune -f
        ;;
    "full")
        print_status "Performing full cleanup..."
        cleanup_containers
        cleanup_images
        cleanup_volumes
        cleanup_networks
        cleanup_build_cache
        cleanup_test_artifacts
        ;;
    "system")
        print_status "Performing system-wide cleanup..."
        cleanup_containers
        cleanup_images
        cleanup_volumes
        cleanup_networks
        cleanup_build_cache
        cleanup_test_artifacts
        cleanup_system
        ;;
    "containers")
        cleanup_containers
        ;;
    "images")
        cleanup_images
        ;;
    "volumes")
        cleanup_volumes
        ;;
    "networks")
        cleanup_networks
        ;;
    "cache")
        cleanup_build_cache
        ;;
    "tests")
        cleanup_test_artifacts
        ;;
    *)
        print_error "Unknown cleanup type: $CLEANUP_TYPE"
        echo -e "\n${BLUE}Available cleanup types:${NC}"
        echo -e "${GREEN}basic${NC}      - Stop containers, remove test artifacts, prune images"
        echo -e "${GREEN}full${NC}       - Remove all AutoGen Docker resources"
        echo -e "${GREEN}system${NC}     - Full cleanup + system-wide Docker cleanup"
        echo -e "${GREEN}containers${NC} - Remove only containers"
        echo -e "${GREEN}images${NC}     - Remove only images"
        echo -e "${GREEN}volumes${NC}    - Remove only volumes"
        echo -e "${GREEN}networks${NC}   - Remove only networks"
        echo -e "${GREEN}cache${NC}      - Remove only build cache"
        echo -e "${GREEN}tests${NC}      - Remove only test artifacts"
        exit 1
        ;;
esac

# Show disk usage after cleanup
echo -e "\n${BLUE}After cleanup:${NC}"
show_disk_usage

# Show what was cleaned
echo -e "\n${BLUE}Cleanup Summary:${NC}"
print_success "✓ Cleanup type: $CLEANUP_TYPE"
print_success "✓ AutoGen Docker resources cleaned"

# Show remaining AutoGen resources (if any)
echo -e "\n${BLUE}Remaining AutoGen resources:${NC}"
echo -e "${YELLOW}Containers:${NC}"
docker ps -a --filter "name=autogen" --format "table {{.Names}}\t{{.Status}}" || echo "None"

echo -e "${YELLOW}Images:${NC}"
docker images --filter "reference=${PROJECT_NAME}*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" || echo "None"

echo -e "${YELLOW}Volumes:${NC}"
docker volume ls --filter "name=autogen" --format "table {{.Name}}\t{{.Driver}}" || echo "None"

echo -e "${YELLOW}Networks:${NC}"
docker network ls --filter "name=autogen" --format "table {{.Name}}\t{{.Driver}}" || echo "None"

print_success "🎉 Docker cleanup completed!"

echo -e "\n${BLUE}Usage Examples:${NC}"
echo -e "${GREEN}./scripts/docker-cleanup.sh${NC}           # Basic cleanup"
echo -e "${GREEN}./scripts/docker-cleanup.sh full${NC}      # Full cleanup"
echo -e "${GREEN}./scripts/docker-cleanup.sh system${NC}    # System-wide cleanup"
echo -e "${GREEN}./scripts/docker-cleanup.sh containers${NC} # Containers only"
