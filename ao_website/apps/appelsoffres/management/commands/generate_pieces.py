import logging

from apps.appelsoffres.models import Piece
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = ["DCE", "Extrait SIRENE", "Extrait KBIS", "RIB", "DPGF", "RC"]

    def provide_piece(self) -> None:
        logging.info(" Adding 'Piece' ...")
        try:
            for piece_libelle in self.data:
                piece, created = Piece.objects.update_or_create(
                    libelle=piece_libelle, defaults={"libelle": piece_libelle}
                )
                if piece:
                    logging.info(f"Piece : {piece_libelle} added")
                else:
                    logging.warning(f"Piece : {piece_libelle} not added")
        except Exception as e:
            logging.warning(f"Error updating or creating Piece : {e}")

    def handle(self, *args, **kwargs):
        self.provide_piece()
