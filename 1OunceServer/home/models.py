from django.db import models
from django.contrib.auth.models import User

class OunceUser(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gold22 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gold24 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    silver = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    passcode = models.IntegerField(default=-1)
    panid = models.CharField(max_length=20, blank=True)
    aadhaar = models.CharField(max_length=20, blank=True)
    companyType = models.IntegerField(default=0)

    def createNewUser(self,username,phone,password,email):
        try:
            user=User(username=phone,email=email,first_name=username)
            user.set_password(password)
            user.save()
            user=User.objects.get(username=phone)
        except:
            return None
        ounceUser=OunceUser(user=user)
        ounceUser.save()
        return ounceUser


class Address(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billingname = models.CharField(max_length=40, blank=True, null=True)
    addressline = models.CharField(max_length=400, blank=True, null=True)
    addressline2 = models.CharField(max_length=400, blank=True, null=True)
    homeno = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    isActive=models.BooleanField(default=True)

class Company(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    gstin = models.CharField(max_length=25, blank=True, null=True)
    pan = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    verificationstatus = models.BooleanField(default=False)  # Field name made lowercase.
    user=models.OneToOneField(User, on_delete=models.CASCADE)#can be changed to foregin key if required


class Delivery(models.Model):
    #DELIVERY STATUS 0->PROCESSING, 1->PROCESSED, 2->ON WAY, 3-> DELIVERED
    id = models.AutoField(primary_key=True)
    deliveryStatus = models.IntegerField(default=0)
    completeDate = models.DateTimeField()
    pid=models.CharField(max_length=15,default="")
    def onWay(self, username,orderId):
        try:
            user=User.objects.get(username=username)
            order=Order.objects.get(id=orderId)
            delivery=Delivery.objects.get(id=order.id)
            delivery.deliveryStatus=1
            delivery.save()
            return delivery
        except:
            return None

    def processed(self,username,orderId):
        try:
            user=User.objects.get(username=username)
            order=Order.objects.get(id=orderId)
            delivery=Delivery.objects.get(id=order.id)
            delivery.deliveryStatus=1
            delivery.save()
            return delivery
        except:
            return None

    def delivered(self,username,orderId):
        try:
            user = User.objects.get(username=username)
            order = Order.objects.get(id=orderId)
            delivery = Delivery.objects.get(id=order.id)
            delivery.deliveryStatus = 1
            delivery.save()
            return delivery
        except:
            return None




#CHANGES NEEDS TO BE MADE
class Order(models.Model):
    #MATERIAL 0->gold22 , 1->gold24, 2->silver
    #TYPE 'b'->buy , 's'->sell , 'd'->delivery , 'e'->exchange , 'a'->accept
    #transactionType 'upi'
    id=models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    material = models.CharField(max_length=15, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=0)
    delivery = models.ForeignKey(Delivery,on_delete=models.SET_NULL,null=True)
    isIgst=models.BooleanField(default=True)
    rate = models.FloatField(blank=True, null=True)
    invoice_number = models.CharField(max_length=30, blank=True, null=True)
    transaction_id=models.CharField(max_length=30,blank=True)
    transactionType=models.CharField(max_length=5,blank=True)
    #exchangedTo=models.ForeignKey(User , on_delete=models.CASCADE)
    def addInvoice(self,user,id,invoice):
        try:
            order=Order.objects.get(user=user,id=id)
            order.invoice_number=invoice
            return order
        except:
            return None





class Rate(models.Model):
    id=models.AutoField(primary_key=True)
    type=models.CharField(max_length=10)
    commission=models.FloatField()



class GiftCard(models.Model):
    id=models.AutoField(primary_key=True)
    giftcardname=models.CharField(max_length=50)
    giftcardvalue=models.CharField(max_length=50)

# #ounce admin model
# class OunceAdmin(models.Model):
#     id=models.AutoField(primary_key=True)
#     user=models.ForeignKey(User,on_delete=CASCADE)

class OunceInvoice(models.Model):
    id=models.AutoField(primary_key=True)
    product=models.CharField(max_length=50,null=True)
    pincode=models.CharField(max_length=10,null=True)
    company_name=models.CharField(max_length=20,null=True)
    address=models.TextField()
    hsncode=models.CharField(max_length=20,null=True)
    area=models.CharField(max_length=20,null=True)
    gst=models.CharField(max_length=20,null=True)
    cgst=models.CharField(max_length=20,null=True)
    sgst=models.CharField(max_length=20,null=True)
    igst=models.CharField(max_length=20,null=True)


