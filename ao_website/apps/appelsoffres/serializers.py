from datetime import datetime

from apps.appelsoffres.models import (
    Acheteur,
    CodeCPV,
    Competence,
    Departement,
    Marche,
    Piece,
    Procedure,
    Region,
    TypeMarche,
)
from rest_framework import serializers


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["code", "nom"]


class DepartementSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Departement
        fields = ["code", "nom", "region"]


class DepartementSimpleSerializer(DepartementSerializer):
    class Meta:
        model = Departement
        fields = ["code", "nom"]


class TypeMarcheSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMarche
        fields = ["libelle"]


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "libelle"]


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ["libelle"]


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ["libelle"]


class CodeCPVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeCPV
        fields = ["code", "nom"]


class CodeCPVBadgeSerializer(serializers.ModelSerializer):
    badge = serializers.SerializerMethodField()

    class Meta:
        model = CodeCPV
        fields = ["badge"]

    def get_badge(self, obj):
        return f"{obj.nom} - {obj.code}"


class AcheteurSerializer(serializers.ModelSerializer):
    url_site = serializers.SerializerMethodField()

    class Meta:
        model = Acheteur
        fields = [
            "id",
            "denomination_sociale",
            "url_site",
            "email",
            "telephone",
            "adresse",
        ]

    def get_url_site(self, obj):
        return obj.url_profil


class MarcheSerializer(serializers.ModelSerializer):
    departements = DepartementSerializer(many=True, read_only=True)
    acheteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Acheteur.objects.all(), write_only=True, source="acheteur"
    )
    procedure_id = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all(), write_only=True, source="procedure"
    )
    alert_date_limite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Marche
        fields = [
            "id",
            "objet",
            "prix",
            "departements",
            "acheteur_id",
            "procedure_id",
            "date_limite",
            "alert_date_limite",
        ]

    def get_alert_date_limite(self, obj):
        if obj.date_limite:
            deadline = obj.date_limite.replace(tzinfo=None)
            current_time = datetime.now().replace(tzinfo=None)
            time_difference = deadline - current_time
            hours_until_deadline = time_difference.total_seconds() / 3600
            if hours_until_deadline <= 24:
                return True
        return False


class MarcheDetaillerSerializer(MarcheSerializer):
    acheteur = AcheteurSerializer(read_only=True)
    procedure = ProcedureSerializer(read_only=True)
    procedure_id = serializers.PrimaryKeyRelatedField(
        queryset=Procedure.objects.all(), write_only=True, source="procedure"
    )
    acheteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Acheteur.objects.all(), write_only=True, source="acheteur"
    )
    departements = DepartementSerializer(many=True, read_only=True)
    departement_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Departement.objects.all(),
        source="departements",
        write_only=True,
    )

    competences = CompetenceSerializer(many=True, read_only=True)
    competence_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Competence.objects.all(),
        source="competences",
        write_only=True,
    )

    pieces = PieceSerializer(many=True, read_only=True)
    piece_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Piece.objects.all(), source="pieces", write_only=True
    )

    class Meta:
        model = Marche
        fields = [
            "id",
            "objet",
            "prix",
            "acheteur_id",
            "acheteur",
            "procedure",
            "procedure_id",
            "departements",
            "departement_ids",
            "competences",
            "competence_ids",
            "pieces",
            "piece_ids",
            "groupement",
            "date_limite",
        ]

    def create(self, validated_data):
        departements = validated_data.pop("departements", [])
        competences = validated_data.pop("competences", [])
        pieces = validated_data.pop("pieces", [])
        marche = Marche.objects.create(**validated_data)
        marche.departements.set(departements)
        marche.competences.set(competences)
        marche.pieces.set(pieces)
        return marche
