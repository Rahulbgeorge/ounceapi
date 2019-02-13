from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import  User
from .models import  OunceUser,Address,Company,Order
from .views import debug,error
from django.shortcuts import HttpResponse
from rest_framework import viewsets
from .mainView import fetchData
from .views import success,fail

class BuyCommodity(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    def post(self,request):
        # aid,cost,materialType,qty,rate=request.POST.get("aid",None),request.POST.get("cost",None)\
        #     ,request.POST.get("materialType",None),request.POST.gete("qty",None),request.POST.get("")
        # fetchData(['cid','cost','name','email','isIgst'],request)

        try:
            aid, cost, materialType, qty, rate, isIgst=fetchData(['aid','cost','materialType','qty','rate','isIgst'],request)
            address=Address.objects.get(id=aid)
            user=User.objects.get(username=request.user.username)
            myuser=OunceUser.objects.get(user=user)
            order=Order(material=materialType,quantity=qty,cost=cost,address=address,
                        rate=rate,isIgst=isIgst,user=user)
            order.type='b'
            if(materialType==0):
                myuser.gold22=float(myuser.gold22)+float(qty)
            elif(materialType==1):
                myuser.gold24=float(myuser.gold24)+float(qty)
            else:
                myuser.silver=float(myuser.silver)+float(qty)

            myuser.save()
            order.save()
            return success("Buy Completed")
        except Exception as e:
            return fail(e)


class SellCommodity(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            data=['aid','qty','cost','materialType','rate','isIgst']
            aid,qty,cost,materialType,rate,isIgst=fetchData(data,request)
            address = Address.objects.get(id=aid)
            user = User.objects.get(username=request.user.username)
            myuser = OunceUser.objects.get(user=user)


            order = Order(material=materialType, quantity=qty, cost=cost, address=address,
                          rate=rate, isIgst=isIgst, user=user)
            order.type='s'
            if (materialType == 0):
                if myuser.gold22>=qty:
                    myuser.gold22 = float(myuser.gold22) - float(qty)
                else:
                    return fail("Insufficient balance")
            elif (materialType == 1):
                if(myuser.gold24>=qty):
                    myuser.gold24 = float(myuser.gold24) - float(qty)
                else:
                    return fail("Insufficient Balance")
            else:
                if(myuser.silver>=qty):
                    myuser.silver = float(myuser.silver) - float(qty)
                else:
                    return fail("Insufficient balance")

            myuser.save()
            order.save()
        except Exception as e:
            return fail(e)


        return success("Sale completed")

class ExchangeCommodity(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            data=['rid','qty','materialType','idType']
            reciever_id,qty,materialType,idType=fetchData(data,request)
            myuser=OunceUser.objects.get(User.objects.get(username=request.user.username))
            if(idType=='pan'):
                ruser=OunceUser.objects.get(panid=reciever_id)

            if(materialType==0):
                if(myuser.gold22>=qty):
                    myuser.gold22=myuser.gold22-qty
                    ruser.gold22=ruser.gold22+qty
                else:
                    return fail("Insufficent balance")
            elif(materialType==1):
                if(myuser.gold24>=qty):
                    myuser.gold24=myuser.gold24-qty
                    ruser.gold24=ruser.gold24+qty
                else:
                    return fail("insufficeient balance")
            else:
                if(myuser.silver>=qty):
                    myuser.silver=myuser.silver-qty
                    ruser.silver=ruser.silver+qty
                else:
                    return fail("Insufficent balance")

            myuser.save()
            ruser.save()
            return success("Exchange complete")
        except Exception as e:
            return fail(e)












