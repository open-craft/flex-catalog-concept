"""
Database models for flex_catalog.
"""
import json
import uuid

from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel
from model_utils.managers import InheritanceManager

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


class FlexibleCatalogModel(TimeStampedModel):
    """
    A flexible model to test replacement options for the discovery service
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    name = models.CharField(max_length=255, help_text="Human friendly")

    objects = InheritanceManager()

    def save(self, *args, **kwargs):
        """
        Make the slugs easily
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_catalog_items(self):
        """
        The base catalog class returns every CourseOverview
        """
        return CourseOverview.objects.all()

    def search(self, search_term):
        """
        Basic implementation of keyword search
        """
        return self.get_catalog_items().filter(
            models.Q(display_name__icontains=search_term)
        )

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return '<FlexibleCatalogModel, ID: {}>'.format(self.id)


class FixedCatalog(FlexibleCatalogModel):
    course_runs = models.ManyToManyField('course_overviews.CourseOverview', blank=True)

    def get_catalog_items(self):
        """
        Returns the associated course_runs.
        """
        return self.course_runs.all()

    def __str__(self):
        return f"FixedCatalog: {self.id}"


class DynamicCatalog(FlexibleCatalogModel):
    query_string = models.TextField(
        help_text="Dynamic query string to filter course_runs.", blank=True, null=True
    )

    def get_catalog_items(self):
        """
        Filters course_runs dynamically based on the query_string.
        """
        if self.query_string:
            try:
                # Dynamically filter CourseOverview using the query string as json
                filter_params = json.loads(self.query_string)
                if not isinstance(filter_params, dict):
                    raise ValidationError("Query string must be a JSON object.")
                return CourseOverview.objects.filter(**filter_params)
            except Exception as e:
                raise ValueError(f"Invalid query_string: {e}")
        return CourseOverview.objects.none()

    def __str__(self):
        return f"DynamicCatalog: {self.id}"
