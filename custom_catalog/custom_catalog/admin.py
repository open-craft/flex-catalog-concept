from django.contrib import admin

from flex_catalog.admin import FixedCatalogAdmin, CourseKeysMixin
from .models import OdysseyCustomCatalog, ExternalOrg, LearningSequence, ExCatalogItem, ExternalOrgCatalog


@admin.register(OdysseyCustomCatalog)
class FixedCatalogAdmin(admin.ModelAdmin, CourseKeysMixin):
    list_display = ('__str__', 'course_keys')
    search_fields = ('flexible_catalog__name', 'flexible_catalog__slug', 'flexible_catalog__id',)
    filter_horizontal = ('filtered_course_runs',)  # Makes managing ManyToMany fields easier in the admin


@admin.register(ExternalOrg)
class ExternalOrgAdmin(admin.ModelAdmin):
    pass


@admin.register(LearningSequence)
class LearningSequenceAdmin(admin.ModelAdmin):
    filter_horizontal = ('courses',)


@admin.register(ExCatalogItem)
class ExCatalogItem(admin.ModelAdmin):
    pass


@admin.register(ExternalOrgCatalog)
class ExternalOrgCatalogAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
