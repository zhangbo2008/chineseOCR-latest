from django.conf.urls import url
from tokenizer import views

urlpatterns = [
    url(r'', views.DocTokenizerService.as_view()),
]