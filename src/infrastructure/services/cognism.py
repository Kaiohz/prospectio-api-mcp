import json
from application.ports.prospect_api import ProspectAPIPort


class CognismAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Cognism API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "EuroTech Solutions",
                    "industry": "B2B Software",
                    "size": 340,
                    "location": "Brussels, Belgium"
                },
                {
                    "name": "GDPR Compliance Ltd",
                    "industry": "Legal Technology",
                    "size": 75,
                    "location": "Dublin, Ireland"
                }
            ],
            "contacts": [
                {
                    "name": "Pierre Dubois",
                    "email": "pierre.dubois@eurotech.be",
                    "phone": "+32 2 123 45 67"
                },
                {
                    "name": "Siobhan O'Connor",
                    "email": "siobhan.oconnor@gdprcompliance.ie",
                    "phone": "+353 1 234 5678"
                }
            ]
        }
        return mock_data
