from abc import ABC, abstractmethod
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
    async def get_jobs(self) -> JobEntity:
        """
        Insert leads into the database.

        Args:
            leads (Leads): The leads data to insert.
        """
        pass

    @abstractmethod
    async def get_companies(self) -> CompanyEntity:
        """
        Retrieve companies from the database.

        Returns:
            CompanyEntity: Domain entity containing list of companies.
        """
        pass

    @abstractmethod
    async def get_contacts(self) -> ContactEntity:
        """
        Retrieve contacts from the database.

        Returns:
            ContactEntity: Domain entity containing list of contacts.
        """
        pass

    @abstractmethod
    async def get_leads(self) -> Leads:
        """
        Retrieve all leads data (companies, jobs, and contacts) from the database.

        Returns:
            Leads: Domain entity containing all companies, jobs, and contacts.
        """
        pass
