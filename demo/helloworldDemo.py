# -*- coding: utf-8 -*-


"""
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
"""
import datetime
from datetime import timedelta 
import time
from agstream.session import AgspSession
t0 = time.time()
session = AgspSession()
session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
session.describe()
print ("")
print ("**************************************************")
print ("* Example 1 :  simplest way to get data")
print ("* get the data, and feed an xlsfile")
print ("**************************************************")

for abs in session.agribases :
    print (u"****************************************")
    print (abs)
    df = session.getAgribaseDataframe(abs)
    print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print (df.head())
    xlsFileName = u"%s.xlsx" % abs.name 
    print(u"Ecriture des  données dans le fichier %s " % xlsFileName)
    df.to_excel(xlsFileName, engine=u"openpyxl")


print ("")
print ("**************************************************")
print ("* Example 2 :  get data with a from and to")
print ("**************************************************")


to_p=datetime.datetime.now() 
from_p = to_p - timedelta(seconds=60*30) # 30 minutes

for abs in session.agribases :
    print (u"****************************************")
    print (abs)
    df = session.getAgribaseDataframe(abs,index_by_sensor_id = False)
    print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print (df.head())




print ("")
print ("**************************************************")
print ("* Example 3 :  index the dataframe with sensor id")
print ("**************************************************")

for abs in session.agribases :
    print (u"****************************************")
    print (abs)
    df = session.getAgribaseDataframe(abs,index_by_sensor_id = True)
    print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print (df.head())


print(u"Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print(u"Fin du z programme: duree %00d ms" % deltams )


