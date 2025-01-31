
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import g

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    from . import tesla
    g.tesla_client = tesla.TeslaClient(os.getenv("TESLA_HOME", "."))
    yield
    g.tesla_client = None

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/1/vehicles/{vin}/command/wake_up")
async def wake_vehicle(vin: str):
    retval = await g.tesla_client.wake(vin)
    return {"success": bool(retval)}


@app.post("/api/1/vehicles/{vin}/command/charge_port_door_open")
async def open_charge_port(vin: str):
    retval = await g.tesla_client.open_charge_port(vin)
    return {"success": bool(retval)}
