from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ApplyOptionDTO(BaseModel):
    """
    Data Transfer Object representing a job application option.

    Attributes:
        publisher (Optional[str]): The publisher of the job posting.
        apply_link (Optional[str]): The URL to apply for the job.
        is_direct (Optional[bool]): Whether the application is direct.
    """

    publisher: Optional[str] = None
    apply_link: Optional[str] = None
    is_direct: Optional[bool] = None


class JobRequiredExperienceDTO(BaseModel):
    """
    Data Transfer Object representing job required experience.

    Attributes:
        no_experience_required (Optional[bool]): Whether no experience is required.
        required_experience_in_months (Optional[int]): Required experience in months.
        experience_mentioned (Optional[bool]): Whether experience is mentioned.
        experience_preferred (Optional[bool]): Whether experience is preferred.
    """

    no_experience_required: Optional[bool] = None
    required_experience_in_months: Optional[int] = None
    experience_mentioned: Optional[bool] = None
    experience_preferred: Optional[bool] = None


class JobHighlightsDTO(BaseModel):
    """
    Data Transfer Object representing job highlights.

    Attributes:
        qualifications (Optional[List[str]]): List of job qualifications.
        responsibilities (Optional[List[str]]): List of job responsibilities.
    """

    qualifications: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None


class JobDataDTO(BaseModel):
    """
    Data Transfer Object representing a job data item from JSearch API.

    Attributes:
        job_id (Optional[str]): The unique job identifier.
        job_title (Optional[str]): The title of the job.
        employer_name (Optional[str]): The name of the employer.
        employer_logo (Optional[str]): The URL to the employer's logo.
        employer_website (Optional[str]): The employer's website URL.
        employer_company_type (Optional[str]): The type of the employer company.
        employer_linkedin (Optional[str]): The employer's LinkedIn URL.
        job_publisher (Optional[str]): The publisher of the job posting.
        job_employment_type (Optional[str]): The type of employment.
        job_employment_types (Optional[List[str]]): List of employment types.
        job_employment_type_text (Optional[str]): Text description of employment type.
        job_apply_link (Optional[str]): The URL to apply for the job.
        job_apply_is_direct (Optional[bool]): Whether the application is direct.
        job_apply_quality_score (Optional[float]): The quality score of the job application.
        apply_options (Optional[List[ApplyOptionDTO]]): List of application options.
        job_description (Optional[str]): The job description.
        job_is_remote (Optional[bool]): Whether the job is remote.
        job_posted_human_readable (Optional[str]): When the job was posted (human readable).
        job_posted_at_timestamp (Optional[int]): The timestamp when the job was posted.
        job_posted_at_datetime_utc (Optional[str]): The UTC datetime when the job was posted.
        job_location (Optional[str]): The job location.
        job_city (Optional[str]): The city where the job is located.
        job_state (Optional[str]): The state where the job is located.
        job_country (Optional[str]): The country where the job is located.
        job_latitude (Optional[float]): The latitude of the job location.
        job_longitude (Optional[float]): The longitude of the job location.
        job_benefits (Optional[str]): The job benefits.
        job_google_link (Optional[str]): The Google link to the job.
        job_offer_expiration_datetime_utc (Optional[str]): The UTC datetime when the job offer expires.
        job_offer_expiration_timestamp (Optional[int]): The timestamp when the job offer expires.
        job_required_experience (Optional[JobRequiredExperienceDTO]): The required experience for the job.
        job_salary (Optional[str]): The job salary.
        job_min_salary (Optional[float]): The minimum salary.
        job_max_salary (Optional[float]): The maximum salary.
        job_salary_currency (Optional[str]): The currency of the salary.
        job_salary_period (Optional[str]): The salary period.
        job_highlights (Optional[JobHighlightsDTO]): The job highlights.
        job_job_title (Optional[str]): Alternative job title field.
        job_posting_language (Optional[str]): The language of the job posting.
        job_onet_soc (Optional[str]): The O*NET SOC code.
        job_onet_job_zone (Optional[str]): The O*NET job zone.
        job_occupational_categories (Optional[List[str]]): List of occupational categories.
        job_naics_code (Optional[str]): The NAICS code.
        job_naics_name (Optional[str]): The NAICS name.
    """

    job_id: Optional[str] = None
    job_title: Optional[str] = None
    employer_name: Optional[str] = None
    employer_logo: Optional[str] = None
    employer_website: Optional[str] = None
    employer_company_type: Optional[str] = None
    employer_linkedin: Optional[str] = None
    job_publisher: Optional[str] = None
    job_employment_type: Optional[str] = None
    job_employment_types: Optional[List[str]] = None
    job_employment_type_text: Optional[str] = None
    job_apply_link: Optional[str] = None
    job_apply_is_direct: Optional[bool] = None
    job_apply_quality_score: Optional[float] = None
    apply_options: Optional[List[ApplyOptionDTO]] = None
    job_description: Optional[str] = None
    job_is_remote: Optional[bool] = None
    job_posted_human_readable: Optional[str] = None
    job_posted_at_timestamp: Optional[int] = None
    job_posted_at_datetime_utc: Optional[str] = None
    job_location: Optional[str] = None
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    job_country: Optional[str] = None
    job_latitude: Optional[float] = None
    job_longitude: Optional[float] = None
    job_benefits: Optional[str] = None
    job_google_link: Optional[str] = None
    job_offer_expiration_datetime_utc: Optional[str] = None
    job_offer_expiration_timestamp: Optional[int] = None
    job_required_experience: Optional[JobRequiredExperienceDTO] = None
    job_salary: Optional[str] = None
    job_min_salary: Optional[float] = None
    job_max_salary: Optional[float] = None
    job_salary_currency: Optional[str] = None
    job_salary_period: Optional[str] = None
    job_highlights: Optional[JobHighlightsDTO] = None
    job_job_title: Optional[str] = None
    job_posting_language: Optional[str] = None
    job_onet_soc: Optional[str] = None
    job_onet_job_zone: Optional[str] = None
    job_occupational_categories: Optional[List[str]] = None
    job_naics_code: Optional[str] = None
    job_naics_name: Optional[str] = None


class JSearchParametersDTO(BaseModel):
    """
    Data Transfer Object representing the parameters of a JSearch API request.

    Attributes:
        query (Optional[str]): The search query string.
        page (Optional[int]): The current page number.
        num_pages (Optional[int]): The total number of pages.
        date_posted (Optional[str]): The date the job was posted.
        country (Optional[str]): The country for the search.
        language (Optional[str]): The language for the search.
    """

    query: Optional[str] = None
    page: Optional[int] = None
    num_pages: Optional[int] = None
    date_posted: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None


class JSearchResponseDTO(BaseModel):
    """
    Data Transfer Object representing the response from the JSearch API.

    Attributes:
        status (Optional[str]): The status of the response.
        request_id (Optional[str]): The unique request identifier.
        parameters (Optional[JSearchParametersDTO]): The parameters used for the request.
        data (Optional[List[JobDataDTO]]): The list of job data items returned by the API.
    """

    status: Optional[str] = None
    request_id: Optional[str] = None
    parameters: Optional[JSearchParametersDTO] = None
    data: Optional[List[JobDataDTO]] = None
