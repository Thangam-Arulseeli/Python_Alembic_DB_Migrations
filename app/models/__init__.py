### This makes the model importable through the models package

### It will also help ensure the model is registered with SQLAlchemy metadata when the package is imported

from app.models.employee import Employee

__all__ = ["Employee"]

