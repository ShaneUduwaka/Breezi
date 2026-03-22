#!/usr/bin/env python
"""
Test Runner - Easy execution of all test suites
Usage: python test_runner.py [option]
"""

import subprocess
import sys
import os
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_menu():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print("BREEZI PRODUCTION TEST RUNNER")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    print("Choose test suite to run:\n")
    print(f"{Colors.BOLD}1{Colors.ENDC}  Production Readiness Test (Comprehensive)")
    print(f"    {Colors.YELLOW}→ All 7 test categories in one command{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}2{Colors.ENDC}  API Unit Tests (pytest)")
    print(f"    {Colors.YELLOW}→ Fast unit tests without live server{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}3{Colors.ENDC}  Health Endpoint Tests Only")
    print(f"    {Colors.YELLOW}→ Quick health check validation{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}4{Colors.ENDC}  Security Tests Only")
    print(f"    {Colors.YELLOW}→ Security and vulnerability checks{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}5{Colors.ENDC}  Integration Tests Only")
    print(f"    {Colors.YELLOW}→ Component connectivity tests{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}6{Colors.ENDC}  Docker Tests Only")
    print(f"    {Colors.YELLOW}→ Docker build and compose validation{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}7{Colors.ENDC}  Performance Tests")
    print(f"    {Colors.YELLOW}→ Response time and load testing{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}8{Colors.ENDC}  Coverage Report Generation")
    print(f"    {Colors.YELLOW}→ Detailed HTML coverage report{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}9{Colors.ENDC}  Full Test Suite (All Tests)")
    print(f"    {Colors.YELLOW}→ Run everything with coverage{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}10{Colors.ENDC} Docker Compose Up (Services)")
    print(f"    {Colors.YELLOW}→ Start mock services for testing{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}0{Colors.ENDC}  Exit\n")

def run_command(cmd, description):
    """Run command with nice output"""
    print(f"{Colors.BOLD}{Colors.BLUE}▶ {description}{Colors.ENDC}")
    print(f"{Colors.CYAN}{cmd}{Colors.ENDC}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"\n{Colors.GREEN}✓ {description} completed successfully!{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.RED}✗ {description} failed with exit code {result.returncode}{Colors.ENDC}\n")
    
    return result.returncode == 0

def test_production_readiness():
    """Run comprehensive production readiness test"""
    return run_command(
        "python fastapi_docker_prod_test.py",
        "Production Readiness Test"
    )

def test_api_unit():
    """Run API unit tests"""
    return run_command(
        "pytest test_api.py -v --tb=short",
        "API Unit Tests"
    )

def test_health_only():
    """Run health endpoint tests only"""
    return run_command(
        "pytest test_api.py::TestHealthEndpoints -v",
        "Health Endpoint Tests"
    )

def test_security():
    """Run security tests"""
    return run_command(
        "pytest test_api.py::TestSecurity -v",
        "Security Tests"
    )

def test_integration():
    """Run integration tests"""
    return run_command(
        "pytest test_api.py::TestIntegration -v",
        "Integration Tests"
    )

def test_docker():
    """Run Docker tests"""
    return run_command(
        "pytest test_api.py::TestDockerIntegration -v",
        "Docker Tests"
    )

def test_performance():
    """Run performance tests"""
    return run_command(
        "pytest test_api.py::TestPerformance -v -s",
        "Performance Tests"
    )

def test_coverage():
    """Generate coverage report"""
    success = run_command(
        "pytest test_api.py --cov --cov-report=html --cov-report=term-missing",
        "Coverage Report Generation"
    )
    
    if success:
        print(f"{Colors.GREEN}📊 HTML coverage report generated in: htmlcov/index.html{Colors.ENDC}\n")
    
    return success

def test_all():
    """Run all tests with coverage"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}Running Full Test Suite...{Colors.ENDC}\n")
    
    # Production readiness
    print(f"{Colors.BOLD}[1/3] {Colors.BLUE}Production Readiness Test{Colors.ENDC}")
    result1 = test_production_readiness()
    
    # Unit tests with coverage
    print(f"{Colors.BOLD}[2/3] {Colors.BLUE}Unit Tests with Coverage{Colors.ENDC}")
    result2 = test_api_unit()
    
    # Coverage report
    print(f"{Colors.BOLD}[3/3] {Colors.BLUE}Coverage Report{Colors.ENDC}")
    result3 = test_coverage()
    
    # Summary
    all_passed = result1 and result2 and result3
    
    print(f"\n{'='*60}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL TEST SUITES PASSED!{Colors.ENDC}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.ENDC}")
    print(f"{'='*60}\n")
    
    return all_passed

def docker_compose_up():
    """Start Docker Compose services"""
    return run_command(
        "docker-compose -f docker-compose.mock.yml up -d",
        "Starting Docker Compose Services"
    )

def docker_compose_down():
    """Stop Docker Compose services"""
    return run_command(
        "docker-compose -f docker-compose.mock.yml down",
        "Stopping Docker Compose Services"
    )

def print_summary(passed):
    """Print test summary"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print("TEST EXECUTION SUMMARY")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    if passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TESTS PASSED{Colors.ENDC}")
        print(f"\n{Colors.GREEN}Your system is production-ready!{Colors.ENDC}\n")
        print("Next steps:")
        print(f"  1. {Colors.CYAN}Review the coverage report (htmlcov/index.html){Colors.ENDC}")
        print(f"  2. {Colors.CYAN}Check security test results{Colors.ENDC}")
        print(f"  3. {Colors.CYAN}Deploy with confidence!{Colors.ENDC}\n")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ TESTS FAILED{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Review the output above for details and fix issues.{Colors.ENDC}\n")

def interactive_menu():
    """Interactive menu-driven test selection"""
    while True:
        print_menu()
        
        try:
            choice = input(f"{Colors.BOLD}Enter your choice (0-10):{Colors.ENDC} ").strip()
            
            if choice == "0":
                print(f"\n{Colors.CYAN}Exiting test runner. Goodbye!{Colors.ENDC}\n")
                sys.exit(0)
            
            elif choice == "1":
                passed = test_production_readiness()
                print_summary(passed)
            
            elif choice == "2":
                passed = test_api_unit()
                print_summary(passed)
            
            elif choice == "3":
                passed = test_health_only()
                print_summary(passed)
            
            elif choice == "4":
                passed = test_security()
                print_summary(passed)
            
            elif choice == "5":
                passed = test_integration()
                print_summary(passed)
            
            elif choice == "6":
                passed = test_docker()
                print_summary(passed)
            
            elif choice == "7":
                passed = test_performance()
                print_summary(passed)
            
            elif choice == "8":
                passed = test_coverage()
                print_summary(passed)
            
            elif choice == "9":
                passed = test_all()
                print_summary(passed)
            
            elif choice == "10":
                docker_compose_up()
            
            else:
                print(f"{Colors.RED}Invalid choice. Please enter 0-10.{Colors.ENDC}\n")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Test runner interrupted by user.{Colors.ENDC}\n")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.ENDC}\n")
            input("Press Enter to continue...")

