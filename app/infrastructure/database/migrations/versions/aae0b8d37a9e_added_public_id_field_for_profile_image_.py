"""added public_id field for profile image in users

Revision ID: aae0b8d37a9e
Revises: 91d2339fd960
Create Date: 2025-08-22 02:57:15.543589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'aae0b8d37a9e'
down_revision: Union[str, Sequence[str], None] = '91d2339fd960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema"""
    op.add_column('users', sa.Column('profile_image_public_id', sa.String(length=255), nullable=True))

    # Alter existing column (if it was previously NOT NULL)
    op.alter_column('users', 'profile_image',
               existing_type=sa.String(length=500),
               nullable=True)

def downgrade() -> None:
    """Downgrade schema."""
    # Revert profile_image to NOT NULL (if that was original)
    op.alter_column('users', 'profile_image',
               existing_type=sa.String(length=500),
               nullable=False)

    # Drop the new column
    op.drop_column('users', 'profile_image_public_id')
    # ### end Alembic commands ###
