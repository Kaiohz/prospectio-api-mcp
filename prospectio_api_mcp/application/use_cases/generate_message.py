from domain.entities.prospect_message import ProspectMessage
from domain.ports.generate_message import GenerateMessagePort
from domain.ports.profile_respository import ProfileRepositoryPort
from domain.ports.leads_repository import LeadsRepositoryPort


class GenerateMessageUseCase:
    """
    Use case for retrieving leads with contacts from a specified source using the strategy pattern.
    This class selects the appropriate strategy based on the source and delegates the lead retrieval logic.
    """

    def __init__(
        self,
        repository: LeadsRepositoryPort,
        profile_repository: ProfileRepositoryPort,
        message_port: GenerateMessagePort
    ):
        """
        Initialize the GetLeadsUseCase with the required parameters and available strategies.

        Args:
            source (str): The lead source identifier (e.g., 'mantiks', 'clearbit').
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        self.repository = repository
        self.profile_repository = profile_repository
        self.message_port = message_port

    async def generate_message(
        self, id: str
    ) -> ProspectMessage:
        """
        Retrieve data based on the specified type from the repository.

        Returns:
            Union[Leads, CompanyEntity, JobEntity, ContactEntity]: The retrieved data object
            corresponding to the requested type.

        Raises:
            KeyError: If the specified type is not supported ('companies', 'jobs', 'contacts', 'leads').
        """
        profile = await self.profile_repository.get_profile()
        if not profile:
            raise ValueError(
                "Profile not found. Please create a profile before generating messages."
            )
        contact = await self.repository.get_contact_by_id(id)
        if not contact:
            raise ValueError(f"Contact with id {id} not found.")
        company = await self.repository.get_company_by_id(contact.company_id or "")
        if not company:
            raise ValueError(f"Company with id {contact.company_id} not found.")
        return await self.message_port.get_message(profile, contact, company)