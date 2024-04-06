@echo off
set /p choice="Choose the application to start (frontend/backend): "

if /i "%choice%"=="frontend" (
    echo Starting frontend application...
    cd frontend
    start npm start
) else if /i "%choice%"=="backend" (
    echo Starting backend application...
    cd backend
    git pull origin master
    start uvicorn main:app --reload
) else (
    echo Invalid choice. Please choose either 'frontend' or 'backend'.
)
