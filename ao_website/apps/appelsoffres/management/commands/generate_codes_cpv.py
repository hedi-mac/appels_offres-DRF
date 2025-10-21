import logging

import pandas as pd
from apps.appelsoffres.models import CodeCPV
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Insérer des Code CPV fictifs dans la base de données.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = "ao_website/apps/static/data/cpv_2008_fr.xls"
        self.df = pd.read_excel(self.file_path)
        self.data = self.df.loc[4:20, ["CODE", "FR"]].iterrows()

    def handle(self, *args, **kwargs):
        """
        Génère et enregistre plusieurs objets 'Code CPV' aléatoires avec des relations associées.
        """
        logging.info(f" Adding 'Code CPV' ...")
        try:
            for index, code_cpv_data in self.data:
                code_cpv, created = CodeCPV.objects.update_or_create(
                    code=code_cpv_data["CODE"],
                    defaults={
                        "code": code_cpv_data["CODE"],
                        "nom": code_cpv_data["FR"],
                    },
                )
                if code_cpv:
                    logging.info(f"Code cpv : {code_cpv_data['CODE']} added")
                else:
                    logging.warning(f"Code cpv : {code_cpv_data['CODE']} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating code cpv : {e}")
