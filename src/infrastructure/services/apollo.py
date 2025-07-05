from domain.ports.prospect_api import ProspectAPIPort


class ApolloAPI(ProspectAPIPort):
    """
    Adapter for the Apollo.io API to fetch lead data.
    """

    async def fetch_leads(self, location: str, job_title: list[str]) -> dict:
        """
        Fetch leads from the Apollo.io API.

        Returns:
            dict: Mock data containing companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "GrowthScale Ventures",
                    "industry": "Sales Technology",
                    "size": 220,
                    "location": "New York, USA"
                },
                {
                    "name": "ProspectMax Inc",
                    "industry": "Lead Generation",
                    "size": 65,
                    "location": "Austin, USA"
                }
            ],
            "contacts": [
                {
                    "name": "Robert Martinez",
                    "email": "robert.martinez@growthscale.com",
                    "phone": "+1 212 555 0789"
                },
                {
                    "name": "Emily Davis",
                    "email": "emily.davis@prospectmax.com",
                    "phone": "+1 512 555 0321"
                }
            ]
        }
        return mock_data
