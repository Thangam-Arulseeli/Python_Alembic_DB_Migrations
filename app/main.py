from fastapi import FastAPI

from app.routers.employee_router import router as employee_router


app = FastAPI(
    title="Employee Management API",
    version="1.0.0",
    description="Employee Management API using FastAPI, SQLAlchemy, PostgreSQL, and Alembic",
)


app.include_router(
    employee_router,
    prefix="/api",
)


@app.get("/")
def root():

    return {
        "message": "Employee Management API is running"
    }

