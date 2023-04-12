python -m uvicorn server.main:app --workers 1 --limit-max-requests 10000 --proxy-headers --port 5555 --host 0.0.0.0
pause