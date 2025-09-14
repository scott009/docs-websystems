@echo off
REM new-project.bat - Create new web system project documentation
REM Usage: new-project.bat <project-name>

setlocal enabledelayedexpansion

set "PROJECT_NAME=%~1"
set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
set "TEMPLATES_DIR=%REPO_ROOT%\templates"
set "PROJECTS_DIR=%REPO_ROOT%\projects"

REM Validate input
if "%PROJECT_NAME%"=="" (
    echo ❌ Usage: %0 ^<project-name^>
    echo.
    echo Examples:
    echo   %0 my-ecommerce-site
    echo   %0 task-management-app
    echo   %0 blog-platform
    exit /b 1
)

REM Check if project already exists
if exist "%PROJECTS_DIR%\%PROJECT_NAME%" (
    echo ❌ Project '%PROJECT_NAME%' already exists at: %PROJECTS_DIR%\%PROJECT_NAME%
    exit /b 1
)

echo ℹ️ Creating new web system project: %PROJECT_NAME%
echo ℹ️ Repository root: %REPO_ROOT%

REM Create project directory
if not exist "%PROJECTS_DIR%\%PROJECT_NAME%" mkdir "%PROJECTS_DIR%\%PROJECT_NAME%"
echo ✅ Created project directory: %PROJECTS_DIR%\%PROJECT_NAME%

REM Get current date and time
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set "CURRENT_DATE=%%a/%%b/%%c"
)

REM Get time with AM/PM
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set "CURRENT_TIME=%%a:%%b"
)

REM Get timezone (simplified - Windows doesn't have a simple TZ command)
set "TZ=Local"
set "CURRENT_TIMESTAMP=!CURRENT_DATE! at !CURRENT_TIME! !TZ!"

echo ℹ️ Using timestamp: !CURRENT_TIMESTAMP!

REM Copy and customize template files
for %%f in ("%TEMPLATES_DIR%\*.md") do (
    set "filename=%%~nxf"
    set "target_file=%PROJECTS_DIR%\%PROJECT_NAME%\!filename!"
    
    echo ℹ️ Processing template: !filename!
    
    REM Use PowerShell for reliable text replacement
    powershell -Command ^
        "(Get-Content '%TEMPLATES_DIR%\!filename!') " ^
        "-replace '{{PROJECT_NAME}}', '%PROJECT_NAME%' " ^
        "-replace '{{DATE}}', '!CURRENT_DATE!' " ^
        "-replace '{{TIMESTAMP}}', '!CURRENT_TIMESTAMP!' " ^
        "| Set-Content '!target_file!'"
    
    echo ✅ Created: !filename!
)

REM Create README.md for the project
(
echo # %PROJECT_NAME%
echo.
echo Documentation for the %PROJECT_NAME% web system project.
echo.
echo ## Documentation Files
echo.
echo - [**project-specification.md**](./project-specification.md^) - Project scope, architecture, and constraints
echo - [**current-status.md**](./current-status.md^) - Current progress and session context
echo - [**operations-guide.md**](./operations-guide.md^) - Commands, procedures, and troubleshooting
echo - [**infrastructure.md**](./infrastructure.md^) - Environment setup and deployment architecture
echo - [**changelog.md**](./changelog.md^) - Documentation evolution tracking
echo.
echo ## Quick Start
echo.
echo 1. Review and customize the project specification
echo 2. Update the current status with your initial setup
echo 3. Follow the operations guide for development setup
echo 4. Configure your infrastructure as documented
echo.
echo ## AI Assistant Integration
echo.
echo This documentation is optimized for use with Claude Code and other AI assistants:
echo.
echo - **Model hints** guide appropriate AI model selection (Haiku ✨ for simple tasks, Sonnet 🧠 for complex analysis^)
echo - **Evidence requirements** ensure proper command output documentation
echo - **Health checks** provide system verification procedures
echo - **Rollback procedures** enable safe deployment practices
echo.
echo Created: !CURRENT_DATE! using docs-websystems template
) > "%PROJECTS_DIR%\%PROJECT_NAME%\README.md"

echo ✅ Created: README.md

REM Summary
echo.
echo ✅ Project '%PROJECT_NAME%' created successfully!
echo.
echo ℹ️ 📁 Project location: %PROJECTS_DIR%\%PROJECT_NAME%
echo ℹ️ 📝 Next steps:
echo    1. Edit project-specification.md to define your project
echo    2. Update current-status.md with your current progress
echo    3. Customize infrastructure.md for your environment
echo    4. Follow operations-guide.md for development setup
echo.
echo ℹ️ 🤖 AI Integration:
echo    • Load project context: type %PROJECTS_DIR%\%PROJECT_NAME%\*.md
echo    • Use model hints: Haiku ✨ for simple tasks, Sonnet 🧠 for complex analysis
echo    • Follow evidence requirements in operations-guide.md
echo.
echo ✅ Happy building! 🚀

endlocal