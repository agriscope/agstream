# -*- coding: utf-8 -*-
'''
Created on 23 mai 2014

@author: renaud
'''
from agstream.devices import Agribase,Sensor
from agstream.connector import AgspConnecteur
import time
import pandas as pd
import pytz
import datetime
from datetime import timedelta
import numpy as np
from pytz import timezone


'''
  Object principal de connection avec les service Agriscoep.
  Permet de se logguer, recuperer les agribases, scanner et trouver les datasources.
'''
    
class AgspSession :
    debug = False
    agribases = list()
    def __init__ (self,server = 'jsonapi.agriscope.fr', timezoneName=u'Europe/Paris'):
        self.agribases = list()
        self.connector = AgspConnecteur(server = server )
        self.set_debug(False)
        self.sessionId = 0
        self.station = False
        self.timezoneName = timezoneName
        self.tz = timezone(self.timezoneName)

    def set_debug(self, value):
        self.debug = value
        self.connector.set_debug(value)
    '''
    login()
    Se loggue au service Agriscope
    Si Ok, lance la mise a jours de la liste d'agribase
    L'objectif est d'avoir la liste des agribase a jour, en particulier pour la
    date de la derniere activitée
    '''
    def login (self, login, password, launchScanAgribase = False):
        status , sessionId = self.connector.login(login,password)
        if status == True :
            # reinitialise 
            self.agribases = list()
            print login + u" connecté."
            if launchScanAgribase == True :
                self.__refreshAgribases()
        if self.debug == True :
            if status == True:
                print login + u" connecté."
                
            else :
                print u"Erreur de connection pour " + login + "."
        self.status=status
        self.sessionId = sessionId
        return status
   
   
    '''
     Retourne l'agribase par numero de serie ou string matching
     Les agribases sont considerees chargées dans le menbre self.agribases.
     Cette fonction ne va pas cherche les agribases sur le serveur
    '''
    def getAgribase(self,searchPattern):
        
        for abse in self.agribases :
            if isinstance(searchPattern, int):
                if abse.serialNumber == searchPattern :
                    return abse
            if isinstance(searchPattern, basestring):
                if searchPattern in abse.name :
                    return abse
        return None

    ''' 
    Retourne un dataframe pour l'agribase pour la periode demandée 
    '''
    def getAgribaseDataframe (self,agribase,from_p=None,to_p=None):
        
        frame = pd.DataFrame()
        frame.tz_convert(self.tz)
        
        for sens in agribase.sensors:
            df = self.getSensorDataframe(sens, from_p, to_p)
            if df is not None and len(df) > 0 :
                frame = pd.concat([frame,df],axis=1)
        return frame
    
    ''' 
    Retourne un dataframe pour le capteur pour la periode demandée 
    '''
    def getSensorDataframe (self,sensor,from_p=None,to_p=None):
        return self.__getSensorDataframe(sensor.agspSensorId, sensor.name, from_p, to_p)
    
    
    
    '''
    Describe 
    '''    
    def describe(self):
        print "login " +  self.connector.lastLogin
        print "    - " + str (len (self.agribases)) + " agribases."
        print "    - Timezone = %s " % self.timezoneName
        count = 0
        for abse in self.agribases :
    
            print "    - " + unicode(abse.name) + ""

  

    '''
    Refresh information
    '''
    def __refreshAgribases(self):
        json = self.connector.getAgribases()
        self.agribases = list()
        for tmpjson in json['agribases'] :
            abse = Agribase()
            abse.loadFromJson(tmpjson)
            abse.intervalInSeconds = self.getAgribaseIntervaleInSeconds(abse.serialNumber)
            self.agribases.append(abse)
        return self.agribases
    

    
    
    
    def __getSensorDataframe (self,sensorid,label,from_p=None,to_p=None):
        if (to_p == None) :
            to_p=self.tz.localize(datetime.datetime.now())
        if (from_p == None) :
            from_p = to_p -timedelta(days=3)
        date, values = self.__loadSensorDataFlat(sensorid, from_p, to_p)
        dataFrame = self.__convertDataToPandasFrame(date,values, label)
        return dataFrame
    '''
     Retourne mes informations generique sur les agribase
    '''
    def getAgribaseIntervaleInSeconds(self,serialNumber):
        #print "getAgribaseIntervaleInSeconds(%d)" % serialNumber
        url = "http://jsonmaint.agriscope.fr/tools/CHECK/agbs.php?sn=%d" % serialNumber
        json=self.connector.executeJsonRequest(url)
        returnv = -1
        if "intervalInSec" in json :
            tmp = json["intervalInSec"]
            if tmp == 'N/A' :
                return 15
            returnv = int(tmp)
        return returnv
    
    
    def getAgribaseTypeName(self,serialNumber):
        url = "http://jsonmaint.agriscope.fr/tools/CHECK/agbs.php?sn=%d" % serialNumber
        json=self.connector.executeJsonRequest(url)
        returnv = -1
        if "agbsType" in json :
            returnv = json["agbsType"]
        return returnv




    def __getDataframe(self, datesArray_p, valuesArray_p,limitFrom,limitTo):
            # en python les tableaux sont des list. 
            newFrame = self.convertDataToPandasFrame(datesArray_p, valuesArray_p, self.datasource.getSmallName())
            newFrame.sort_index(inplace=True)
            if len(newFrame) > 0 :
                # On borne la plage....
                # Bug du serveur ariscope... En effet parfois il renvoie des dates hors de l'intervalle demandée (par exemple 1992)
                # On limit l'effet, en 'coupant' les index dont les dates ne sont pas dans l'intervalle demane
                currentFirst = newFrame.index[0]
                currentLast = newFrame.index[len(newFrame) - 1]
                if limitFrom > currentFirst :
                    newFrame= newFrame[limitFrom:currentLast]
                
                if limitTo < currentLast :
                    newFrame = newFrame[currentFirst:limitTo]
            
            
            
            if len(newFrame) > 0 :
                #print_full(newFrame)   
                self.rawPandaDataFrame = pd.concat ([self.rawPandaDataFrame,newFrame])
            return self.rawPandaDataFrame
    def __convertDataToPandasFrame (self, datesArray_p, valuesArray_p, label):
        freshDates = []
        freshValues =  []
        ##print 'len(dates) : %d, len(values) : %d' % (len(datesArray_p), len(valuesArray_p))
        if len(datesArray_p) > 0 :
            for  i in range(len(datesArray_p) ):
  
                dat = self.convertUnixTimeStamp2PyDate(datesArray_p[i])
                freshDates.append(dat)
            for  i in range(len(valuesArray_p) ):
                freshValues.append (valuesArray_p[i])
            return pd.DataFrame(freshValues,index=freshDates,columns=[label])
                # Remove freshValue
        freshDates = []
        freshValues =  []
        return None
    
    
    def __loadSensorData(self,sensor = None, from_p = None,  to_p = None):
        return self.__loadSensorDataFlat(sensor.agspSensorId, time.mktime(from_p.timetuple()), time.mktime(to_p.timetuple()))
    
    def __loadSensorDataFlat(self,sensorId = None, from_p = None,  to_p = None):
        return self.connector.getSensorData(sensorId, time.mktime(from_p.timetuple()), time.mktime(to_p.timetuple()))
    
            
    def convertUnixTimeStamp2PyDate (self,unixtimeStamp) :
        '''
        Convert a unixtime stamp (provenant du serveur agriscope) en Temps python avec une timezone UTC
        '''
        #
        # Comportement bizarre de sync 1199/thermomètre(-485966252) Marsillargues Marseillais Nord(1199) T° AIR °C no user parameter
        # lors de la syncrhonination de base de l'univers
        # il y a vait:
#unixtimestamp=1412937447499
#unixtimestamp=1412937832500
#unixtimestamp=1404910637499
#unixtimestamp=-30373006607501
#======================================================================
#ERROR: test_firstUnivers (tests.agspUniversTests.TestAgspUnivers)
#----------------------------------------------------------------------
#Traceback (most recent call last):
#  File "C:\Users\guillaume\Documents\Developpement\django\trunk\datatooling\pandas\tests\agspUniversTests.py", line 37, in test_firstUnivers
        #print unixtimeStamp
        if unixtimeStamp < 0 :
            unixtimeStamp = 1
        #print "unixtimestamp=" + unicode(unixtimeStamp)
        returnv = self.tz.localize(datetime.datetime.utcfromtimestamp(unixtimeStamp/1000))
        #print unicode(returnv)
        #print "%s" % returnv.year
        #if (returnv.year == 1992) :
            
            #print "%d %s" % (unixtimeStamp, unicode(returnv))
        return returnv    
    
    
    
