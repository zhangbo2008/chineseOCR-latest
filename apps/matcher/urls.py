from django.conf.urls import url
from matcher import views

urlpatterns = [
    url(r'', views.PolicyMatchService.as_view()),
    url(r'', views.PolicySearchService.as_view()),
    url(r'', views.CompanyMatchService.as_view()),
]
