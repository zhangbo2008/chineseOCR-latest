from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.

class PolicyMatchService(View):
    '''
    企业找政策，政策文件匹配服务（/policyMatch/policyList）
    :return
    '''
    def get(self, request):
        #TODO
        return HttpResponse("GET request from PolicyMatchService")

    def post(self, request):
        #TODO
        return HttpResponse("POST request from PolicyMatchService")


class PolicySearchService(View):
    '''
    企业找政策，政策搜索服务（/policySearch/policyList）
    '''
    def get(self, request):
        return  HttpResponse("GET request from PolicySearchService")

    def post(self, request):
        return HttpResponse("POST request from PolicySearchService")


class CompanyMatchService(View):
    '''
    政策找企业，企业搜索服务 (/companyMatch/companyList)
    '''
    def get(self, request):
        return HttpResponse("GET request from CompanyMatchService")

    def post(self, request):
        return HttpResponse("POST request from CompanyMatchService")