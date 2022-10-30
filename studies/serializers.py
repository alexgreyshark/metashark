from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import (
    UserRoles,
)
from .models import (
    AcademicGroup,
    Report,
    Student,
    StudyDirection,
    Subject,
)


class AcademicGroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Учебной группы
    """

    class Meta:
        model = AcademicGroup
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Студент
    """

    class Meta:
        model = Student
        fields = '__all__'


class StudyDirectionSerializer(serializers.ModelSerializer):
    """Сериализатор модели Направление подготовки
    """

    def save(self, **kwargs):
        if self.validated_data.get('curator', 0):
            curator = self.validated_data['curator']
            if curator.role != UserRoles.curator:
                raise ValidationError(
                    detail={
                        'restriction': 'Может быть пользователь с ролью Куратор',
                    },
                )

    class Meta:
        model = StudyDirection
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор модели Учебная дисциплина
    """

    class Meta:
        model = Subject
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    """Сериализатор модели Отчет
    """

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['status'] = instance.get_status_display()
        return rep

    class Meta:
        model = Report
        fields = '__all__'
