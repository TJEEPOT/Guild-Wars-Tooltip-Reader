# Bypass the execution policy
PowerShell -ExecutionPolicy Bypass -Command {
    & ".\.venv\Scripts\python.exe" ".\start.py"
}