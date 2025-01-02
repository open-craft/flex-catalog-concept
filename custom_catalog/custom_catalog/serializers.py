from rest_framework import serializers

from .models import ExCatalogItem, ExternalOrgCatalog


class ExCatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExCatalogItem
        fields = ["id", "name"]


class ExternalOrgCatalogSerializer(serializers.ModelSerializer):
    """
    This will be used to set the serializer class in LMS Settings.

    This is currently set in settings.py

    FLEX_CATALOG_SERIALIZER = "custom_catalog.serializers.ExternalCatalogSerializer"
    """
    items = ExCatalogItemSerializer(many=True, required=False)
    class Meta:
        model = ExternalOrgCatalog
        fields = ["id", "name", "slug", "items"]
