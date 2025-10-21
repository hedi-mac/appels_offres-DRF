import logging

from apps.appelsoffres.models import Competence
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Insérer des Competences fictifs dans la base de données.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [
            "Ingénierie des infrastructures routières",
            "OPC",
            "Gestion de projet",
            "Analyse financière",
            "Marketing digital",
            "Gestion des ressources humaines",
            "Ingénierie des matériaux",
            "Analyse de marché",
            "Service client",
            "Gestion des stocks",
        ]

    def handle(self, *args, **kwargs):
        logging.info(f" Adding 'Competence' ...")
        try:
            for competence_libelle in self.data:
                competence, created = Competence.objects.update_or_create(
                    libelle=competence_libelle, defaults={"libelle": competence_libelle}
                )
                if competence:
                    logging.info(f"Competence : {competence_libelle} added")
                else:
                    logging.warning(f"Competence : {competence_libelle} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Competence : {e}")
