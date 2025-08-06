from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.mixins import TimestampMixin, ActiveFlagMixin


class Company(Base, TimestampMixin, ActiveFlagMixin):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    location = Column(String(100))
    industry = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", backref="companies")

    def __str__(self):
        obj_repr = f"{self.name} ({self.industry})"
        return obj_repr
