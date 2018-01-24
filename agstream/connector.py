# -*- coding: utf-8 -*-
'''
Created on 23 mai 2014

@author: renaud
'''

import json
import urllib

import django.utils.http as djangoUtils
import rexec
import os

'''
Error class
'''
class AgspError(Exception):
        def __init__(self, value):
            self.value = value
        def __unicode__(self): 
            return repr(self.value)
        def __str__(self):
            return unicode(self).encode('utf-8')

'''
Agriscope API connector
'''
class AgspConnecteur :
   
    debug=True
    "Acces a l'API du serveur AGRISCOPE"
    def __init__ (self, server = u'jsonapi.agriscope.fr' ):
        self.sessionOpen = False
        self.agspSessionId = 0
        self.server = u'http://' + server
        self.application = u'/agriscope-web/app'
        self.lastLogin = 'undefined'
        self.lastPassword = 'undefined'
        self.debug=False

    def set_debug(self, value):
        self.debug = value

    def login (self, login_p, password_p):
        self.lastLogin = login_p
        self.lastPassword = password_p
        url = self.server + self.application + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"login","parameters":{"login":"' + login_p + '","password":"' + password_p + '"}}'
        obj = self.executeJsonRequest (url,'login()')
        if obj['returnStatus'] != 'RETURN_STATUS_OK' :
            print("Failed to open the agriscope session for login " + login_p)
            print(obj['infoMessage'])
            self.sessionOpen = False
            self.agspSessionId = -1
        elif obj['loginOk'] == True:
            # print("Agriscope session open for login " + login_p)
            self.sessionOpen = True
            self.agspSessionId = obj['agriscopeSessionId']
        elif obj['loginOk'] == False:
            print("Agriscope session failed for login " + login_p)
            self.sessionOpen = False
            self.agspSessionId = obj['agriscopeSessionId']
        return (self.sessionOpen, self.agspSessionId)

    def getAgribases(self, id_p = -1):
        if id_p == -1 :
            id_p = self.agspSessionId
        
        url = self.server + self.application + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"getAgribases","parameters":{"agriscopeSessionId":' + unicode(id_p) + '}}'
        return self.executeJsonRequest(url, "getAgribases()") 
        
            
    def getSensorData(self, sensorId, from_p = None,  to_p = None):
        id_p = self.agspSessionId
        from_p = long (from_p * 1000)
        to_p = long (to_p * 1000)

        url = self.server + self.application + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"getSensorData","parameters":{"personalKey":"DUMMY","sensorInternalId":'+unicode(sensorId)+',"agriscopeSessionId":' + unicode(id_p) + ',"from":' + unicode(from_p) + ',"to":' + unicode(to_p) + '}}'
        tmpJson= self.executeJsonRequest(url, "getSensorData()") 
        return tmpJson['atomicResults'][0]['dataDates'],tmpJson['atomicResults'][0]['dataValues']
    
    def executeJsonRequest (self, url, method=""):
        try : 
            
            if self.debug == True :
                    print url
            str_response=""    
            # RECORD MODE
            retry=3
            i = 0
            while retry > 0 :
                try :
                    response = urllib.urlopen( url)
                    retry = -1
                except Exception, e:
                    retry = retry - 1
                    i = i+1
                    print str(i) + " retry connection "
                    
            if retry == 0 :
                print "Probleme de connexion pour aller vers " + url
                return
            str_response = response.read().decode('utf-8')

            if self.debug == True :
                print str_response
            obj = json.loads(str_response,strict=False)
            infomessage="N/A"
            if 'infoMessage' in obj :
                infomessage = obj['infoMessage']
                if  "session invalide" in infomessage:
                    if len(method) > 0 :
                        print u"Numero de session invalide dans l'appel de " + method +" par l'api."
                    else :
                        print u"Numero de session invalide  par l'api."
                        raise AgspError(u"Erreur de connection")
            return (obj)
        except Exception, e:
            print e.__doc__
            print e.message
            if len(method) > 0 :
                raise AgspError(u"Erreur de connection dans " + method )
            else :
                raise AgspError(u"Erreur de connection "  )
            
    debug = property(None, set_debug, None, "debug's docstring")
            
        
