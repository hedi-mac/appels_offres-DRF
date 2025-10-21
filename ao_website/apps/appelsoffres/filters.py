import django_filters
from apps.appelsoffres.models import Competence, Departement, Marche
from django.db.models import Q
from django.http import HttpRequest


def get_clean_filter_params(request: HttpRequest) -> dict:
    """
    Extract only non-empty GET parameters from an HTTP request.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        dict: A dictionary containing only non-empty query parameters.
    """
    filter_params = request.GET.copy()
    for key in list(filter_params.keys()):
        if not filter_params.get(key):
            del filter_params[key]
    return filter_params


class MarcheFilter(django_filters.FilterSet):
    """
    Advanced filter for Marche supporting all main fields.
    """

    objet = django_filters.CharFilter(
        field_name="objet",
        lookup_expr="icontains",
        label="Objet (mot-clé)",
    )
    prix = django_filters.RangeFilter(
        field_name="prix",
        label="Plage de prix",
    )
    date_limite = django_filters.DateFromToRangeFilter(
        field_name="date_limite",
        label="Date limite (plage)",
    )
    competences = django_filters.ModelMultipleChoiceFilter(
        queryset=Competence.objects.all(),
        field_name="competences",
        to_field_name="id",
        label="Compétences",
    )
    departements = django_filters.ModelMultipleChoiceFilter(
        queryset=Departement.objects.all(),
        field_name="departements",
        to_field_name="id",
        label="Départements",
    )

    search = django_filters.CharFilter(
        method="filter_search",
        label="Recherche globale",
    )

    def filter_search(self, queryset, name, value):
        """
        Allow global search by objet, description, or other textual fields.
        """
        return queryset.filter(Q(objet__icontains=value) | Q(description__icontains=value))

    class Meta:
        model = Marche
        fields = {
            "objet": ["icontains"],
            "prix": ["gte", "lte"],
            "competences": ["exact"],
            "departements": ["exact"],
            "date_limite": ["exact"],
        }
