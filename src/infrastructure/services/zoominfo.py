import json
from application.ports.prospect_api import ProspectAPIPort


class ZoomInfoAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the ZoomInfo API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "Enterprise DataMax Inc",
                    "industry": "Enterprise Data Solutions",
                    "size": 1500,
                    "location": "Boston, USA"
                },
                {
                    "name": "Global CRM Systems",
                    "industry": "CRM Software",
                    "size": 750,
                    "location": "Atlanta, USA"
                }
            ],
            "contacts": [
                {
                    "name": "Katherine Miller",
                    "email": "katherine.miller@enterprisedatamax.com",
                    "phone": "+1 617 555 0147"
                },
                {
                    "name": "Thomas Anderson",
                    "email": "thomas.anderson@globalcrm.com",
                    "phone": "+1 404 555 0258"
                }
            ]
        }
        return mock_data
