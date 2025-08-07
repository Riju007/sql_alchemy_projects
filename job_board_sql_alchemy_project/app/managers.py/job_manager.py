from sqlalchemy.orm import Session
from app.models.job import JobPost


class JobManger:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active_jobs(self, limit=10):
        active_job_list = (
            self.db.query(JobPost)
            .filter(JobPost.is_active == True)
            .order_by(JobPost.posted_on.desc())
            .limit(limit)
            .all()
        )
        return active_job_list

    def search_by_keyword(self, keyword: str):
        job_list = (
            self.db.query(JobPost)
            .filter(JobPost.description.ilike(f"%{keyword}%"))
            .order_by(JobPost.posted_on.desc())
            .all()
        )
        return job_list
