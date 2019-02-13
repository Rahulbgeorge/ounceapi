from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import  User
from .models import  OunceUser,Address,Company,Order
from .views import debug,error
from django.shortcuts import HttpResponse
from .views import success,fail
from rest_framework import viewsets
import json


def fetchData(dataList,request):
    dataOut=[]
    for i in dataList:
        data=request.POST.get(i,None)
        print(i+":"+data)
        if(data is not None):
            dataOut.append(data)
        else:
            print("crashed")
            return None
    return dataOut

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def post(self, request):
        print(request)
        print(request.user)
        print(request.user.password)
        content = {'message': 'Hello, World!'}
        return Response(content)

class UserDetails(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def post(self,request):
        debug(request.user.username+" has requested data")
        user=User.objects.get(username=request.user)
        myUser=OunceUser.objects.get(user=user)
        content={'balance':myUser.balance,'gold22':myUser.gold22,'gold24':myUser.gold24,'silver':myUser.silver
                 ,'passcode':myUser.passcode,'name':request.user.first_name,'email':request.user.email
                 ,'companyStatus':myUser.companyType,'pan':myUser.panid,'phone':request.user.username}
        return Response(content)



class AddAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            data=['addressline1','addressline2','country','homeno','billingname','city','state','pincode']
            addressline1,addressline2,country,homeno,billingname,city,state,pincode=fetchData(data,request)
        except:
            return fail("unable to add address")
        # try:
        user=User.objects.get(username=request.user.username)
        address=Address(user=user,billingname=billingname,addressline=addressline1,
                        addressline2=addressline2,homeno=homeno,country=country,city=city,state=state,
                        pincode=pincode)
        address.save()

        return success("user data saved")


class DeleteAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        aid=request.POST['aid']
        try:
            address=Address(id=aid)
            address.isActive=False
            address.delete()
            return success("data deleted")
        except:
            return fail("unable to delete data")

class DisplayAllAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user=User.objects.get(username=request.user.username)
        address=Address.objects.filter(user=user,isActive=True)
        out=[]
        for i in address:
            data={}
            data['id']=i.id
            data['addressline1']=i.addressline
            data['addressline2']=i.addressline2
            data['billingname']=i.billingname
            data['homeno']=i.homeno
            data['country']=i.country
            data['city']=i.city
            data['state']=i.state
            data['pincode']=i.pincode
            out.append(data)
        return Response(out)

class DeleteAddress(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        id=request.POST.get("aid",None)
        user=User.objects.get(username=request.user.username)
        try:
            address=Address.objects.get(user=user,id=id)
            address.delete()
            return success("Address deleted successfully")
        except Exception as e:
            return fail(e)


class EditAddress(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            data=['aid','addressline1','addressline2','country','homeno','billingname','city','state','pincode']
            aid,addressline1,addressline2,country,homeno,billingname,city,state,pincode=fetchData(data,request)
            # try:
            user = User.objects.get(username=request.user.username)
            address = Address.objects.get(id=aid, user=user, isActive=False)
            address.addressline = addressline1
            address.addressline2 = addressline2
            address.billingname = billingname
            address.country = country
            address.homeno = homeno
            address.pincode = pincode
            address.city = city
            address.state = state
            address.save()
            return success("user data saved")
        except Exception as e:
            return fail(e)

class AddNewCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            data=['name','gstin','pan','address','pincode','email','phone']
            name,gstin,pan,address,pincode,email,phone=fetchData(data,request)
            user=User.objects.get(username=request.user.username)
            company=Company(user=user,name=name,gstin=gstin,pan=pan,address=address,
                            pincode=pincode,email=email,phone=phone)
            company.save()
            return success("successfully added company")
        except Exception as e:
            print("spme error occured")
            print(e)
            return fail(e)

class DisplayAllOrders(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            user=User.objects.get(username=request.user.username)
            orders=Order.objects.filter(user=user)
            out=[]
            for ord in orders:
                data={}
                data['type']=ord.type
                data['material']=ord.material
                data['qty']=ord.quantity
                data['date']=str(ord.date)
                data['cost']=str(ord.cost)
                data['rate']=str(ord.rate)
                data['transactionId']=ord.transaction_id
                data['invoice']=ord.invoice_number
                out.append(data)
            return success("Completed successfully")
        except Exception as e:
            return fail(e)


class DisplayMyCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        user=User.objects.get(username=request.user.username)
        try:
            company=Company.objects.get(user=user)
            out={}
            out['name']=company.name
            out['gstin']=company.gstin
            out['pan']=company.pan
            out['address']=company.address
            out['pincode']=company.pincode
            out['email']=company.email
            out['phone']=company.phone
            out['verificationStatus']=company.verificationstatus()
            return success(out)
        except Exception as e:
            return fail("Error occured")



class EditMyCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        inputData = ['name', 'gst', 'pan', 'phone', 'address', 'pincode', 'email']
        try:
            name, gst, pan, phone, address, pincode, email = fetchData(inputData, request)
            user=User.objects.get(username=request.user.username)
            company=Company.objects.get(user=user)
            company.name=name
            company.gstin=gst
            company.pan=pan
            company.address=address
            company.pincode=pincode
            company.email=email
            company.save()
            return success("Edit completed successfully")
        except:
            return fail("Unable to edit company")



@csrf_exempt
def rateApi(request):
    f=open("/home/rahul_bgeorge/vin2/rate.json","r")
    out=f.read()
    f.close()
    a=json.loads(out)
    return fail("something went wrong")
    #is this right
    return success(a)

































