@echo off

cd /d C:\Users\19931\OneDrive\pococha-burst-viewer

uv run python generate.py

git add .

git diff --cached --quiet
if %errorlevel%==0 exit /b

git commit -m "auto update"

git push