from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

class DocTokenizerService(View):

    def get(self, request):

        return HttpResponse("GET method from DocTokenizerService")

    def post(self, request):

        return HttpResponse("POST method from DocTokneizerService")
