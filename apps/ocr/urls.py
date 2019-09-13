from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'',views.PolicyExtractorService.as_view()),
]
