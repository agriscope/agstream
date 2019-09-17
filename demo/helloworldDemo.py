# -*- coding: utf-8 -*-


"""
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
"""
from __future__ import print_function



from agstream.session import AgspSession
session = AgspSession()
session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
session.describe()
for abs in session.agribases :
    print (u"****************************************")
    print (abs)
    df = session.getAgribaseDataframe(abs)
    print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print (df.head())
    xlsFileName = u"%s.xlsx" % abs.name 
    print (u"Ecriture des données dans le fichier %s " % xlsFileName)
    df.to_excel(xlsFileName,engine=u'openpyxl')
print(u"Fin du programme")


"""
for abs in session.agribases :
    print abs.name
    for sensor in abs.sensors :
        print sensor.name
        df=session.getSensorDataframe(sensor)
        print df.head()
        xlsFileName = "%s.xlsx" % abs.name 
        print u"Ecriture des données %s " % xlsFileName
        df.to_excel(xlsFileName,engine='openpyxl')
"""
