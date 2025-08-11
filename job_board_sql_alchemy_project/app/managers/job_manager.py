from sqlalchemy.orm import Session
from app.models import JobPost, Company
from sqlalchemy import select


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

    def post_job(
        self,
        title: str,
        description: str,
        company_id: int,
        location: str | None = None,
    ) -> JobPost:
        company_obj = self.db.execute(
            select(Company).where(Company.id == company_id)
        ).scalar_one_or_none()
        if not company_obj:
            raise ValueError(f"Company with ID {company_id} does not exists.")
        job_obj: JobPost = JobPost(
            title=title,
            description=description,
            company_id=company_id,
            location=location,
        )
        self.db.add(job_obj)
        self.db.commit()
        self.db.refresh(job_obj)
        return job_obj
