from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.mixins import TimestampMixin, ActiveFlagMixin


class JobPost(Base, TimestampMixin, ActiveFlagMixin):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100))
    posted_on = Column(DateTime(timezone=True), server_default=func.now())

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", backref="job_posts")

    def __str__(self):
        obj_str = f"{self.title} at {self.company.name} ({self.location})"
        return obj_str
