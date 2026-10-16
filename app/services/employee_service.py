from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate


class DuplicateEmployeeError(Exception):
    pass


class EmployeeService:

    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)
        self.db = db

    def create_employee(
        self,
        data: EmployeeCreate,
    ) -> Employee:

        employee = self.repository.create(
            employee_name=data.employee_name,
            email=str(data.email),
            department=data.department,
        )

        try:
            self.db.commit()

        except IntegrityError as exc:
            self.db.rollback()

            raise DuplicateEmployeeError(
                "The employee could not be created "
                "because a database constraint was violated."
            ) from exc

        self.db.refresh(employee)

        return employee


    def get_employees(self) -> list[Employee]:

        return self.repository.get_all()

    def get_employee(
        self,
        employee_id: int,
    ) -> Employee | None:

        return self.repository.get_by_id(
            employee_id
        )

    