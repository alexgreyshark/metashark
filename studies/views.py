from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from users.permissions import (
    IsAdmin,
    IsCurator,
    IsSuperUser,
)
from .serializers import (
    AcademicGroupSerializer,
    ReportSerializer,
    StudentSerializer,
    StudyDirectionSerializer,
    SubjectSerializer,
)
from .models import (
    AcademicGroup,
    Report,
    Student,
    StudyDirection,
    Subject,
)
from .tasks import run_report


class AcademicGroupViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD для модели Учебная группа
    """
    queryset = AcademicGroup.objects.all()
    serializer_class = AcademicGroupSerializer
    permission_classes = [
        IsCurator | IsSuperUser,
    ]

    def get_permissions(self):
        if self.action in (
                'list',
                'retrieve',
        ):
            self.permission_classes = [
                AllowAny,
            ]
        return super().get_permissions()


class StudentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD для модели Студент
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [
        IsCurator | IsSuperUser,
    ]

    def get_permissions(self):
        if self.action in (
                'list',
                'retrieve',
        ):
            self.permission_classes = [
                AllowAny,
            ]
        return super().get_permissions()


class StudyDirectionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD Для модели Направление подготовки
    """
    queryset = StudyDirection.objects.all()
    serializer_class = StudyDirectionSerializer
    permission_classes = [
        IsAdmin | IsSuperUser,
    ]

    def get_permissions(self):
        if self.action in (
                'list',
                'retrieve',
        ):
            self.permission_classes = [
                AllowAny,
            ]
        return super().get_permissions()


class SubjectViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD для модели Учебная дисциплина
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [
        IsAdmin | IsSuperUser,
    ]

    def get_permissions(self):
        if self.action in (
                'list',
                'retrieve',
        ):
            self.permission_classes = [
                AllowAny,
            ]
        return super().get_permissions()


class ReportXlsxView(viewsets.ViewSet):
    """Отчет для администратора
    """
    permission_classes = [
        IsAdmin | IsSuperUser,
    ]

    @action(detail=False, methods=['GET'])
    def make(self, request):
        report = Report.objects.create()
        run_report.apply_async(
            kwargs={
                'report_id': report.id,
            },
        )
        return Response(
            data={
                "message": "Отчет генерируется "\
                           f"Результаты ожидайте на http://localhost:8003/report/{report.id}",
            },
        )


class ReportViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Read для модели Отчет
    """
    queryset = Report.objects.order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [
        IsAdmin | IsSuperUser,
    ]
