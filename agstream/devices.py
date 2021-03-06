# -*- coding: utf-8 -*-
"""
    Created on 23 mai 2014
    
    @author: renaud
    
    Agriscope Objects
    -----------------
    Python object of Agribase IOT devices.



"""
from __future__ import division

from builtins import str
from builtins import object
from past.utils import old_div
import datetime
from pytz import timezone
import pytz


"""
    Classe de l'agribase, contient sa liste de capteurs.
    Transforme la string JSON provenant du serveur Agriscope en objet direct.
"""


class Agribase(object):
    """
    Class implementing necessary information for an Agribase
 
    It hold stuff like name, serialNumber, GPS coordinates, lastActivity
    
    It contains sensors list.
    
    .. note::
 
        Objects are build from the json stream comming from the agriscope server
    
    """

    name = "?"
    """Agribase name"""
    lat = 0.0
    """GPS coordinate"""
    long = 0.0
    """GPS coordinate"""
    serialNumber = 0
    """Agriabse serial number"""
    agspInternalId = 0
    """Agribase key in thesAgriscope server database"""
    utctz = pytz.utc
    """timezone"""
    lastActivity = utctz.localize(datetime.datetime(1971, 1, 1, 0, 0, 0))
    """Last registered activity"""
    start = utctz.localize(datetime.datetime(1970, 1, 1, 0, 0, 0))
    """First registered activity"""

    intervalInSeconds = 60 * 15

    def __init__(self):
        self.start = datetime.datetime(1970, 1, 1, 0, 0, 0)

    def getSensors(self):
        """
        Return the list of sensors belonging to the Agribases
        """
        return self.sensors

    def loadFromJson(self, json):
        """
            Update Agribase informations from the json flow coming from Agriscope API
        """
        self.name = json["name"]
        self.lat = json["latitude"]
        self.long = json["longitude"]
        self.serialNumber = json["serialNumber"]
        self.agspInternalId = json["internalId"]

        self.lastActivity = self.utctz.localize(
            datetime.datetime.utcfromtimestamp(old_div(json["lastActivityDate"], 1000))
        )
        self.start = self.utctz.localize(
            datetime.datetime.utcfromtimestamp(old_div(json["startupDate"], 1000))
        )
        if u"samplingMinute" in json:
            self.intervalInSeconds = json[u"samplingMinute"]
        else:
            self.intervalInSeconds = -1
        if u"agriscopeType" in json:
            self.agriscopeType = json[u"agriscopeType"]
        else:
            self.agriscopeType = u"NaN"

        if u"linkType" in json:
            self.linkType = json[u"linkType"]
        else:
            self.linkType = u"Nan"

        self.sensors = list()

        for tmpJson in json[u"sensors"]:
            tmpSens = Sensor()
            tmpSens.loadFromJson(tmpJson)
            self.sensors.append(tmpSens)

    def __repr__(self):
        returnv = u"%s(%d) %s %s containing %d sensors" % (
            self.name,
            self.serialNumber,
            self.agriscopeType,
            self.linkType,
            len(self.sensors),
        )
        return returnv

    


"""
    Classe de capteur contenant ses informations.
"""


class Sensor(object):
    """
    Class implementing necessary information for an single sensor
 
    Contains information like name, sensorType, measuretype and internal agriscope
    key needed to get data by the Agriscope API
   
    
    """

    name = "?"
    """name of the sensor"""
    sensorType = "?"
    """Type of the sensors"""
    measureType = "?"
    """Measure type sampled by the sensor """
    agspSensorId = 0
    """ Agriscope internal key of this sensor"""
    modulePosition = 0
    """ Physical module position in the Agribase device"""
    sensorPosition = 0
    """Physical sensor position within the module """
    
    unit = "?"

    def __init__(self):
        self.name = "?"

    def loadFromJson(self, json):
        """
            Update Sensor informations from the json flow coming from Sensor API
        """
        self.name = json["name"]
        self.sensorType = json["sensorType"]
        self.measureType = json["measureType"]
        self.agspSensorId = json["internalId"]
        self.sensorPosition = json['channelPosition']
        self.modulePosition = json['modulePosition']

    def __repr__(self):
        return ( "%s(%d) %s, %s" % (self.name,self.agspSensorId,self.sensorType, self.measureType))
        