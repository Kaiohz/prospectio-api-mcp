from typing import Any, Dict, Optional
import httpx

class BaseApiClient:
    """
    Client HTTP générique pour consommer des APIs externes de leads.
    Utilise httpx.AsyncClient pour les requêtes asynchrones.
    """
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: float = 30.0) -> None:
        """
        Initialise le client avec une base URL, des headers optionnels et un timeout.
        :param base_url: URL de base de l'API.
        :param headers: Dictionnaire d'en-têtes HTTP par défaut.
        :param timeout: Timeout en secondes pour les requêtes HTTP.
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self._client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=timeout)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        Effectue une requête GET asynchrone.
        :param endpoint: Chemin relatif de l'endpoint.
        :param params: Paramètres de requête optionnels.
        :return: Réponse httpx.Response
        """
        response = await self._client.get(endpoint, params=params)
        return response

    async def post(self, endpoint: str, data: Optional[Any] = None, json: Optional[Any] = None) -> httpx.Response:
        """
        Effectue une requête POST asynchrone.
        :param endpoint: Chemin relatif de l'endpoint.
        :param data: Données à envoyer dans le corps de la requête.
        :param json: Données JSON à envoyer dans le corps de la requête.
        :return: Réponse httpx.Response
        """
        return await self._client.post(endpoint, data=data, json=json)

    async def close(self) -> None:
        """
        Ferme le client HTTPX proprement.
        """
        await self._client.aclose()
