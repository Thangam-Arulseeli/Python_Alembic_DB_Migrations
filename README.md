Creating / Migrating DB table using Alembic
********************************************
This project covers Alembic setup, database migrations, autogeneration, upgrade/downgrade operations, migration history, migration review and related operations

Understanding Alembic
======================
1.1 What is Alembic?
---------------------
Alembic is a database migration tool for SQLAlchemy.

It manages changes to your database schema over time.

For example, suppose your Employee Management System initially contains an employees table.

Initially:
-------------
employee_id 	employee_name	email
1	            Arun	        arun@example.com
2	            Priya	        priya@example.com


Later, the business requires a new column named department.
-----------------------------------------------------------
You need to modify the database structure without deleting existing employee records.

Alembic allows you to create and execute a migration that adds the new column.

After migration:
-----------------
employee_id 	employee_name	email	             department
1	            Arun	        arun@example.com	    IT
2	            Priya	        priya@example.com	    HR


NOTE: The existing records remain intact.


Without Alembic   : Developers might manually execute SQL statements such as:
---------------------
ALTER TABLE employees
ADD COLUMN department VARCHAR(100);


This works for an individual database, but managing changes across development, testing, and production becomes difficult.

With Alembic : You create a migration file containing the schema changes.
----------------
For example:

def upgrade():
op.add_column(
"employees",
sa.Column("department", sa.String(100))
)


def downgrade():
op.drop_column("employees", "department")


NOTE: Alembic records which migrations have been applied and provides commands to move between database schema versions.


1.2 What does Alembic manage?
--------------------------------------
Alembic manages changes such as:

Creating tables.
Adding or removing columns.
Changing column definitions.
Creating indexes.
Adding foreign keys.
Adding unique constraints.
Modifying relationships at the database schema level.
Tracking migration versions.
Applying and reverting supported schema changes.


IMPORTANT NOTE: Alembic primarily manages database schema changes. It does not automatically manage all application data changes or business logic.



2. SQLAlchemy vs Alembic vs FastAPI
==========================================
These technologies have different responsibilities.

Technology	    Primary responsibility	Example
FastAPI	Exposes HTTP APIs	POST /employees
Pydantic	Validates request and response data	Validates email and employee name
SQLAlchemy ORM	Maps Python classes to database tables and performs database operations	Insert or retrieve an employee
Alembic	Manages database schema changes	Add a department column
PostgreSQL	Stores application data	Stores employee records
Uvicorn	Runs the ASGI application	Starts the FastAPI server


Consider this example:
class Employee(Base):
__tablename__ = "employees"

employee_id: Mapped[int] = mapped_column(
primary_key=True
)

employee_name: Mapped[str] = mapped_column(
String(100),
nullable=False
)

SQLAlchemy defines how the Python model maps to a database table.

However, defining this class does not automatically mean that a migration has been created.

Alembic compares your model metadata with the database schema and can generate a proposed migration.

You then review and execute that migration.

Key distinction
-----------------
SQLAlchemy models describe the intended database structure.
Alembic migration files describe changes to that structure.
PostgreSQL stores the actual structure and data.


3. Understanding Database Migrations
========================================
A migration represents a controlled change from one database schema version to another.

Suppose your application evolves through the following stages.

Version	        Change
--------------------------------------------------
Revision A	    Create the employees table
Revision B	    Add the department column
Revision C	    Add the salary column
Revision D	    Add an index on department
Revision E	    Add an employment status column


These revisions form a migration history.

Conceptually:
Initial Database
|
v
Revision A
Create employees table
|
v
Revision B
Add department
|
v
Revision C
Add salary
|
v
Revision D
Create department index
|
v
Revision E
Add employment status


Each revision identifies a particular schema change.

Alembic tracks the current revision in a database table named:  alembic_version

#################################################################


4. Complete Project Folder Structure
=========================================
We will create a simple but structured Employee Management API.

The application uses:

FastAPI
SQLAlchemy 2.x
PostgreSQL
Pydantic
Alembic
Environment-based configuration
Separate models, schemas, repositories, and services


Folder Structure
=====================
Python_Alembic_DB_Migrations/
│
├── .env
├── .gitignore
├── requirements.txt
├── alembic.ini
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   │
│   └── versions/
│       ├── 8f21a9c4b720_create_employees.py
│       └── 3b45c7d91a20_add_department.py
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── employee.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── employee.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── employee_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── employee_service.py
│   │
│   └── routers/
│       ├── __init__.py
│       └── employee_router.py
│
└── tests/
└── test_employees.py

==================================================


4.2 Request processing flow
--------------------------------
When a client sends a request to create an employee, the flow is:

