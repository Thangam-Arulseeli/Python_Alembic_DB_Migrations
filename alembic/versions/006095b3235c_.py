"""empty message

Revision ID: 006095b3235c
Revises: ad840aafcd00
Create Date: 2026-10-15 11:25:58.478162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006095b3235c'
down_revision: Union[str, Sequence[str], None] = 'ad840aafcd00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
