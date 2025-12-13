"""add content column to posts table

Revision ID: d4a3cc67eafd
Revises: 23e1aa6da84f
Create Date: 2025-12-13 20:07:07.860627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4a3cc67eafd'
down_revision: Union[str, Sequence[str], None] = '23e1aa6da84f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
