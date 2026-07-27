"""descricao opcional em tarefas

Revision ID: b519ebe22c9f
Revises: 8a8059b35204
Create Date: 2026-07-27 02:39:50.054819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b519ebe22c9f'
down_revision: Union[str, Sequence[str], None] = '8a8059b35204'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
