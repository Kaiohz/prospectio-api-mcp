import json
from application.ports.get_leads import ProspectAPIPort


class LushaAPI(ProspectAPIPort):
    
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Lusha API.
        Returns a mock JSON with companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "B2B Connect Ltd",
                    "industry": "Business Intelligence",
                    "size": 190,
                    "location": "Tel Aviv, Israel"
                },
                {
                    "name": "TechSegment Corp",
                    "industry": "Technology Consulting",
                    "size": 80,
                    "location": "London, UK"
                }
            ],
            "contacts": [
                {
                    "name": "Avi Cohen",
                    "email": "avi.cohen@b2bconnect.co.il",
                    "phone": "+972 3 123 4567"
                },
                {
                    "name": "Oliver Brown",
                    "email": "oliver.brown@techsegment.co.uk",
                    "phone": "+44 20 7946 0123"
                }
            ]
        }
        return mock_data
