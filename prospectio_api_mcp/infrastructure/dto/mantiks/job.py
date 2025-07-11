from typing import Any, Optional, List
from pydantic import BaseModel
from infrastructure.dto.mantiks.salary import SalaryDTO


class JobDTO(BaseModel):
    """
    Data Transfer Object representing a job position within a company.

    Attributes:
        date_creation (Optional[str]): Creation date of the job posting.
        description (Optional[str]): Description of the job.
        job_board (Optional[str]): Name of the job board.
        job_board_id (Optional[Any]): Identifier for the job board.
        job_board_url (Optional[str]): URL to the job board posting.
        job_id (Optional[str]): Unique job identifier.
        job_title (Optional[str]): Title of the job.
        last_seen (Optional[str]): Last seen date for the job posting.
        location (Optional[str]): Location of the job.
        salary (Optional[SalaryDTO]): Salary details for the job.
        job_seniority (Optional[str]): Seniority level of the job.
        job_type (Optional[str]): Type of job (e.g., full-time, part-time).
        sectors (Optional[List[str]]): List of sectors related to the job.
        indeed_easy_apply (Optional[bool]): Whether Indeed Easy Apply is available.
        indeed_apply_url (Optional[str]): URL for Indeed application.
        linkedin_recruiter_name (Optional[str]): Name of the LinkedIn recruiter.
        linkedin_recruiter_title (Optional[str]): Title of the LinkedIn recruiter.
        linkedin_recruiter_link (Optional[str]): LinkedIn profile link of the recruiter.
        linkedin_apply_url (Optional[str]): URL for LinkedIn application.
    """

    date_creation: Optional[str] = None
    description: Optional[str] = None
    job_board: Optional[str] = None
    job_board_id: Optional[Any] = None
    job_board_url: Optional[str] = None
    job_id: Optional[str] = None
    job_title: Optional[str] = None
    last_seen: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[SalaryDTO] = None
    job_seniority: Optional[str] = None
    job_type: Optional[str] = None
    sectors: Optional[List[str]] = None
    indeed_easy_apply: Optional[bool] = None
    indeed_apply_url: Optional[str] = None
    linkedin_recruiter_name: Optional[str] = None
    linkedin_recruiter_title: Optional[str] = None
    linkedin_recruiter_link: Optional[str] = None
    linkedin_apply_url: Optional[str] = None
