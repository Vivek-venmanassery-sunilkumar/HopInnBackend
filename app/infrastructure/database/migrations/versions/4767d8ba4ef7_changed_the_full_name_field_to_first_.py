"""changed the full_name field to first and last name fields

Revision ID: 4767d8ba4ef7
Revises: aae0b8d37a9e
Create Date: 2025-08-25 22:44:41.943762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4767d8ba4ef7'
down_revision: Union[str, Sequence[str], None] = 'aae0b8d37a9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
     # Drop old column
    op.drop_column('users', 'full_name')

    # Add new columns
    op.add_column('users', sa.Column('first_name', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Remove new columns
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')

    # Re-add old column
    op.add_column('users', sa.Column('full_name', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###
    
