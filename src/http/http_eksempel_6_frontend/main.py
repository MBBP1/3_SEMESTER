from src.http.http_eksempel_6_frontend.frontend_api import CoolNetFrontend


frontend = CoolNetFrontend()
app = frontend.app



# Start backend server with:
# uvicorn src.http_eksempel_4.main:app --reload

# Start frontend server with: 
# uvicorn src.http_eksempel_6_frontend.main:app --port 8500 --reload

# Test on: http://127.0.0.1:8500