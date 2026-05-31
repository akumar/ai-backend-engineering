from fastapi import FastAPI
from app.api import auth


def create_app() -> FastAPI:
    app = FastAPI(title="Demo Auth App")
    app.include_router(auth.router)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
