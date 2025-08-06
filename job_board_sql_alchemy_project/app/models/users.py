import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db import Base
from app.models.mixins import ActiveFlagMixin, TimestampMixin


class UserRole(enum.Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"


class User(Base, TimestampMixin, ActiveFlagMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    def __str__(self):
        obj_str = f"{self.name} ({self.role.value})"
        return obj_str
