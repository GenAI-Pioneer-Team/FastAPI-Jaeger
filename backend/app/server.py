from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.database.config import db_engine
from app.router import user_router
from app.jaeger.tracing import *
from app.jaeger.metrics import metrics_middleware

# Create the FastAPI app
app = FastAPI()

# app = metrics_middleware(app, "example_app")

# Index route
@app.get("/")
async def index():
    return {"message": "Master Server API"}

app.include_router(user_router, prefix="/api")


# Configure Jaeger Trace
FastAPIInstrumentor.instrument_app(app=app)
SQLAlchemyInstrumentor().instrument(engine=db_engine.sync_engine)