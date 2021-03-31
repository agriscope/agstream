
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
session = AgspSession()
session.login(u"gailet", u"gailetventoux", updateAgribaseInfo=True)
session.describe()

to_p=datetime.datetime.now() 
from_p = to_p - timedelta(seconds=60*30)

for abs in session.agribases :
    print (u"****************************************")
    print (abs)
    df = session.getAgribaseDataframe(abs,from_p=from_p, to_p=to_p)
    print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print (df.head())
    xlsFileName = u"%s.xlsx" % abs.name 
    print(u"Ecriture des  données dans le fichier %s " % xlsFileName)
    #df.to_excel(xlsFileName, engine=u"openpyxl")
print(u"Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print(u"Fin du z programme: duree %00d ms" % deltams )



