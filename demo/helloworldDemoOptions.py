
"""
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
"""

from datetime import timedelta 
import time
from agstream.session import AgspSession
import datetime
t0 = time.time()
session = AgspSession(server="jsonapi.agriscope.fr")
session.login(u"sam", u"marsi34", updateAgribaseInfo=True)
#session.login(u"paul", u"mourot", updateAgribaseInfo=True)

session.describe()

to_p=datetime.datetime.now() 
from_p = to_p - timedelta(seconds=60*30)
print (u"****************************************")
print (u"START DATE POUR AGRIBASES SAM")
print (u"****************************************")
   
for abs in  sorted(session.agribases, key=lambda x: x.start, reverse=True) :
    print (" - %s [%d] %s %s" % (abs.start, abs.serialNumber,abs.agriscopeType, abs.name) )
    #df.to_excel(xlsFileName, engine=u"openpyxl")
print(u"Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print(u"Fin du z programme: duree %00d ms" % deltams )