Client
|
v
FastAPI Router
|
v
Pydantic Validation
|
v
Service Layer
|
v
Repository Layer
|
v
SQLAlchemy Session
|
v
PostgreSQL


Alembic follows a separate workflow:
-----------------------------------------
SQLAlchemy Models
|
v
Alembic Autogenerate
|
v
Migration File
|
v
Developer Reviews Migration
|
v
alembic upgrade head
|
v
PostgreSQL Schema Updated


NOTE: The distinction is important: Alembic migrations normally run as a deployment or maintenance operation, not every time an API request arrives.

===========================================================


5. Environment Setup
------------------------------
5.1 Create a virtual environment [Create the termial in the project folder]

> python -m venv venv

Activate it:

> .\venv\Scripts\Activate.ps1    OR venv\Scripts\activate


5.2 Install the required packages

Create requirements.txt
`````````````````````````````
fastapi
uvicorn[standard]
sqlalchemy>=2.0
alembic
psycopg[binary]
pydantic-settings
email-validator
httpx
pytest

> python -m pip install -r requirements.txt

=================================================

5.3 Configure PostgreSQL
---------------------------------
Create a database in PostgreSQL.

For example:
CREATE DATABASE Python_Alembic_DB_Migration;

Make sure your PostgreSQL server is running and that the application user has appropriate permissions.


5.4 Create the .env file
------------------------------
Place .env in the project root.
-------------------------------------
DDATABASE_URL=postgresql+psycopg://postgres:Postgres%40123@127.0.0.1:5432/Python_Alembic_DB_Migration

Replace your_password with the actual password'

If your password contains reserved URL characters, such as @, encode them appropriately in the connection URL.


Do not commit .env to source control.

5.6. Add the following to .gitignore:
------------------------------------
venv/
__pycache__/
.env
.pytest_cache/

===========================================




======================================

Configure Alembic
--------------------
Alembic must know:
Where your database is located.
Which SQLAlchemy metadata describes your application models.
How to generate and execute migration scripts.

9.1 Initialize Alembic
---------------------
Run this command from the project root:

> alembic init alembic

This generates the Alembic configuration and migration environment.

The generated structure includes:

alembic/
├── env.py
├── script.py.mako
└── versions/

alembic.ini

NOTE: Run this command only once for an existing project. If you have already initialized Alembic, modify the existing files rather than initializing it again.

--------------------------

Configure alembic/env.py
--------------------------
This is one of the most important steps in Alembic integration.
alembic/env.py file is auto created when "alembic init alembic" is used.
Then we modify it and the moodels when we want to migrate it.

Note 1:
------------
Important: Why do we import Employee?
from app.models import Employee


Alembic cannot automatically discover model classes that have never been imported into the metadata used for comparison.

If the model is not registered, Alembic may fail to detect the corresponding table.

For larger applications, ensure that all model modules are imported before Alembic accesses Base.metadata.

------


Note 2:
------------
Why do we use target_metadata?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

target_metadata = Base.metadata

This provides Alembic with the intended schema from SQLAlchemy.
Autogenerate compares that metadata with the existing database schema.



Note 3:
------------
Why do we use compare_type=True?

It instructs Alembic to compare column types when detecting schema differences.
This can help identify changes such as a column changing from VARCHAR(100) to VARCHAR(200).


Note 4:
------------
Why do we escape % in the URL?
```````````````````````````````
settings.DATABASE_URL.replace("%", "%%")

Alembic's configuration uses percent-based interpolation. Escaping percent characters helps prevent encoded URL characters from being interpreted as configuration placeholders.

##############################################################

Create the First Migration
=============================
We have defined the Employee model, but the table does not yet exist in PostgreSQL.

We need to generate a migration.

