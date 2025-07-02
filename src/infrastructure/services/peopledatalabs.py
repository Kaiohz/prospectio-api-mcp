import json
from application.ports.get_leads import ProspectAPIPort


class PeopleDataLabsAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the People Data Labs API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "InnovateTech Corp",
                    "industry": "Artificial Intelligence",
                    "size": 180,
                    "location": "San Francisco, USA"
                },
                {
                    "name": "DataPro Analytics",
                    "industry": "Data Science",
                    "size": 95,
                    "location": "Toronto, Canada"
                }
            ],
            "contacts": [
                {
                    "name": "Sarah Johnson",
                    "email": "sarah.johnson@innovatetech.com",
                    "phone": "+1 415 555 0123"
                },
                {
                    "name": "Michael Chen",
                    "email": "michael.chen@datapro.ca",
                    "phone": "+1 416 555 0456"
                }
            ]
        }
        return mock_data
