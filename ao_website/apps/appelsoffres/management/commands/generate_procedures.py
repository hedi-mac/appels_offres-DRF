import logging

from apps.appelsoffres.models import Procedure
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Insérer des Procedures de marche fictifs dans la base de données.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [
            "Procédure Adaptée",
            "Procédure Concours ouvert",
            "Procédure Concours restreint",
            "Procédure Dialogue compétitif",
            "Procédure NC",
            "Procédure Négociée",
            "Procédure Ouverte",
            "Procédure Partenariat innovation",
            "Procédure Restreinte",
        ]

    def handle(self, *args, **kwargs):
        logging.info(f" Adding 'Procedure' ...")
        try:
            for procedure_libelle in self.data:
                procedure, created = Procedure.objects.update_or_create(
                    libelle=procedure_libelle, defaults={"libelle": procedure_libelle}
                )
                if procedure:
                    logging.info(f"Procedure : {procedure_libelle} added")
                else:
                    logging.warning(f"Procedure : {procedure_libelle} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Procedure : {e}")
