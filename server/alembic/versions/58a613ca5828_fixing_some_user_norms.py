"""Fixing some User norms

Revision ID: 58a613ca5828
Revises: 9012adabfd24
Create Date: 2024-12-02 09:35:37.178730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '58a613ca5828'
down_revision: Union[str, None] = '9012adabfd24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'name',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
    op.alter_column('users', 'name',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###