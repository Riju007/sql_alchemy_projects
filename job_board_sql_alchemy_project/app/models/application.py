from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db import Base
from app.models.mixins import TimestampMixin, ActiveFlagMixin


class Application(Base, TimestampMixin, ActiveFlagMixin):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_posts.id"), nullable=False)
    applied_on = Column(DateTime(timezone=True), server_default=func.now())

    # prevent duplicate application by the same user for the same job.
    __table_args__ = (UniqueConstraint("user_id", "job_id", name="unique_user_job"),)

    # relationship
    user = relationship("User", backref="applications")
    job = relationship("JobPost", backref="applications")

    def __str__(self):
        obj_repr = f"Application(user_id={self.user_id}, job_id={self.job_id})"
        return obj_repr
