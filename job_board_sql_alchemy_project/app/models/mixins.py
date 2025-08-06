from sqlalchemy import Column, Boolean, DateTime, func


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ActiveFlagMixin:
    is_active = Column(Boolean, default=True, nullable=False)
