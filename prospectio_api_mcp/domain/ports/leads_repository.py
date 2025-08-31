from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.leads import Leads
from domain.entities.company import CompanyEntity
from domain.entities.job import JobEntity
from domain.entities.contact import ContactEntity


class LeadsRepositoryPort(ABC):
    """
    Abstract port interface for inserting leads into a database.
    """

    @abstractmethod
    async def save_leads(self, leads: Leads) -> None:
        """
        Insert leads into the database.

        Args:
            leads (Leads): The leads data to insert.
        """
        pass

    @abstractmethod
    async def get_jobs(self, offset: int, limit: int) -> JobEntity:
        """
        Retrieve jobs from the database with pagination.

        Args:
            offset (int): Number of jobs to skip.
            limit (int): Maximum number of jobs to return.

        Returns:
            JobEntity: Domain entity containing list of jobs.
        """
        pass

    @abstractmethod
    async def get_jobs_by_title_and_location(
        self, title: list[str], location: list[str]
    ) -> JobEntity:
        """
        Retrieve a job by its title and location from the database.

        Args:
            title (str): The title of the job to search for.
            location (str): The location of the job to search for.

        Returns:
            JobEntity: Domain entity containing the job details.
        """
        pass

    @abstractmethod
    async def get_companies(self, offset: int, limit: int) -> CompanyEntity:
        """
        Retrieve companies from the database.

        Returns:
            CompanyEntity: Domain entity containing list of companies.
        """
        pass

    @abstractmethod
    async def get_companies_by_names(self, company_names: List[str]) -> CompanyEntity:
        """
        Retrieve companies by their names from the database.

        Args:
            company_names (List[str]): List of company names to search for.

        Returns:
            CompanyEntity: Domain entity containing list of companies matching the names.
        """
        pass

    @abstractmethod
    async def get_contacts(self, offset: int, limit: int) -> ContactEntity:
        """
        Retrieve contacts from the database.

        Returns:
            ContactEntity: Domain entity containing list of contacts.
        """
        pass

    @abstractmethod
    async def get_contacts_by_name_and_title(
        self, names: list[str], titles: list[str]
    ) -> ContactEntity:
        """
        Retrieve contacts by their name and title from the database.
        Args:
            name (str): The name of the contact to search for.
            title (str): The title of the contact to search for.

        Returns:
            ContactEntity: Domain entity containing list of contacts matching the name and title.
        """
        pass

    @abstractmethod
    async def get_leads(self, offset: int, limit: int) -> Leads:
        """
        Retrieve all leads data (companies, jobs, and contacts) from the database.

        Returns:
            Leads: Domain entity containing all companies, jobs, and contacts.
        """
        pass
