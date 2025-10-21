from apps.appelsoffres.filters import MarcheFilter, get_clean_filter_params
from apps.appelsoffres.models import Marche
from apps.appelsoffres.serializers import MarcheDetaillerSerializer, MarcheSerializer
from apps.appelsoffres.utils import MarchePagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class MarcheViewSet(ModelViewSet):
    """
    ViewSet for Marche with filtering, pagination, and persistent filters.
    """

    queryset = Marche.objects.all().order_by("-date_limite")
    serializer_class = MarcheSerializer
    filterset_class = MarcheFilter
    pagination_class = MarchePagination

    def get_queryset(self):
        """
        Return all Marche if no filters provided, else return filtered queryset.
        """
        if self.action != "list":
            return self.queryset

        filter_params = get_clean_filter_params(self.request)
        if not filter_params:
            return self.queryset

        filterset = self.filterset_class(filter_params, queryset=self.queryset)
        if filterset.is_valid():
            return filterset.qs.distinct()
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single Marche with detailed serializer.
        """
        self.pagination_class = None
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        Switch serializer for detailed view.
        """
        if self.action in ["retrieve", "create"]:
            return MarcheDetaillerSerializer
        return MarcheSerializer
