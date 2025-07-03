from domain.ports.prospect_api import ProspectAPIPort



class HunterAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Hunter.io API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "StartupHub Co",
                    "industry": "Business Services",
                    "size": 85,
                    "location": "Berlin, Germany"
                },
                {
                    "name": "CloudFirst Solutions",
                    "industry": "Cloud Computing",
                    "size": 300,
                    "location": "Amsterdam, Netherlands"
                }
            ],
            "contacts": [
                {
                    "name": "Hans Mueller",
                    "email": "hans.mueller@startuphub.de",
                    "phone": "+49 30 12345678"
                },
                {
                    "name": "Anna van Berg",
                    "email": "anna.vanberg@cloudfirst.nl",
                    "phone": "+31 20 1234567"
                }
            ]
        }
        return mock_data
