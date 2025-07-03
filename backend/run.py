import os
from fastapi import FastAPI
import uvicorn

if __name__ == "__main__":
    # Change directory to the directory containing this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the app
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
