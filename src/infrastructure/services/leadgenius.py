from domain.ports.prospect_api import ProspectAPIPort



class LeadGeniusAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the LeadGenius API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "Enterprise Solutions Group",
                    "industry": "Enterprise Software",
                    "size": 850,
                    "location": "Seattle, USA"
                },
                {
                    "name": "Custom Data Corp",
                    "industry": "Data Analytics",
                    "size": 150,
                    "location": "Chicago, USA"
                }
            ],
            "contacts": [
                {
                    "name": "Jennifer Thompson",
                    "email": "jennifer.thompson@enterprisesg.com",
                    "phone": "+1 206 555 0987"
                },
                {
                    "name": "David Kim",
                    "email": "david.kim@customdata.com",
                    "phone": "+1 312 555 0654"
                }
            ]
        }
        return mock_data
