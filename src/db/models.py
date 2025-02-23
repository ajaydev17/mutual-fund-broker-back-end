from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import date, datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, List


# class for handling user related things
class User(SQLModel, table=True):

    # define the table name
    __tablename__ = 'users'

    # define the required fields
    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )
    email: str
    password_hash: str = Field(
        sa_column=Column(
            pg.VARCHAR, nullable=False
        ),
        exclude=True
    )
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now,
            onupdate=datetime.now
        )
    )
    investments: List['Investment'] = Relationship(
        back_populates='user', sa_relationship_kwargs={'lazy': 'selectin'}
    )


class Investment(SQLModel, table=True):

    # define the table name
    __tablename__ = 'investments'

    # define the required fields
    investment_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='users.user_id'
    )
    scheme_code: int
    units: float
    fund_family: str
    user: Optional[User] = Relationship(back_populates="investments")
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now,
            onupdate=datetime.now
        )
    )
