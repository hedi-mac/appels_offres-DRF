from django.db import models


class Region(models.Model):
    class Meta:
        db_table = "region"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, unique=True)


class Departement(models.Model):
    class Meta:
        db_table = "departement"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="departements",
        db_column="id_region",
        blank=True,
        null=True,
    )

    @classmethod
    def get_choices(cls):
        departements = cls.objects.values_list("code", "nom")
        return departements

    @classmethod
    def get_filtred_choices(cls, departement: str):
        filtred_departements = Departement.objects.filter(nom__istartswith=departement).values_list("code", "nom")
        choices = [(code, name) for code, name in filtred_departements]
        return choices

    @classmethod
    def get_exist_by_code(cls, code):
        if Departement.objects.filter(code=code).first():
            return True
        return False

    @classmethod
    def get_by_code(cls, code):
        return cls.objects.filter(code=code).first()


class Procedure(models.Model):
    class Meta:
        db_table = "procedure_marche"

    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_choices(cls):
        procedures = cls.objects.values_list("id", "libelle")
        return procedures


class TypeMarche(models.Model):
    class Meta:
        db_table = "type_marche"

    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_choices(cls):
        types = cls.objects.values_list("id", "libelle")
        return types


class Piece(models.Model):
    class Meta:
        db_table = "piece"

    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, unique=True)


class Competence(models.Model):
    class Meta:
        db_table = "competence"

    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_choices(cls):
        competences = cls.objects.values_list("id", "libelle")
        return competences


class CodeCPV(models.Model):
    class Meta:
        db_table = "code_cpv"

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_choices(cls):
        codes_cpv = cls.objects.values_list("code", "nom")
        return codes_cpv

    @classmethod
    def get_by_code(cls, code):
        return CodeCPV.objects.filter(code=code).first()


class Acheteur(models.Model):
    class Meta:
        db_table = "acheteur"

    id = models.AutoField(primary_key=True)
    denomination_sociale = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    telephone = models.CharField(max_length=255, null=True)
    adresse = models.CharField(max_length=255, null=True)
    url_profil = models.CharField(max_length=255, null=True)


class Marche(models.Model):
    class Meta:
        db_table = "marche"

    id = models.AutoField(primary_key=True)
    objet = models.CharField(max_length=512, unique=True)
    prix = models.FloatField(blank=True, null=True)
    groupement = models.TextField(blank=True, null=True)
    date_limite = models.DateTimeField(blank=True, null=True)
    code_cpv = models.ForeignKey(
        "CodeCPV",
        on_delete=models.CASCADE,
        related_name="code_cpv_marche",
        null=True,
        db_column="id_code_cpv",
    )
    acheteur = models.ForeignKey(
        "Acheteur",
        on_delete=models.CASCADE,
        related_name="acheteur_marche",
        null=True,
        db_column="id_acheteur",
    )
    procedure = models.ForeignKey(
        "Procedure",
        on_delete=models.CASCADE,
        related_name="marches",
        null=True,
        db_column="id_procedure",
    )
    departements = models.ManyToManyField("Departement", symmetrical=False, related_name="marches")
    pieces = models.ManyToManyField("Piece", symmetrical=False, related_name="marches")
    competences = models.ManyToManyField("Competence", symmetrical=False, related_name="marches")
    types = models.ManyToManyField("TypeMarche", symmetrical=False, related_name="marches")
