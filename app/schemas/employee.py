from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):

    employee_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    department: str = Field(
        min_length=2,
        max_length=100,
    )


class EmployeeResponse(BaseModel):

    employee_id: int

    employee_name: str

    email: EmailStr

    department: str

    model_config = ConfigDict(
        from_attributes=True,
    )


    '''
    Why do we need schemas?

SQLAlchemy models and Pydantic schemas serve different purposes.

SQLAlchemy model	                                 Pydantic schema
Defines database mapping	                         Defines API input and output
Contains column types and database constraints	     Contains request validation rules
Used for persistence	                             Used for data validation and serialization
mapped_column()	                                     Field()

    '''