python -m uvicorn server.main:app --workers 2 --limit-max-requests 10000 --timeout-keep-alive 15 --proxy-headers --port 5555 --host 0.0.0.0
pause