import logging
from typing import Dict, Optional

import requests
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def call_api(api_url: str, params: Dict) -> Optional[Dict]:
    """
    Effectue une requête GET sur l'API et renvoie la réponse JSON.

    Args:
        api_url (str): URL complète de l'API.
        params (json): Paramètres de requête.

    Returns:
        dict | list | None: Réponse JSON ou None en cas d'erreur.
    """
    try:
        if params:
            response = requests.get(url=api_url, params=params)
        else:
            response = requests.get(url=api_url)
        if response.status_code == 200:
            json_response = response.json()
            return json_response
        else:
            logging.warning(f"Error : {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"An error occurred calling API : {e}")
    return None


class MarchePagination(PageNumberPagination):
    """Custom pagination for Marche."""

    page_size = 10
    page_size_query_param = "nb_per_page"
    max_page_size = 100

    def get_paginated_response(self, data: list[Dict]) -> Response:
        """
        Build a standardized paginated API response for the Marche resource.

        Args:
            data (list[dict]): The serialized list of items for the current page.

        Returns:
            Response: A DRF Response object containing both results and pagination metadata.
        """
        return Response(
            {
                "marches": data,
                "pagination": {
                    "page": self.page.number,
                    "page_size": self.get_page_size(self.request),
                    "total_pages": self.page.paginator.num_pages,
                    "total_count": self.page.paginator.count,
                    "next_page_number": (self.page.next_page_number() if self.page.has_next() else None),
                    "previous_page_number": (self.page.previous_page_number() if self.page.has_previous() else None),
                },
            }
        )
