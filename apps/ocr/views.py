from django.shortcuts import render, HttpResponse
from django.views import View
import json
import os,sys
print(os.path.dirname(os.path.dirname( os.path.dirname(os.path.abspath( __file__ )) )))
sys.path.append(   os.path.dirname(os.path.abspath( __file__ ))            )
sys.path.append(   os.path.dirname(os.path.dirname( os.path.dirname(os.path.abspath( __file__ )) ))   )
import test
# Create your views here.
class PolicyExtractorService(View):
    '''
    扫描身份证:做的还差挺多.图片旋转没弄

    '''
    def get(self, request):

        return HttpResponse("GET request from PolicyExtractorService")

    def post(self, request):
        tmp=json.dumps(test.main(request.POST.get('url') ))
        return HttpResponse(tmp)
