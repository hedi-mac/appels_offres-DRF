import logging

from apps.appelsoffres.models import Acheteur
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    """
    Insérer ou mettre à jour des acheteurs fictifs dans la base de données.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker("fr_FR")

    def generate_fake_address(self) -> str:
        """
        Génère une adresse fictive réaliste en français.

        Returns:
            str: Adresse complète sous forme de texte.
        """
        street_number = self.fake.building_number()
        street_name = self.fake.street_name()
        postal_code = self.fake.postcode()
        city = self.fake.city()
        address = f"{street_number} {street_name} {postal_code} {city}"
        return address

    def handle(self, *args, **kwargs):
        """
        Crée ou met à jour les acheteurs dans la base de données à partir d'une liste prédéfinie.
        """
        logging.info(f" Adding 'Acheteur' ...")
        try:
            acheteurs_list = [
                "rubis",
                "Enedis",
                "Clearbit",
                "Deloitte",
                "PwC",
                "CBS",
                "JP Morgan",
                "natixis",
                "eramet",
                "parispremiere",
                "solmax",
                "polytex",
            ]
            for denomination_acheteur in acheteurs_list:
                acheteur, created = Acheteur.objects.update_or_create(
                    denomination_sociale=denomination_acheteur,
                    defaults={
                        "denomination_sociale": denomination_acheteur,
                        "email": f"{denomination_acheteur}@gmail.com",
                        "adresse": self.generate_fake_address(),
                        "telephone": self.fake.phone_number(),
                    },
                )
                if acheteur:
                    logging.info(f"Acheteur : {acheteur.denomination_sociale} added")
                else:
                    logging.warning(f"Acheteur : {denomination_acheteur} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Acheteur : {e}")
