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
from agstream.session_extended import AgspExtendedSession
t0 = time.time()
session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
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
    for sensor in abs.sensors:
        print(u"%s %s" % (abs.name, sensor.name))
        df = session.getSensorDataframe(sensor)
        if df is not None:
            print(df.tail())
    

print(u"Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print(u"Fin du z programme: duree %00d ms" % deltams )

