from rest_framework import status
from rest_framework.test import APITestCase
from apps.appelsoffres.models import Marche, Acheteur, Procedure, Departement, Competence, Piece

class MarcheAPITestCase(APITestCase):
    """
    Test API /api/marche/ CRUD + filters + pagination
    """

    created_marches = []

    def setUp(self):
        self.acheteur = Acheteur.objects.create(
            denomination_sociale="rubis",
            email="rubis@gmail.com",
            telephone="0367295025",
            adresse="91 boulevard de Lacroix 22414 Lucas-sur-Goncalves",
        )

        self.procedure = Procedure.objects.create(libelle="Procédure Concours ouvert")

        self.departement1 = Departement.objects.create(code="02", nom="Aisne")
        self.departement2 = Departement.objects.create(code="05", nom="Hautes-Alpes")

        self.competence1 = Competence.objects.create(libelle="OPC")
        self.competence2 = Competence.objects.create(libelle="Marketing digital")

        self.piece = Piece.objects.create(libelle="DPGF")

        self.base_url = "/api/marche/"

        self.marche_data = {
            "objet": "xxx yyyy zzzz ww",
            "prix": 99.0,
            "departement_ids": [self.departement1.id, self.departement2.id],
            "date_limite": "2026-11-14",
            "procedure_id": self.procedure.id,
            "competence_ids": [self.competence1.id, self.competence2.id],
            "piece_ids": [self.piece.id],
            "acheteur_id": self.acheteur.id,
            "groupement": "compteEn cas de groupement conjoint, le mandataire doit oeuvreEn cas de groupement conjoint, le mandataire doit "
        }

    def test_create_marche(self):
        """Test POST /api/marche/"""
        response = self.client.post(self.base_url, data=self.marche_data, format="json")
        self.created_marches.append(response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.marche_id = response.data["id"]

        self.assertEqual(response.data["objet"], self.marche_data["objet"])
        self.assertEqual(response.data["prix"], self.marche_data["prix"])
        self.assertEqual(response.data["acheteur"]["denomination_sociale"], "rubis")

    def test_retrieve_marche(self):
        """Test GET /api/marche/<id>/"""
        marche = Marche.objects.create(
            objet="1xxx yyyy zzzz ww",
            prix=99.0,
            acheteur=self.acheteur,
            procedure=self.procedure,
            groupement="test groupement",
            date_limite="2026-11-14",
        )
        marche.competences.set([self.competence1, self.competence2])
        marche.departements.set([self.departement1, self.departement2])

        url = f"{self.base_url}{marche.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], marche.id)
        self.assertEqual(response.data["objet"], "1xxx yyyy zzzz ww")

    def test_update_marche(self):
        """Test PUT /api/marche/<id>/"""
        marche = Marche.objects.create(
            objet="1xxx yyyy zzzz ww",
            prix=99.0,
            acheteur=self.acheteur,
            procedure=self.procedure,
            date_limite="2026-11-14",
        )
        marche.competences.set([self.competence1])
        marche.departements.set([self.departement1])

        updated_data = self.marche_data.copy()
        updated_data["objet"] = "2xxx yyyy zzzz ww"

        url = f"{self.base_url}{marche.id}/"
        response = self.client.put(url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["objet"], "2xxx yyyy zzzz ww")

    def test_filter_marche_by_objet(self):
        """Test GET /api/marche/?objet=xxxx"""
        Marche.objects.create(
            objet="appel d'offre spécial",
            prix=500,
            acheteur=self.acheteur,
            procedure=self.procedure,
            date_limite="2026-11-14",
        )
        response = self.client.get(f"{self.base_url}?objet=spécial")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["marches"]), 1)

    def test_pagination_marche(self):
        """Test GET /api/marche/?page=1&nb_per_page=2"""
        created_marches = []
        for i in range(5):
            self.marche_data['objet'] = f"test {i}"
            self.marche_data['prix'] = 100 + i
            response = self.client.post(self.base_url, data=self.marche_data, format="json")
            created_marches.append(response.data["id"])
        response = self.client.get(f"{self.base_url}?page=1&nb_per_page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pagination", response.data)
        self.assertLessEqual(len(response.data["marches"]), 2)
        #Delete all created marches 
        for marche_id in created_marches:
            delete_url = f"{self.base_url}{marche_id}/"
            self.client.delete(delete_url)


    def test_delete_marche(self):
        """Test DELETE /api/marche/<id>/"""

        # Create marches
        for i in range(5):
            data = self.marche_data.copy()
            data['objet'] = f"test {i}"
            data['prix'] = 100 + i
            response = self.client.post(self.base_url, data=data, format="json")
            self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

        # Get all marches
        list_response = self.client.get(self.base_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        marches = list_response.data["marches"]
        self.assertTrue(len(marches) > 0)

        # Delete each marche by ID
        for marche in marches:
            marche_id = marche["id"]
            delete_url = f"{self.base_url}{marche_id}/"
            delete_response = self.client.delete(delete_url)
            self.assertIn(delete_response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        # Verify all deleted
        final_response = self.client.get(self.base_url)
        self.assertEqual(final_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(final_response.data["marches"]), 0)