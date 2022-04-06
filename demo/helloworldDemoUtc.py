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
session = AgspSession(timezoneName='UTC')
session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
session.describe()
print ("")
print ("**************************************************")
print ("* Example 1 :  simplest way to get data en UTC")
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
    # suppression des timezone, car excel ne le supporte pas
    df=session.remove_any_timezone_info(df) 
    df.to_excel(xlsFileName, engine=u"openpyxl")


print(u"Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print(u"Fin du z programme: duree %00d ms" % deltams )


