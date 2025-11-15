# PowerShell script to start both backend and Streamlit servers

Write-Host "Starting Aivara Backend and Streamlit Frontend..." -ForegroundColor Green

# Check if backend is already running
$backendRunning = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backendRunning) {
    Write-Host "Backend server is already running on port 8000" -ForegroundColor Yellow
} else {
    Write-Host "Starting backend server on port 8000..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    Start-Sleep -Seconds 3
}

# Check if Streamlit is already running
$streamlitRunning = Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue
if ($streamlitRunning) {
    Write-Host "Streamlit server is already running on port 8501" -ForegroundColor Yellow
} else {
    Write-Host "Starting Streamlit frontend on port 8501..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; streamlit run streamlit_app.py --server.port 8501"
    Start-Sleep -Seconds 2
}

Write-Host "`nServers started!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Backend Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Streamlit App: http://localhost:8501" -ForegroundColor Cyan
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")




