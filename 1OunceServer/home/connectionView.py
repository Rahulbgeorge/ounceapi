from django.views.decorators.csrf import csrf_exempt

from .views import login,registration,success,fail

@csrf_exempt
def formsGet(request):
    if(request.method=="POST"):
        requestType=request.POST.get('requestType',None)
        if(requestType!=None):
            makeRequest={}
            makeRequest['1']=login
            makeRequest['2']=registration
            try:
                return makeRequest[requestType](request)
            except:
                return fail("INVALID REQUEST TYPE")



