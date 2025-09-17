from abc import ABC, abstractmethod
from math import e
from domain.entities.company import Company
from domain.entities.profile import Profile
from domain.entities.contact import Contact
from domain.entities.prospect_message import ProspectMessage


class GenerateMessagePort(ABC):

    @abstractmethod
    async def get_message(
        self, profile: Profile, contact: Contact, company: Company
    ) -> ProspectMessage:
        pass
