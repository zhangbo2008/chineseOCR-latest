from django.conf.urls import url
from extractor import views

urlpatterns = [
    url(r'',views.PolicyExtractorService.as_view()),
]
