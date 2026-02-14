from rest_framework import serializers
from . import models



class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'



class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'



class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'



class MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = '__all__'


class EnrollmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = ['student', 'course']


class QuestionAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswer
        fields = '__all__'

