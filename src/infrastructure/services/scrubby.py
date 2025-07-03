from domain.ports.prospect_api import ProspectAPIPort


class ScrubbyAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Scrubby API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "Data Cleansing France",
                    "industry": "Data Management",
                    "size": 42,
                    "location": "Marseille, France"
                },
                {
                    "name": "CRM Optimization SAS",
                    "industry": "Business Software",
                    "size": 28,
                    "location": "Bordeaux, France"
                }
            ],
            "contacts": [
                {
                    "name": "Antoine Rousseau",
                    "email": "antoine.rousseau@datacleansing.fr",
                    "phone": "+33 4 91 23 45 67"
                },
                {
                    "name": "Sophie Martin",
                    "email": "sophie.martin@crmoptimization.fr",
                    "phone": "+33 5 56 78 90 12"
                }
            ]
        }
        return mock_data
