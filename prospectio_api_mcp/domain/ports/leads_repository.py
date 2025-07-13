from abc import ABC, abstractmethod
from domain.entities.leads import Leads


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