def main():
    """Main entry point"""
    # Check if argument provided
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ["prod", "production", "1"]:
            sys.exit(0 if test_production_readiness() else 1)
        elif arg in ["unit", "api", "2"]:
            sys.exit(0 if test_api_unit() else 1)
        elif arg in ["health", "3"]:
            sys.exit(0 if test_health_only() else 1)
        elif arg in ["security", "4"]:
            sys.exit(0 if test_security() else 1)
        elif arg in ["integration", "5"]:
            sys.exit(0 if test_integration() else 1)
        elif arg in ["docker", "6"]:
            sys.exit(0 if test_docker() else 1)
        elif arg in ["performance", "perf", "7"]:
            sys.exit(0 if test_performance() else 1)
        elif arg in ["coverage", "cov", "8"]:
            sys.exit(0 if test_coverage() else 1)
        elif arg in ["all", "full", "9"]:
            sys.exit(0 if test_all() else 1)
        elif arg in ["up", "start", "10"]:
            sys.exit(0 if docker_compose_up() else 1)
        elif arg in ["down", "stop"]:
            sys.exit(0 if docker_compose_down() else 1)
        elif arg in ["help", "-h", "--help"]:
            print(f"""
{Colors.BOLD}Breezi Production Test Runner{Colors.ENDC}

Usage: python test_runner.py [option]

Options:
  1, prod, production    Run production readiness test
  2, unit, api           Run API unit tests
  3, health              Run health endpoint tests
  4, security            Run security tests
  5, integration         Run integration tests
  6, docker              Run Docker tests
  7, performance, perf   Run performance tests
  8, coverage, cov       Generate coverage report
  9, all, full           Run all tests
  10, up, start          Start Docker Compose services
     down, stop          Stop Docker Compose services
  help, -h, --help       Show this help message

Examples:
  python test_runner.py prod      # Run production test
  python test_runner.py all       # Run all tests
  python test_runner.py coverage  # Generate coverage report
            """)
            sys.exit(0)
        else:
            print(f"{Colors.RED}Unknown option: {arg}{Colors.ENDC}\n")
            interactive_menu()
    else:
        # No arguments, show interactive menu
        interactive_menu()

if __name__ == "__main__":
    main()
