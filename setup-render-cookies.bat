@echo off
echo ========================================
echo   RENDER BACKEND SETUP HELPER
echo ========================================
echo.
echo This script will help you get the cookies content
echo that you need to paste into Render's YOUTUBE_COOKIES
echo environment variable.
echo.
echo ========================================
echo.

if not exist "backend\cookies.txt" (
    echo ERROR: cookies.txt not found in backend folder!
    echo Please make sure you have exported cookies from your browser.
    pause
    exit /b 1
)

echo Your cookies.txt file contains:
type backend\cookies.txt | find /c /v ""
echo lines
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Click on your 'yt-downloader-backend' service
echo 3. Go to Environment tab
echo 4. Add a new environment variable:
echo    - Key: YOUTUBE_COOKIES
echo    - Value: Copy the ENTIRE content shown below
echo.
echo 5. After adding, click "Save Changes"
echo 6. Then click "Manual Deploy" -^> "Deploy latest commit"
echo.
echo ========================================
echo COOKIES CONTENT (Copy everything below):
echo ========================================
echo.
type backend\cookies.txt
echo.
echo ========================================
echo END OF COOKIES
echo ========================================
echo.
echo Press any key to exit...
pause >nul
