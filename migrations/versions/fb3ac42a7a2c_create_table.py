"""create table

Revision ID: fb3ac42a7a2c
Revises: 
Create Date: 2022-11-30 12:37:56.410430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fb3ac42a7a2c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=True),
        sa.Column("brand", sa.String(length=20), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("category", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("brand"),
        schema="productmanager",
    )
    op.create_index(
        op.f("ix_productmanager_Product_id"),
        "Product",
        ["id"],
        unique=False,
        schema="productmanager",
    )
    op.create_table(
        "Order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("date_created", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date_modified", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["productmanager.Product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="productmanager",
    )
    op.create_index(
        op.f("ix_productmanager_Order_id"),
        "Order",
        ["id"],
        unique=False,
        schema="productmanager",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_productmanager_Order_id"), table_name="Order", schema="productmanager"
    )
    op.drop_table("Order", schema="productmanager")
    op.drop_index(
        op.f("ix_productmanager_Product_id"),
        table_name="Product",
        schema="productmanager",
    )
    op.drop_table("Product", schema="productmanager")
    # ### end Alembic commands ###
