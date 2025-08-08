from sqlalchemy.orm import Session
from app.models.application import Application


class ApplicationManager:

    def __init__(self, db: Session):
        self.db = db

    def apply(self, user_id: int, job_id: int):
        exists = (
            self.db.query(Application)
            .filter(Application.user_id == user_id, Application.job_id == job_id)
            .first()
        )
        if exists:
            raise ValueError("User has already applied for this job.")
        application = Application(user_id=user_id, job_id=job_id)
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_application_by_user(self, user_id: int):
        queryset = (
            self.db.query(Application).filter(Application.user_id == user_id).all()
        )
        return queryset
