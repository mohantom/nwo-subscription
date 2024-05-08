import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from app.routers import subscription_routes

app = FastAPI(title="Discern API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)

app.include_router(subscription_routes.router)


@app.get("/health", name="Health", tags=["Health"], include_in_schema=True)
def health_check():
    return Response("OK")


if __name__ == "__main__":
    print("Running for local tests...")
    os.environ["env"] = "local"
    uvicorn.run("main:app", port=8001, reload=True)
