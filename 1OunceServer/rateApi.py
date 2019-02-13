
import requests
import json
import mysql.connector
import time
# import mysql.connector import Error
#FETECHES RATE FROM EXTERNAL API
def fetchVal():
	data=requests.get('https://gold-feed.com/paid/APIec258954d41428c98139e22f7185753b8c77c21fc8956c554f/all_metals_json_inr.php')
	finaldata=data.text
	jsondata=json.loads(finaldata)
	basicGold=float(jsondata['gold_ask_inr_toz'])
	basicSilver=float(jsondata['silver_ask_inr_toz'])

	firstGoldVal=float(basicGold/31.1034)
	firstGoldVal=firstGoldVal+(firstGoldVal * 0.10)
	gold=firstGoldVal+(firstGoldVal * 0.03)

	firstSilverVal=float(basicSilver/31.1034)
	firstSilverVal=firstSilverVal+(firstSilverVal * 0.10)
	silver=firstSilverVal+(firstSilverVal * 0.03)

	gold=float(gold)
	gold=round(gold,2)

	silver=float(silver)
	silver=round(silver,2)

	gold22=float(gold*0.95)
	gold22=round(gold22,2)

	rateval={}
	rateval['gold24']=gold
	rateval['gold22']=gold22
	rateval['silver']=silver
	rateval=json.dumps(rateval)
	print(rateval)
	return rateval


def fetchfinalRate():
    val = fetchVal()

    val = json.loads(val)

    print(val)
    gold24 = float(val['gold24'])
    gold22 = float(val['gold22'])
    silver = float(val['silver'])
    # rate = Rate.objects.all()
    # b24,b22,bs,s24,s22,ss=0.0,0.0,0.0,0.0,0.0,0.0

    # b24=(float(gold24)+float(rate[0].type))+(float(gold24)+float(rate[0].type))*0.03;
    golddict = {}

    try:
        mydb = mysql.connector.connect(host='35.247.134.44', database='django_ounce', user='root',
                                       password='mystrongpassword')
        s = "select * from home_rate"
        cursor = mydb.cursor()
        cursor.execute(s)
        records = cursor.fetchall()
        for data in records:
            golddict[data[1]] = data[2]

    except:
        print("Error occured | exception")
        return "Error found"



    b24 = (float(golddict['b24']))
    b22 = (float(golddict['b22']))
    bs = (float(golddict['bs']))
    s24 = (float(golddict['s24']))
    s22 = (float(golddict['s22']))
    ss = (float(golddict['ss']))

    bgold24 = (gold24 + (b24)) + (gold24 + (b24)) * 0.03

    bgold22 = (gold22 + (b22)) + (gold22 + (b22)) * 0.03

    bsilver = (silver + (bs)) + (silver + (bs)) * 0.03

    sgold24 = gold24 + (s24)
    sgold22 = gold22 + (s22)
    ssilver = silver + (ss)

    finaloutput = {}
    finaloutput['buy24k'] = bgold24
    finaloutput['buy22k'] = bgold22
    finaloutput['buysilver'] = bsilver
    finaloutput['sell24k'] = sgold24
    finaloutput['sell22k'] = sgold22
    finaloutput['sellsilver'] = ssilver
    print(finaloutput)
    return finaloutput


# def dbFetch():
#     try:
#         mydb = mysql.connector.connect(host='35.247.134.44', database='django_ounce', user='root',password='mystrongpassword')
#         s = "select * from home_rate"
#         cursor = mydb.cursor()
#         cursor.execute(s)
#         records = cursor.fetchall()
#         for data in records:
#             golddict[data[1]]=data[2]
#
#     except:
#         print("Error occured | exception")



while(True):
    rate=fetchfinalRate()
    outputfile=open("/home/rahul_bgeorge/vin2/rate.json","w")
    outputfile.write(json.dumps(rate))
    outputfile.close()
    time.sleep(20*1000)
