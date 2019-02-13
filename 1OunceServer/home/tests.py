from django.test import TestCase
from django.contrib.auth.models import User
from .models import OunceUser
# Create your tests here.

def fillDummyData():
    user=User(username='9008522228',email="rahul.bgeorge@gmail.com")
    user.set_password("password")
    ounceUser=OunceUser(user=user)
    ounceUser.save()

    OunceUser.createNewUser("vinnarasu",'9159414383','password','vin@gmail.com')


