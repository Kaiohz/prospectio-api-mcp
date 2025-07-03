from domain.ports.prospect_api import ProspectAPIPort



class DropcontactAPI(ProspectAPIPort):
    """
    Adapter for the Dropcontact API to fetch lead data.
    """
    async def fetch_leads(self) -> dict:
        """
        Fetch leads from the Dropcontact API.

        Returns:
            dict: Mock data containing companies and contacts.
        """
        mock_data = {
            "companies": [
                {
                    "name": "French Innovations SARL",
                    "industry": "HR Technology",
                    "size": 55,
                    "location": "Nantes, France"
                },
                {
                    "name": "RGPD Solutions SAS",
                    "industry": "Compliance Technology",
                    "size": 35,
                    "location": "Toulouse, France"
                }
            ],
            "contacts": [
                {
                    "name": "Julien Moreau",
                    "email": "julien.moreau@frenchinnovations.fr",
                    "phone": "+33 2 40 12 34 56"
                },
                {
                    "name": "Camille Laurent",
                    "email": "camille.laurent@rgpdsolutions.fr",
                    "phone": "+33 5 61 78 90 12"
                }
            ]
        }
        return mock_data
