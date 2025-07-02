from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SalaryDTO(BaseModel):
    """DTO représentant le salaire d'un poste."""
    min: Optional[int] = None
    max: Optional[int] = None
    type: Optional[str] = None

class JobDTO(BaseModel):
    """DTO représentant un poste/job dans une entreprise."""
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

class CompanyDTO(BaseModel):
    """DTO représentant une entreprise avec ses offres d'emploi."""
    id: Optional[str] = None
    jobs: Optional[List[JobDTO]] = None
    max_company_size: Optional[int] = None
    min_company_size: Optional[int] = None
    name: Optional[str] = None
    social_urls: Optional[Dict[str, str]] = None
    website: Optional[str] = None

class CompanyResponseDTO(BaseModel):
    """DTO représentant la réponse complète de recherche d'entreprises et jobs."""
    companies: Optional[List[CompanyDTO]] = None
    credits_cost: Optional[int] = None
    credits_remaining: Optional[int] = None
    nb_companies: Optional[int] = None
    nb_jobs: Optional[int] = None
