from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.
class PolicyExtractorService(View):

    def get(self, request):

        return HttpResponse("GET request from PolicyExtractorService")

    def post(self, request):

        return HttpResponse("POST request from PolicyExtractorService")
