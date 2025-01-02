from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import FlexibleCatalogModel, FixedCatalog, DynamicCatalog

class CourseKeysMixin:
    def course_keys(self, obj):
        """
        Renders the IDs of the courses from get_course_runs.
        """
        course_runs = obj.get_catalog_items()
        if course_runs.exists():
            course_ids = [str(course.id) for course in course_runs]  # Collect IDs of each course
            return format_html('<br>'.join(course_ids))  # Render IDs as a list
        return "No course runs available"

    course_keys.short_description = "Course IDs"

@admin.register(FlexibleCatalogModel)
class FlexibleCatalogModelAdmin(admin.ModelAdmin, CourseKeysMixin):
    list_display = ('name', 'slug', 'id', 'model_class_name', 'course_keys')
    search_fields = ('name', 'slug', 'id')
    prepopulated_fields = {'slug': ('name',)}

    def model_class_name(self, obj):
        """
        Provide a link to the admin edit page for the specific subclass instance.
        """
        subclass_admin_url = reverse(
            f'admin:{obj._meta.app_label}_{obj.__class__.__name__.lower()}_change',
            args=[obj.id]
        )
        return format_html('<a href="{}">{}</a>', subclass_admin_url, obj.__class__.__name__)

    model_class_name.short_description = "Update Link"

    def get_queryset(self, request):
        """
        Override the queryset to use select_subclasses for subclass resolution.
        """
        return FlexibleCatalogModel.objects.select_subclasses()


@admin.register(FixedCatalog)
class FixedCatalogAdmin(admin.ModelAdmin, CourseKeysMixin):
    list_display = ('__str__', 'course_keys')
    search_fields = ('flexible_catalog__name', 'flexible_catalog__slug', 'flexible_catalog__id',)
    filter_horizontal = ('course_runs',)  # Makes managing ManyToMany fields easier in the admin


@admin.register(DynamicCatalog)
class DynamicCatalogAdmin(admin.ModelAdmin, CourseKeysMixin):
    list_display = ('__str__', 'query_string', 'course_keys')
    search_fields = ('flexible_catalog__name', 'flexible_catalog__slug', 'flexible_catalog__id', 'query_string')

    def course_keys(self, obj):
        """
        Return the ids for easy debug in the admin views
        """
        course_runs = obj.get_course_runs()
        if course_runs.exists():
            course_ids = [str(course.id) for course in course_runs]  # Collect IDs of each course
            return format_html('<br>'.join(course_ids))  # Render IDs as a list
        return "No course runs available"
