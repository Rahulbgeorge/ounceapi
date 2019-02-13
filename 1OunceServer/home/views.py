from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import  OunceUser


# from .models import User
import json
import logging
logger = logging.getLogger(__name__)
import requests
import random


# # Create your views here.
# def homescreen(request):
#     return HttpResponse("This is your home page")
#
# @csrf_exempt
# def login(request):
#
#     phone,password=str(request.POST.get("phone",None)),request.POST.get("password",None)
#     if(phone==None or password==None):
#         return fail("invalid")
#     else:
#         try:
#             print(phone)
#             user=User.objects.get(phone=phone,password=password)
#             out={}
#             out['phone'],out['email'],out['balance'],out['g22'],out['g24'],out['silver'],out['passcode'],out['id']=user.phone,user.email,user.balance,user.gold22,user.gold24,user.silver,user.passcode,user.panid
#             out['companyStatus'],out['pan']=user.companyType,user.panid
#             debug(user.phone+" successfully logged in!")
#             return success(out)
#         except:
#             fail("Invalid Login using "+phone+","+password)
#             return fail("Invalid user")
#
#
# @csrf_exempt
# def registration(request):
#     phone,password,email=request.POST.get("phone",None),request.POST.get("password",None),request.POST.get("email",None)
#     if(phone==None or password==None or email==None):
#         return fail("invalid data")
#     else:
#         try:
#             user=User(phone=phone,password=password,email=email)
#             user.save()
#             debug("user "+phone+" saved successfully")
#             return success("user saved successfully")
#         except:
#             error("Error while saving user")
#
#
# @csrf_exempt
# def forgotPassword(request):
#     phone,password=request.POST.get("phone",None),request.POST.get("password",None)
#     if(phone==None or password==None):
#         return fail("Invalid")
#     else:
#         try:
#             user=User.objects.get(phone=phone)
#             user.password=password
#             user.save()
#             debug(phone+" changed password ")
#             return success("Successful changed password")
#         except:
#             error(phone+" was unable to change password")
#             return fail("Unable to change password")
#

@csrf_exempt
def login1(request):
    phone,password=request.POST.get("phone",None),request.POST.get("password",None)
    print(phone)
    print(password)
    if (phone == None or password == None):
        return fail("Invalid")
    else:
        try:
            user=authenticate(username=phone,password=password)
            if(user is not None):
                return success("user validated"+user.email)
            else:
                return success("user not validated")
            debug(phone + " changed password ")
            return success("Successful changed password")
        except:
            error(phone + " was unable to change password")
            return fail("Unable to change password")

@csrf_exempt
def registration(request):
    phone,password,email,username=request.POST.get("phone",None),request.POST.get("password",None),request.POST.get("email",None),request.POST.get("username",None)

    if (phone == None or password == None or email== None or username==None):
        return fail("Invalid")
    else:
        #valid user
        print(phone)
        #WE STORE THE FULL USER NAME AS FIRST NAME
        user=OunceUser().createNewUser(username,phone,password,email)
        if(user is None):
            return fail("unable to signup")

        return success("user signup completed")


@csrf_exempt
def sendUserVerficationOtp(request):
    otpurl="http://api.msg91.com/api/sendhttp.php"
    if(request.method=="POST"):
        otp=random.randint(1000,9999)
        mobile=request.POST.get("mobile",None)
        if(mobile!=None):
            params={'message':"Your 1Ounce otp is "+str(otp),'authkey':'243807AWIErnmLDQ5bcc7ac9','mobiles':mobile,'sender':'MSGIND'
                    ,'country':'91','route':4}
            result=requests.get(url = otpurl, params = params)
            print(str(result.content))
            print(otp)
            return success(str(otp))
        return fail("Invalid credentials")
    return fail("invalid page")

















def nothing():
    return HttpResponse("nothing")


def success(message):
    output = {}
    output["result"] = "success"
    output["description"] = message
    return HttpResponse(json.dumps(output))

def fail(message):
    output={}
    output["result"] = "fail"
    output["description"] = message
    return HttpResponse(json.dumps(output))


def debug(message):
    logger.debug("DEBUG | Message:" +message)

def error(message):
    logger.debug("ERROR | Message:"+message)

