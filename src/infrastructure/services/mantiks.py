import json
from application.ports.leads.get_leads import ProspectAPIPort


class MantiksAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Mantiks API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "Acme Corp",
                    "industry": "Technology",
                    "size": 250,
                    "location": "Paris, France"
                },
                {
                    "name": "Globex Inc",
                    "industry": "Finance",
                    "size": 1200,
                    "location": "London, UK"
                }
            ],
            "contacts": [
                {
                    "name": "John Doe",
                    "email": "john.doe@acme.com",
                    "phone": "+33 1 23 45 67 89"
                },
                {
                    "name": "Jane Smith",
                    "email": "jane.smith@globex.com",
                    "phone": "+44 20 7946 0958"
                }
            ]
        }
        return mock_data