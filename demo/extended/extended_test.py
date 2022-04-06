'''
Created on 7 nov. 2019

@author: guill
'''
import pandas as pd
import time
from agstream.session import AgspSession
from agstream.session_extended import AgspExtendedSession


session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
session.login(u'masnumeriqueAgStream', u'masnumeriqueAgStream', updateAgribaseInfo=True)

session.describe()


print (u"Description du parc")
for abs in session.agribases :
    print ("")
    print (u"%s (%d) "  %(abs.name,abs.serialNumber))
    for sensor in abs.sensors :
        print ("    - %s" % sensor)
print ("")
for abs in session.agribases :
    print ("**************************")
    print( u"%s (%d) "  %(abs.name,abs.serialNumber))
    df = session.getAgribaseDataframe(abs)
    if df is not None :
        print (df.tail())
        