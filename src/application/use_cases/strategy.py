from abc import abstractmethod

from application.ports.prospect_api import ProspectAPIPort


class GetLeadsStrategy:
    """
    Port for getting leads with contacts.
    """
    def __init__(self, location: str, port: ProspectAPIPort):
        self.location = location
        self.port = port

    @abstractmethod
    async def execute(self):
        pass