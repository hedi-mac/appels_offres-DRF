import logging
import random
from datetime import timedelta
from random import randint

from apps.appelsoffres.models import Acheteur, Competence, Departement, Marche, Piece, Procedure
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker


class Command(BaseCommand):
    """
    Insérer des marchés fictifs dans la base de données.
    """

    def handle(self, *args, **kwargs):
        """
        Génère et enregistre plusieurs objets 'Marche' aléatoires avec des relations associées.
        """
        logging.info(f" Adding 'Marche' ...")
        fake = Faker("fr_FR")
        departements = Departement.objects.all()
        acheteurs = Acheteur.objects.all()
        procedures = Procedure.objects.all()
        pieces = Piece.objects.all()
        competences = Competence.objects.all()
        for _ in range(108):
            try:
                MIN_DAYS = 50
                MAX_DAYS = 1000
                dates = []
                for _ in range(6):
                    random_days = random.randint(MIN_DAYS, MAX_DAYS)
                    random_date = timezone.localtime(timezone.now()) + timedelta(days=random_days)
                    dates.append(random_date)
                dates.append(timezone.make_aware(fake.date_time_this_year()))
                marche = Marche.objects.create(
                    objet=fake.sentence(nb_words=6, variable_nb_words=True),
                    prix=fake.random_number(digits=6),
                    groupement=fake.lexify(
                        text="En cas de groupement conjoint, le mandataire doit ".join([fake.word() for _ in range(10)])
                    ),
                    date_limite=dates[randint(0, len(dates) - 1)],
                    acheteur=acheteurs[randint(0, acheteurs.count() - 1)],
                    procedure=procedures[randint(0, procedures.count() - 1)],
                )
                num_departments = randint(1, 2)
                if num_departments == 2:
                    marche.departements.set(
                        [
                            departements[randint(0, departements.count() - 1)],
                            departements[randint(0, departements.count() - 1)],
                        ]
                    )
                else:
                    marche.departements.set([departements[randint(0, departements.count() - 1)]])

                marche.pieces.set(pieces.order_by("?")[: randint(1, pieces.count() - 1)])
                marche.competences.set(competences.order_by("?")[: randint(1, competences.count() - 1)])
                if marche:
                    logging.info(f"Marche: '{marche.objet}' added")
                else:
                    logging.warning(f"Marche : '{marche.objet}' not added")
            except Exception as e:
                logging.warning(f"Error updating or creating Marche : {e}")
