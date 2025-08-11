import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.db import SessionLocal
from app.models import JobPost, Application, Company
from app.managers import JobManger


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


@jobs_app.command("job-count-company")
def job_per_company(
    limit: int = typer.Option(None, help="Limit the number of companies shown")
):
    """Job per company."""
    db: Session = next(get_db())
    job_count = func.count(JobPost.id).label("job_count")
    statement = (
        select(Company.name, job_count)
        .join(JobPost, Company.id == JobPost.company_id)
        .group_by(Company.id, Company.name)
        .order_by(job_count.desc())
    )
    if limit:
        statement = statement.limit(limit)
    job_count_list = db.execute(statement).all()

    # calculate total jobs
    total_jobs = sum(count for _, count in job_count_list)
    table = Table(title="Job Count by company")
    table.add_column("Index", style="red")
    table.add_column("Company Name", style="cyan")
    table.add_column("Job Count", style="green")
    for index, (company_name, count) in enumerate(job_count_list, 1):
        table.add_row(str(index), company_name, str(count))

    # add summary row
    table.add_section()
    table.add_row(
        "", "[bold yellow]Total[/bold yellow]", f"[bold green]{total_jobs}[/bold green]"
    )
    console.print(table)
    return job_count_list


@jobs_app.command("add-job", help="Add a new job")
def add_job_via_cli(
    title: str, description: str, company_id: int, location: str | None = None
):
    """Add a job post via cli."""
    db = next(get_db())
    manager = JobManger(db)
    job = manager.post_job(title, description, company_id, location)
    console.print(f"[green]Job Created:[/green] {job.title} (ID: {job.id})")


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
