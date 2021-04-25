from fastapi import FastAPI
from routers import client_side, background

app = FastAPI()

app.include_router(client_side.router, tags=["client"])
app.include_router(background.router, prefix="/background", tags=["background"])
