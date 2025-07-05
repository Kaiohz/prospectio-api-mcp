from domain.ports.prospect_api import ProspectAPIPort


class PeopleDataLabsAPI(ProspectAPIPort):
    """
    Adapter for the People Data Labs API to fetch lead data.
    """

    async def fetch_leads(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch leads from the People Data Labs API.

        Returns:
            dict: Mock data containing companies and contacts.
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
