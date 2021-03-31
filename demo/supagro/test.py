'''
Created on 7 nov. 2019

@author: guill
'''
import pandas as pd
import time
from agstream.session import AgspSession



session = AgspSession()
session.login(u'masnumerique', u'masnumerique', updateAgribaseInfo=True)
session.describe()


print (u"Description du parc")
for abs in session.agribases :
    print ("")
    print (u"%s (%d) "  %(abs.name,abs.serialNumber))
    for sensor in abs.sensors :
        print ("    -%s" %sensor.name)
print ("")
for abs in session.agribases :
    print ("**************************")
    print( u"%s (%d) "  %(abs.name,abs.serialNumber))
    df = session.getAgribaseDataframe(abs)
    if df is not None :
        print df.tail()
        