import importlib
from django.conf import settings
from django.shortcuts import get_object_or_404
from openedx.core.djangoapps.content.course_overviews.serializers import CourseOverviewBaseSerializer
from rest_framework import generics, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import FlexibleCatalogModel
from .serializers import FlexibleCatalogModelSerializer


class FlexibleCatalogModelViewSet(ModelViewSet):
    queryset = FlexibleCatalogModel.objects.select_related().select_subclasses()

    def get_serializer_class(self):
        """
        Get the serializer class that can serialize the catalog's items.
        """
        serializer_class = FlexibleCatalogModelSerializer
        if settings.FLEX_CATALOG_SERIALIZER:
            try:
                module_name, class_name = settings.FLEX_CATALOG_SERIALIZER.rsplit(".", 1)
                module = importlib.import_module(module_name)
                serializer_class = getattr(module, class_name)
            except:
                print("Failed to load serializer from %s", settings.FLEX_CATALOG_SERIALIZER)

        return serializer_class

    def get_object(self):
        """
        Ensures the retrieved object is the specific subclass.
        Note: Not entirely sure this is needed after select_subclasses
        """
        obj = super().get_object()
        # Cast to the correct subclass if not already resolved
        if hasattr(obj, 'cast'):
            return obj.cast()
        return obj

    @action(detail=True, methods=['get'], url_path='course-runs')
    def get_course_runs(self, request, slug=None):
        """
        Forward the REST view to the get_course_runs in the object.
        """
        catalog = get_object_or_404(FlexibleCatalogModel.objects.select_subclasses(), slug=slug)
        course_runs = catalog.get_catalog_items()  # Call the model method
        serializer = CourseOverviewBaseSerializer(course_runs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='search')
    def get_search(self, request, slug=None):
        """
        Perform a search for a specific catalog.

        Use at /flex-catalog/catalogs/<SLUG>/search/?q=demo
        """
        catalog = get_object_or_404(FlexibleCatalogModel.objects.select_subclasses(), slug=slug)
        search_term = request.query_params.get('q', '')
        if not search_term:
            return Response(
                {"detail": "Must pass a search query 'q'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        search_results = catalog.search(search_term=search_term)
        serializer = CourseOverviewBaseSerializer(search_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
