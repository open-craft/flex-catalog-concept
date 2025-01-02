"""
Database models for custom_catalog.
"""

from django.db import models
from model_utils.models import TimeStampedModel
from flex_catalog.models import FlexibleCatalogModel, FixedCatalog

from django.conf import settings
from django.utils.html import format_html


class OdysseyCustomCatalog(FlexibleCatalogModel):
    """
    A catalog that does 1:1 matching (as the fixedcatalog does) but filters the available input courses
    """

    filtered_course_runs = models.ManyToManyField(
        "course_overviews.CourseOverview",
        blank=True,
        related_name="filtered_catalogs",
        limit_choices_to=settings.AVAILABLE_COURSES_FILTER,
    )

    def get_catalog_items(self):
        """
        Returns the associated course_runs.
        """
        return self.filtered_course_runs.all()

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return "<OdysseyCustomCatalog, ID: {}>".format(self.id)


class ExternalOrg(models.Model):
    """
    External organization that subscribes to specific catalogs of content.
    """
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"


class LearningSequence(models.Model):
    """
    A collection of courses. Think guided pathways.
    """
    name = models.CharField(max_length=120)
    courses = models.ManyToManyField(
        "course_overviews.CourseOverview",
        blank=True,
        related_name="linked_learning_sequences",
    )

    def __str__(self):
        return f"{self.name}"


class ExCatalogItem(models.Model):
    """
    Wrapper to provide a single entity type for the items in a catalog, around course and lerning paths.

    NOTE: Maybe this wrapper is not needed. But helps think this clearly. So, it's going to stay here for now.
    """

    class ExCatalogItemType(models.TextChoices):
        COURSE = "COURSE", "Course"
        LEARNING_SEQUENCE = "LSEQ", "Learning Sequence"

    name = models.CharField(max_length=120)
    item_type = models.CharField(
        max_length=8, choices=ExCatalogItemType.choices, default=ExCatalogItemType.COURSE
    )
    course_run = models.ForeignKey(
        "course_overviews.CourseOverview",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    learning_sequence = models.ForeignKey(
        LearningSequence, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.name}"


class ExternalOrgCatalog(FlexibleCatalogModel):
    """
    A catalog specific to an organization.
    """
    org = models.ForeignKey(ExternalOrg, on_delete=models.CASCADE)
    items = models.ManyToManyField(ExCatalogItem, blank=True, related_name="linked_catalogs")

    def get_catalog_items(self):
        return self.items.all()

    def __str__(self):
        return f"ExternalOrgCatalog for {self.org.name}"

    def course_keys(self, obj):
        return format_html("<br>".join(item.name for item in obj.items))
