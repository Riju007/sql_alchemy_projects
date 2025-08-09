import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import JobPost, Application

app = typer.Typer(help="Job Board ClI")
console = Console()


# dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# job commands
jobs_app = typer.Typer(help="Manage Jobs")


@jobs_app.command("list")
def list_jobs():
    """List all jobs"""
    db: Session = next(get_db())
    jobs = db.query(JobPost).all()

    table = Table(title="Jobs")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Company", style="magenta")

    for job in jobs:
        table.add_row(str(job.id), job.title, job.company.name)

    console.print(table)


@jobs_app.command("job-by-company")
def jobs_by_company(company_id: int):
    """Get all the jobs available for a company."""
    db: Session = next(get_db())
    jobs = db.query(JobPost).filter(JobPost.company_id == company_id).all()

    table = Table(title=f"Jobs for company {company_id}", width=50)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")

    for job in jobs:
        table.add_row(str(job.id), job.title)
    console.print(table)


applications_app = typer.Typer(help="Manage Applications")


@applications_app.command("by-user")
def applications_by_user(user_id: int):
    db: Session = next(get_db())
    applications = db.query(Application).filter(Application.user_id == user_id).all()
    table = Table(title=f"Application by user {user_id}")
    table.add_column("Application ID", style="cyan")
    table.add_column("Job ID", style="green")

    for application in applications:
        table.add_row(f"{application.user.name}", f"{application.job.title}")
    console.print(table)


# add sub commands
app.add_typer(jobs_app, name="jobs")
app.add_typer(applications_app, name="applications")

if __name__ == "__main__":
    app()
