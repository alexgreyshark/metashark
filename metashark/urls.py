from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
   include,
   path,
   re_path,
)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework import routers

from studies.views import (
   AcademicGroupViewSet,
   StudentViewSet,
   StudyDirectionViewSet,
   SubjectViewSet,
   ReportXlsxView,
   ReportViewSet,
)

router = routers.DefaultRouter()
"""Маршруты приложения studies"""
router.register('academic-group', AcademicGroupViewSet, basename='Academic Group')
router.register('student', StudentViewSet, basename='Student')
router.register('study-direction', StudyDirectionViewSet, basename='Study Direction')
router.register('subject', SubjectViewSet, basename='Subject')
router.register('report', ReportViewSet, basename='Report')
router.register('reports', ReportXlsxView, basename='Report Xlsx')

schema_view = get_schema_view(
   openapi.Info(
      title="Study WebService API",
      default_version='v1',
      description="Заглушка",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),

]

djoser_auth = [
   path('auth/', include('djoser.urls.authtoken')),
   path('auth/users/', UserViewSet.as_view(
      {
         'post': 'create',
      }
   )),
]

urlpatterns += router.urls
urlpatterns += djoser_auth
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)