# -*- coding: utf-8 -*-


'''
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
'''


from agstream.session import AgspSession


session = AgspSession()
session.login(u'masnumeriqueAgStream', u'1AgStream', updateAgribaseInfo=True)

session.describe()

print u""
for abs in session.agribases :
    for sensor in abs.sensors :
        print u"%s %s" %  (abs.name,sensor.name)
        df=session.getSensorDataframe(sensor)
        if df is not None :
            print df.tail()
        
    
print u'Fin du programme'


'''
for abs in session.agribases :
    print abs.name
    for sensor in abs.sensors :
        print sensor.name
        df=session.getSensorDataframe(sensor)
        print df.head()
        xlsFileName = "%s.xlsx" % abs.name 
        print u"Ecriture des données %s " % xlsFileName
        df.to_excel(xlsFileName,engine='openpyxl')
'''


