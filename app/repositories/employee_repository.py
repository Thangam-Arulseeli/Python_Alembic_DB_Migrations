from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        employee_name: str,
        email: str,
        department: str,
    ) -> Employee:

        employee = Employee(
            employee_name=employee_name,
            email=email,
            department=department,
        )

        self.db.add(employee)

        return employee


    def get_all(self) -> list[Employee]:

        statement = select(Employee).order_by(
            Employee.employee_id
        )

        return list(
            self.db.scalars(statement).all()
        )


    def get_by_id(
        self,
        employee_id: int,
    ) -> Employee | None:

        return self.db.get(
            Employee,
            employee_id,
        )


    '''

The repository handles database persistence and retrieval.

It does not decide how the API should respond to every business error.

For example, deciding whether a missing employee should produce an HTTP 404 response is typically handled in the service or API layer.


Why use a repository?
```````````````````````
A repository centralizes data-access logic.

Without one, database queries may become scattered throughout routers and services.

A repository is especially useful when an application has complex querying, multiple persistence operations, or a need to abstract the data-access implementation.

    '''