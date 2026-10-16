from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.employee_service import (
    DuplicateEmployeeError,
    EmployeeService,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

# Annotated — attaches additional information to a type.
# Depends(get_db) — tells FastAPI to obtain a database session through the get_db dependency.
def get_employee_service(
    db: Annotated[Session, Depends(get_db)],  # This function creates an EmployeeService object and provides it to FastAPI endpoints.
) -> EmployeeService:

    return EmployeeService(db)


EmployeeServiceDependency = Annotated[
    EmployeeService,
    Depends(get_employee_service),
]


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    data: EmployeeCreate,
    service: EmployeeServiceDependency,
):

    try:
        return service.create_employee(data)

    except DuplicateEmployeeError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "/",
    response_model=list[EmployeeResponse],
)
def list_employees(
    service: EmployeeServiceDependency,
):

    return service.get_employees()


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    service: EmployeeServiceDependency,
):

    employee = service.get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee

