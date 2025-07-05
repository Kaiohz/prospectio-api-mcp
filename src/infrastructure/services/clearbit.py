from domain.ports.prospect_api import ProspectAPIPort



class ClearbitAPI(ProspectAPIPort):
    """
    Adapter for the Clearbit API to fetch lead data.
    """
    
    async def fetch_leads(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch leads from the Clearbit API.

        Returns:
            dict: Mock data containing companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "TechStart SAS",
                    "industry": "SaaS",
                    "size": 45,
                    "location": "Lyon, France"
                },
                {
                    "name": "Digital Solutions Ltd",
                    "industry": "Marketing Technology",
                    "size": 120,
                    "location": "Manchester, UK"
                }
            ],
            "contacts": [
                {
                    "name": "Marie Dupont",
                    "email": "marie.dupont@techstart.fr",
                    "phone": "+33 4 72 85 96 74"
                },
                {
                    "name": "James Wilson",
                    "email": "james.wilson@digitalsolutions.co.uk",
                    "phone": "+44 161 234 5678"
                }
            ]
        }
        return mock_data
