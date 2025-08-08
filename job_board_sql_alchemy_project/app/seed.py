from faker import Faker
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User, JobPost, Company, Application, UserRole
from random import choice, randint

fake = Faker()


def seed_user(db: Session, count=5):
    users = []
    for _ in range(count):
        user_obj = User(
            email=fake.unique.email(),
            name=fake.name(),
            role=choice([UserRole.CANDIDATE, UserRole.EMPLOYER]),
        )
        db.add(user_obj)
        users.append(user_obj)
    db.commit()
    return users


def seed_companies(db: Session, users, count=5):
    companies = []
    for _ in range(count):
        user_obj = choice(users)
        company_obj = Company(
            name=fake.company(),
            location=fake.city(),
            industry=fake.bs(),
            owner_id=user_obj.id,
        )
        db.add(company_obj)
        companies.append(company_obj)
    db.commit()
    return companies


def seed_jobs(db: Session, companies: list, count=5):
    jobs = []
    for _ in range(count):
        job_obj = JobPost(
            title=fake.job(),
            description=fake.text(),
            location=fake.city(),
            company_id=choice(companies).id,
        )
        db.add(job_obj)
        jobs.append(job_obj)
    db.commit()
    return jobs


def seed_application(db: Session, users, jobs, count=5):
    for _ in range(count):
        user = choice(users)
        job = choice(jobs)
        exists = (
            db.query(Application)
            .filter(Application.user_id == user.id, Application.job_id == job.id)
            .first()
        )
        if not exists:
            application_obj = Application(user_id=user.id, job_id=job.id)
            db.add(application_obj)
    db.commit()


def run_seed():
    db: Session = SessionLocal()
    users = seed_user(db)
    companies = seed_companies(db, users)
    jobs = seed_jobs(db, companies)
    seed_application(db, users, jobs)
    db.close()


if __name__ == "__main__":
    run_seed()
