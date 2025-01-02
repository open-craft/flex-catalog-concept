from openedx.core.djangoapps.content.course_overviews.serializers import CourseOverviewBaseSerializer
from rest_framework import serializers

from .models import FlexibleCatalogModel, CourseOverview


class CourseOverviewSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOverview
        fields = ['id']


class FlexibleCatalogModelSerializer(serializers.ModelSerializer):
    course_runs = serializers.SerializerMethodField()

    class Meta:
        model = FlexibleCatalogModel
        fields = ['id', 'name', 'slug', 'course_runs']

    def get_course_runs(self, obj):
        """
        Fetches the related course runs using the `get_course_runs` method.
        """
        course_runs = obj.get_catalog_items()
        return CourseOverviewBaseSerializer(course_runs, many=True).data
