from typing import List, Optional
from datetime import datetime
from sqlalchemy import ARRAY, DateTime, String, Text, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from infrastructure.dto.database.base import Base


class Job(Base):
    """
    Represents a job with optional fields to match frontend requirements.
    SQLAlchemy model for database persistence.
    """

    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="Unique identifier for the job",
    )
    company_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("companies.id", ondelete="CASCADE"),
        doc="ID of the company associated with the job",
    )
    date_creation: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), doc="Creation date of the job posting"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, doc="Description of the job"
    )
    job_title: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Title of the job"
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Location of the job"
    )
    salary: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Salary details for the job"
    )
    job_seniority: Mapped[Optional[str]] = mapped_column(
        String(100), doc="Seniority level of the job (e.g., junior, mid, senior)"
    )
    job_type: Mapped[Optional[str]] = mapped_column(
        String(100), doc="Type of job (e.g., full-time, part-time)"
    )
    sectors: Mapped[Optional[str]] = mapped_column(
        String(255), doc="Sectors related to the job"
    )
    apply_url: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), doc="List of URLs to apply for the job"
    )

    def __repr__(self) -> str:
        """
        String representation of the Job object.

        Returns:
            str: A string representation showing id, job_title, and company_id.
        """
        return f"Job(id={self.id!r}, job_title={self.job_title!r}, company_id={self.company_id!r})"


# Type alias for a list of jobs
JobList = List[Job]
