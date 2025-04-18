@echo off
set /p TAG_NAME="Enter tag name (e.g. before-chapter-16-enhancement): "
set /p TAG_MSG="Enter tag message (e.g. Tag before starting enhancement): "

echo.
echo Creating Git tag: %TAG_NAME%
git add .
git commit -m "Checkpoint before tag %TAG_NAME%" >nul 2>&1

git tag -a %TAG_NAME% -m "%TAG_MSG%"
git push origin %TAG_NAME%

echo.
echo ✅ Tag '%TAG_NAME%' created and pushed.
pause
