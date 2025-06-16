#!/bin/bash

# AutoGen Workflow Docker Manager
# Main script to manage all Docker operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${BLUE}"
cat << "EOF"
   ___        __        ______            
  / _ | __ __/ /____   / _____ ___  ___   
 / __ |/ // / __/ _ \ / (_ / -_) _ \/ _ \  
/_/ |_|\_,_/\__/\___/ \___/\__/_//_/_//_/  
                                          
    Docker Container Management System    
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

print_command() {
    echo -e "${CYAN}[CMD]${NC} $1"
}

# Function to show help
show_help() {
    echo -e "${BLUE}AutoGen Workflow Docker Manager${NC}"
    echo -e "Comprehensive Docker management for AutoGen Programming Workflow"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  $0 <command> [options]"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${GREEN}build${NC}                    Build all Docker images"
    echo -e "  ${GREEN}dev${NC}                      Start development environment"
    echo -e "  ${GREEN}prod${NC}                     Start production environment"
    echo -e "  ${GREEN}test${NC}                     Run test suite"
    echo -e "  ${GREEN}stop${NC}                     Stop all services"
    echo -e "  ${GREEN}restart${NC}                  Restart all services"
    echo -e "  ${GREEN}logs${NC}                     Show service logs"
    echo -e "  ${GREEN}status${NC}                   Show service status"
    echo -e "  ${GREEN}cleanup${NC}                  Clean up Docker resources"
    echo -e "  ${GREEN}shell${NC}                    Access container shell"
    echo -e "  ${GREEN}health${NC}                   Check service health"
    echo -e "  ${GREEN}backup${NC}                   Backup data volumes"
    echo -e "  ${GREEN}restore${NC}                  Restore data volumes"
    echo -e "  ${GREEN}update${NC}                   Update and rebuild services"
    echo -e "  ${GREEN}monitor${NC}                  Show resource monitoring"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  $0 build                     # Build all images"
    echo -e "  $0 dev                       # Start development environment"
    echo -e "  $0 prod                      # Start production environment"
    echo -e "  $0 test unit                 # Run unit tests"
    echo -e "  $0 logs autogen-app          # Show app logs"
    echo -e "  $0 shell autogen-app         # Access app container"
    echo -e "  $0 cleanup full              # Full cleanup"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_status "✓ Prerequisites check passed"
}

# Function to ensure .env file exists
ensure_env_file() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your API keys"
        return 1
    fi
    return 0
}

# Function to show service status
show_status() {
    print_header "Service Status"
    
    echo -e "${YELLOW}Production Services:${NC}"
    docker-compose ps 2>/dev/null || echo "Not running"
    
    echo -e "\n${YELLOW}Development Services:${NC}"
    docker-compose -f docker-compose.dev.yml ps 2>/dev/null || echo "Not running"
    
    echo -e "\n${YELLOW}Docker System Info:${NC}"
    docker system df
}

# Function to show logs
show_logs() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        print_status "Showing all service logs..."
        docker-compose logs -f --tail=100
    else
        print_status "Showing logs for service: $service"
        docker-compose logs -f --tail=100 $service
    fi
}

# Function to access container shell
access_shell() {
    local service=${1:-"autogen-app"}
    
    print_status "Accessing shell for service: $service"
    
    if docker-compose ps $service | grep -q "Up"; then
        docker-compose exec $service /bin/bash
    elif docker-compose -f docker-compose.dev.yml ps $service | grep -q "Up"; then
        docker-compose -f docker-compose.dev.yml exec $service /bin/bash
    else
        print_error "Service $service is not running"
        exit 1
    fi
}

# Function to check health
check_health() {
    print_header "Health Check"
    
    # Check main application
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✓ Main application is healthy"
    else
        print_warning "✗ Main application health check failed"
    fi
    
    # Check Nginx (if running)
    if curl -f http://localhost/health > /dev/null 2>&1; then
        print_status "✓ Nginx is healthy"
    else
        print_warning "✗ Nginx health check failed or not running"
    fi
    
    # Check Redis
    if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
        print_status "✓ Redis is healthy"
    else
        print_warning "✗ Redis health check failed"
    fi
    
    # Check PostgreSQL
    if docker-compose exec postgres pg_isready -U autogen_user > /dev/null 2>&1; then
        print_status "✓ PostgreSQL is healthy"
    else
        print_warning "✗ PostgreSQL health check failed"
    fi
}

# Function to show resource monitoring
show_monitoring() {
    print_header "Resource Monitoring"
    
    echo -e "${YELLOW}Container Resource Usage:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo -e "\n${YELLOW}Docker System Usage:${NC}"
    docker system df
    
    echo -e "\n${YELLOW}Running Containers:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Main command processing
COMMAND=${1:-"help"}

case $COMMAND in
    "build")
        check_prerequisites
        print_command "./scripts/docker-build.sh"
        ./scripts/docker-build.sh
        ;;
    "dev"|"development")
        check_prerequisites
        ensure_env_file
        print_command "./scripts/docker-deploy.sh development up"
        ./scripts/docker-deploy.sh development up
        ;;
    "prod"|"production")
        check_prerequisites
        ensure_env_file
        print_command "./scripts/docker-deploy.sh production up"
        ./scripts/docker-deploy.sh production up
        ;;
    "test")
        check_prerequisites
        ensure_env_file
        TEST_TYPE=${2:-"all"}
        print_command "./scripts/docker-test.sh $TEST_TYPE"
        ./scripts/docker-test.sh $TEST_TYPE
        ;;
    "stop")
        print_command "Stopping all services"
        docker-compose down 2>/dev/null || true
        docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
        docker-compose -f docker-compose.test.yml down 2>/dev/null || true
        ;;
    "restart")
        print_command "Restarting services"
        docker-compose restart
        ;;
    "logs")
        SERVICE=${2:-""}
        show_logs $SERVICE
        ;;
    "status")
        show_status
        ;;
    "cleanup")
        CLEANUP_TYPE=${2:-"basic"}
        print_command "./scripts/docker-cleanup.sh $CLEANUP_TYPE"
        ./scripts/docker-cleanup.sh $CLEANUP_TYPE
        ;;
    "shell")
        SERVICE=${2:-"autogen-app"}
        access_shell $SERVICE
        ;;
    "health")
        check_health
        ;;
    "monitor")
        show_monitoring
        ;;
    "update")
        check_prerequisites
        print_command "Updating and rebuilding services"
        docker-compose down
        ./scripts/docker-build.sh
        docker-compose up -d
        ;;
    "backup")
        print_status "Backup functionality not yet implemented"
        ;;
    "restore")
        print_status "Restore functionality not yet implemented"
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
