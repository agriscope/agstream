import unittest   # The test framework
import datetime
from datetime import timedelta 
import time
from agstream.session_extended import AgspExtendedSession


class Test_AgspStreamBasic(unittest.TestCase):
    def test_getAgribaseDataframe01(self):
        session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
        session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
        abs = session.getAgribase(2061)
        df = session.getAgribaseDataframe(abs)
        print (u"Récuperation de %d données" % (df.shape[0] * df.shape[1]))
        print (df.head())
        xlsFileName = u"%s.xlsx" % abs.name 
        print(u"Ecriture des  données dans le fichier %s " % xlsFileName)
        # suppression des timezone, car excel ne le supporte pas
        df=session.remove_any_timezone_info(df)
        if len(df) > 0 : 
            df.to_excel(xlsFileName, engine=u"openpyxl")
            
        # la meme chose mais avec un date specifie
        to_p=datetime.datetime.now() 
        from_p = to_p - timedelta(seconds=60*30) # 30 minutes    
        df_short = session.getAgribaseDataframe(abs,from_p=from_p,to_p=to_p)
        self.assertTrue(len(df)>=len(df_short))
        
        # indexation des colonnes de la dataframes par index
        df_short = session.getAgribaseDataframe(abs,from_p=from_p,to_p=to_p,index_by_sensor_id = True)
        print (df_short.columns)
        
        
    def test_get_data_by_each_sensors(self):
        session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
        session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True)
        abs = session.getAgribase(2061)

        print (u"****************************************")
        print (abs)
        df = session.getAgribaseDataframe(abs)
        for sensor in abs.sensors:
            print(u"%s %s" % (abs.name, sensor.name))
            df = session.getSensorDataframe(sensor)
            if df is not None:
                print(df.tail())

    def test_update_agribase_info(self):
        session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
        session.set_debug(True)
        session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True,showVirtualSensors=[])
        # abs=session.getAgribaseInfo(2061)
        abs=session.getAgribase(2061)
        self.assertFalse(any(sens.measureType=='TEMPERATURE HUMIDE' for sens in abs.sensors))
        session.updateAgribaseInfo(2061)      
        self.assertTrue(any(sens.measureType=='TEMPERATURE HUMIDE' for sens in abs.sensors))
        

    def test_update_agribase_info_on_login(self):
        session = AgspExtendedSession(wanted_virtual_types=['POINT ROSE','HEURES DE FROID','HUMIDE'])
        session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True,showVirtualSensors=[])
        # abs=session.getAgribaseInfo(2061)
        abs=session.getAgribase(2061)
        self.assertFalse(any(sens.measureType=='TEMPERATURE HUMIDE' for sens in abs.sensors))
        session.login(u"masnumeriqueAgStream", u"1AgStream", updateAgribaseInfo=True,showVirtualSensors=[2061])
        abs=session.getAgribase(2061)
        self.assertTrue(any(sens.measureType=='TEMPERATURE HUMIDE' for sens in abs.sensors))
        
if __name__ == '__main__':
    unittest.main()
