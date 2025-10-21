import logging

from apps.appelsoffres.models import TypeMarche
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Insérer des Types de marche fictifs dans la base de données.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = ["Travaux", "Fournitures", "Services"]

    def handle(self, *args, **kwargs):
        logging.info(f" Adding 'Type Marche' ...")
        try:
            for type_marche_libelle in self.data:
                type_marche, created = TypeMarche.objects.update_or_create(
                    libelle=type_marche_libelle,
                    defaults={"libelle": type_marche_libelle},
                )
                if type_marche:
                    logging.info(f"TypeMarche : {type_marche_libelle} added")
                else:
                    logging.warning(f"TypeMarche : {type_marche_libelle} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating TypeMarche : {e}")
