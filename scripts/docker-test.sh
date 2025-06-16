#!/bin/bash

# AutoGen Workflow Docker Test Script
# This script runs comprehensive tests in Docker containers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 AutoGen Workflow Docker Test Suite${NC}"
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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Copying from .env.example"
    cp .env.example .env
fi

# Create test results directory
mkdir -p test-results coverage

# Function to run specific test suite
run_test_suite() {
    local test_type=$1
    local description=$2
    
    print_status "Running $description..."
    
    case $test_type in
        "unit")
            docker-compose -f docker-compose.test.yml run --rm autogen-test-suite
            ;;
        "gemini")
            docker-compose -f docker-compose.test.yml run --rm --profile gemini-tests gemini-api-test
            ;;
        "shell")
            docker-compose -f docker-compose.test.yml run --rm --profile shell-tests shell-test
            ;;
        "performance")
            docker-compose -f docker-compose.test.yml run --rm --profile performance-tests performance-test
            ;;
        "integration")
            docker-compose -f docker-compose.test.yml run --rm --profile integration-tests integration-test
            ;;
        "all")
            # Run all test suites
            run_test_suite "unit" "Unit Tests"
            run_test_suite "gemini" "Gemini API Tests"
            run_test_suite "shell" "Shell Script Tests"
            ;;
        *)
            print_error "Unknown test type: $test_type"
            return 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        print_success "✓ $description completed successfully"
        return 0
    else
        print_error "✗ $description failed"
        return 1
    fi
}

# Function to check test results
check_test_results() {
    print_status "Checking test results..."
    
    if [ -f "test-results/autogen-report.html" ]; then
        print_success "✓ AutoGen test report generated"
    fi
    
    if [ -d "coverage/autogen" ]; then
        print_success "✓ Coverage report generated"
    fi
    
    if [ -f "test-results/shell-test-results.txt" ]; then
        print_success "✓ Shell test results available"
        echo "Shell test summary:"
        tail -n 5 test-results/shell-test-results.txt
    fi
}

# Function to generate test summary
generate_test_summary() {
    print_status "Generating test summary..."
    
    local summary_file="test-results/test-summary.md"
    
    cat > $summary_file << EOF
# AutoGen Workflow Test Summary

**Test Date:** $(date)
**Environment:** Docker Containers

## Test Results

EOF
    
    # Check for test result files and add to summary
    if [ -f "test-results/autogen-report.html" ]; then
        echo "- ✅ AutoGen Unit Tests: PASSED" >> $summary_file
    else
        echo "- ❌ AutoGen Unit Tests: FAILED" >> $summary_file
    fi
    
    if [ -f "test-results/shell-test-results.txt" ]; then
        if grep -q "SUCCESS" test-results/shell-test-results.txt; then
            echo "- ✅ Shell Script Tests: PASSED" >> $summary_file
        else
            echo "- ❌ Shell Script Tests: FAILED" >> $summary_file
        fi
    fi
    
    cat >> $summary_file << EOF

## Coverage Report

Coverage reports are available in the \`coverage/\` directory.

## Test Artifacts

- HTML Reports: \`test-results/\`
- Coverage Reports: \`coverage/\`
- Shell Test Results: \`test-results/shell-test-results.txt\`

## Next Steps

1. Review test reports for any failures
2. Check coverage reports for code coverage
3. Fix any failing tests before deployment

EOF
    
    print_success "Test summary generated: $summary_file"
}

# Main execution
TEST_TYPE=${1:-"all"}

print_status "Starting Docker test suite..."
print_status "Test type: $TEST_TYPE"

# Clean up any existing test containers
print_status "Cleaning up existing test containers..."
docker-compose -f docker-compose.test.yml down --remove-orphans

# Run tests based on type
case $TEST_TYPE in
    "quick")
        print_status "Running quick test suite..."
        run_test_suite "unit" "Quick Unit Tests"
        ;;
    "full")
        print_status "Running full test suite..."
        run_test_suite "all" "All Tests"
        ;;
    *)
        run_test_suite "$TEST_TYPE" "Specified Tests"
        ;;
esac

# Check results
check_test_results

# Generate summary
generate_test_summary

# Clean up
print_status "Cleaning up test containers..."
docker-compose -f docker-compose.test.yml down --remove-orphans

# Show final results
print_status "Test execution completed!"
echo -e "\n${BLUE}Test Results Location:${NC}"
echo -e "📊 HTML Reports: ${GREEN}test-results/${NC}"
echo -e "📈 Coverage: ${GREEN}coverage/${NC}"
echo -e "📋 Summary: ${GREEN}test-results/test-summary.md${NC}"

echo -e "\n${BLUE}Usage Examples:${NC}"
echo -e "${GREEN}./scripts/docker-test.sh${NC}          # Run all tests"
echo -e "${GREEN}./scripts/docker-test.sh unit${NC}     # Run unit tests only"
echo -e "${GREEN}./scripts/docker-test.sh gemini${NC}   # Run Gemini API tests"
echo -e "${GREEN}./scripts/docker-test.sh quick${NC}    # Run quick test suite"
echo -e "${GREEN}./scripts/docker-test.sh full${NC}     # Run full test suite"

print_success "🎉 Docker test suite execution completed!"
