from abc import abstractmethod

from application.ports.get_leads import ProspectAPIPort


class GetLeadsStrategy:
    """
    Port for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        self.port = port

    @abstractmethod
    async def execute(source: str):
        pass