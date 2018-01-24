# -*- coding: utf-8 -*-


'''
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
'''


from agstream.session import AgspSession


session = AgspSession()
session.login('masnumeriqueAgStream', '1AgStream', launchScanAgribase=True)

session.describe()

print ""

for abs in session.agribases :
    df = session.getAgribaseDataframe(abs)
    print df.tail()
    xlsFileName = "%s.xlsx" % abs.name 
    print u"Ecriture des données %s " % xlsFileName
    df.to_excel(xlsFileName,engine='openpyxl')
    
print u'Fin du programme'
'''
for abs in session.agribases :
    print abs.name
    for sensor in abs.sensors :
        print sensor.name
        df=session.getSensorDataframe(sensor)
        print df.head()
'''


