import logging

from apps.appelsoffres.models import Departement, Region
from apps.appelsoffres.utils import call_api
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Insérer des Departements et leurs Regions dans la base de données.
    """

    BASE_URL = "https://geo.api.gouv.fr"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def provide_regions(self) -> None:
        logging.info(f" Adding 'Region' ...")
        try:
            json_data = call_api(api_url=f"{self.BASE_URL}/regions", params=None)
            for result in json_data:
                region, created = Region.objects.update_or_create(
                    code=result["code"],
                    defaults={"code": result["code"], "nom": result["nom"]},
                )
                if region:
                    logging.info(f"Region : {result['nom']} added")
                else:
                    logging.warning(f"Region : {result['nom']} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Region : {e}")

    def provide_departement(self) -> None:
        logging.info(f" Adding 'Departement' ...")
        try:
            json_data = call_api(api_url=f"{self.BASE_URL}/departements", params=None)
            for result in json_data:
                departement, created = Departement.objects.update_or_create(
                    code=result["code"],
                    defaults={
                        "code": result["code"],
                        "nom": result["nom"],
                        "region": Region.objects.filter(code=result["codeRegion"]).first(),
                    },
                )
                if departement:
                    logging.info(f"Departement : {result['nom']} added")
                else:
                    logging.warning(f"Departement : {result['nom']} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Departement : {e}")

    def handle(self, *args, **kwargs):
        self.provide_regions()
        self.provide_departement()
