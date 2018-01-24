# -*- coding: utf-8 -*-
'''
Created on 23 mai 2014

@author: renaud


Contains Agriscope devices objects
(Agribase and sensors)

'''

import datetime
from pytz import timezone
import pytz 




'''
    Classe de l'agribase, contient sa liste de capteurs.
    Transforme la string JSON provenant du serveur Agriscope en objet direct.
'''
class Agribase :
    name="?"
    lat = 0.0
    long = 0.0
    serialNumber=0
    agspInternalId=0
    utctz = pytz.utc
    lastActivity= utctz.localize(datetime.datetime(1971, 1, 1,0,0,0))
    start = utctz.localize(datetime.datetime(1970, 1, 1,0,0,0))
    intervalInSeconds = 60*15
    
    def __init__ (self):
        self.start=datetime.datetime(1970, 1, 1,0,0,0)
    
    def loadFromJson (self,json):
        self.name= json['name']
        self.lat= json['latitude']
        self.long = json['longitude']
        self.serialNumber = json['serialNumber']
        self.agspInternalId =json ['internalId']
        self.lastActivity=self.utctz.localize(datetime.datetime.utcfromtimestamp(json ['lastActivityDate']/1000))
        self.start= self.utctz.localize(datetime.datetime.utcfromtimestamp(json ['startupDate']/1000))
        self.sensors=list()

        for tmpJson in json ['sensors'] :
            tmpSens = Sensor()
            tmpSens.loadFromJson(tmpJson)
            self.sensors.append(tmpSens)
        
    
    def __str__(self):
        return unicode(self).encode('utf-8')

        
    def __unicode__(self): 
        return (self.name+'('+unicode(self.serialNumber)+')'+ " containing " + unicode(len(self.sensors)) + " sensors")
'''
    Classe de capteur contenant ses informations.
'''   
class Sensor :
    name="?";
    sensorType="?"
    measureType="?"
    agspSensorId=0;
    modulePosition=0
    sensorPosition=0
    def __init__ (self):
        self.name="?"
        
    def loadFromJson (self,json):
        self.name= json['name']
        self.sensorType=json['sensorType']
        self.measureType=json['measureType']
        self.agspSensorId = json['internalId']
 
    def __str__(self):
        return unicode(self).encode('utf-8')
        
    def __unicode__(self): 
        return (self.name+'('+unicode(self.agspSensorId)+')'+ " " +self.sensorType + ", " + self.measureType)