Generate a revision
`````````````````````
Run:
alembic init alembic
> alembic revision --autogenerate -m "create employees table"

The command tells Alembic to:

Load the configured migration environment.
Import the SQLAlchemy metadata.
Inspect the connected database schema.
Compare the schema with the model metadata.
Generate a proposed migration file.


A migration file will be created under:
---------------------------------
alembic/versions/

For example:

alembic/versions/8f21a9c4b720_create_employees_table.py

The revision ID and filename will be generated automatically.


revision = "8f21a9c4b720"   @@@

down_revision = None   ### Intitially for the first migration



Suppose we create 2nd migration
``````````````````````````````````
revision = "3b45c7d91a20"

down_revision = "8f21a9c4b720" @@@

IMPORTANT NOTE: The second migration depends on the first.

The relationship is :
8f21a9c4b720
|
v
3b45c7d91a20
This dependency structure allows Alembic to identify the correct order for applying schema changes.
==========================================================

Understanding upgrade() and downgrade()
-----------------------------------------------
Every standard Alembic revision contains two important functions.

def upgrade(): 
...
def downgrade():
...

############################################

Execute the Migration
-----------------------
Generating a migration does not modify the database.

To apply the migration, execute:

> alembic upgrade head  ### instructs Alembic to apply all necessary migrations until the database reaches that revision.

What does head mean?

head refers to the latest revision at the end of a migration history branch.
In a normal linear migration history, it represents the latest schema revision.

NOTE: The table is created in Postgres SQL

In Postgres SQL: 
SELECT *  FROM alembic_version;    --> To see the current alembic revision

SELECT * FROM employees;  

###############################################

IMPORTANT ALEMBIC COMMANDS
******************************
> alembic init alembic    ---- Initialze alembic 
> alembic revision --autogenerate -m "create employees table"   ----- create migration file 
> alembic history	    ---- Displays available migration history
> alembic upgrade head	 --- Applies migrations to the latest revision
> alembic current	--- Displays the revision currently applied to the database
> alembic revision --autogenerate -m "add employee status"  -----  SQLALchemy ORM reviws the existing migration and Checks the Model and Alembic will attempt to identify the difference and create a migration file.

Alembic Upgrade Commands
****************************
> alembic upgrade head  --> Applies all required migrations to reach the current head.
> alembic upgrade +1    --> Applies one revision step forward along the relevant migration path. [Use the revision graph and current database version to understand the exact transition.]
> alembic upgrade 8f21a9c4b720  --> Upgrade to a specific revision
> alembic downgrade -1   --> To move a database currently at Revision C back to Revision B 
> alembic downgrade <revision_B_id>   --> downgrade to a specific revision
> alembic downgrade base   --> downgrade to the initial state

NOTE: alembic downgrade base
This attempts to reverse all applicable migrations back to the base revision.
It can remove tables and other schema objects and may destroy data.
Do not use it casually against a production database.

Alembic History and Revision Commands
*****************************************
> alembic history   --> Display migration history
> alembic history --verbose         --> For a more detailed view
> alembic current   --> Shows the revision currently recorded by Alembic for the connected database.
> alembic heads   -->  Display available heads [Shows the head revisions in the migration graph]   
NOTE: A simple project commonly has one head. 
Multiple heads can occur when different migration branches are created
> alembic show head     --> Displays information about the revision identified as head
> alembic show 8f21a9c4b720   --> inspect a particular revision
> alembic upgrade head --sql    --> Check the SQL before execution. This generates SQL for the migration path.


What If Multiple Developers Create Migrations?
**********************************************
Consider this situation:

Developer A adds a salary column.
Developer B adds a status column.

Both developers start from the same revision:

    Revision A
    /        \
    v          v
Revision B        Revision C
Salary column     Status column

There are now two migration heads.

Check them using:

> alembic heads
> alembic merge -m "merge migration heads" <revision_B_id> <revision_C_id>

NOTE: Alembic creates a merge revision with both earlier revisions as parents.
A merge revision may not contain any schema operations of its own.
It joins the two migration histories.

You may need a merge migration.

First, identify the actual revision identifiers returned by Alembic.
##################################################

Add new changes in the migration [--autogenerate]
===================================================
> alembic revision --autogenerate -m "add employee status"  -----  SQLALchemy ORM reviws the existing migration and Checks the Model and Alembic will attempt to identify the difference and create a migration file.

Add this status column in 
def upgrade(): 

op.add_column(
"employees",
sa.Column(
"status",
sa.String(length=20),
nullable=False,
),
)


downgrade()    ### Defines the reverse operation.
def downgrade():
op.drop_column(
"employees",
"status",
)


NOTE: PostgreSQL cannot generally add a new NOT NULL column to a populated table without a suitable value for existing rows.

default="ACTIVE"  is an ORM-side default. By itself, it does not necessarily provide a database-side default for existing rows during an Alembic migration.

This is why migration review is essential.
===========================================

##################################################

FastAPI Database Integration
##################################

Now we will connect Alembic-managed PostgreSQL tables to FastAPI.
The database schema will be managed through Alembic, while FastAPI will use SQLAlchemy sessions to perform CRUD operations.

Create the database session dependency
---------------------------------------
Create app/database.py [with the following complete version if you have not already done so:]
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


engine = create_engine(
settings.DATABASE_URL,
pool_pre_ping=True,
pool_size=5,
max_overflow=10,
)

SessionLocal = sessionmaker(
bind=engine,
class_=Session,
autoflush=False,
expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:

db = SessionLocal()

try:
yield db

finally:
db.close()


*******************************************

Without dependency injection
===============================
You might write:

@app.get("/employees")
def list_employees():

db = SessionLocal()

try:
...
finally:
db.close()

This repeats session-management code in every endpoint.

==============

NOTE: Depends() is FastAPI's dependency injection mechanism.
FastAPI sees that the function requires a database session.
It calls the dependency, obtains the session, and passes it into the endpoint.
You do not need to manually create a new session inside every endpoint.

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db


def get_employees(db: Session = Depends(get_db)):
...


With dependency injection
=================================
@app.get("/employees")
def list_employees(
db: Session = Depends(get_db),
):
...

FastAPI manages the dependency lifecycle.
The endpoint receives the session it needs.
This makes the code easier to maintain and test.

############################################


Dependency Injection vs Dependency Inversion
#############################################

These two concepts are related, but they are not the same.

Dependency Injection
++++++++++++++++++++++++

Dependency injection means that a required object or service is supplied to a component instead of being constructed directly inside it.

Example:

def list_employees(
db: Session = Depends(get_db),
):
...

FastAPI injects the database session.


Dependency Inversion Principle
+++++++++++++++++++++++++++++++++

The Dependency Inversion Principle is one of the SOLID principles.

It states that high-level modules should depend on abstractions rather than directly depending on low-level implementation details.

For example, a service that implements business rules should ideally not be tightly coupled to a specific database implementation.

A simplified architecture is:
````````````````````````````````
FastAPI Router
|
v
Employee Service
|
v
Employee Repository Interface
^
|
SQLAlchemy Repository
|
v
PostgreSQL

The service depends on a repository contract.

#######################################################

End points for the application
===============================
| Method | Endpoint                       | Purpose                    |
| ------ | ------------------------------ | -------------------------- |
| GET    | `/`                            | Health-style root response |
| POST   | `/api/employees/`              | Create an employee         |
| GET    | `/api/employees/`              | Retrieve all employees     |
| GET    | `/api/employees/{employee_id}` | Retrieve one employee      |

#########################################################

Start the FastAPI application
===============================

Before starting the application, make sure you have generated and applied the Alembic migration.

From the project root, run:

> alembic upgrade head

Then start FastAPI:

> python -m uvicorn app.main:app --reload

Open Swagger UI at:

> http://127.0.0.1:8000/docs

You should see the Employee Management API endpoint

#############################################################

Should We Use Base.metadata.create_all() With Alembic?
===========================================================
You may have encountered this code in SQLAlchemy applications:

Base.metadata.create_all(bind=engine)

It creates missing tables represented in the metadata.

However, it is not a replacement for Alembic migrations.

create_all()	                        Alembic
====================================================================================
Creates missing tables	                Manages schema changes over time
Does not provide a migration history	Tracks revisions
Does not automatically apply column     Generates or executes reviewed schema changes
changes to existing tables
Useful for simple experiments and       Suitable for version-controlled schema evolution
some isolated tests	

#####################################################

Production Considerations
============================

The example above demonstrates the core concepts. Production deployments require additional care.

34.1 Migration review

Autogeneration can miss certain changes or produce operations that require manual editing.

Review every migration before applying it.

34.2 Migration and application compatibility

If a deployment changes the database schema and application code simultaneously, consider whether old and new application instances can safely operate against the schema during deployment.

For zero-downtime deployments, an expand-and-contract strategy is often useful:

Add a compatible schema change.
Deploy code that supports both old and new structures.
Migrate or backfill data.
Switch the application to the new structure.
Remove obsolete schema elements in a later migration.
34.3 Avoid destructive migrations without a recovery plan

Dropping columns, tables, or constraints can permanently remove information.

Backups and tested recovery procedures are important.

34.4 Do not automatically run migrations in every application worker

For production systems, run migrations as a controlled deployment step or dedicated migration job.

If every application worker tries to apply migrations during startup, startup races and operational problems can occur.

34.5 Use database constraints

Application validation improves error messages and user experience.

Database constraints protect data integrity even when data is written by another application or concurrent request.

For example:

email: Mapped[str] = mapped_column(
String(255),
unique=True,
nullable=False,
)
34.6 Handle transaction failures

After a failed SQLAlchemy transaction, a rollback is generally required before reusing the session.

For example:

try:
db.commit()

except Exception:
db.rollback()
raise

In production code, catch specific exceptions where possible, log unexpected errors appropriately, and avoid exposing database internals to clients.

34.7 Separate migration credentials when appropriate

A production environment may use a more privileged database role for schema migrations and a more restricted role for normal application operations.

This reduces the privileges available to the running application.

34.8 Test migrations

Test migrations against a disposable database or an appropriate staging environment.

Check both the resulting schema and application behavior, not merely whether the migration command exits successfully.
#####################################################################

