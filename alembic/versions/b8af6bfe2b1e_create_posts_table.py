"""create posts table

Revision ID: b8af6bfe2b1e
Revises: 
Create Date: 2025-06-15 20:44:15.422903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8af6bfe2b1e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column('id', sa.Integer, primary_key=True, autoincrement=True), sa.Column('title', sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
