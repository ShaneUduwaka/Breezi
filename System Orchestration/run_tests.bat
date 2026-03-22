@echo off
REM Breezi Production Testing Suite - Windows Batch Runner
REM Usage: run_tests.bat [option]

setlocal enabledelayedexpansion

REM Define colors (Windows terminal colors)
set "RESET=[0m"
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "BOLD=[1m"

cls

if "%1"=="" (
    echo.
    echo %CYAN%%BOLD%======================================================%RESET%
    echo %CYAN%%BOLD%  BREEZI PRODUCTION TESTING SUITE%RESET%
    echo %CYAN%%BOLD%======================================================%RESET%
    echo.
    echo Usage: run_tests.bat [option]
    echo.
    echo Options:
    echo   prod        Run production readiness test
    echo   unit        Run API unit tests
    echo   all         Run all tests
    echo   help        Show this help message
    echo.
    echo Examples:
    echo   run_tests.bat prod      REM Production readiness
    echo   run_tests.bat unit      REM Unit tests only
    echo   run_tests.bat all       REM All tests
    echo.
    goto :end
)

if "%1"=="prod" (
    echo.
    echo %BLUE%%BOLD%Running Production Readiness Test...%RESET%
    echo.
    python fastapi_docker_prod_test.py
    if !errorlevel! equ 0 (
        echo.
        echo %GREEN%%BOLD%SUCCESS: Production test passed!%RESET%
    ) else (
        echo.
        echo %RED%%BOLD%FAILED: Production test failed!%RESET%
    )
    goto :end
)

if "%1"=="unit" (
    echo.
    echo %BLUE%%BOLD%Running Unit Tests...%RESET%
    echo.
    pytest test_api.py -v --tb=short
    if !errorlevel! equ 0 (
        echo.
        echo %GREEN%%BOLD%SUCCESS: Unit tests passed!%RESET%
    ) else (
        echo.
        echo %RED%%BOLD%FAILED: Unit tests failed!%RESET%
    )
    goto :end
)

if "%1"=="all" (
    echo.
    echo %BLUE%%BOLD%Running All Tests...%RESET%
    echo.
    
    echo %CYAN%[1/3] Production Readiness Test%RESET%
    python fastapi_docker_prod_test.py
    set "result1=!errorlevel!"
    
    echo.
    echo %CYAN%[2/3] Unit Tests%RESET%
    pytest test_api.py -v --tb=short
    set "result2=!errorlevel!"
    
    echo.
    echo %CYAN%[3/3] Coverage Report%RESET%
    pytest test_api.py --cov --cov-report=html
    set "result3=!errorlevel!"
    
    echo.
    echo ======================================================
    if !result1! equ 0 if !result2! equ 0 if !result3! equ 0 (
        echo %GREEN%%BOLD%SUCCESS: All tests passed!%RESET%
    ) else (
        echo %RED%%BOLD%FAILED: Some tests failed!%RESET%
    )
    echo ======================================================
    
    goto :end
)

if "%1"=="help" (
    cls
    echo.
    echo %CYAN%%BOLD%Breezi Production Testing Suite%RESET%
    echo.
    echo %BOLD%Usage:%RESET%
    echo   run_tests.bat [option]
    echo.
    echo %BOLD%Options:%RESET%
    echo   prod           Production readiness test (recommended)
    echo   unit           API unit tests
    echo   all            All tests with coverage
    echo   install        Install test dependencies
    echo   requirements   Show required packages
    echo   help           Show this help message
    echo.
    echo %BOLD%Examples:%RESET%
    echo   run_tests.bat prod      %YELLOW%REM Pre-deployment check%RESET%
    echo   run_tests.bat unit      %YELLOW%REM Quick unit tests%RESET%
    echo   run_tests.bat all       %YELLOW%REM Complete coverage%RESET%
    echo.
    goto :end
)

if "%1"=="install" (
    echo.
    echo %BLUE%%BOLD%Installing test dependencies...%RESET%
    echo.
    pip install -r test_requirements.txt
    if !errorlevel! equ 0 (
        echo.
        echo %GREEN%%BOLD%SUCCESS: Dependencies installed!%RESET%
    ) else (
        echo.
        echo %RED%%BOLD%FAILED: Installation failed!%RESET%
    )
    goto :end
)

if "%1"=="requirements" (
    echo.
    echo %CYAN%%BOLD%Required Packages:%RESET%
    echo.
    type test_requirements.txt
    echo.
    goto :end
)

echo %RED%Unknown option: %1%RESET%
echo.
echo Type: run_tests.bat help
echo.

:end
pause
