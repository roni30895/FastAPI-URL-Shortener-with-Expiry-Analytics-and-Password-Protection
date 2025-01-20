from fastapi import FastAPI
from app.routes import shortner, redirect, analytics

app = FastAPI()

app.include_router(shortner.router)
app.include_router(redirect.router)
app.include_router(analytics.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)