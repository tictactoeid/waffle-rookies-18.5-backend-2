from django.urls import include, path
from rest_framework.routers import SimpleRouter
from seminar.views import SeminarViewSet

app_name = 'seminar'

router = SimpleRouter()
router.register('seminar', SeminarViewSet, basename='seminar')  # /api/v1/seminar/

urlpatterns = [
    path('', include((router.urls))),
]
