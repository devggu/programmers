import pyodbc
from zipfile import ZipFile
import glob
import os
import os.path
import time
import getpass
from datetime import datetime
import pandas as pd
from numpy import NaN
import openpyxl
import msoffcrypto
import io
import json
from natsort import natsorted
from sqlalchemy import create_engine, text
import urllib
import sqlite3 as db
import numpy as np
import clr
from System.IO import Directory, Path, File
from System import String, Environment
import psycopg2
class slmApplication:
    def __init__(OOO0000O0000O000O , O0OOOO000OO00O000 , O000OOOO0O0O0O0O0 , OOOO0000OOO0OOOO0 , OOO00OO00OO0O0OOO , O0000OOOOO0O0OOO0 , OOO0OOO00OOOOO00O , OO0OO00000000OO0O ):
        try:
            OOO0000O0000O000O .excel_pwd = OOOO0000OOO0OOOO0 
            if OO0OO00000000OO0O  == '':
                OO0OO00000000OO0O  = '/usr/local/lib/dwsim/'
            OOO0000O0000O000O .conn_string = f'dbname ={O0000OOOOO0O0OOO0 } user={O0OOOO000OO00O000 } password={O000OOOO0O0O0O0O0 } host={OOO00OO00OO0O0OOO } port={OOO0OOO00OOOOO00O }'
            OOO0000O0000O000O .conn = psycopg2.connect(OOO0000O0000O000O .conn_string)
            OOO0000O0000O000O .cursor = OOO0000O0000O000O .conn.cursor()
            OO00OOO0O00OO00OO  = urllib.parse.quote_plus(OOO0000O0000O000O .conn_string)
            print('SQL connected!')
        except:
            print('SQL not connected!')
        O0O0O0O0OOO0OO0OO  = OO0OO00000000OO0O 
        OOO0000O0000O000O .test_run = 0
        OOO0O00OO00OOOO0O  = True
        if OOO0O00OO00OOOO0O :
            OOO0000O0000O000O .log_inputs_realtime = 0
            OOO0000O0000O000O .log_inputs_history = 0
            OOO0000O0000O000O .hide_rules = 1
        else:
            OOO0000O0000O000O .log_inputs_realtime = 1
            OOO0000O0000O000O .log_inputs_history = 1
            OOO0000O0000O000O .hide_rules = 0
        OOO0000O0000O000O .compare_pre_and_curr_status = 1
        OOO0000O0000O000O .log_less_priority_items = 0
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'CapeOpen.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.Automation.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.Interfaces.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.GlobalSettings.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.SharedClasses.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.Thermodynamics.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.UnitOperations.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'DWSIM.Inspector.dll')
        clr.AddReference(O0O0O0O0OOO0OO0OO  + 'System.Buffers.dll')
        from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
        from DWSIM.Thermodynamics import Streams, PropertyPackages
        from DWSIM.UnitOperations import UnitOperations
        from DWSIM.Automation import Automation3
        from DWSIM.GlobalSettings import Settings
        OOO0000O0000O000O .interf = Automation3()
        OOOO0OO00000OOO00  = 'assets/'
        OO000O00O0000OO0O  = 'assets/py_conn/'
        OOOOO0O00O0OOO00O  = os.path.abspath(os.path.dirname(__file__))
        OOO0000O0000O000O .RCA_mastersheet_path = os.path.join(OOOOO0O00O0OOO00O , OOOO0OO00000OOO00  + 'SHI Rules Master sheet_12142023_rev3.7')
        OOOO0O0OOO0O0OO00  = OOOO0OO00000OOO00  + 'simfiles'
        OOO0000O0000O000O .simfiles_path = os.path.join(OOOOO0O00O0OOO00O , OOOO0O0OOO0O0OO00 )
        OO000O0OOO0OO0OOO  = os.path.join(OOOOO0O00O0OOO00O , OO000O00O0000OO0O )
        OOO0000O0000O000O .ent = '@@@LD2_S2_out_actual_specific_enthalpy@@@'
        OOO0000O0000O000O .sim1 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'sclr_py_conn.dwxmz')
        print('sim1-SC interface ready')
        OOO0000O0000O000O .sim2 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'fv_py_conn.dwxmz')
        print('sim2-FV interface ready')
        OOO0000O0000O000O .sim3 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'lngv_py_conn.dwxmz')
        print('sim3-LNGV interface ready')
        OOO0000O0000O000O .sim4 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'bogh_py_conn.dwxmz')
        print('sim4-BOGH interface ready')
        OOO0000O0000O000O .sim5 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'wuh_py_conn.dwxmz')
        print('sim5-WUH interface ready')
        OOO0000O0000O000O .sim6 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'gwhs_py_conn.dwxmz')
        print('sim6-GWHStm interface ready')
        OOO0000O0000O000O .sim7 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'LD1_py_conn.dwxmz')
        print('sim7-LD1 interface ready')
        OOO0000O0000O000O .sim8 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'LD2_py_conn.dwxmz')
        print('sim8-LD2 interface ready')
        OOO0000O0000O000O .sim9 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'HD1_py_conn.dwxmz')
        print('sim9-HD1 interface ready')
        OOO0000O0000O000O .sim10 = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'HD2_py_conn.dwxmz')
        print('sim10-HD2 interface ready')
        OOO0000O0000O000O .ME1_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'ME1_py_conn.dwxmz')
        OOO0000O0000O000O .ME2_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'ME2_py_conn.dwxmz')
        OOO0000O0000O000O .GE1_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'GE1_py_conn.dwxmz')
        OOO0000O0000O000O .GE2_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'GE2_py_conn.dwxmz')
        OOO0000O0000O000O .GE3_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'GE3_py_conn.dwxmz')
        OOO0000O0000O000O .GE4_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'GE4_py_conn.dwxmz')
        print('ME1/2 and GE1/2/3/4 interface ready')
        OOO0000O0000O000O .NG1_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'NG1_py_conn.dwxmz')
        OOO0000O0000O000O .NG2_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'NG2_py_conn.dwxmz')
        print('NG1/2 interface ready')
        OOO0000O0000O000O .AB1_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'AB1_py_conn.dwxmz')
        OOO0000O0000O000O .AB2_sim = OOO0000O0000O000O .interf.LoadFlowsheet(OO000O0OOO0OO0OOO  + 'AB2_py_conn.dwxmz')
        print('AB1/2 interface ready')
        OOO0000O0000O000O .agg = {}
        OOO0000O0000O000O .persistence = {}
        OOO0000O0000O000O .mavg_samples = {}
        OOO0000O0000O000O .for_test = 'none_for_test'
        OOO0000O0000O000O .agg_test = 'none'
    def validateInputs(O0O00O0OOOOOO0000 , O0O0O0O0O00OOOO00 , OO000O00OOOO00000 , O000O0OOOO000OO00 ):
        O0OO0OO0OOOOO0O0O  = {}
        for key in OO000O00OOOO00000 .keys():
            OOO0O00O0OO0O0O00  = O0O0O0O0O00OOOO00 [key]
            O00OO0O0OOOO000OO  = OO000O00OOOO00000 [key][0]
            OO00O0OOO000OO000  = OO000O00OOOO00000 [key][1]
            OOOO00O0OO0OO0OO0  = O00OO0O0OOOO000OO [0]
            OO000O000O00OOO00  = O00OO0O0OOOO000OO [1]
            OO000000O0O00O00O  = 'normal range of ' + key + ': [' + str(OOOO00O0OO0OO0OO0 ) + ',' + str(OO000O000O00OOO00 ) + ']. Current value of ' + key + ': ' + str(OOO0O00O0OO0O0O00 ) + '. Temporary value of ' + str(OO00O0OOO000OO000 ) + ' will be used in dwsim to avoid non-convergence of flowsheet.'
            O0O00O0OOOOOO0000 .cursor.execute('select "Tag" from public."Log_messages"')
            OOOO00O0O00000O0O  = O0O00O0OOOOOO0000 .cursor.fetchall()
            O0O00O0OOOOOO0000 .conn.commit()
            O0O0O0O000O00O00O  = [item[0] for item in OOOO00O0O00000O0O ]
            if OOO0O00O0OO0O0O00  < OOOO00O0OO0OO0OO0  or OOO0O00O0OO0O0O00  > OO000O000O00OOO00 :
                print(key, 'is out of range, so using temporary value which is: ', OO00O0OOO000OO000 )
                O0OO0OO0OOOOO0O0O [key] = OO00O0OOO000OO000 
                if key not in O0O0O0O000O00O00O :
                    O0O00O0OOOOOO0000 .cursor.execute('insert into public."Log_messages" values(%s, %s, %s, %s)', [O000O0OOOO000OO00 , key, 'dwsimSimulation', OO000000O0O00O00O ])
                    O0O00O0OOOOOO0000 .conn.commit()
            else:
                pass
        return O0OO0OO0OOOOO0O0O 
    def dwsimSimulation(O0000OOO0OOO0OO00 , OOOOO00OOO0O0O00O , OOO0000O00000OOOO , OO0O0O0O000O0O00O , O00OO00O00OO00O00 ):
        O00OO0O000O0OO0O0  = {}
        OO0O00O0O0OO000O0  = {}
        OO0OOO00O00OOO0O0  = {}
        O00OO00O0OOOOO0OO  = {}
        OO0O0O00O00O00O00  = {}
        OOOOOO0O0O0O0O0OO  = {}
        O0OO000OOO0000O00  = {}
        O00O0O00000O0O0OO  = {}
        OOO0O0OOO0OOOO0OO  = {}
        OOOOOO00O000OO0OO  = {}
        OO0000OOOOOO00OO0  = {}
        OO0OOO0O0OOOOOO0O  = {}
        OOO0OO0O00OO0O0OO  = {}
        OOOO00O000O00OO0O  = {}
        OO0OOO00O00OO00OO  = {}
        OO0OOOOO0OOO00OOO  = {}
        O00O0O00OO0OO0O0O  = {}
        OO000000O0000OOO0  = {}
        O00O0OOO0OOOOOOO0  = {}
        OO00O00OO0000000O  = {}
        OOO0O00OO00O0OO00  = {}
        O0O0O0O00O000O0OO  = {}
        OOOOO0OO00OO0OO0O  = {}
        O00OO0O000O000O0O  = {}
        O0OOO0O000OO00OO0  = {}
        OO0O00OO000O0000O  = {}
        OO000O00OOOO00000  = {'CM_LNGSubClr_Flow': [[3, 10], 5], 'ME1_EG_ScavAirMeanPrs': [[0.1, 0.5], 0.26], 'ME2_EG_ScavAirMeanPrs': [[0.1, 0.5], 0.26]}
        O0OO0OO0OOOOO0O0O  = O0000OOO0OOO0OO00 .validateInputs(OOOOO00OOO0O0O00O , OO000O00OOOO00000 , OO0O0O0O000O0O00O )
        if OOO0000O00000OOOO ['SC'] == 1:
            print('starting dwsim SC')
            O0O00OO0000O0OOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('LNG_in').GetAsObject()
            O0OO00000000OOOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('LNG_out').GetAsObject()
            OOOO00OO00O000O00  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX2_LNG_cooling').GetAsObject()
            OOOO000OO0O0O0O0O  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_comp_in').GetAsObject()
            O0000O0O0O000OOO0  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_comp').GetAsObject()
            OOO00O0OO000000O0  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_comp_out_ideal').GetAsObject()
            OO0O00000OO0OOOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_comp_out_actual').GetAsObject()
            O0O00O00O0OOOOOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX300').GetAsObject()
            OO0O0000OO0O000OO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_exp').GetAsObject()
            O0O0OOO0O00OO0OO0  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_exp_in').GetAsObject()
            OOOO0O0O000OO0000  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_exp_out_ideal').GetAsObject()
            O000OOO0000OO0OO0  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MTC_exp_out_actual').GetAsObject()
            OO0O0O00OO0O00OOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MC_comp_in').GetAsObject()
            OO0OO0OOOO00OOOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MC_comp').GetAsObject()
            OOOO0OOOO0O0000OO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MC_comp_out_ideal').GetAsObject()
            O00OO00O000OOOO00  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('MC_comp_out_actual').GetAsObject()
            O00OO000OO00000OO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX200').GetAsObject()
            OOO00O000OOOOOO00  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX200_out').GetAsObject()
            OO00O0OO00OO0OOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX1_ref_cooling').GetAsObject()
            O0OO0OOOOO0O0OOOO  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX1-2_ref_heating').GetAsObject()
            OOOOO00OO00O0OO0O  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX1-2_out').GetAsObject()
            O0OOOO00O0O0OOO00  = O0000OOO0OOO0OO00 .sim1.GetFlowsheetSimulationObject('HX1-2_ideal').GetAsObject()
            OOOOOO0OOO0O0OOO0  = 100000.0
            OOO0O00OOOO0O00O0  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_DropPrs'] / 1000.0
            OO0OOOOO000OOO00O  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_OutPrs']
            OO0O00OOOOOO00000  = OO0OOOOO000OOO00O  + OOO0O00OOOO0O00O0 
            O0O00OO0000O0OOOO .SetPressure(OO0O00OOOOOO00000  * OOOOOO0OOO0O0OOO0 )
            OOOO00OO00O000O00 .set_DeltaP(OOO0O00OOOO0O00O0  * OOOOOO0OOO0O0OOO0 )
            O0O00OO0000O0OOOO .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_InTemp'] + 273.15)
            if 'CM_LNGSubClr_Flow' in O0OO0OO0OOOOO0O0O :
                O00000OOOO0O0O00O  = O0OO0OO0OOOOO0O0O ['CM_LNGSubClr_Flow']
            else:
                O00000OOOO0O0O00O  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_Flow']
            O0O00OO0000O0OOOO .SetMassFlow(O00000OOOO0O0O00O  / 3600.0)
            OOOO00OO00O000O00 .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_OutTemp'] + 273.15)
            OOOO000OO0O0O0O0O .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompInPrs'] * OOOOOO0OOO0O0OOO0 )
            OOOO000OO0O0O0O0O .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompInTemp'] + 273.15)
            O0000O0O0O000OOO0 .set_POut(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompOutPrs'] * OOOOOO0OOO0O0OOO0 )
            OO0O00000OO0OOOOO .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompOutPrs'] * OOOOOO0OOO0O0OOO0 )
            OO0O00000OO0OOOOO .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompOutTemp'] + 273.15)
            O0O00O00O0OOOOOOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_Hx300_OutTemp'] + 273.15)
            OOO000O0O000OO000  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_CompOutPrs'] - OOOOO00OOO0O0O00O ['CM_LNGSubClr_Hx300_OutPrs']
            O0O00O00O0OOOOOOO .set_DeltaP(OOO000O0O000OO000  * OOOOOO0OOO0O0OOO0 )
            OO0OO0OOOO00OOOOO .set_POut(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC_CompOutPrs'] * OOOOOO0OOO0O0OOO0 )
            O00OO00O000OOOO00 .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC_CompOutPrs'] * OOOOOO0OOO0O0OOO0 )
            O00OO00O000OOOO00 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC_CompOutTemp'] + 273.15)
            O00OO000OO00000OO .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_Hx1_InTemp'] + 273.15)
            OO00O0OO00OO0OOOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineInTemp'] + 273.15)
            O0OOO000OOOOO0000  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC_CompOutPrs'] - OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineInPrs']
            OO00O0OO00OO0OOOO .set_DeltaP(O0OOO000OOOOO0000  * OOOOOO0OOO0O0OOO0 )
            OO0O0000OO0O000OO .set_POut(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineOutPrs'] * OOOOOO0OOO0O0OOO0 )
            O000OOO0000OO0OO0 .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineOutPrs'] * OOOOOO0OOO0O0OOO0 )
            O000OOO0000OO0OO0 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineOutTemp'] + 273.15)
            O0OOOO00O0O0OOO00 .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC_TurbineOutPrs'] * OOOOOO0OOO0O0OOO0 )
            O0OOOO00O0O0OOO00 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGSubClr_Hx1_InTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim1)
            OOO0000OO0OOO00O0  = {}
            OOOO0O0OO000OO00O  = O0O00OO0000O0OOOO .GetTemperature() - 273.15
            OO0OOOOO000OOO00O  = O0OO00000000OOOOO .GetPressure() / OOOOOO0OOO0O0OOO0 
            OO0O00O000O0O0OOO  = O0OO00000000OOOOO .GetMassFlow() * 3600
            O00OO0O000000O0OO  = OOOO000OO0O0O0O0O .GetPressure() / OOOOOO0OOO0O0OOO0 
            O0O0OO0O0000O000O  = OOOO000OO0O0O0O0O .GetTemperature() - 273.15
            OO00O0000OOO0OO0O  = OO0O00000OO0OOOOO .GetPressure() / OOOOOO0OOO0O0OOO0 
            OOOO000OO00O00O00  = OO0O00000OO0OOOOO .GetTemperature() - 273.15
            O0000O00O0OOO000O  = OO0O0O00OO0O00OOO .GetPressure() / OOOOOO0OOO0O0OOO0 
            OOOOO0O00OO000O00  = OO0O0O00OO0O00OOO .GetTemperature() - 273.15
            O00000O00OO000O00  = O00OO00O000OOOO00 .GetPressure() / OOOOOO0OOO0O0OOO0 
            OOO00OOO00000O0OO  = O00OO00O000OOOO00 .GetTemperature() - 273.15
            OOO000O0000O0O0OO  = OOO00O000OOOOOO00 .GetTemperature() - 273.15
            OO0OOO0OO00O000OO  = O0O0OOO0O00OO0OO0 .GetPressure() / OOOOOO0OOO0O0OOO0 
            O0000OO00O0OOO00O  = O0O0OOO0O00OO0OO0 .GetTemperature() - 273.15
            O00O0OOOO0OO0OO00  = O000OOO0000OO0OO0 .GetPressure() / OOOOOO0OOO0O0OOO0 
            OO0OOO00OO000O000  = O000OOO0000OO0OO0 .GetTemperature() - 273.15
            OO0O0OO000OOO00OO  = OOOOO00OO00O0OO0O .GetTemperature() - 273.15
            OOO0000OO0OOO00O0 ['LNG_in_temp'] = OOOO0O0OO000OO00O 
            OOO0000OO0OOO00O0 ['LNG_out_pres'] = OO0OOOOO000OOO00O 
            OOO0000OO0OOO00O0 ['LNG_out_flow'] = OO0O00O000O0O0OOO 
            OOO0000OO0OOO00O0 ['MTC_comp_in_pres'] = O00OO0O000000O0OO 
            OOO0000OO0OOO00O0 ['MTC_comp_in_temp'] = O0O0OO0O0000O000O 
            OOO0000OO0OOO00O0 ['MTC_comp_out_pres'] = OO00O0000OOO0OO0O 
            OOO0000OO0OOO00O0 ['MTC_comp_out_temp'] = OOOO000OO00O00O00 
            OOO0000OO0OOO00O0 ['MC_comp_in_pres'] = O0000O00O0OOO000O 
            OOO0000OO0OOO00O0 ['MC_comp_in_temp'] = OOOOO0O00OO000O00 
            OOO0000OO0OOO00O0 ['MC_comp_out_pres'] = O00000O00OO000O00 
            OOO0000OO0OOO00O0 ['MC_comp_out_temp'] = OOO00OOO00000O0OO 
            OOO0000OO0OOO00O0 ['HX200_out_temp'] = OOO000O0000O0O0OO 
            OOO0000OO0OOO00O0 ['MTC_exp_in_pres'] = OO0OOO0OO00O000OO 
            OOO0000OO0OOO00O0 ['MTC_exp_in_temp'] = O0000OO00O0OOO00O 
            OOO0000OO0OOO00O0 ['MTC_exp_out_pres'] = O00O0OOOO0OO0OO00 
            OOO0000OO0OOO00O0 ['MTC_exp_out_temp'] = OO0OOO00OO000O000 
            OOO0000OO0OOO00O0 ['HX12_out_temp'] = OO0O0OO000OOO00OO 
            OO00O0O0O0O0O00OO  = OOOO000OO0O0O0O0O .GetMassEnthalpy()
            OOO0OO00OOO00O0OO  = OO00O0000OOO0OO0O  / O00OO0O000000O0OO 
            O00000000O0O0OO0O  = abs(O0000O0O0O000OOO0 .GetPowerGeneratedOrConsumed())
            O00O000O0O0O0OOO0  = O0000O0O0O000OOO0 .get_PolytropicHead()
            O0O0O0OO0OO000O0O  = OOO00O0OO000000O0 .GetTemperature() - 273.15
            OO00O0O0O0O0O00OO  = OOOO000OO0O0O0O0O .GetMassEnthalpy()
            O00000000000O0000  = OOO00O0OO000000O0 .GetMassEnthalpy()
            OO0OO00OOO0O0O0OO  = OO0O00000OO0OOOOO .GetMassEnthalpy()
            O0O0O00O0000O0000  = O00000000000O0000  - OO00O0O0O0O0O00OO 
            OOOOO00O0OOOO0OO0  = OO0OO00OOO0O0O0OO  - OO00O0O0O0O0O00OO 
            OO0OO000000OO0000  = O0O0O00O0000O0000  / OOOOO00O0OOOO0OO0  * 100
            OOOO0O0O0O00OOO0O  = O0O00O00O0OOOOOOO .get_DeltaT()
            O0OOO0O0OO000O0O0  = O0O00O00O0OOOOOOO .GetPowerGeneratedOrConsumed()
            O00OO0O000O0OO0O0 ['SC_MTC_comp_in_specific_enthalpy'] = OO00O0O0O0O0O00OO 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_pressure_ratio'] = OOO0OO00OOO00O0OO 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_polytropic_power'] = O00000000O0O0OO0O 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_polytropic_head'] = O00O000O0O0O0OOO0 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_in_specific_enthalpy'] = OO00O0O0O0O0O00OO 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_out_actual_specific_enthalpy'] = OO0OO00OOO0O0O0OO 
            O00OO0O000O0OO0O0 ['SC_MTC_comp_polytropic_efficiency'] = OO0OO000000OO0000 
            O00OO0O000O0OO0O0 ['SC_HX300_deltaT'] = OOOO0O0O0O00OOO0O 
            O00OO0O000O0OO0O0 ['SC_HX300_duty'] = O0OOO0O0OO000O0O0 
            OO00O0OO0O00OOO00  = OO0O0O00OO0O00OOO .GetMassEnthalpy()
            O00O00000O000O000  = O00000O00OO000O00  / O0000O00O0OOO000O 
            O0OO000O0OO000000  = abs(OO0OO0OOOO00OOOOO .GetPowerGeneratedOrConsumed())
            O0000OOOO00OO0O0O  = OO0OO0OOOO00OOOOO .get_PolytropicHead()
            O0O000O0O0O0OO0OO  = OOOO0OOOO0O0000OO .GetTemperature() - 273.15
            OO00O0OO0O00OOO00  = OO0O0O00OO0O00OOO .GetMassEnthalpy()
            O0OO0OOO00O0000OO  = OOOO0OOOO0O0000OO .GetMassEnthalpy()
            O0O0OO00O000O0O0O  = O00OO00O000OOOO00 .GetMassEnthalpy()
            O00OO0O0OO00O0OO0  = O0OO0OOO00O0000OO  - OO00O0OO0O00OOO00 
            OO0OOOOO0000OOO00  = O0O0OO00O000O0O0O  - OO00O0OO0O00OOO00 
            OOOO00O000O00O0OO  = O00OO0O0OO00O0OO0  / OO0OOOOO0000OOO00  * 100
            O00O0OOOOO00O0O00  = O00OO000OO00000OO .get_DeltaT()
            OO00OO0OOO0OOO000  = O00OO000OO00000OO .GetPowerGeneratedOrConsumed()
            O00OO0O000O0OO0O0 ['SC_MC_comp_in_specific_enthalpy'] = OO00O0OO0O00OOO00 
            O00OO0O000O0OO0O0 ['SC_MC_comp_pressure_ratio'] = O00O00000O000O000 
            O00OO0O000O0OO0O0 ['SC_MC_comp_polytropic_power'] = O0OO000O0OO000000 
            O00OO0O000O0OO0O0 ['SC_MC_comp_polytropic_head'] = O0000OOOO00OO0O0O 
            O00OO0O000O0OO0O0 ['SC_MC_comp_in_specific_enthalpy'] = OO00O0OO0O00OOO00 
            O00OO0O000O0OO0O0 ['SC_MC_comp_out_actual_specific_enthalpy'] = O0O0OO00O000O0O0O 
            O00OO0O000O0OO0O0 ['SC_MC_comp_polytropic_efficiency'] = OOOO00O000O00O0OO 
            O00OO0O000O0OO0O0 ['SC_HX200_deltaT'] = O00O0OOOOO00O0O00 
            O00OO0O000O0OO0O0 ['SC_HX200_duty'] = OO00OO0OOO0OOO000 
            O0OO0O0OOOO0OOO0O  = O0O0OOO0O00OO0OO0 .GetMassEnthalpy()
            OOOO00O000O00O0O0  = OO0OOO0OO00O000OO  / O00O0OOOO0OO0OO00 
            OO00O00O00000OO0O  = abs(OO0O0000OO0O000OO .GetPowerGeneratedOrConsumed())
            O000000OO00O0O0O0  = OO0O0000OO0O000OO .get_PolytropicHead()
            O0O0000000000OO0O  = OOOO0O0O000OO0000 .GetTemperature() - 273.15
            O0OO0O0OOOO0OOO0O  = O0O0OOO0O00OO0OO0 .GetMassEnthalpy()
            O0OOOOOOO000OO0O0  = OOOO0O0O000OO0000 .GetMassEnthalpy()
            O0O00O0OO0O000O00  = O000OOO0000OO0OO0 .GetMassEnthalpy()
            OO00OOO0OO0O0O0OO  = O0OOOOOOO000OO0O0  - O0OO0O0OOOO0OOO0O 
            O00O00OOO0O0O00O0  = O0O00O0OO0O000O00  - O0OO0O0OOOO0OOO0O 
            O00OO00O00OOO0000  = O00O00OOO0O0O00O0  / OO00OOO0OO0O0O0OO  * 100
            O00OO0O000O0OO0O0 ['SC_MTC_exp_in_specific_enthalpy'] = O0OO0O0OOOO0OOO0O 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_pressure_ratio'] = OOOO00O000O00O0O0 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_polytropic_power'] = OO00O00O00000OO0O 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_polytropic_head'] = O000000OO00O0O0O0 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_in_specific_enthalpy'] = O0OO0O0OOOO0OOO0O 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_out_actual_specific_enthalpy'] = O0O00O0OO0O000O00 
            O00OO0O000O0OO0O0 ['SC_MTC_exp_polytropic_efficiency'] = O00OO00O00OOO0000 
            OOOO00000O00O0O00  = OOOO00OO00O000O00 .get_DeltaT()
            OO0O000OOOO00O00O  = OOOO00OO00O000O00 .GetPowerGeneratedOrConsumed()
            OO000OO0O0O0OO000  = OO00O0OO00OO0OOOO .get_DeltaT()
            O0O0OO00O00OO00OO  = OO00O0OO00OO0OOOO .GetPowerGeneratedOrConsumed()
            O0O0OO000OOO00OO0  = O0OO0OOOOO0O0OOOO .get_DeltaT()
            OO0OO000OO000OOO0  = O0OO0OOOOO0O0OOOO .GetPowerGeneratedOrConsumed()
            O00OO0O000O0OO0O0 ['SC_HX2_deltaT'] = OOOO00000O00O0O00 
            O00OO0O000O0OO0O0 ['SC_HX2_LNG_cold_power'] = OO0O000OOOO00O00O 
            O00OO0O000O0OO0O0 ['SC_HX1_deltaT'] = OO000OO0O0O0OO000 
            O00OO0O000O0OO0O0 ['SC_HX1_duty'] = O0O0OO00O00OO00OO 
            O00OO0O000O0OO0O0 ['SC_HX12_regenerator_deltaT'] = O0O0OO000OOO00OO0 
            O00OO0O000O0OO0O0 ['SC_HX12_regenerator_duty'] = OO0OO000OO000OOO0 
            O0OO0O0OO0OOOOO00  = OO0OOO00OO000O000 
            O0O0O0000OOOO0O00  = OOO00OOO00000O0OO 
            OO00O000O0O000OO0  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC1_Pwr'] + OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC2_Pwr'] + OOOOO00OOO0O0O00O ['CM_LNGSubClr_MTC3_Pwr']
            O0000OOO00OO000OO  = OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC1_Pwr'] + OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC2_Pwr'] + OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC3_Pwr'] + OOOOO00OOO0O0O00O ['CM_LNGSubClr_MC4_Pwr']
            OOO0O0O0O0OO00OO0  = OO0O000OOOO00O00O  / (OO00O000O0O000OO0  + O0000OOO00OO000OO )
            O00OO0O000O0OO0O0 ['SC_SC_min_temp'] = O0OO0O0OO0OOOOO00 
            O00OO0O000O0OO0O0 ['SC_SC_max_temp'] = O0O0O0000OOOO0O00 
            O00OO0O000O0OO0O0 ['SC_MTC_actual_power'] = OO00O000O0O000OO0 
            O00OO0O000O0OO0O0 ['SC_MC_actual_power'] = O0000OOO00OO000OO 
            O00OO0O000O0OO0O0 ['SC_COP'] = OOO0O0O0O0OO00OO0 
            for key in O00OO0O000O0OO0O0 .keys():
                O00OO0O000O0OO0O0 [key] = float('{0:.2f}'.format(O00OO0O000O0OO0O0 [key]))
        if OOO0000O00000OOOO ['FV'] == 1:
            print('starting dwsim FV')
            OO0OOOO0O0O00O0OO  = O0000OOO0OOO0OO00 .sim2.GetFlowsheetSimulationObject('FV_cold_in').GetAsObject()
            OO000000O00000OO0  = O0000OOO0OOO0OO00 .sim2.GetFlowsheetSimulationObject('FV_cold_out').GetAsObject()
            O0OO00OO0OOO0O000  = O0000OOO0OOO0OO00 .sim2.GetFlowsheetSimulationObject('FV_HT_1').GetAsObject()
            OOO00O0O0O00OOOOO  = O0000OOO0OOO0OO00 .sim2.GetFlowsheetSimulationObject('FV_stm_in').GetAsObject()
            OO0OOO0O0OOOOO0OO  = O0000OOO0OOO0OO00 .sim2.GetFlowsheetSimulationObject('FV_stm_out').GetAsObject()
            OO0OOOO0O0O00O0OO .SetTemperature(OOOOO00OOO0O0O00O ['FG_FV_InTempInd'] + 273.15)
            OO0OOOO0O0O00O0OO .SetPressure(OOOOO00OOO0O0O00O ['FG_FV_InPrs'] * 1000.0)
            OO0OOOO0O0O00O0OO .SetMassFlow(OOOOO00OOO0O0O00O ['FG_FV_DischFlow'] / 3600.0)
            O0OO00OO0OOO0O000 .set_OutletTemperature(OOOOO00OOO0O0O00O ['FG_FV_OutTemp2Ind'] + 273.15)
            O00OO0O00O0O0O000  = OOOOO00OOO0O0O00O ['FG_FV_InPrs'] - OOOOO00OOO0O0O00O ['FG_FV_OutPrs']
            O0OO00OO0OOO0O000 .set_DeltaP(O00OO0O00O0O0O000  * 1000.0)
            OOO00O0O0O00OOOOO .SetTemperature(OOOOO00OOO0O0O00O ['FG_FV_CondWtrTempInd'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim2)
            OOO0O00000O0000O0  = {}
            OOO00000OOO00O0O0  = OO0OOOO0O0O00O0OO .GetTemperature() - 273.15
            OOO0O000O00O00O0O  = OO0OOOO0O0O00O0OO .GetPressure() / 1000.0
            OOO0O00000O0000O0 ['FV_cold_in_temp'] = OOO00000OOO00O0O0 
            OOO0O00000O0000O0 ['FV_cold_in_pres'] = OOO0O000O00O00O0O 
            OOO00OO0OO0OOO00O  = OO0OOOO0O0O00O0OO .GetMassFlow() * 3600.0
            OOO0O00000O0000O0 ['FV_mass_flow'] = OOO00OO0OO0OOO00O 
            O000OO0O00O0O00OO  = OO000000O00000OO0 .GetTemperature() - 273.15
            OO0OOOOOO0OO0O0OO  = OO000000O00000OO0 .GetPressure() / 1000.0
            OOO0O00000O0000O0 ['FV_cold_out_temp'] = O000OO0O00O0O00OO 
            OOO0O00000O0000O0 ['FV_cold_out_pres'] = OO0OOOOOO0OO0O0OO 
            O0O0O000OOOOO0O0O  = OOO00O0O0O00OOOOO .GetTemperature() - 273.15
            O00OO0O0O00OOOO0O  = O0O0O000OOOOO0O0O 
            OOO0O00000O0000O0 ['FV_stm_in_temp'] = O0O0O000OOOOO0O0O 
            OOO0O00000O0000O0 ['FV_stm_out_temp'] = O00OO0O0O00OOOO0O 
            OOO0O0O00O00OO0O0  = abs(O0OO00OO0OOO0O000 .GetPowerGeneratedOrConsumed())
            OO0O00O0O0OO000O0 ['FV_Qc'] = OOO0O0O00O00OO0O0 
            OO0O0OO00000OOO0O  = (O0O0O000OOOOO0O0O  - O000OO0O00O0O00OO  - (O00OO0O0O00OOOO0O  - OOO00000OOO00O0O0 )) / np.log((O0O0O000OOOOO0O0O  - O000OO0O00O0O00OO ) / (O00OO0O0O00OOOO0O  - OOO00000OOO00O0O0 ))
            OO0O00O0O0OO000O0 ['FV_LMTD'] = OO0O0OO00000OOO0O 
            OOOOO00000000O00O  = 6.1
            OO0OO00O0OO0O0000  = OOO0O0O00O00OO0O0  / (OOOOO00000000O00O  * OO0O0OO00000OOO0O ) * 1000
            OO0O00O0O0OO000O0 ['FV_U'] = OO0OO00O0OO0O0000 
            O0O0OOOOOO00000OO  = 424.0
            O0000OOO0OOO0OO00 .cursor.execute('select "Value" from public."Output_Tags" where "TagName" = \'FV_fouling_factor\';')
            OOOO00O0O00000O0O  = O0000OOO0OOO0OO00 .cursor.fetchall()
            O0000OOO0OOO0OO00 .conn.commit()
            O0OO00O0OO000O00O  = OOOO00O0O00000O0O [0][0]
            if OOOOO00OOO0O0O00O ['FG_FV_DischFlow'] > 2500:
                OO0OO0000O0OO0O00  = 1 / OO0OO00O0OO0O0000  - 1 / O0O0OOOOOO00000OO 
                OO0OO0000O0OO0O00  = (1 - OO0OO0000O0OO0O00 ) * 100
            elif O0OO00O0OO000O00O  < 100.0:
                OO0OO0000O0OO0O00  = O0OO00O0OO000O00O 
            else:
                OO0OO0000O0OO0O00  = 100
            OO0O00O0O0OO000O0 ['FV_fouling_factor'] = OO0OO0000O0OO0O00 
            OOO0OOO0000000OOO  = OO0OOOO0O0O00O0OO .GetMassEnthalpy()
            OO0O00O0O0OO000O0 ['FV_cold_in_specific_enthalpy'] = OOO0OOO0000000OOO 
            O00000O0OO0O00O00  = OO000000O00000OO0 .GetMassEnthalpy()
            OO0O00O0O0OO000O0 ['FV_cold_out_specific_enthalpy'] = O00000O0OO0O00O00 
            OO0OOOOOO0OOOOOOO  = O000OO0O00O0O00OO  - OOO00000OOO00O0O0 
            OO0O00O0O0OO000O0 ['FV_cold_temp_rise'] = OO0OOOOOO0OOOOOOO 
            O000O0O00OOO0OO00  = O0O0O000OOOOO0O0O  - O000OO0O00O0O00OO 
            OO0O00O0O0OO000O0 ['FV_minimum_approach'] = O000O0O00OOO0OO00 
            O0O00OO0000000000  = OOO00O0O0O00OOOOO .GetMassFlow() * 3600
            OO0O00O0O0OO000O0 ['FV_steam_required'] = O0O00OO0000000000 
            OOO00000OOO000O0O  = OO0OOOO0O0O00O0OO .GetEnergyFlow()
            OO0O00O0O0OO000O0 ['FV_cold_in_energy_flow'] = OOO00000OOO000O0O 
            O000O0O0OO0O0O0OO  = OO000000O00000OO0 .GetEnergyFlow()
            OO0O00O0O0OO000O0 ['FV_cold_out_energy_flow'] = O000O0O0OO0O0O0OO 
            for key in OO0O00O0O0OO000O0 .keys():
                OO0O00O0O0OO000O0 [key] = float('{0:.2f}'.format(OO0O00O0O0OO000O0 [key]))
        if OOO0000O00000OOOO ['LNGV'] == 1:
            print('starting dwsim LNGV')
            O00OO000OO00OO0O0  = O0000OOO0OOO0OO00 .sim3.GetFlowsheetSimulationObject('LNGV_cold_in').GetAsObject()
            OO000O0OO0O0OOO0O  = O0000OOO0OOO0OO00 .sim3.GetFlowsheetSimulationObject('LNGV_cold_out').GetAsObject()
            O00OOOOO00O0O000O  = O0000OOO0OOO0OO00 .sim3.GetFlowsheetSimulationObject('LNGV_HT_1').GetAsObject()
            O000O00000000OOOO  = O0000OOO0OOO0OO00 .sim3.GetFlowsheetSimulationObject('LNGV_stm_in').GetAsObject()
            O0000O000OOOO0OOO  = O0000OOO0OOO0OO00 .sim3.GetFlowsheetSimulationObject('LNGV_stm_out').GetAsObject()
            O00OO000OO00OO0O0 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGVapr_InTempInd'] + 273.15)
            O00OO000OO00OO0O0 .SetPressure(OOOOO00OOO0O0O00O ['CM_LNGVapr_InPrs'] * 1000.0)
            O00OO000OO00OO0O0 .SetMassFlow(OOOOO00OOO0O0O00O ['FG_Flow_VaprToAtm'] / 3600.0)
            O00OOOOO00O0O000O .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LNGVapr_OutTempInd'] + 273.15)
            OO00O0OO0OOO0O0O0  = OOOOO00OOO0O0O00O ['CM_LNGVapr_InPrs'] - OOOOO00OOO0O0O00O ['CM_LNGVapr_OutPrs']
            O00OOOOO00O0O000O .set_DeltaP(OO00O0OO0OOO0O0O0  * 1000.0)
            O000O00000000OOOO .SetTemperature(OOOOO00OOO0O0O00O ['CM_LNGVapr_CondWtrTempInd'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim3)
            O0OOOO0O0OO0OOOOO  = {}
            OOO00OOO0O0OOO0O0  = O00OO000OO00OO0O0 .GetTemperature() - 273.15
            OOOO0OOO000O0000O  = O00OO000OO00OO0O0 .GetPressure() / 1000.0
            O0OOOO0O0OO0OOOOO ['LNGV_cold_in_temp'] = OOO00OOO0O0OOO0O0 
            O0OOOO0O0OO0OOOOO ['LNGV_cold_in_pres'] = OOOO0OOO000O0000O 
            OOO0000O0O0OOOO0O  = O00OO000OO00OO0O0 .GetMassFlow() * 3600.0
            O0OOOO0O0OO0OOOOO ['LNGV_mass_flow'] = OOO0000O0O0OOOO0O 
            OO0OOOOO0O000OO0O  = OO000O0OO0O0OOO0O .GetTemperature() - 273.15
            O000000000O0000O0  = OO000O0OO0O0OOO0O .GetPressure() / 1000.0
            O0OOOO0O0OO0OOOOO ['LNGV_cold_out_temp'] = OO0OOOOO0O000OO0O 
            O0OOOO0O0OO0OOOOO ['LNGV_cold_out_pres'] = O000000000O0000O0 
            OOO00OO00O0OO00O0  = O000O00000000OOOO .GetTemperature() - 273.15
            OO0OO0O0OO0O000OO  = OOO00OO00O0OO00O0 
            O0OOOO0O0OO0OOOOO ['LNGV_stm_in_temp'] = OOO00OO00O0OO00O0 
            O0OOOO0O0OO0OOOOO ['LNGV_stm_out_temp'] = OO0OO0O0OO0O000OO 
            OO0OOOO00O0OOO0O0  = abs(O00OOOOO00O0O000O .GetPowerGeneratedOrConsumed())
            OO0OOO00O00OOO0O0 ['LNGV_Qc'] = OO0OOOO00O0OOO0O0 
            OO0OO00O000OO00OO  = (OOO00OO00O0OO00O0  - OO0OOOOO0O000OO0O  - (OO0OO0O0OO0O000OO  - OOO00OOO0O0OOO0O0 )) / np.log((OOO00OO00O0OO00O0  - OO0OOOOO0O000OO0O ) / (OO0OO0O0OO0O000OO  - OOO00OOO0O0OOO0O0 ))
            OO0OOO00O00OOO0O0 ['LNGV_LMTD'] = OO0OO00O000OO00OO 
            O00O00OO0O0O0O00O  = 71.0
            O0O0O0000OO0OO000  = OO0OOOO00O0OOO0O0  / (O00O00OO0O0O0O00O  * OO0OO00O000OO00OO ) * 1000
            OO0OOO00O00OOO0O0 ['LNGV_U'] = O0O0O0000OO0OO000 
            O000OO00O0OOO00O0  = 183.8
            O0000OOO0OOO0OO00 .cursor.execute('select "Value" from public."Output_Tags" where "TagName" = \'LNGV_fouling_factor\';')
            OOOO00O0O00000O0O  = O0000OOO0OOO0OO00 .cursor.fetchall()
            O0000OOO0OOO0OO00 .conn.commit()
            O0OO00O0OO000O00O  = OOOO00O0O00000O0O [0][0]
            if OOOOO00OOO0O0O00O ['FG_Flow_VaprToAtm'] > 20000:
                O00OO0OOO0O00O000  = 1 / O0O0O0000OO0OO000  - 1 / O000OO00O0OOO00O0 
                O00OO0OOO0O00O000  = (1 - O00OO0OOO0O00O000 ) * 100
            elif O0OO00O0OO000O00O  < 100.0:
                O00OO0OOO0O00O000  = O0OO00O0OO000O00O 
            else:
                O00OO0OOO0O00O000  = 100
            OO0OOO00O00OOO0O0 ['LNGV_fouling_factor'] = O00OO0OOO0O00O000 
            O0O0OO00OOOOO0000  = O00OO000OO00OO0O0 .GetMassEnthalpy()
            OO0OOO00O00OOO0O0 ['LNGV_cold_in_specific_enthalpy'] = O0O0OO00OOOOO0000 
            O0000OOO000000OO0  = OO000O0OO0O0OOO0O .GetMassEnthalpy()
            OO0OOO00O00OOO0O0 ['LNGV_cold_out_specific_enthalpy'] = O0000OOO000000OO0 
            O0OO0OO00OO00OO00  = OO0OOOOO0O000OO0O  - OOO00OOO0O0OOO0O0 
            OO0OOO00O00OOO0O0 ['LNGV_cold_temp_rise'] = O0OO0OO00OO00OO00 
            O0OO0O00000OOOOOO  = OOO00OO00O0OO00O0  - OO0OOOOO0O000OO0O 
            OO0OOO00O00OOO0O0 ['LNGV_minimum_approach'] = O0OO0O00000OOOOOO 
            OO0OO00OO000OO0O0  = O000O00000000OOOO .GetMassFlow() * 3600
            OO0OOO00O00OOO0O0 ['LNGV_steam_required'] = OO0OO00OO000OO0O0 
            O00OOO000OO00OOOO  = O00OO000OO00OO0O0 .GetEnergyFlow()
            OO0OOO00O00OOO0O0 ['LNGV_cold_in_energy_flow'] = O00OOO000OO00OOOO 
            OO0O000O0O0000OOO  = OO000O0OO0O0OOO0O .GetEnergyFlow()
            OO0OOO00O00OOO0O0 ['LNGV_cold_out_energy_flow'] = OO0O000O0O0000OOO 
            for key in OO0OOO00O00OOO0O0 .keys():
                OO0OOO00O00OOO0O0 [key] = float('{0:.2f}'.format(OO0OOO00O00OOO0O0 [key]))
        if OOO0000O00000OOOO ['BOGH'] == 1:
            print('starting dwsim BOGH')
            OOOOO0OOO0OOO0OOO  = O0000OOO0OOO0OO00 .sim4.GetFlowsheetSimulationObject('BOGH_cold_in').GetAsObject()
            OO000OOO00OO00OO0  = O0000OOO0OOO0OO00 .sim4.GetFlowsheetSimulationObject('BOGH_cold_out').GetAsObject()
            OO0000OO0O0OO0OOO  = O0000OOO0OOO0OO00 .sim4.GetFlowsheetSimulationObject('BOGH_HT_1').GetAsObject()
            OOO000OO0O0OO0O00  = O0000OOO0OOO0OO00 .sim4.GetFlowsheetSimulationObject('BOGH_stm_in').GetAsObject()
            OOOOOO0O0000OO0OO  = O0000OOO0OOO0OO00 .sim4.GetFlowsheetSimulationObject('BOGH_stm_out').GetAsObject()
            OOOOO0OOO0OOO0OOO .SetTemperature(OOOOO00OOO0O0O00O ['FG_FV_OutTempInd'] + 273.15)
            OOOOO0OOO0OOO0OOO .SetPressure(OOOOO00OOO0O0O00O ['FG_FV_OutPrs'] * 1000.0)
            OOOOO0OOO0OOO0OOO .SetMassFlow(OOOOO00OOO0O0O00O ['FG_FV_DischFlow'] / 3600.0)
            OO0000OO0O0OO0OOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['FG_FBOG_BogHtr_OutTempInd'] + 273.15)
            OO0OOO000O0OOO000  = OOOOO00OOO0O0O00O ['FG_FV_OutPrs'] - OOOOO00OOO0O0O00O ['FG_FBOG_BogHtr_OutPrs']
            OO0000OO0O0OO0OOO .set_DeltaP(OO0OOO000O0OOO000  * 1000.0)
            OOO000OO0O0OO0O00 .SetTemperature(OOOOO00OOO0O0O00O ['FG_FBOG_BogHtr_CondWtrTempInd'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim4)
            OOOO00OO0000O000O  = {}
            O0O0O0OO0OOO0O000  = OOOOO0OOO0OOO0OOO .GetTemperature() - 273.15
            O00O0OO000OOOO0O0  = OOOOO0OOO0OOO0OOO .GetPressure() / 1000.0
            OOOO00OO0000O000O ['BOGH_cold_in_temp'] = O0O0O0OO0OOO0O000 
            OOOO00OO0000O000O ['BOGH_cold_in_pres'] = O00O0OO000OOOO0O0 
            O0000O0O0O0OOO0OO  = OOOOO0OOO0OOO0OOO .GetMassFlow() * 3600.0
            OOOO00OO0000O000O ['BOGH_mass_flow'] = O0000O0O0O0OOO0OO 
            O0OOO0000000000OO  = OO000OOO00OO00OO0 .GetTemperature() - 273.15
            OOOOOOO00O0OOOO0O  = OO000OOO00OO00OO0 .GetPressure() / 1000.0
            OOOO00OO0000O000O ['BOGH_cold_out_temp'] = O0OOO0000000000OO 
            OOOO00OO0000O000O ['BOGH_cold_out_pres'] = OOOOOOO00O0OOOO0O 
            O0OOOOOO0O000OOOO  = OOO000OO0O0OO0O00 .GetTemperature() - 273.15
            O0OO000OO00OOOO00  = O0OOOOOO0O000OOOO 
            OOOO00OO0000O000O ['BOGH_stm_in_temp'] = O0OOOOOO0O000OOOO 
            OOOO00OO0000O000O ['BOGH_stm_out_temp'] = O0OO000OO00OOOO00 
            O0OOOOOO0OOOO0O0O  = abs(OO0000OO0O0OO0OOO .GetPowerGeneratedOrConsumed())
            O00OO00O0OOOOO0OO ['BOGH_Qc'] = O0OOOOOO0OOOO0O0O 
            O0000O0OO00O0OOOO  = (O0OOOOOO0O000OOOO  - O0OOO0000000000OO  - (O0OO000OO00OOOO00  - O0O0O0OO0OOO0O000 )) / np.log((O0OOOOOO0O000OOOO  - O0OOO0000000000OO ) / (O0OO000OO00OOOO00  - O0O0O0OO0OOO0O000 ))
            O00OO00O0OOOOO0OO ['BOGH_LMTD'] = O0000O0OO00O0OOOO 
            O0O0OOOOO0OO0O00O  = 15.5
            OO0OOOOOO0O0O00OO  = O0OOOOOO0OOOO0O0O  / (O0O0OOOOO0OO0O00O  * O0000O0OO00O0OOOO ) * 1000
            O00OO00O0OOOOO0OO ['BOGH_U'] = OO0OOOOOO0O0O00OO 
            O0000O000O0OOOOOO  = 145.0
            O0000OOO0OOO0OO00 .cursor.execute('select "Value" from public."Output_Tags" where "TagName" = \'BOGH_fouling_factor\';')
            OOOO00O0O00000O0O  = O0000OOO0OOO0OO00 .cursor.fetchall()
            O0000OOO0OOO0OO00 .conn.commit()
            O0OO00O0OO000O00O  = OOOO00O0O00000O0O [0][0]
            if OOOOO00OOO0O0O00O ['FG_FV_DischFlow'] > 2500:
                O00000000OOO0OOO0  = 1 / OO0OOOOOO0O0O00OO  - 1 / O0000O000O0OOOOOO 
                O00000000OOO0OOO0  = (1 - O00000000OOO0OOO0 ) * 100
            elif O0OO00O0OO000O00O  < 100.0:
                O00000000OOO0OOO0  = O0OO00O0OO000O00O 
            else:
                O00000000OOO0OOO0  = 100
            O00OO00O0OOOOO0OO ['BOGH_fouling_factor'] = O00000000OOO0OOO0 
            O0000OO0O0O0000OO  = OOOOO0OOO0OOO0OOO .GetMassEnthalpy()
            O00OO00O0OOOOO0OO ['BOGH_cold_in_specific_enthalpy'] = O0000OO0O0O0000OO 
            OO0O0O0OOOO00O000  = OO000OOO00OO00OO0 .GetMassEnthalpy()
            O00OO00O0OOOOO0OO ['BOGH_cold_out_specific_enthalpy'] = OO0O0O0OOOO00O000 
            O0O00OO00OOO0OOOO  = O0OOO0000000000OO  - O0O0O0OO0OOO0O000 
            O00OO00O0OOOOO0OO ['BOGH_cold_temp_rise'] = O0O00OO00OOO0OOOO 
            O00OO00O0O0O0000O  = O0OOOOOO0O000OOOO  - O0OOO0000000000OO 
            O00OO00O0OOOOO0OO ['BOGH_minimum_approach'] = O00OO00O0O0O0000O 
            O00O000O0OO0OO0O0  = OOO000OO0O0OO0O00 .GetMassFlow() * 3600
            O00OO00O0OOOOO0OO ['BOGH_steam_required'] = O00O000O0OO0OO0O0 
            OO0O0OOO000OO0000  = OOOOO0OOO0OOO0OOO .GetEnergyFlow()
            O00OO00O0OOOOO0OO ['BOGH_cold_in_energy_flow'] = OO0O0OOO000OO0000 
            O000OOO00OOOOOOO0  = OO000OOO00OO00OO0 .GetEnergyFlow()
            O00OO00O0OOOOO0OO ['BOGH_cold_out_energy_flow'] = O000OOO00OOOOOOO0 
            for key in O00OO00O0OOOOO0OO .keys():
                O00OO00O0OOOOO0OO [key] = float('{0:.2f}'.format(O00OO00O0OOOOO0OO [key]))
        if OOO0000O00000OOOO ['WUH'] == 1:
            print('starting dwsim WUH')
            O0O00OOOOO000OOOO  = O0000OOO0OOO0OO00 .sim5.GetFlowsheetSimulationObject('WUH_cold_in').GetAsObject()
            OO0O000OO0OOOOO0O  = O0000OOO0OOO0OO00 .sim5.GetFlowsheetSimulationObject('WUH_cold_out').GetAsObject()
            OOO0O0O0OO0OOO000  = O0000OOO0OOO0OO00 .sim5.GetFlowsheetSimulationObject('WUH_HT_1').GetAsObject()
            OOOO0OOO0O0O0OOO0  = O0000OOO0OOO0OO00 .sim5.GetFlowsheetSimulationObject('WUH_stm_in').GetAsObject()
            O0O0O0OO00O00OO00  = O0000OOO0OOO0OO00 .sim5.GetFlowsheetSimulationObject('WUH_stm_out').GetAsObject()
            O0O00OOOOO000OOOO .SetTemperature(OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_InTempInd'] + 273.15)
            O0O00OOOOO000OOOO .SetPressure(OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_InPrs'] * 1000.0)
            OOO0O0O0OO0OOO000 .set_OutletTemperature(OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_OutTempInd'] + 273.15)
            O000OOOO000OO000O  = OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_InPrs'] - OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_OutPrs']
            OOO0O0O0OO0OOO000 .set_DeltaP(O000OOOO000OO000O  * 1000.0)
            OOOO0OOO0O0O0OOO0 .SetTemperature(OOOOO00OOO0O0O00O ['FG_FBOG_WuHtr_CondWtrTempInd'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim5)
            O00OO00O00O0O0O00  = {}
            OOO0O00OO00OO00OO  = O0O00OOOOO000OOOO .GetTemperature() - 273.15
            OO0O00O00O00OOO00  = O0O00OOOOO000OOOO .GetPressure() / 1000.0
            O00OO00O00O0O0O00 ['WUH_cold_in_temp'] = OOO0O00OO00OO00OO 
            O00OO00O00O0O0O00 ['WUH_cold_in_pres'] = OO0O00O00O00OOO00 
            OO00000000O00O0O0  = O0O00OOOOO000OOOO .GetMassFlow() * 3600.0
            O00OO00O00O0O0O00 ['WUH_mass_flow'] = OO00000000O00O0O0 
            OOOOOO0OOOOO0O000  = OO0O000OO0OOOOO0O .GetTemperature() - 273.15
            OOO0O00O00O0O0O0O  = OO0O000OO0OOOOO0O .GetPressure() / 1000.0
            O00OO00O00O0O0O00 ['WUH_cold_out_temp'] = OOOOOO0OOOOO0O000 
            O00OO00O00O0O0O00 ['WUH_cold_out_pres'] = OOO0O00O00O0O0O0O 
            OOOOOO0OO0000OO0O  = OOOO0OOO0O0O0OOO0 .GetTemperature() - 273.15
            OO0000OO00OO0OOO0  = OOOOOO0OO0000OO0O 
            O00OO00O00O0O0O00 ['WUH_stm_in_temp'] = OOOOOO0OO0000OO0O 
            O00OO00O00O0O0O00 ['WUH_stm_out_temp'] = OO0000OO00OO0OOO0 
            O0OOOO0OOO00O0000  = abs(OOO0O0O0OO0OOO000 .GetPowerGeneratedOrConsumed())
            OO0O0O00O00O00O00 ['WUH_Qc'] = O0OOOO0OOO00O0000 
            O0O0OO000O00O00OO  = (OOOOOO0OO0000OO0O  - OOOOOO0OOOOO0O000  - (OO0000OO00OO0OOO0  - OOO0O00OO00OO00OO )) / np.log((OOOOOO0OO0000OO0O  - OOOOOO0OOOOO0O000 ) / (OO0000OO00OO0OOO0  - OOO0O00OO00OO00OO ))
            OO0O0O00O00O00O00 ['WUH_LMTD'] = O0O0OO000O00O00OO 
            OO0O0O0O0OOO0O000  = 38.2
            OO0OOOO00OOOO00OO  = O0OOOO0OOO00O0000  / (OO0O0O0O0OOO0O000  * O0O0OO000O00O00OO ) * 1000
            OO0O0O00O00O00O00 ['WUH_U'] = OO0OOOO00OOOO00OO 
            O0OO00O00000O00O0  = 394.6
            O0OOOOO0O0O000OO0  = 100
            OO0O0O00O00O00O00 ['WUH_fouling_factor'] = O0OOOOO0O0O000OO0 
            OO000OOOOO0OOOOOO  = O0O00OOOOO000OOOO .GetMassEnthalpy()
            OO0O0O00O00O00O00 ['WUH_cold_in_specific_enthalpy'] = OO000OOOOO0OOOOOO 
            OOOO00OOOO0OO000O  = OO0O000OO0OOOOO0O .GetMassEnthalpy()
            OO0O0O00O00O00O00 ['WUH_cold_out_specific_enthalpy'] = OOOO00OOOO0OO000O 
            O00O00OOOO00OO0O0  = OOOOOO0OOOOO0O000  - OOO0O00OO00OO00OO 
            OO0O0O00O00O00O00 ['WUH_cold_temp_rise'] = O00O00OOOO00OO0O0 
            OO0O0O00OOOOOOO00  = OOOOOO0OO0000OO0O  - OOOOOO0OOOOO0O000 
            OO0O0O00O00O00O00 ['WUH_minimum_approach'] = OO0O0O00OOOOOOO00 
            O00OOOOOO000OOO0O  = OOOO0OOO0O0O0OOO0 .GetMassFlow() * 3600
            OO0O0O00O00O00O00 ['WUH_steam_required'] = O00OOOOOO000OOO0O 
            OO000000O000O0OOO  = O0O00OOOOO000OOOO .GetEnergyFlow()
            OO0O0O00O00O00O00 ['WUH_cold_in_energy_flow'] = OO000000O000O0OOO 
            OO00O0O0O0O00O0OO  = OO0O000OO0OOOOO0O .GetEnergyFlow()
            OO0O0O00O00O00O00 ['WUH_cold_out_energy_flow'] = OO00O0O0O0O00O0OO 
            for key in OO0O0O00O00O00O00 .keys():
                OO0O0O00O00O00O00 [key] = float('{0:.2f}'.format(OO0O0O00O00O00O00 [key]))
        if OOO0000O00000OOOO ['GWH_Stm'] == 1:
            print('starting dwsim GWH_Stm')
            O0O0000O000OO0OOO  = O0000OOO0OOO0OO00 .sim6.GetFlowsheetSimulationObject('GWHS_cold_in').GetAsObject()
            O000O0O0O0OO0OO00  = O0000OOO0OOO0OO00 .sim6.GetFlowsheetSimulationObject('GWHS_cold_out').GetAsObject()
            OO0O0OOOO0000OO0O  = O0000OOO0OOO0OO00 .sim6.GetFlowsheetSimulationObject('GWHS_HT_1').GetAsObject()
            OOO00OOO0OOO00O0O  = O0000OOO0OOO0OO00 .sim6.GetFlowsheetSimulationObject('GWHS_stm_in').GetAsObject()
            O0O0OOOO0OO0OOO00  = O0000OOO0OOO0OO00 .sim6.GetFlowsheetSimulationObject('GWHS_stm_out').GetAsObject()
            O0O0000O000OO0OOO .SetTemperature(OOOOO00OOO0O0O00O ['FG_GW_MainHtr_RtnTemp'] + 273.15)
            O0O0000O000OO0OOO .SetPressure(OOOOO00OOO0O0O00O ['FG_GW_MainHtr_InPrs'] * 1000.0)
            OO0O0OOOO0000OO0O .set_OutletTemperature(OOOOO00OOO0O0O00O ['FG_GW_MainHtr_OutTempCtrl'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim6)
            OOO0OO0OO0O0O00OO  = {}
            O00OOOO00OOOOO0O0  = O0O0000O000OO0OOO .GetTemperature() - 273.15
            OOOOOOO0O00OOO0O0  = O0O0000O000OO0OOO .GetPressure() / 1000.0
            OOO0OO0OO0O0O00OO ['GWHS_cold_in_temp'] = O00OOOO00OOOOO0O0 
            OOO0OO0OO0O0O00OO ['GWHS_cold_in_pres'] = OOOOOOO0O00OOO0O0 
            O0OO000OO0OOOOO0O  = O0O0000O000OO0OOO .GetMassFlow() * 3600.0
            OOO0OO0OO0O0O00OO ['GWHS_mass_flow'] = O0OO000OO0OOOOO0O 
            O00O000OOOO00OOOO  = O000O0O0O0OO0OO00 .GetTemperature() - 273.15
            O0O0O0OOO0O0O0O00  = O000O0O0O0OO0OO00 .GetPressure() / 1000.0
            OOO0OO0OO0O0O00OO ['GWHS_cold_out_temp'] = O00O000OOOO00OOOO 
            OOO0OO0OO0O0O00OO ['GWHS_cold_out_pres'] = O0O0O0OOO0O0O0O00 
            OO00O00O00O0OO0O0  = OOO00OOO0OOO00O0O .GetTemperature() - 273.15
            O0OO00OO0OOO0OOO0  = O0O0OOOO0OO0OOO00 .GetTemperature() - 273.15
            O0OO00OO0OOO0OOO0  = OO00O00O00O0OO0O0 
            OOO0OO0OO0O0O00OO ['GWHS_stm_in_temp'] = OO00O00O00O0OO0O0 
            OOO0OO0OO0O0O00OO ['GWHS_stm_out_temp'] = O0OO00OO0OOO0OOO0 
            OOOO00OOO0000O0OO  = abs(OO0O0OOOO0000OO0O .GetPowerGeneratedOrConsumed())
            OOOOOO0O0O0O0O0OO ['GWHS_Qc'] = OOOO00OOO0000O0OO 
            O000OOO0O0OOOO000  = (OO00O00O00O0OO0O0  - O00O000OOOO00OOOO  - (O0OO00OO0OOO0OOO0  - O00OOOO00OOOOO0O0 )) / np.log((OO00O00O00O0OO0O0  - O00O000OOOO00OOOO ) / (O0OO00OO0OOO0OOO0  - O00OOOO00OOOOO0O0 ))
            OOOOOO0O0O0O0O0OO ['GWHS_LMTD'] = O000OOO0O0OOOO000 
            OOO00OO00O0O00O00  = 4.59
            O00O000O000000OO0  = OOOO00OOO0000O0OO  / (OOO00OO00O0O00O00  * O000OOO0O0OOOO000 ) * 1000
            OOOOOO0O0O0O0O0OO ['GWHS_U'] = O00O000O000000OO0 
            OO0OO0O0000OOOO0O  = 3375.8
            OOOOOOO00OO0OOO0O  = 100
            OOOOOO0O0O0O0O0OO ['GWHS_fouling_factor'] = OOOOOOO00OO0OOO0O 
            OOO0OOO00OOOO0000  = O0O0000O000OO0OOO .GetMassEnthalpy()
            OOOOOO0O0O0O0O0OO ['GWHS_cold_in_specific_enthalpy'] = OOO0OOO00OOOO0000 
            OOO0OOO0O0000OOO0  = O000O0O0O0OO0OO00 .GetMassEnthalpy()
            OOOOOO0O0O0O0O0OO ['GWHS_cold_out_specific_enthalpy'] = OOO0OOO0O0000OOO0 
            OOOO0O0O000OOOO00  = O00O000OOOO00OOOO  - O00OOOO00OOOOO0O0 
            OOOOOO0O0O0O0O0OO ['GWHS_cold_temp_rise'] = OOOO0O0O000OOOO00 
            OO0O000000000OOO0  = OO00O00O00O0OO0O0  - O00O000OOOO00OOOO 
            OOOOOO0O0O0O0O0OO ['GWHS_minimum_approach'] = OO0O000000000OOO0 
            OOOOOOOO0OO00O000  = OOO00OOO0OOO00O0O .GetMassFlow() * 3600
            OOOOOO0O0O0O0O0OO ['GWHS_steam_required'] = OOOOOOOO0OO00O000 
            O000OO0OO000O0O0O  = O0O0000O000OO0OOO .GetEnergyFlow()
            OOOOOO0O0O0O0O0OO ['GWHS_cold_in_energy_flow'] = O000OO0OO000O0O0O 
            O00OOO0000O000O0O  = O000O0O0O0OO0OO00 .GetEnergyFlow()
            OOOOOO0O0O0O0O0OO ['GWHS_cold_out_energy_flow'] = O00OOO0000O000O0O 
            for key in OOOOOO0O0O0O0O0OO .keys():
                OOOOOO0O0O0O0O0OO [key] = float('{0:.2f}'.format(OOOOOO0O0O0O0O0OO [key]))
        if OOO0000O00000OOOO ['LD1'] == 1:
            print('starting dwsim LD1')
            OO000O00OOO0000OO  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S1_in').GetAsObject()
            OO00O000OO000OOOO  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S1').GetAsObject()
            O0OO000OO0000O00O  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S1_out_ideal').GetAsObject()
            O0000O0OO0OO00OO0  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S1_out_actual').GetAsObject()
            OO0O0OO0OOO00OO0O  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_interclr').GetAsObject()
            OOOO0OOO0O000OOO0  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S2_in').GetAsObject()
            OOOO0O0O0OOOOO0O0  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S2').GetAsObject()
            OOO000OOOOOO00O0O  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S2_out_ideal').GetAsObject()
            OO0OO00000000O0OO  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_S2_out_actual').GetAsObject()
            O0O000O0O0O00O0OO  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_afterclr').GetAsObject()
            O0O0000O0OOO0OO00  = O0000OOO0OOO0OO00 .sim7.GetFlowsheetSimulationObject('LD1_out').GetAsObject()
            OO000O00OOO0000OO .SetPressure(OOOOO00OOO0O0O00O ['CM_LD1_CtrlPrs'] * 1000.0)
            OO000O00OOO0000OO .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD1_CtrlTemp'] + 273.15)
            OO000O00OOO0000OO .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD1_Flow'] / 3600.0)
            O0000O0OO0OO00OO0 .SetPressure(OOOOO00OOO0O0O00O ['CM_LD1_Stage2InPrs'] * 1000.0)
            O0000O0OO0OO00OO0 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD1_Stage1DischAlrmTemp'] + 273.15)
            O0000O0OO0OO00OO0 .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD1_Flow'] / 3600.0)
            OO00O000OO000OOOO .set_POut(OOOOO00OOO0O0O00O ['CM_LD1_Stage2InPrs'] * 1000.0)
            OO0O0OO0OOO00OO0O .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LD1_Stage2InTemp'] + 273.15)
            OOOO0O0O0OOOOO0O0 .set_POut(OOOOO00OOO0O0O00O ['CM_LD1_Stage2DischAlrmCtrlPrs'] * 1000.0)
            OO0OO00000000O0OO .SetPressure(OOOOO00OOO0O0O00O ['CM_LD1_Stage2DischAlrmCtrlPrs'] * 1000.0)
            OO0OO00000000O0OO .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD1_Stage2DischAlrmTemp'] + 273.15)
            OO0OO00000000O0OO .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD1_Flow'] / 3600.0)
            O0O000O0O0O00O0OO .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LD1_DischTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim7)
            OO0000O000O0OOO00  = {}
            OO0OO0OOOO0O0O0OO  = OO000O00OOO0000OO .GetPressure() / 1000.0
            OO0000O000O0OOO00 ['LD1_S1_in_pres'] = OO0OO0OOOO0O0O0OO 
            O000OO0000OOOOOOO  = OO000O00OOO0000OO .GetTemperature() - 273.15
            OO0000O000O0OOO00 ['LD1_S1_in_temp'] = O000OO0000OOOOOOO 
            OO0OO0O0OOOO00000  = OO000O00OOO0000OO .GetMassFlow() * 3600.0
            OO0000O000O0OOO00 ['LD1_mass_flow'] = OO0OO0O0OOOO00000 
            OOOO000O0O0OOOO00  = O0OO000OO0000O00O .GetPressure() / 1000.0
            OO0000O000O0OOO00 ['LD1_S1_out_pres'] = OOOO000O0O0OOOO00 
            OO0O000O0OO0OO00O  = O0000O0OO0OO00OO0 .GetTemperature() - 273.15
            OO0000O000O0OOO00 ['LD1_S1_out_temp'] = OO0O000O0OO0OO00O 
            O00O000000O0OOOOO  = OOOO0OOO0O000OOO0 .GetPressure() / 1000.0
            OO0000O000O0OOO00 ['LD1_S2_in_pres'] = O00O000000O0OOOOO 
            OOO00O0000OOOO0O0  = OOOO0OOO0O000OOO0 .GetTemperature() - 273.15
            OO0000O000O0OOO00 ['LD1_S2_in_temp'] = OOO00O0000OOOO0O0 
            O00OOOOOO0O0000O0  = OOO000OOOOOO00O0O .GetPressure() / 1000.0
            OO0000O000O0OOO00 ['LD1_S2_out_pres'] = O00OOOOOO0O0000O0 
            OOO00O0OO00OOO00O  = OO0OO00000000O0OO .GetTemperature() - 273.15
            OO0000O000O0OOO00 ['LD1_S2_out_temp'] = OOO00O0OO00OOO00O 
            O00O00OOO00O0OOOO  = O0O0000O0OOO0OO00 .GetTemperature() - 273.15
            OO0000O000O0OOO00 ['LD1_out_temp'] = O00O00OOO00O0OOOO 
            O00000O0OO000O0OO  = OO000O00OOO0000OO .GetMassEnthalpy()
            O0OO000OOO0000O00 ['LD1_S1_in_specific_enthalpy'] = O00000O0OO000O0OO 
            OO0OOOO0OOO000OO0  = OOOO000O0O0OOOO00  / OO0OO0OOOO0O0O0OO 
            O0OO000OOO0000O00 ['LD1_S1_pressure_ratio'] = OO0OOOO0OOO000OO0 
            O000OO00O0O00OO0O  = abs(OO00O000OO000OOOO .GetPowerGeneratedOrConsumed())
            O0OO000OOO0000O00 ['LD1_S1_polytropic_power'] = O000OO00O0O00OO0O 
            OOO0OO00O0000OO0O  = OO00O000OO000OOOO .get_PolytropicHead()
            O0OO000OOO0000O00 ['LD1_S1_polytropic_head'] = OOO0OO00O0000OO0O 
            OO0OO0OOO0O000000  = O0OO000OO0000O00O .GetMassEnthalpy()
            O0O0O000OO000OOO0  = O0000O0OO0OO00OO0 .GetMassEnthalpy()
            O0OO000OOO0000O00 ['LD1_S1_out_actual_specific_enthalpy'] = O0O0O000OO000OOO0 
            O000OOO0O0O00O000  = OO0OO0OOO0O000000  - O00000O0OO000O0OO 
            OOOO0000OO000O0OO  = O0O0O000OO000OOO0  - O00000O0OO000O0OO 
            O0OO000OOO0000O00 ['LD1_S1_actual_ethalpy_change'] = OOOO0000OO000O0OO 
            if OOOO0000OO000O0OO  == 0:
                OOOO0000OO000O0OO  = 1
            O00O0O00OOOOO00OO  = O000OOO0O0O00O000  / OOOO0000OO000O0OO  * 100
            O0OO000OOO0000O00 ['LD1_S1_polytropic_efficiency'] = O00O0O00OOOOO00OO 
            O0OOO00OO0O000000  = OO0O0OO0OOO00OO0O .get_DeltaT()
            O0OO000OOO0000O00 ['LD1_interclr_deltaT'] = O0OOO00OO0O000000 
            O0OOOO00OOO0OO0OO  = OO0O0OO0OOO00OO0O .GetPowerGeneratedOrConsumed()
            O0OO000OOO0000O00 ['LD1_interclr_duty'] = O0OOOO00OOO0OO0OO 
            O0O000OOO00O0O000  = OOOO0OOO0O000OOO0 .GetMassEnthalpy()
            O0OO000OOO0000O00 ['LD1_S2_in_specific_enthalpy'] = O0O000OOO00O0O000 
            O0000OOO00000OOO0  = O00OOOOOO0O0000O0  / O00O000000O0OOOOO 
            O0OO000OOO0000O00 ['LD1_S2_pressure_ratio'] = O0000OOO00000OOO0 
            O0OO000OO00OO00OO  = abs(OOOO0O0O0OOOOO0O0 .GetPowerGeneratedOrConsumed())
            O0OO000OOO0000O00 ['LD1_S2_polytropic_power'] = O0OO000OO00OO00OO 
            OOOOOO00O00OO0000  = OOOO0O0O0OOOOO0O0 .get_PolytropicHead()
            O0OO000OOO0000O00 ['LD1_S2_polytropic_head'] = OOOOOO00O00OO0000 
            O0O0000O0O0000OO0  = OOO000OOOOOO00O0O .GetMassEnthalpy()
            O0O00OOOO0000OOO0  = OO0OO00000000O0OO .GetMassEnthalpy()
            O0OO000OOO0000O00 ['LD1_S2_out_actual_specific_enthalpy'] = O0O00OOOO0000OOO0 
            OO000000O0O0O0O00  = O0O0000O0O0000OO0  - O0O000OOO00O0O000 
            O000OOO0O0000OO0O  = O0O00OOOO0000OOO0  - O0O000OOO00O0O000 
            O0OO000OOO0000O00 ['LD1_S2_actual_ethalpy_change'] = O000OOO0O0000OO0O 
            if O000OOO0O0000OO0O  == 0:
                O000OOO0O0000OO0O  = 1
            O00O0O0OO00OOOOO0  = OO000000O0O0O0O00  / O000OOO0O0000OO0O  * 100
            O0OO000OOO0000O00 ['LD1_S2_polytropic_efficiency'] = O00O0O0OO00OOOOO0 
            OO00OOOO0OOO0O00O  = O0O000O0O0O00O0OO .get_DeltaT()
            O0OO000OOO0000O00 ['LD1_afterclr_deltaT'] = OO00OOOO0OOO0O00O 
            O00OO0OOOOO00OO0O  = O0O000O0O0O00O0OO .GetPowerGeneratedOrConsumed()
            O0OO000OOO0000O00 ['LD1_afterclr_duty'] = O00OO0OOOOO00OO0O 
            O0O0O0000OOOO0OOO  = O0O0000O0OOO0OO00 .GetMassEnthalpy()
            O0OO000OOO0000O00 ['LD1_out_specific_enthalpy'] = O0O0O0000OOOO0OOO 
            O0OO000OOO0000O00 ['LD1_polytropic_efficiency'] = (O00O0O00OOOOO00OO  + O00O0O0OO00OOOOO0 ) / 2
            for key in O0OO000OOO0000O00 .keys():
                O0OO000OOO0000O00 [key] = float('{0:.2f}'.format(O0OO000OOO0000O00 [key]))
        if OOO0000O00000OOOO ['LD2'] == 1:
            print('starting dwsim LD2')
            OO000OOOOO0OO0000  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S1_in').GetAsObject()
            OO00O0000O0OO00O0  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S1').GetAsObject()
            O00000OO0O000O00O  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S1_out_ideal').GetAsObject()
            OO000O0000000O0O0  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S1_out_actual').GetAsObject()
            OO0O000OO0O00OO0O  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_interclr').GetAsObject()
            OOO000O0O000OO00O  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S2_in').GetAsObject()
            O0OO00OOO0O0OO000  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S2').GetAsObject()
            O0OO000000OO00OO0  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S2_out_ideal').GetAsObject()
            OOO0O000000OOOOO0  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_S2_out_actual').GetAsObject()
            OOO0OOO0O000O0OOO  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_afterclr').GetAsObject()
            O00O00O00000O0000  = O0000OOO0OOO0OO00 .sim8.GetFlowsheetSimulationObject('LD2_out').GetAsObject()
            OO000OOOOO0OO0000 .SetPressure(OOOOO00OOO0O0O00O ['CM_LD2_CtrlPrs'] * 1000.0)
            OO000OOOOO0OO0000 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD2_CtrlTemp'] + 273.15)
            OO000OOOOO0OO0000 .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD2_Flow'] / 3600.0)
            OO000O0000000O0O0 .SetPressure(OOOOO00OOO0O0O00O ['CM_LD2_Stage2InPrs'] * 1000.0)
            OO000O0000000O0O0 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD2_Stage1DischAlrmTemp'] + 273.15)
            OO000O0000000O0O0 .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD2_Flow'] / 3600.0)
            OO00O0000O0OO00O0 .set_POut(OOOOO00OOO0O0O00O ['CM_LD2_Stage2InPrs'] * 1000.0)
            OO0O000OO0O00OO0O .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LD2_Stage2InTemp'] + 273.15)
            O0OO00OOO0O0OO000 .set_POut(OOOOO00OOO0O0O00O ['CM_LD2_Stage2DischAlrmCtrlPrs'] * 1000.0)
            OOO0O000000OOOOO0 .SetPressure(OOOOO00OOO0O0O00O ['CM_LD2_Stage2DischAlrmCtrlPrs'] * 1000.0)
            OOO0O000000OOOOO0 .SetTemperature(OOOOO00OOO0O0O00O ['CM_LD2_Stage2DischAlrmTemp'] + 273.15)
            OOO0O000000OOOOO0 .SetMassFlow(OOOOO00OOO0O0O00O ['CM_LD2_Flow'] / 3600.0)
            OOO0OOO0O000O0OOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['CM_LD2_DischTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim8)
            OOOO00O0O0O0OO000  = {}
            OO00O0O00OO00000O  = OO000OOOOO0OO0000 .GetPressure() / 1000.0
            OOOO00O0O0O0OO000 ['LD2_S1_in_pres'] = OO00O0O00OO00000O 
            OO0O0OOO0OO00OO00  = OO000OOOOO0OO0000 .GetTemperature() - 273.15
            OOOO00O0O0O0OO000 ['LD2_S1_in_temp'] = OO0O0OOO0OO00OO00 
            O0O0000O00O0000O0  = OO000OOOOO0OO0000 .GetMassFlow() * 3600.0
            OOOO00O0O0O0OO000 ['LD2_mass_flow'] = O0O0000O00O0000O0 
            OOO0OO00OO0OO0O00  = O00000OO0O000O00O .GetPressure() / 1000.0
            OOOO00O0O0O0OO000 ['LD2_S1_out_pres'] = OOO0OO00OO0OO0O00 
            O0000O0OOO000O0OO  = OO000O0000000O0O0 .GetTemperature() - 273.15
            OOOO00O0O0O0OO000 ['LD2_S1_out_temp'] = O0000O0OOO000O0OO 
            OO00OO000OO00O0OO  = OOO000O0O000OO00O .GetPressure() / 1000.0
            OOOO00O0O0O0OO000 ['LD2_S2_in_pres'] = OO00OO000OO00O0OO 
            OO0O00OO0O00O0000  = OOO000O0O000OO00O .GetTemperature() - 273.15
            OOOO00O0O0O0OO000 ['LD2_S2_in_temp'] = OO0O00OO0O00O0000 
            OO00000O0OOOO000O  = O0OO000000OO00OO0 .GetPressure() / 1000.0
            OOOO00O0O0O0OO000 ['LD2_S2_out_pres'] = OO00000O0OOOO000O 
            O0OO00O00OOOO0O00  = OOO0O000000OOOOO0 .GetTemperature() - 273.15
            OOOO00O0O0O0OO000 ['LD2_S2_out_temp'] = O0OO00O00OOOO0O00 
            O00OOO00O0O0OO00O  = O00O00O00000O0000 .GetTemperature() - 273.15
            OOOO00O0O0O0OO000 ['LD2_out_temp'] = O00OOO00O0O0OO00O 
            O0OO0OO0000OOOO00  = OO000OOOOO0OO0000 .GetMassEnthalpy()
            O00O0O00000O0O0OO ['LD2_S1_in_specific_enthalpy'] = O0OO0OO0000OOOO00 
            O00O0OO00O0000000  = OOO0OO00OO0OO0O00  / OO00O0O00OO00000O 
            O00O0O00000O0O0OO ['LD2_S1_pressure_ratio'] = O00O0OO00O0000000 
            O0O0OOOO00OO00OOO  = abs(OO00O0000O0OO00O0 .GetPowerGeneratedOrConsumed())
            O00O0O00000O0O0OO ['LD2_S1_polytropic_power'] = O0O0OOOO00OO00OOO 
            OOO00OOO00O000O0O  = OO00O0000O0OO00O0 .get_PolytropicHead()
            O00O0O00000O0O0OO ['LD2_S1_polytropic_head'] = OOO00OOO00O000O0O 
            OO00OOOOOO0OO00OO  = O00000OO0O000O00O .GetMassEnthalpy()
            O00O0O00O00OO0OOO  = OO000O0000000O0O0 .GetMassEnthalpy()
            O00O0O00000O0O0OO ['LD2_S1_out_actual_specific_enthalpy'] = O00O0O00O00OO0OOO 
            OO0O00O00O00O000O  = OO00OOOOOO0OO00OO  - O0OO0OO0000OOOO00 
            OO0O0000O000OO0OO  = O00O0O00O00OO0OOO  - O0OO0OO0000OOOO00 
            O00O0O00000O0O0OO ['LD2_S1_actual_ethalpy_change'] = OO0O0000O000OO0OO 
            if OO0O0000O000OO0OO  == 0:
                OO0O0000O000OO0OO  = 1
            O0OOOOO00O0OOOOOO  = OO0O00O00O00O000O  / OO0O0000O000OO0OO  * 100
            O00O0O00000O0O0OO ['LD2_S1_polytropic_efficiency'] = O0OOOOO00O0OOOOOO 
            OO0O0O0OOOO000000  = OO0O000OO0O00OO0O .get_DeltaT()
            O00O0O00000O0O0OO ['LD2_interclr_deltaT'] = OO0O0O0OOOO000000 
            OO0O00OO00O0OOOO0  = OO0O000OO0O00OO0O .GetPowerGeneratedOrConsumed()
            O00O0O00000O0O0OO ['LD2_interclr_duty'] = OO0O00OO00O0OOOO0 
            OO0000OO00O000O00  = OOO000O0O000OO00O .GetMassEnthalpy()
            O00O0O00000O0O0OO ['LD2_S2_in_specific_enthalpy'] = OO0000OO00O000O00 
            OO00O00OOOOO0000O  = OO00000O0OOOO000O  / OO00OO000OO00O0OO 
            O00O0O00000O0O0OO ['LD2_S2_pressure_ratio'] = OO00O00OOOOO0000O 
            O000O0OO0O0OOOO0O  = abs(O0OO00OOO0O0OO000 .GetPowerGeneratedOrConsumed())
            O00O0O00000O0O0OO ['LD2_S2_polytropic_power'] = O000O0OO0O0OOOO0O 
            OOO00O0O00OOOO0OO  = O0OO00OOO0O0OO000 .get_PolytropicHead()
            O00O0O00000O0O0OO ['LD2_S2_polytropic_head'] = OOO00O0O00OOOO0OO 
            OOOO000O0O000O00O  = O0OO000000OO00OO0 .GetMassEnthalpy()
            OOOO0000O000OOO00  = OOO0O000000OOOOO0 .GetMassEnthalpy()
            O00O0O00000O0O0OO ['LD2_S2_out_actual_specific_enthalpy'] = OOOO0000O000OOO00 
            OO0O0OO00O0O00OO0  = OOOO000O0O000O00O  - OO0000OO00O000O00 
            OOOO00O0OOOOOO0OO  = OOOO0000O000OOO00  - OO0000OO00O000O00 
            O00O0O00000O0O0OO ['LD2_S2_actual_ethalpy_change'] = OOOO00O0OOOOOO0OO 
            if OOOO00O0OOOOOO0OO  == 0:
                OOOO00O0OOOOOO0OO  = 1
            O0OOOOOOO00000OO0  = OO0O0OO00O0O00OO0  / OOOO00O0OOOOOO0OO  * 100
            O00O0O00000O0O0OO ['LD2_S2_polytropic_efficiency'] = O0OOOOOOO00000OO0 
            OO00OOO0000O00OOO  = OOO0OOO0O000O0OOO .get_DeltaT()
            O00O0O00000O0O0OO ['LD2_afterclr_deltaT'] = OO00OOO0000O00OOO 
            O0OOOOOOO000OOOO0  = OOO0OOO0O000O0OOO .GetPowerGeneratedOrConsumed()
            O00O0O00000O0O0OO ['LD2_afterclr_duty'] = O0OOOOOOO000OOOO0 
            O00O00O00OO0O00O0  = O00O00O00000O0000 .GetMassEnthalpy()
            O00O0O00000O0O0OO ['LD2_out_specific_enthalpy'] = O00O00O00OO0O00O0 
            O00O0O00000O0O0OO ['LD2_polytropic_efficiency'] = (O0OOOOO00O0OOOOOO  + O0OOOOOOO00000OO0 ) / 2
            for key in O00O0O00000O0O0OO .keys():
                O00O0O00000O0O0OO [key] = float('{0:.2f}'.format(O00O0O00000O0O0OO [key]))
        if OOO0000O00000OOOO ['HD1'] == 1:
            print('starting dwsim HD1')
            OO0OOOOOO00000O00  = O0000OOO0OOO0OO00 .sim9.GetFlowsheetSimulationObject('HD1_in').GetAsObject()
            OOOO0000O0000O00O  = O0000OOO0OOO0OO00 .sim9.GetFlowsheetSimulationObject('HD1').GetAsObject()
            O0OOO0O00OO00O0O0  = O0000OOO0OOO0OO00 .sim9.GetFlowsheetSimulationObject('HD1_out_ideal').GetAsObject()
            O0OO0O00O0OO0OOOO  = O0000OOO0OOO0OO00 .sim9.GetFlowsheetSimulationObject('HD1_out_actual').GetAsObject()
            OO0OOOOOO00000O00 .SetPressure(OOOOO00OOO0O0O00O ['CM_HD1_InPrsAlrmCtrl'] * 1000.0)
            OO0OOOOOO00000O00 .SetTemperature(OOOOO00OOO0O0O00O ['CM_HD1_InTemp'] + 273.15)
            O0OO0O00O0OO0OOOO .SetPressure(OOOOO00OOO0O0O00O ['CM_HD1_DischPrs'] * 1000.0)
            O0OO0O00O0OO0OOOO .SetTemperature(OOOOO00OOO0O0O00O ['CM_HD1_CtrlTemp'] + 273.15)
            OOOO0000O0000O00O .set_POut(OOOOO00OOO0O0O00O ['CM_HD1_DischPrs'] * 1000.0)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim9)
            OOOOO00OO00O00O00  = {}
            OOO0O000OO0OOO00O  = OO0OOOOOO00000O00 .GetPressure() / 1000.0
            OOOOO00OO00O00O00 ['HD1_in_pres'] = OOO0O000OO0OOO00O 
            O0OOO000OOO0OOOO0  = OO0OOOOOO00000O00 .GetTemperature() - 273.15
            OOOOO00OO00O00O00 ['HD1_in_temp'] = O0OOO000OOO0OOOO0 
            O0000O00O00OOO0O0  = OO0OOOOOO00000O00 .GetMassFlow() * 3600.0
            OOOOO00OO00O00O00 ['HD1_mass_flow'] = O0000O00O00OOO0O0 
            OO0OO0O0OO0O00O00  = O0OOO0O00OO00O0O0 .GetPressure() / 1000.0
            OOOOO00OO00O00O00 ['HD1_out_pres'] = OO0OO0O0OO0O00O00 
            OO0OO00O0O0O000OO  = O0OO0O00O0OO0OOOO .GetTemperature() - 273.15
            OOOOO00OO00O00O00 ['HD1_out_temp'] = OO0OO00O0O0O000OO 
            OOOOOOO00OO0O00O0  = OO0OOOOOO00000O00 .GetMassEnthalpy()
            OOO0O0OOO0OOOO0OO ['HD1_in_specific_enthalpy'] = OOOOOOO00OO0O00O0 
            O0O00OO000000OO00  = OO0OO0O0OO0O00O00  / OOO0O000OO0OOO00O 
            OOO0O0OOO0OOOO0OO ['HD1_pressure_ratio'] = O0O00OO000000OO00 
            O00O0O00OO00OO0OO  = abs(OOOO0000O0000O00O .GetPowerGeneratedOrConsumed())
            OOO0O0OOO0OOOO0OO ['HD1_polytropic_power'] = O00O0O00OO00OO0OO 
            OOOOO0O0O0O00000O  = OOOO0000O0000O00O .get_PolytropicHead()
            OOO0O0OOO0OOOO0OO ['HD1_polytropic_head'] = OOOOO0O0O0O00000O 
            OOO000OO0000O0OO0  = O0OOO0O00OO00O0O0 .GetMassEnthalpy()
            OOO0O0OOO0OOOO0OO ['HD1_out_ideal_specific_enthalpy'] = OOO000OO0000O0OO0 
            O0OOO000OOOOOO0OO  = O0OO0O00O0OO0OOOO .GetMassEnthalpy()
            OOO0O0OOO0OOOO0OO ['HD1_out_actual_specific_enthalpy'] = O0OOO000OOOOOO0OO 
            O0000OO0000OO0O00  = OOO000OO0000O0OO0  - OOOOOOO00OO0O00O0 
            O0O0OOO0000OOO0OO  = O0OOO000OOOOOO0OO  - OOOOOOO00OO0O00O0 
            if O0O0OOO0000OOO0OO  == 0:
                O0O0OOO0000OOO0OO  = 1
            OO00OO00OOO0OOOOO  = O0000OO0000OO0O00  / O0O0OOO0000OOO0OO  * 100
            OOO0O0OOO0OOOO0OO ['HD1_polytropic_efficiency'] = OO00OO00OOO0OOOOO 
            for key in OOO0O0OOO0OOOO0OO .keys():
                OOO0O0OOO0OOOO0OO [key] = float('{0:.2f}'.format(OOO0O0OOO0OOOO0OO [key]))
        if OOO0000O00000OOOO ['HD2'] == 1:
            print('starting dwsim HD2')
            OOO0O0OOOOOOOOO00  = O0000OOO0OOO0OO00 .sim10.GetFlowsheetSimulationObject('HD2_in').GetAsObject()
            OOOOO0OO00OO0OO00  = O0000OOO0OOO0OO00 .sim10.GetFlowsheetSimulationObject('HD2').GetAsObject()
            OOOO00OO0OOO0O000  = O0000OOO0OOO0OO00 .sim10.GetFlowsheetSimulationObject('HD2_out_ideal').GetAsObject()
            O0O0OOO0OO000OOOO  = O0000OOO0OOO0OO00 .sim10.GetFlowsheetSimulationObject('HD2_out_actual').GetAsObject()
            OOO0O0OOOOOOOOO00 .SetPressure(OOOOO00OOO0O0O00O ['CM_HD2_InPrsAlrmCtrl'] * 1000.0)
            OOO0O0OOOOOOOOO00 .SetTemperature(OOOOO00OOO0O0O00O ['CM_HD2_InTemp'] + 273.15)
            O0O0OOO0OO000OOOO .SetPressure(OOOOO00OOO0O0O00O ['CM_HD2_DischPrs'] * 1000.0)
            O0O0OOO0OO000OOOO .SetTemperature(OOOOO00OOO0O0O00O ['CM_HD2_CtrlTemp'] + 273.15)
            OOOOO0OO00OO0OO00 .set_POut(OOOOO00OOO0O0O00O ['CM_HD2_DischPrs'] * 1000.0)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .sim10)
            OOO0OOOO000O0000O  = {}
            OO00O0O00O0O0OOOO  = OOO0O0OOOOOOOOO00 .GetPressure() / 1000.0
            OOO0OOOO000O0000O ['HD2_in_pres'] = OO00O0O00O0O0OOOO 
            O00OO00OOO0O00O0O  = OOO0O0OOOOOOOOO00 .GetTemperature() - 273.15
            OOO0OOOO000O0000O ['HD2_in_temp'] = O00OO00OOO0O00O0O 
            OOOOOO00OO0OOO0OO  = OOO0O0OOOOOOOOO00 .GetMassFlow() * 3600.0
            OOO0OOOO000O0000O ['HD2_mass_flow'] = OOOOOO00OO0OOO0OO 
            OOOO0000O0O00OO0O  = OOOO00OO0OOO0O000 .GetPressure() / 1000.0
            OOO0OOOO000O0000O ['HD2_out_pres'] = OOOO0000O0O00OO0O 
            OOO0O00OO0OOO0OOO  = O0O0OOO0OO000OOOO .GetTemperature() - 273.15
            OOO0OOOO000O0000O ['HD2_out_temp'] = OOO0O00OO0OOO0OOO 
            OOO0OOOOOOO000000  = OOO0O0OOOOOOOOO00 .GetMassEnthalpy()
            OOOOOO00O000OO0OO ['HD2_in_specific_enthalpy'] = OOO0OOOOOOO000000 
            OO0O00OO000OO0OO0  = OOOO0000O0O00OO0O  / OO00O0O00O0O0OOOO 
            OOOOOO00O000OO0OO ['HD2_pressure_ratio'] = OO0O00OO000OO0OO0 
            OOO0OOOO0O0OO0000  = abs(OOOOO0OO00OO0OO00 .GetPowerGeneratedOrConsumed())
            OOOOOO00O000OO0OO ['HD2_polytropic_power'] = OOO0OOOO0O0OO0000 
            OO0OOOO0OOO0OO000  = OOOOO0OO00OO0OO00 .get_PolytropicHead()
            OOOOOO00O000OO0OO ['HD2_polytropic_head'] = OO0OOOO0OOO0OO000 
            OOOO00O00000O0OOO  = OOOO00OO0OOO0O000 .GetMassEnthalpy()
            OOOOOO00O000OO0OO ['HD2_out_ideal_specific_enthalpy'] = OOOO00O00000O0OOO 
            OO00OO0OOO00O00O0  = O0O0OOO0OO000OOOO .GetMassEnthalpy()
            OOOOOO00O000OO0OO ['HD2_out_actual_specific_enthalpy'] = OO00OO0OOO00O00O0 
            O000OOOO0O0000OOO  = OOOO00O00000O0OOO  - OOO0OOOOOOO000000 
            OOOOOOO0O0O00OO0O  = OO00OO0OOO00O00O0  - OOO0OOOOOOO000000 
            if OOOOOOO0O0O00OO0O  == 0:
                OOOOOOO0O0O00OO0O  = 1
            OOOO0OOO00O0O0000  = O000OOOO0O0000OOO  / OOOOOOO0O0O00OO0O  * 100
            OOOOOO00O000OO0OO ['HD2_polytropic_efficiency'] = OOOO0OOO00O0O0000 
            for key in OOOOOO00O000OO0OO .keys():
                OOOOOO00O000OO0OO [key] = float('{0:.2f}'.format(OOOOOO00O000OO0OO [key]))
        O00000OO00000OOOO  = 0.72
        OOOOOO00O0O0OO000  = 3.086
        OO0O0OO000OOO000O  = 5
        O0OO0O0O0OO0O0OO0  = 50000.0
        OOOOOO000O0O000OO  = 45000.0
        OOOO0OO0O000O0O0O  = 45000.0
        OO0O0O000OOOO00OO  = 0.35
        OOOOOOOOOOOOO0O00  = 0.4
        OO000OO00OOO000O0  = 8
        O0O00O0OO0OOO0000  = 6
        O000O00OOOOOO00O0  = 6
        OOOO000O000OOOOOO  = 8
        if OOO0000O00000OOOO ['ME1'] == 1:
            print('starting dwsim ME1')
            OO00OOOOOOOOO0O00  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_Air_in').GetAsObject()
            OO00O00O0O00OO0O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_Heat_added').GetAsObject()
            OOO000OOOOO0O0000  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_compression').GetAsObject()
            O0O00OO000OO000O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_compression_power').GetAsObject()
            O0OOOO0O0000OO00O  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_compressed').GetAsObject()
            OOOO00OOO000OOOO0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_heat_addition').GetAsObject()
            OOOO0OO0OOO00OOO0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_heated').GetAsObject()
            O0O0OOOOO0OO0OO00  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_expansion').GetAsObject()
            O000OOO00O00O00OO  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_brake_power').GetAsObject()
            O000O0OO000OO0000  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_Exhaust_gases').GetAsObject()
            OOO00O0OOOOO0O0OO  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_TC_exp').GetAsObject()
            OO0OOO0O0O0O0O00O  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_TC_comp').GetAsObject()
            OOOOO0O0000OO00O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_compressed_fresh_air').GetAsObject()
            OOO0O0OO00OOOOOO0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_fresh_air_in').GetAsObject()
            OO0OOOOOOO0O0O0O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_scav_air_cooler').GetAsObject()
            OOO0000OOO0O000OO  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_cw_in').GetAsObject()
            O000O00000OO00O0O  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_scav_air').GetAsObject()
            O00OO0OOO00O0O0O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_CL').GetAsObject()
            O0OOOOO00OOOO00O0  = O0000OOO0OOO0OO00 .ME1_sim.GetFlowsheetSimulationObject('ME1_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] = (OOOOO00OOO0O0O00O ['ME1_EG_Cyl1_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME1_EG_Cyl2_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME1_EG_Cyl3_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME1_EG_Cyl4_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME1_EG_Cyl5_ScavAirPistonUnderTemp']) / 5
            OOOOO00OOO0O0O00O ['ME1_PF_Flow'] = OOOOO00OOO0O0O00O ['ME1_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['ME1_FO_Flow_InstMass'] * 0.005
            if OOOOO00OOO0O0O00O ['ME1_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['ME1_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['ME1_Suction_volumetric_flow'] = 3.14 * (1 / 4) * O00000OO00000OOOO  ** 2 * OOOOOO00O0O0OO000  * OO0O0OO000OOO000O  * OOOOO00OOO0O0O00O ['ME1_Misc_Spd'] * 60
            OOOOO00OOO0O0O00O ['ME1_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['ME1_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME1_FO_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME1_PF_Flow']
            if OOOOO00OOO0O0O00O ['ME1_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['ME1_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['ME1_Heat_added'] = OOOOO00OOO0O0O00O ['ME1_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            if 'ME1_EG_ScavAirMeanPrs' in O0OO0OO0OOOOO0O0O :
                OO0O0OOOO0OO00O00  = O0OO0OO0OOOOO0O0O ['ME1_EG_ScavAirMeanPrs']
            else:
                OO0O0OOOO0OO00O00  = OOOOO00OOO0O0O00O ['ME1_EG_ScavAirMeanPrs']
            OO00OOOOOOOOO0O00 .SetTemperature(OOOOO00OOO0O0O00O ['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            OO00OOOOOOOOO0O00 .SetPressure(OO0O0OOOO0OO00O00  * 1000000)
            OO00OOOOOOOOO0O00 .SetVolumetricFlow(OOOOO00OOO0O0O00O ['ME1_Suction_volumetric_flow'] / 3600.0)
            OOO000OOOOO0O0000 .set_POut(OOOOO00OOO0O0O00O ['ME1_Cyl_AvgFiringPrs'] * 1000000)
            OO00O00O0O00OO0O0 .set_EnergyFlow(OOOOO00OOO0O0O00O ['ME1_Heat_added'])
            O0O0OOOOO0OO0OO00 .set_POut(OO0O0OOOO0OO00O00  * 1000000)
            O00OO0OOO00O0O0O0 .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME1_EG_TC1_InTemp'] + 273.15)
            OOO0O0OO00OOOOOO0 .SetTemperature(OOOOO00OOO0O0O00O ['ME1_EG_TC_AirInTempA'] + 273.15)
            OO0OOO0O0O0O0O00O .set_POut(OO0O0OOOO0OO00O00  * 1000000)
            OO0OOOOOOO0O0O0O0 .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            OOO0000OOO0O000OO .SetPressure(OOOOO00OOO0O0O00O ['ME1_EG_ScavAir_CWInPrs'] * 1000000)
            OOO0000OOO0O000OO .SetTemperature(OOOOO00OOO0O0O00O ['ME1_EG_ScavAir_CWInTemp'] + 273.15)
            O0OOOOO00OOOO00O0 .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME1_EG_ScavAir_CWOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .ME1_sim)
            OO0000OOOOOO00OO0 ['ME1_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['ME1_Suction_volumetric_flow']
            OO0000OOOOOO00OO0 ['ME1_Combustion_air_flow'] = OO00OOOOOOOOO0O00 .GetMassFlow() * 3600
            OO0000OOOOOO00OO0 ['ME1_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['ME1_Total_fuel_flow']
            OO0000OOOOOO00OO0 ['ME1_AirFuel_ratio'] = OO0000OOOOOO00OO0 ['ME1_Combustion_air_flow'] / OO0000OOOOOO00OO0 ['ME1_Total_fuel_flow']
            OO0000OOOOOO00OO0 ['ME1_Heat_added'] = OOOOO00OOO0O0O00O ['ME1_Heat_added']
            OO0000OOOOOO00OO0 ['ME1_Isentropic_compression_power'] = abs(OOO000OOOOO0O0000 .GetPowerGeneratedOrConsumed())
            OO0000OOOOOO00OO0 ['ME1_Maximum_pressure'] = OOOOO00OOO0O0O00O ['ME1_Cyl_AvgFiringPrs'] * 10
            OO0000OOOOOO00OO0 ['ME1_CylTemperature_after_isentropic_compression'] = O0OOOO0O0000OO00O .GetTemperature() - 273.15
            OO0000OOOOOO00OO0 ['ME1_CylTemperature_after_combustion'] = OOOO0OO0OOO00OOO0 .GetTemperature() - 273.15
            OO0000OOOOOO00OO0 ['ME1_Total_ideal_brake_power'] = abs(O0O0OOOOO0OO0OO00 .GetPowerGeneratedOrConsumed())
            OO0000OOOOOO00OO0 ['ME1_Net_ideal_brake_power'] = OO0000OOOOOO00OO0 ['ME1_Total_ideal_brake_power'] - OO0000OOOOOO00OO0 ['ME1_Isentropic_compression_power']
            OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['Sft1_Misc_Pwr']
            if OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power'] == 0.0:
                OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power'] = 1.0
            OO0000OOOOOO00OO0 ['ME1_Ideal_brake_thermal_efficiency'] = OO0000OOOOOO00OO0 ['ME1_Net_ideal_brake_power'] / OO0000OOOOOO00OO0 ['ME1_Heat_added'] * 100
            OO0000OOOOOO00OO0 ['ME1_Actual_brake_thermal_efficiency'] = OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power'] / OO0000OOOOOO00OO0 ['ME1_Heat_added'] * 100
            OO0000OOOOOO00OO0 ['ME1_Relative_efficiency'] = OO0000OOOOOO00OO0 ['ME1_Actual_brake_thermal_efficiency'] / OO0000OOOOOO00OO0 ['ME1_Ideal_brake_thermal_efficiency'] * 100
            OO0000OOOOOO00OO0 ['ME1_Ideal_brake_specific_fuel_consumption'] = OO0000OOOOOO00OO0 ['ME1_Total_fuel_flow'] / OO0000OOOOOO00OO0 ['ME1_Net_ideal_brake_power']
            OO0000OOOOOO00OO0 ['ME1_Actual_brake_specific_fuel_consumption'] = OO0000OOOOOO00OO0 ['ME1_Total_fuel_flow'] / OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power']
            OO0000OOOOOO00OO0 ['ME1_Actual_brake_mean_effective_pressure'] = OO0000OOOOOO00OO0 ['ME1_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['ME1_Suction_volumetric_flow'] * 36
            OO0000OOOOOO00OO0 ['ME1_Ideal_brake_mean_effective_pressure'] = OO0000OOOOOO00OO0 ['ME1_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['ME1_Suction_volumetric_flow'] * 36
            OO0000OOOOOO00OO0 ['ME1_Compression_pressure_ratio'] = OO0000OOOOOO00OO0 ['ME1_Maximum_pressure'] / (OO0O0OOOO0OO00O00  * 10)
            OO0000OOOOOO00OO0 ['ME1_TC_compression_power'] = abs(OO0OOO0O0O0O0O00O .GetPowerGeneratedOrConsumed())
            OO0OOO0O0OOOOOO0O ['ME1_SAC_air_in_temperature'] = OOOOO0O0000OO00O0 .GetTemperature() - 273.15
            OO0OOO0O0OOOOOO0O ['ME1_SAC_scav_air_in_SpecificEnthalpy'] = OOOOO0O0000OO00O0 .GetMassEnthalpy()
            OO0OOO0O0OOOOOO0O ['ME1_SAC_scav_air_out_SpecificEnthalpy'] = O000O00000OO00O0O .GetMassEnthalpy()
            OO0OOO0O0OOOOOO0O ['ME1_SAC_cw_duty'] = OO0OOOOOOO0O0O0O0 .GetPowerGeneratedOrConsumed()
            OO0OOO0O0OOOOOO0O ['ME1_SAC_cw_flow_required'] = OOO0000OOO0O000OO .GetMassFlow() * 3600
            OO0000OOOOOO00OO0  = OO0000OOOOOO00OO0  | OO0OOO0O0OOOOOO0O 
            for key in OO0000OOOOOO00OO0 .keys():
                OO0000OOOOOO00OO0 [key] = float('{0:.3f}'.format(OO0000OOOOOO00OO0 [key]))
        if OOO0000O00000OOOO ['ME2'] == 1:
            print('starting dwsim ME2')
            O00OOOOO0O0OO0000  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_Air_in').GetAsObject()
            OOOO0O0000O0O0000  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_Heat_added').GetAsObject()
            O0OO0OO0O000O0OOO  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_compression').GetAsObject()
            O0OOOOO00O00OO000  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_compression_power').GetAsObject()
            O0000OOO00O00O000  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_compressed').GetAsObject()
            OO000OO00OO000OO0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_heat_addition').GetAsObject()
            O0O000OO0O00O00O0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_heated').GetAsObject()
            OOO0O0OO000OOO0OO  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_expansion').GetAsObject()
            OOOO00OOO0OO00000  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_brake_power').GetAsObject()
            O00O0O00OOO00O0O0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_Exhaust_gases').GetAsObject()
            OOO0OO0OO0OOOO0O0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_TC_exp').GetAsObject()
            OOOOO0O0O000O00O0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_TC_comp').GetAsObject()
            OOOOOOO0OOOOO00OO  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_compressed_fresh_air').GetAsObject()
            OOO0000O0O00OOOO0  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_fresh_air_in').GetAsObject()
            O000OOOO00OO00O00  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_scav_air_cooler').GetAsObject()
            OOOOOOOO00O0OOO0O  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_cw_in').GetAsObject()
            O00O0O0OO0O00OO0O  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_scav_air').GetAsObject()
            OO00O0000OO00OO0O  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_CL').GetAsObject()
            O0O0OOOO00OOO0O00  = O0000OOO0OOO0OO00 .ME2_sim.GetFlowsheetSimulationObject('ME2_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] = (OOOOO00OOO0O0O00O ['ME2_EG_Cyl1_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME2_EG_Cyl2_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME2_EG_Cyl3_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME2_EG_Cyl4_ScavAirPistonUnderTemp'] + OOOOO00OOO0O0O00O ['ME2_EG_Cyl5_ScavAirPistonUnderTemp']) / 5
            OOOOO00OOO0O0O00O ['ME2_PF_Flow'] = OOOOO00OOO0O0O00O ['ME2_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['ME2_FO_Flow_InstMass'] * 0.005
            if OOOOO00OOO0O0O00O ['ME2_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['ME2_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['ME2_Suction_volumetric_flow'] = 3.14 * (1 / 4) * O00000OO00000OOOO  ** 2 * OOOOOO00O0O0OO000  * OO0O0OO000OOO000O  * OOOOO00OOO0O0O00O ['ME2_Misc_Spd'] * 60
            OOOOO00OOO0O0O00O ['ME2_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['ME2_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME2_FO_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME2_PF_Flow']
            if OOOOO00OOO0O0O00O ['ME2_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['ME2_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['ME2_Heat_added'] = OOOOO00OOO0O0O00O ['ME2_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            if 'ME2_EG_ScavAirMeanPrs' in O0OO0OO0OOOOO0O0O :
                OOOO00OO00OOOOOOO  = O0OO0OO0OOOOO0O0O ['ME2_EG_ScavAirMeanPrs']
            else:
                OOOO00OO00OOOOOOO  = OOOOO00OOO0O0O00O ['ME2_EG_ScavAirMeanPrs']
            O00OOOOO0O0OO0000 .SetTemperature(OOOOO00OOO0O0O00O ['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            O00OOOOO0O0OO0000 .SetPressure(OOOO00OO00OOOOOOO  * 1000000)
            O00OOOOO0O0OO0000 .SetVolumetricFlow(OOOOO00OOO0O0O00O ['ME2_Suction_volumetric_flow'] / 3600.0)
            O0OO0OO0O000O0OOO .set_POut(OOOOO00OOO0O0O00O ['ME2_Cyl_AvgFiringPrs'] * 1000000)
            OOOO0O0000O0O0000 .set_EnergyFlow(OOOOO00OOO0O0O00O ['ME2_Heat_added'])
            OOO0O0OO000OOO0OO .set_POut(OOOO00OO00OOOOOOO  * 1000000)
            OO00O0000OO00OO0O .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME2_EG_TC1_InTemp'] + 273.15)
            OOO0000O0O00OOOO0 .SetTemperature(OOOOO00OOO0O0O00O ['ME2_EG_TC_AirInTempA'] + 273.15)
            OOOOO0O0O000O00O0 .set_POut(OOOO00OO00OOOOOOO  * 1000000)
            O000OOOO00OO00O00 .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            OOOOOOOO00O0OOO0O .SetPressure(OOOOO00OOO0O0O00O ['ME2_EG_ScavAir_CWInPrs'] * 1000000)
            OOOOOOOO00O0OOO0O .SetTemperature(OOOOO00OOO0O0O00O ['ME2_EG_ScavAir_CWInTemp'] + 273.15)
            O0O0OOOO00OOO0O00 .set_OutletTemperature(OOOOO00OOO0O0O00O ['ME2_EG_ScavAir_CWOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .ME2_sim)
            OOO0OO0O00OO0O0OO ['ME2_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['ME2_Suction_volumetric_flow']
            OOO0OO0O00OO0O0OO ['ME2_Combustion_air_flow'] = O00OOOOO0O0OO0000 .GetMassFlow() * 3600
            OOO0OO0O00OO0O0OO ['ME2_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['ME2_Total_fuel_flow']
            OOO0OO0O00OO0O0OO ['ME2_AirFuel_ratio'] = OOO0OO0O00OO0O0OO ['ME2_Combustion_air_flow'] / OOO0OO0O00OO0O0OO ['ME2_Total_fuel_flow']
            OOO0OO0O00OO0O0OO ['ME2_Heat_added'] = OOOOO00OOO0O0O00O ['ME2_Heat_added']
            OOO0OO0O00OO0O0OO ['ME2_Isentropic_compression_power'] = abs(O0OO0OO0O000O0OOO .GetPowerGeneratedOrConsumed())
            OOO0OO0O00OO0O0OO ['ME2_Maximum_pressure'] = OOOOO00OOO0O0O00O ['ME2_Cyl_AvgFiringPrs'] * 10
            OOO0OO0O00OO0O0OO ['ME2_CylTemperature_after_isentropic_compression'] = O0000OOO00O00O000 .GetTemperature() - 273.15
            OOO0OO0O00OO0O0OO ['ME2_CylTemperature_after_combustion'] = O0O000OO0O00O00O0 .GetTemperature() - 273.15
            OOO0OO0O00OO0O0OO ['ME2_Total_ideal_brake_power'] = abs(OOO0O0OO000OOO0OO .GetPowerGeneratedOrConsumed())
            OOO0OO0O00OO0O0OO ['ME2_Net_ideal_brake_power'] = OOO0OO0O00OO0O0OO ['ME2_Total_ideal_brake_power'] - OOO0OO0O00OO0O0OO ['ME2_Isentropic_compression_power']
            OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['Sft1_Misc_Pwr']
            if OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power'] == 0.0:
                OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power'] = 1.0
            OOO0OO0O00OO0O0OO ['ME2_Ideal_brake_thermal_efficiency'] = OOO0OO0O00OO0O0OO ['ME2_Net_ideal_brake_power'] / OOO0OO0O00OO0O0OO ['ME2_Heat_added'] * 100
            OOO0OO0O00OO0O0OO ['ME2_Actual_brake_thermal_efficiency'] = OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power'] / OOO0OO0O00OO0O0OO ['ME2_Heat_added'] * 100
            OOO0OO0O00OO0O0OO ['ME2_Relative_efficiency'] = OOO0OO0O00OO0O0OO ['ME2_Actual_brake_thermal_efficiency'] / OOO0OO0O00OO0O0OO ['ME2_Ideal_brake_thermal_efficiency'] * 100
            OOO0OO0O00OO0O0OO ['ME2_Ideal_brake_specific_fuel_consumption'] = OOO0OO0O00OO0O0OO ['ME2_Total_fuel_flow'] / OOO0OO0O00OO0O0OO ['ME2_Net_ideal_brake_power']
            OOO0OO0O00OO0O0OO ['ME2_Actual_brake_specific_fuel_consumption'] = OOO0OO0O00OO0O0OO ['ME2_Total_fuel_flow'] / OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power']
            OOO0OO0O00OO0O0OO ['ME2_Actual_brake_mean_effective_pressure'] = OOO0OO0O00OO0O0OO ['ME2_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['ME2_Suction_volumetric_flow'] * 36
            OOO0OO0O00OO0O0OO ['ME2_Ideal_brake_mean_effective_pressure'] = OOO0OO0O00OO0O0OO ['ME2_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['ME2_Suction_volumetric_flow'] * 36
            OOO0OO0O00OO0O0OO ['ME2_Compression_pressure_ratio'] = OOO0OO0O00OO0O0OO ['ME2_Maximum_pressure'] / (OOOO00OO00OOOOOOO  * 10)
            OOO0OO0O00OO0O0OO ['ME2_TC_compression_power'] = abs(OOOOO0O0O000O00O0 .GetPowerGeneratedOrConsumed())
            OOOO00O000O00OO0O ['ME2_SAC_air_in_temperature'] = OOOOOOO0OOOOO00OO .GetTemperature() - 273.15
            OOOO00O000O00OO0O ['ME2_SAC_scav_air_in_SpecificEnthalpy'] = OOOOOOO0OOOOO00OO .GetMassEnthalpy()
            OOOO00O000O00OO0O ['ME2_SAC_scav_air_out_SpecificEnthalpy'] = O00O0O0OO0O00OO0O .GetMassEnthalpy()
            OOOO00O000O00OO0O ['ME2_SAC_cw_duty'] = O000OOOO00OO00O00 .GetPowerGeneratedOrConsumed()
            OOOO00O000O00OO0O ['ME2_SAC_cw_flow_required'] = OOOOOOOO00O0OOO0O .GetMassFlow() * 3600
            OOO0OO0O00OO0O0OO  = OOO0OO0O00OO0O0OO  | OOOO00O000O00OO0O 
            for key in OOO0OO0O00OO0O0OO .keys():
                OOO0OO0O00OO0O0OO [key] = float('{0:.3f}'.format(OOO0OO0O00OO0O0OO [key]))
        if OOO0000O00000OOOO ['GE1'] == 1:
            print('starting dwsim GE1')
            O00O00O00OOO0OO0O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_Air_in').GetAsObject()
            O0O0O00O0000O0O0O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_Heat_added').GetAsObject()
            O0O000O000O000O00  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_compression').GetAsObject()
            OO0000OOO00OO00OO  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_compression_power').GetAsObject()
            OO0OO0O0O00OOOOO0  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_compressed').GetAsObject()
            OO000OOOOOO00OO0O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_heat_addition').GetAsObject()
            OOO0O0OOOO0OOOOOO  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_heated').GetAsObject()
            OO000OOOOO0OO0OO0  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_expansion').GetAsObject()
            OO000OOO000O0O00O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_brake_power').GetAsObject()
            O0O00O000OO0OOOOO  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_Exhaust_gases').GetAsObject()
            OO0OOO0000OO0000O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_TC_exp').GetAsObject()
            OOOO0O0O0OO0O00O0  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_TC_comp').GetAsObject()
            OO0000OOO00000O00  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_compressed_fresh_air').GetAsObject()
            O00O00OO0000OO0O0  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_fresh_air_in').GetAsObject()
            O00OO00OOO000OOOO  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_scav_air_cooler').GetAsObject()
            O00O0OO0O00OOOO0O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_cw_in').GetAsObject()
            O0OOOOO0O0OOOO000  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_scav_air').GetAsObject()
            OOO000O00OO00OO0O  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_CL').GetAsObject()
            O00O00OOOOOO0O000  = O0000OOO0OOO0OO00 .GE1_sim.GetFlowsheetSimulationObject('GE1_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['GE1_CylAvg_CompressionPrs'] = (OOOOO00OOO0O0O00O ['GE1_Cyl1_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl2_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl3_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl4_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl5_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl6_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl7_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE1_Cyl8_CompressionPrs']) / 8
            if OOO0000O00000OOOO ['GE1'] == 1 and OOO0000O00000OOOO ['GE2'] == 1:
                OOOOO00OOO0O0O00O ['GE1_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE1GE2_Flow_InstMass'] / 2
            else:
                OOOOO00OOO0O0O00O ['GE1_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE1GE2_Flow_InstMass']
            OOOOO00OOO0O0O00O ['GE1_PF_Flow'] = OOOOO00OOO0O0O00O ['GE1_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['GE1_FO_flow'] * 0.005
            if OOOOO00OOO0O0O00O ['GE1_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['GE1_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['GE1_Suction_volumetric_flow'] = 3.14 * (1 / 4) * OO0O0O000OOOO00OO  ** 2 * OOOOOOOOOOOOO0O00  * OO000OO00OOO000O0  * OOOOO00OOO0O0O00O ['GE1_Misc_Spd'] * 60 / 2
            OOOOO00OOO0O0O00O ['GE1_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE1_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE1_FO_flow'] + OOOOO00OOO0O0O00O ['GE1_PF_Flow']
            if OOOOO00OOO0O0O00O ['GE1_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['GE1_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['GE1_Heat_added'] = OOOOO00OOO0O0O00O ['GE1_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            O00O00O00OOO0OO0O .SetTemperature(OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutTemp'] + 273.15)
            O00O00O00OOO0OO0O .SetPressure(OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutPrs'] * 1000000)
            O00O00O00OOO0OO0O .SetVolumetricFlow(OOOOO00OOO0O0O00O ['GE1_Suction_volumetric_flow'] / 3600.0)
            O0O000O000O000O00 .set_POut(OOOOO00OOO0O0O00O ['GE1_CylAvg_CompressionPrs'] * 1000000)
            O0O0O00O0000O0O0O .set_EnergyFlow(OOOOO00OOO0O0O00O ['GE1_Heat_added'])
            OO000OOOOO0OO0OO0 .set_POut(OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutPrs'] * 1000000)
            OOO000O00OO00OO0O .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE1_EG_TC1_InTemp'] + 273.15)
            O00O00OO0000OO0O0 .SetTemperature(OOOOO00OOO0O0O00O ['GE1_EG_TC1_AirIntakeTemp'] + 273.15)
            OOOO0O0O0OO0O00O0 .set_POut(OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutPrs'] * 1000000)
            O00OO00OOO000OOOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutTemp'] + 273.15)
            O00O0OO0O00OOOO0O .SetPressure(OOOOO00OOO0O0O00O ['GE1_CS_LTCFW_AirClrInPrs'] * 1000000)
            O00O0OO0O00OOOO0O .SetTemperature(OOOOO00OOO0O0O00O ['GE1_CS_LTCFW_AirClrInTemp'] + 273.15)
            O00O00OOOOOO0O000 .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE1_CS_LTCFW_AirClrOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .GE1_sim)
            OO0OOO00O00OO00OO ['GE1_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['GE1_Suction_volumetric_flow']
            OO0OOO00O00OO00OO ['GE1_Combustion_air_flow'] = O00O00O00OOO0OO0O .GetMassFlow() * 3600
            OO0OOO00O00OO00OO ['GE1_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE1_Total_fuel_flow']
            OO0OOO00O00OO00OO ['GE1_AirFuel_ratio'] = OO0OOO00O00OO00OO ['GE1_Combustion_air_flow'] / OO0OOO00O00OO00OO ['GE1_Total_fuel_flow']
            OO0OOO00O00OO00OO ['GE1_Heat_added'] = OOOOO00OOO0O0O00O ['GE1_Heat_added']
            OO0OOO00O00OO00OO ['GE1_Isentropic_compression_power'] = abs(O0O000O000O000O00 .GetPowerGeneratedOrConsumed())
            OO0OOO00O00OO00OO ['GE1_Maximum_pressure'] = OOOOO00OOO0O0O00O ['GE1_CylAvg_CompressionPrs'] * 10
            OO0OOO00O00OO00OO ['GE1_CylTemperature_after_isentropic_compression'] = OO0OO0O0O00OOOOO0 .GetTemperature() - 273.15
            OO0OOO00O00OO00OO ['GE1_CylTemperature_after_combustion'] = OOO0O0OOOO0OOOOOO .GetTemperature() - 273.15
            OO0OOO00O00OO00OO ['GE1_Total_ideal_brake_power'] = abs(OO000OOOOO0OO0OO0 .GetPowerGeneratedOrConsumed())
            OO0OOO00O00OO00OO ['GE1_Net_ideal_brake_power'] = OO0OOO00O00OO00OO ['GE1_Total_ideal_brake_power'] - OO0OOO00O00OO00OO ['GE1_Isentropic_compression_power']
            OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['GE1_Misc_Pwr']
            if OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power'] == 0.0:
                OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power'] = 1.0
            OO0OOO00O00OO00OO ['GE1_Ideal_brake_thermal_efficiency'] = OO0OOO00O00OO00OO ['GE1_Net_ideal_brake_power'] / OO0OOO00O00OO00OO ['GE1_Heat_added'] * 100
            OO0OOO00O00OO00OO ['GE1_Actual_brake_thermal_efficiency'] = OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power'] / OO0OOO00O00OO00OO ['GE1_Heat_added'] * 100
            OO0OOO00O00OO00OO ['GE1_Relative_efficiency'] = OO0OOO00O00OO00OO ['GE1_Actual_brake_thermal_efficiency'] / OO0OOO00O00OO00OO ['GE1_Ideal_brake_thermal_efficiency'] * 100
            OO0OOO00O00OO00OO ['GE1_Ideal_brake_specific_fuel_consumption'] = OO0OOO00O00OO00OO ['GE1_Total_fuel_flow'] / OO0OOO00O00OO00OO ['GE1_Net_ideal_brake_power']
            OO0OOO00O00OO00OO ['GE1_Actual_brake_specific_fuel_consumption'] = OO0OOO00O00OO00OO ['GE1_Total_fuel_flow'] / OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power']
            OO0OOO00O00OO00OO ['GE1_Actual_brake_mean_effective_pressure'] = OO0OOO00O00OO00OO ['GE1_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['GE1_Suction_volumetric_flow'] * 36
            OO0OOO00O00OO00OO ['GE1_Ideal_brake_mean_effective_pressure'] = OO0OOO00O00OO00OO ['GE1_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['GE1_Suction_volumetric_flow'] * 36
            OO0OOO00O00OO00OO ['GE1_Compression_pressure_ratio'] = OO0OOO00O00OO00OO ['GE1_Maximum_pressure'] / (OOOOO00OOO0O0O00O ['GE1_CS_AirClr_ChAirOutPrs'] * 10)
            OO0OOO00O00OO00OO ['GE1_TC_compression_power'] = abs(OOOO0O0O0OO0O00O0 .GetPowerGeneratedOrConsumed())
            OO0OOOOO0OOO00OOO ['GE1_SAC_air_in_temperature'] = OO0000OOO00000O00 .GetTemperature() - 273.15
            OO0OOOOO0OOO00OOO ['GE1_SAC_scav_air_in_SpecificEnthalpy'] = OO0000OOO00000O00 .GetMassEnthalpy()
            OO0OOOOO0OOO00OOO ['GE1_SAC_scav_air_out_SpecificEnthalpy'] = O0OOOOO0O0OOOO000 .GetMassEnthalpy()
            OO0OOOOO0OOO00OOO ['GE1_SAC_cw_duty'] = O00OO00OOO000OOOO .GetPowerGeneratedOrConsumed()
            OO0OOOOO0OOO00OOO ['GE1_SAC_cw_flow_required'] = O00O0OO0O00OOOO0O .GetMassFlow() * 3600
            OO0OOO00O00OO00OO  = OO0OOO00O00OO00OO  | OO0OOOOO0OOO00OOO 
            for key in OO0OOO00O00OO00OO .keys():
                OO0OOO00O00OO00OO [key] = float('{0:.3f}'.format(OO0OOO00O00OO00OO [key]))
        if OOO0000O00000OOOO ['GE2'] == 1:
            print('starting dwsim GE2')
            OOO0O00O0OOO00000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_Air_in').GetAsObject()
            OOOOOOO00000OO00O  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_Heat_added').GetAsObject()
            O00OO00O00OO00OO0  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_compression').GetAsObject()
            O00000O0O00OOO000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_compression_power').GetAsObject()
            OOOOOO0OO0O0OOO00  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_compressed').GetAsObject()
            OOO00000O0OO0OOOO  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_heat_addition').GetAsObject()
            OO00O0O000000OO00  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_heated').GetAsObject()
            OO00O0000000O0000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_expansion').GetAsObject()
            OO0OOO000OO0O0000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_brake_power').GetAsObject()
            OOOO0OOOOO000O000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_Exhaust_gases').GetAsObject()
            O000000O0000O0O0O  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_TC_exp').GetAsObject()
            OOOO000000OOO0OOO  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_TC_comp').GetAsObject()
            OO0OO00O00O00O000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_compressed_fresh_air').GetAsObject()
            O0OOOO0O0O000O000  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_fresh_air_in').GetAsObject()
            O00O0O0000O0OO00O  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_scav_air_cooler').GetAsObject()
            OOO0OOOO0O00O00OO  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_cw_in').GetAsObject()
            OO0O0O0O00O0OO0O0  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_scav_air').GetAsObject()
            O00000OOO0O0OO00O  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_CL').GetAsObject()
            OO0OOOOOO00000OOO  = O0000OOO0OOO0OO00 .GE2_sim.GetFlowsheetSimulationObject('GE2_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['GE2_CylAvg_CompressionPrs'] = (OOOOO00OOO0O0O00O ['GE2_Cyl1_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE2_Cyl2_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE2_Cyl3_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE2_Cyl4_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE2_Cyl5_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE2_Cyl6_CompressionPrs']) / 8
            if OOO0000O00000OOOO ['GE1'] == 1 and OOO0000O00000OOOO ['GE2'] == 1:
                OOOOO00OOO0O0O00O ['GE2_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE1GE2_Flow_InstMass'] / 2
            else:
                OOOOO00OOO0O0O00O ['GE2_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE1GE2_Flow_InstMass']
            OOOOO00OOO0O0O00O ['GE2_PF_Flow'] = OOOOO00OOO0O0O00O ['GE2_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['GE2_FO_flow'] * 0.005
            if OOOOO00OOO0O0O00O ['GE2_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['GE2_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['GE2_Suction_volumetric_flow'] = 3.14 * (1 / 4) * OO0O0O000OOOO00OO  ** 2 * OOOOOOOOOOOOO0O00  * O0O00O0OO0OOO0000  * OOOOO00OOO0O0O00O ['GE2_Misc_Spd'] * 60 / 2
            OOOOO00OOO0O0O00O ['GE2_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE2_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE2_FO_flow'] + OOOOO00OOO0O0O00O ['GE2_PF_Flow']
            if OOOOO00OOO0O0O00O ['GE2_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['GE2_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['GE2_Heat_added'] = OOOOO00OOO0O0O00O ['GE2_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            OOO0O00O0OOO00000 .SetTemperature(OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutTemp'] + 273.15)
            OOO0O00O0OOO00000 .SetPressure(OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutPrs'] * 1000000)
            OOO0O00O0OOO00000 .SetVolumetricFlow(OOOOO00OOO0O0O00O ['GE2_Suction_volumetric_flow'] / 3600.0)
            O00OO00O00OO00OO0 .set_POut(OOOOO00OOO0O0O00O ['GE2_CylAvg_CompressionPrs'] * 1000000)
            OOOOOOO00000OO00O .set_EnergyFlow(OOOOO00OOO0O0O00O ['GE2_Heat_added'])
            OO00O0000000O0000 .set_POut(OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutPrs'] * 1000000)
            O00000OOO0O0OO00O .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE2_EG_TC1_InTemp'] + 273.15)
            O0OOOO0O0O000O000 .SetTemperature(OOOOO00OOO0O0O00O ['GE2_EG_TC1_AirIntakeTemp'] + 273.15)
            OOOO000000OOO0OOO .set_POut(OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutPrs'] * 1000000)
            O00O0O0000O0OO00O .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutTemp'] + 273.15)
            OOO0OOOO0O00O00OO .SetPressure(OOOOO00OOO0O0O00O ['GE2_CS_LTCFW_AirClrInPrs'] * 1000000)
            OOO0OOOO0O00O00OO .SetTemperature(OOOOO00OOO0O0O00O ['GE2_CS_LTCFW_AirClrInTemp'] + 273.15)
            OO0OOOOOO00000OOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE2_CS_LTCFW_AirClrOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .GE2_sim)
            O00O0O00OO0OO0O0O ['GE2_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['GE2_Suction_volumetric_flow']
            O00O0O00OO0OO0O0O ['GE2_Combustion_air_flow'] = OOO0O00O0OOO00000 .GetMassFlow() * 3600
            O00O0O00OO0OO0O0O ['GE2_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE2_Total_fuel_flow']
            O00O0O00OO0OO0O0O ['GE2_AirFuel_ratio'] = O00O0O00OO0OO0O0O ['GE2_Combustion_air_flow'] / O00O0O00OO0OO0O0O ['GE2_Total_fuel_flow']
            O00O0O00OO0OO0O0O ['GE2_Heat_added'] = OOOOO00OOO0O0O00O ['GE2_Heat_added']
            O00O0O00OO0OO0O0O ['GE2_Isentropic_compression_power'] = abs(O00OO00O00OO00OO0 .GetPowerGeneratedOrConsumed())
            O00O0O00OO0OO0O0O ['GE2_Maximum_pressure'] = OOOOO00OOO0O0O00O ['GE2_CylAvg_CompressionPrs'] * 10
            O00O0O00OO0OO0O0O ['GE2_CylTemperature_after_isentropic_compression'] = OOOOOO0OO0O0OOO00 .GetTemperature() - 273.15
            O00O0O00OO0OO0O0O ['GE2_CylTemperature_after_combustion'] = OO00O0O000000OO00 .GetTemperature() - 273.15
            O00O0O00OO0OO0O0O ['GE2_Total_ideal_brake_power'] = abs(OO00O0000000O0000 .GetPowerGeneratedOrConsumed())
            O00O0O00OO0OO0O0O ['GE2_Net_ideal_brake_power'] = O00O0O00OO0OO0O0O ['GE2_Total_ideal_brake_power'] - O00O0O00OO0OO0O0O ['GE2_Isentropic_compression_power']
            O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['GE2_Misc_Pwr']
            if O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power'] == 0.0:
                O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power'] = 1.0
            O00O0O00OO0OO0O0O ['GE2_Ideal_brake_thermal_efficiency'] = O00O0O00OO0OO0O0O ['GE2_Net_ideal_brake_power'] / O00O0O00OO0OO0O0O ['GE2_Heat_added'] * 100
            O00O0O00OO0OO0O0O ['GE2_Actual_brake_thermal_efficiency'] = O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power'] / O00O0O00OO0OO0O0O ['GE2_Heat_added'] * 100
            O00O0O00OO0OO0O0O ['GE2_Relative_efficiency'] = O00O0O00OO0OO0O0O ['GE2_Actual_brake_thermal_efficiency'] / O00O0O00OO0OO0O0O ['GE2_Ideal_brake_thermal_efficiency'] * 100
            O00O0O00OO0OO0O0O ['GE2_Ideal_brake_specific_fuel_consumption'] = O00O0O00OO0OO0O0O ['GE2_Total_fuel_flow'] / O00O0O00OO0OO0O0O ['GE2_Net_ideal_brake_power']
            O00O0O00OO0OO0O0O ['GE2_Actual_brake_specific_fuel_consumption'] = O00O0O00OO0OO0O0O ['GE2_Total_fuel_flow'] / O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power']
            O00O0O00OO0OO0O0O ['GE2_Actual_brake_mean_effective_pressure'] = O00O0O00OO0OO0O0O ['GE2_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['GE2_Suction_volumetric_flow'] * 36
            O00O0O00OO0OO0O0O ['GE2_Ideal_brake_mean_effective_pressure'] = O00O0O00OO0OO0O0O ['GE2_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['GE2_Suction_volumetric_flow'] * 36
            O00O0O00OO0OO0O0O ['GE2_Compression_pressure_ratio'] = O00O0O00OO0OO0O0O ['GE2_Maximum_pressure'] / (OOOOO00OOO0O0O00O ['GE2_CS_AirClr_ChAirOutPrs'] * 10)
            O00O0O00OO0OO0O0O ['GE2_TC_compression_power'] = abs(OOOO000000OOO0OOO .GetPowerGeneratedOrConsumed())
            OO000000O0000OOO0 ['GE2_SAC_air_in_temperature'] = OO0OO00O00O00O000 .GetTemperature() - 273.15
            OO000000O0000OOO0 ['GE2_SAC_scav_air_in_SpecificEnthalpy'] = OO0OO00O00O00O000 .GetMassEnthalpy()
            OO000000O0000OOO0 ['GE2_SAC_scav_air_out_SpecificEnthalpy'] = OO0O0O0O00O0OO0O0 .GetMassEnthalpy()
            OO000000O0000OOO0 ['GE2_SAC_cw_duty'] = O00O0O0000O0OO00O .GetPowerGeneratedOrConsumed()
            OO000000O0000OOO0 ['GE2_SAC_cw_flow_required'] = OOO0OOOO0O00O00OO .GetMassFlow() * 3600
            O00O0O00OO0OO0O0O  = O00O0O00OO0OO0O0O  | OO000000O0000OOO0 
            for key in O00O0O00OO0OO0O0O .keys():
                O00O0O00OO0OO0O0O [key] = float('{0:.3f}'.format(O00O0O00OO0OO0O0O [key]))
        if OOO0000O00000OOOO ['GE3'] == 1:
            print('starting dwsim GE3')
            O000OOOO0O00000O0  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_Air_in').GetAsObject()
            OO0OOO0OO000O0O00  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_Heat_added').GetAsObject()
            OO00OOO00OOOO0OOO  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_compression').GetAsObject()
            O0OOO0O000O000OO0  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_compression_power').GetAsObject()
            O00OO00OO00000OOO  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_compressed').GetAsObject()
            O0OO0OOO000O00O0O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_heat_addition').GetAsObject()
            OOOO00O000O0000O0  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_heated').GetAsObject()
            O0OO0O0000OO0OO0O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_expansion').GetAsObject()
            OOOO00000OO0O0O0O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_brake_power').GetAsObject()
            O00OOO0O0O0OOO00O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_Exhaust_gases').GetAsObject()
            OO0OOOO0O000O0O0O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_TC_exp').GetAsObject()
            O0O0O0OOOO00OO0O0  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_TC_comp').GetAsObject()
            OOO0OOO0OOOO000OO  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_compressed_fresh_air').GetAsObject()
            OOOOOO00O0OO0OO0O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_fresh_air_in').GetAsObject()
            O0O0OOOOOO0OOOOOO  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_scav_air_cooler').GetAsObject()
            OO0O0OOO0OOOO000O  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_cw_in').GetAsObject()
            OOO0O00OOO0O0O0O0  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_scav_air').GetAsObject()
            OOOO0O0O0O000OO00  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_CL').GetAsObject()
            O0OO00OO00O0O00OO  = O0000OOO0OOO0OO00 .GE3_sim.GetFlowsheetSimulationObject('GE3_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['GE3_CylAvg_CompressionPrs'] = (OOOOO00OOO0O0O00O ['GE3_Cyl1_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE3_Cyl2_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE3_Cyl3_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE3_Cyl4_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE3_Cyl5_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE3_Cyl6_CompressionPrs']) / 8
            if OOO0000O00000OOOO ['GE3'] == 1 and OOO0000O00000OOOO ['GE4'] == 1:
                OOOOO00OOO0O0O00O ['GE3_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE3GE4_Flow_InstMass'] / 2
            else:
                OOOOO00OOO0O0O00O ['GE3_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE3GE4_Flow_InstMass']
            OOOOO00OOO0O0O00O ['GE3_PF_Flow'] = OOOOO00OOO0O0O00O ['GE3_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['GE3_FO_flow'] * 0.005
            if OOOOO00OOO0O0O00O ['GE3_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['GE3_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['GE3_Suction_volumetric_flow'] = 3.14 * (1 / 4) * OO0O0O000OOOO00OO  ** 2 * OOOOOOOOOOOOO0O00  * O000O00OOOOOO00O0  * OOOOO00OOO0O0O00O ['GE3_Misc_Spd'] * 60 / 2
            OOOOO00OOO0O0O00O ['GE3_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE3_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE3_FO_flow'] + OOOOO00OOO0O0O00O ['GE3_PF_Flow']
            if OOOOO00OOO0O0O00O ['GE3_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['GE3_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['GE3_Heat_added'] = OOOOO00OOO0O0O00O ['GE3_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            O000OOOO0O00000O0 .SetTemperature(OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutTemp'] + 273.15)
            O000OOOO0O00000O0 .SetPressure(OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutPrs'] * 1000000)
            O000OOOO0O00000O0 .SetVolumetricFlow(OOOOO00OOO0O0O00O ['GE3_Suction_volumetric_flow'] / 3600.0)
            OO00OOO00OOOO0OOO .set_POut(OOOOO00OOO0O0O00O ['GE3_CylAvg_CompressionPrs'] * 1000000)
            OO0OOO0OO000O0O00 .set_EnergyFlow(OOOOO00OOO0O0O00O ['GE3_Heat_added'])
            O0OO0O0000OO0OO0O .set_POut(OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutPrs'] * 1000000)
            OOOO0O0O0O000OO00 .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE3_EG_TC1_InTemp'] + 273.15)
            OOOOOO00O0OO0OO0O .SetTemperature(OOOOO00OOO0O0O00O ['GE3_EG_TC1_AirIntakeTemp'] + 273.15)
            O0O0O0OOOO00OO0O0 .set_POut(OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutPrs'] * 1000000)
            O0O0OOOOOO0OOOOOO .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutTemp'] + 273.15)
            OO0O0OOO0OOOO000O .SetPressure(OOOOO00OOO0O0O00O ['GE3_CS_LTCFW_AirClrInPrs'] * 1000000)
            OO0O0OOO0OOOO000O .SetTemperature(OOOOO00OOO0O0O00O ['GE3_CS_LTCFW_AirClrInTemp'] + 273.15)
            O0OO00OO00O0O00OO .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE3_CS_LTCFW_AirClrOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .GE3_sim)
            O00O0OOO0OOOOOOO0 ['GE3_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['GE3_Suction_volumetric_flow']
            O00O0OOO0OOOOOOO0 ['GE3_Combustion_air_flow'] = O000OOOO0O00000O0 .GetMassFlow() * 3600
            O00O0OOO0OOOOOOO0 ['GE3_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE3_Total_fuel_flow']
            O00O0OOO0OOOOOOO0 ['GE3_AirFuel_ratio'] = O00O0OOO0OOOOOOO0 ['GE3_Combustion_air_flow'] / O00O0OOO0OOOOOOO0 ['GE3_Total_fuel_flow']
            O00O0OOO0OOOOOOO0 ['GE3_Heat_added'] = OOOOO00OOO0O0O00O ['GE3_Heat_added']
            O00O0OOO0OOOOOOO0 ['GE3_Isentropic_compression_power'] = abs(OO00OOO00OOOO0OOO .GetPowerGeneratedOrConsumed())
            O00O0OOO0OOOOOOO0 ['GE3_Maximum_pressure'] = OOOOO00OOO0O0O00O ['GE3_CylAvg_CompressionPrs'] * 10
            O00O0OOO0OOOOOOO0 ['GE3_CylTemperature_after_isentropic_compression'] = O00OO00OO00000OOO .GetTemperature() - 273.15
            O00O0OOO0OOOOOOO0 ['GE3_CylTemperature_after_combustion'] = OOOO00O000O0000O0 .GetTemperature() - 273.15
            O00O0OOO0OOOOOOO0 ['GE3_Total_ideal_brake_power'] = abs(O0OO0O0000OO0OO0O .GetPowerGeneratedOrConsumed())
            O00O0OOO0OOOOOOO0 ['GE3_Net_ideal_brake_power'] = O00O0OOO0OOOOOOO0 ['GE3_Total_ideal_brake_power'] - O00O0OOO0OOOOOOO0 ['GE3_Isentropic_compression_power']
            O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['GE3_Misc_Pwr']
            if O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power'] == 0.0:
                O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power'] = 1.0
            O00O0OOO0OOOOOOO0 ['GE3_Ideal_brake_thermal_efficiency'] = O00O0OOO0OOOOOOO0 ['GE3_Net_ideal_brake_power'] / O00O0OOO0OOOOOOO0 ['GE3_Heat_added'] * 100
            O00O0OOO0OOOOOOO0 ['GE3_Actual_brake_thermal_efficiency'] = O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power'] / O00O0OOO0OOOOOOO0 ['GE3_Heat_added'] * 100
            O00O0OOO0OOOOOOO0 ['GE3_Relative_efficiency'] = O00O0OOO0OOOOOOO0 ['GE3_Actual_brake_thermal_efficiency'] / O00O0OOO0OOOOOOO0 ['GE3_Ideal_brake_thermal_efficiency'] * 100
            O00O0OOO0OOOOOOO0 ['GE3_Ideal_brake_specific_fuel_consumption'] = O00O0OOO0OOOOOOO0 ['GE3_Total_fuel_flow'] / O00O0OOO0OOOOOOO0 ['GE3_Net_ideal_brake_power']
            O00O0OOO0OOOOOOO0 ['GE3_Actual_brake_specific_fuel_consumption'] = O00O0OOO0OOOOOOO0 ['GE3_Total_fuel_flow'] / O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power']
            O00O0OOO0OOOOOOO0 ['GE3_Actual_brake_mean_effective_pressure'] = O00O0OOO0OOOOOOO0 ['GE3_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['GE3_Suction_volumetric_flow'] * 36
            O00O0OOO0OOOOOOO0 ['GE3_Ideal_brake_mean_effective_pressure'] = O00O0OOO0OOOOOOO0 ['GE3_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['GE3_Suction_volumetric_flow'] * 36
            O00O0OOO0OOOOOOO0 ['GE3_Compression_pressure_ratio'] = O00O0OOO0OOOOOOO0 ['GE3_Maximum_pressure'] / (OOOOO00OOO0O0O00O ['GE3_CS_AirClr_ChAirOutPrs'] * 10)
            O00O0OOO0OOOOOOO0 ['GE3_TC_compression_power'] = abs(O0O0O0OOOO00OO0O0 .GetPowerGeneratedOrConsumed())
            OO00O00OO0000000O ['GE3_SAC_air_in_temperature'] = OOO0OOO0OOOO000OO .GetTemperature() - 273.15
            OO00O00OO0000000O ['GE3_SAC_scav_air_in_SpecificEnthalpy'] = OOO0OOO0OOOO000OO .GetMassEnthalpy()
            OO00O00OO0000000O ['GE3_SAC_scav_air_out_SpecificEnthalpy'] = OOO0O00OOO0O0O0O0 .GetMassEnthalpy()
            OO00O00OO0000000O ['GE3_SAC_cw_duty'] = O0O0OOOOOO0OOOOOO .GetPowerGeneratedOrConsumed()
            OO00O00OO0000000O ['GE3_SAC_cw_flow_required'] = OO0O0OOO0OOOO000O .GetMassFlow() * 3600
            O00O0OOO0OOOOOOO0  = O00O0OOO0OOOOOOO0  | OO00O00OO0000000O 
            for key in O00O0OOO0OOOOOOO0 .keys():
                O00O0OOO0OOOOOOO0 [key] = float('{0:.3f}'.format(O00O0OOO0OOOOOOO0 [key]))
        if OOO0000O00000OOOO ['GE4'] == 1:
            print('starting dwsim GE4')
            OOOOO0O00OO0O00O0  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_Air_in').GetAsObject()
            OO0OO0OO000OO0000  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_Heat_added').GetAsObject()
            OO0000O0OO0000OOO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_compression').GetAsObject()
            OOOOOO00O00O00OO0  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_compression_power').GetAsObject()
            O0O00OO0OO00O0OO0  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_compressed').GetAsObject()
            O0O00O00O0OOO00O0  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_heat_addition').GetAsObject()
            O0000OOO0O0O0O000  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_heated').GetAsObject()
            OOO0O0O0OOOOOO0OO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_expansion').GetAsObject()
            O0OO00O0OOO00O0OO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_brake_power').GetAsObject()
            OO00000OOO0000OOO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_Exhaust_gases').GetAsObject()
            OOO0O0O0O00OO0O0O  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_TC_exp').GetAsObject()
            OOO000OO0OO00OOOO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_TC_comp').GetAsObject()
            OOOO00OOOO0OO0O0O  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_compressed_fresh_air').GetAsObject()
            O00OO0OOOOO0O0000  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_fresh_air_in').GetAsObject()
            OO0O00OOOO00OO000  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_scav_air_cooler').GetAsObject()
            O0OOO0000000000O0  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_cw_in').GetAsObject()
            O0OOO0000O00OOO0O  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_scav_air').GetAsObject()
            OO0OO0O0O0OO0O0OO  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_CL').GetAsObject()
            O0O0O0OO00000O00O  = O0000OOO0OOO0OO00 .GE4_sim.GetFlowsheetSimulationObject('GE4_HT').GetAsObject()
            OOOOO00OOO0O0O00O ['GE4_CylAvg_CompressionPrs'] = (OOOOO00OOO0O0O00O ['GE4_Cyl1_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE4_Cyl2_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE4_Cyl3_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE4_Cyl4_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE4_Cyl5_CompressionPrs'] + OOOOO00OOO0O0O00O ['GE4_Cyl6_CompressionPrs']) / 8
            if OOO0000O00000OOOO ['GE3'] == 1 and OOO0000O00000OOOO ['GE4'] == 1:
                OOOOO00OOO0O0O00O ['GE4_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE3GE4_Flow_InstMass'] / 2
            else:
                OOOOO00OOO0O0O00O ['GE4_FO_flow'] = OOOOO00OOO0O0O00O ['GE_FO_GE3GE4_Flow_InstMass']
            OOOOO00OOO0O0O00O ['GE4_PF_Flow'] = OOOOO00OOO0O0O00O ['GE4_FG_Flow_InstMass'] * 0.01 + OOOOO00OOO0O0O00O ['GE4_FO_flow'] * 0.005
            if OOOOO00OOO0O0O00O ['GE4_Misc_Spd'] == 0.0:
                OOOOO00OOO0O0O00O ['GE4_Misc_Spd'] = 1.0
            OOOOO00OOO0O0O00O ['GE4_Suction_volumetric_flow'] = 3.14 * (1 / 4) * OO0O0O000OOOO00OO  ** 2 * OOOOOOOOOOOOO0O00  * OOOO000O000OOOOOO  * OOOOO00OOO0O0O00O ['GE4_Misc_Spd'] * 60 / 2
            OOOOO00OOO0O0O00O ['GE4_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE4_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE4_FO_flow'] + OOOOO00OOO0O0O00O ['GE4_PF_Flow']
            if OOOOO00OOO0O0O00O ['GE4_Total_fuel_flow'] == 0.0:
                OOOOO00OOO0O0O00O ['GE4_Total_fuel_flow'] = 1.0
            OOOOO00OOO0O0O00O ['GE4_Heat_added'] = OOOOO00OOO0O0O00O ['GE4_Total_fuel_flow'] * O0OO0O0O0OO0O0OO0  / 3600
            OOOOO0O00OO0O00O0 .SetTemperature(OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutTemp'] + 273.15)
            OOOOO0O00OO0O00O0 .SetPressure(OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutPrs'] * 1000000)
            OOOOO0O00OO0O00O0 .SetVolumetricFlow(OOOOO00OOO0O0O00O ['GE4_Suction_volumetric_flow'] / 3600.0)
            OO0000O0OO0000OOO .set_POut(OOOOO00OOO0O0O00O ['GE4_CylAvg_CompressionPrs'] * 1000000)
            OO0OO0OO000OO0000 .set_EnergyFlow(OOOOO00OOO0O0O00O ['GE4_Heat_added'])
            OOO0O0O0OOOOOO0OO .set_POut(OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutPrs'] * 1000000)
            OO0OO0O0O0OO0O0OO .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE4_EG_TC1_InTemp'] + 273.15)
            O00OO0OOOOO0O0000 .SetTemperature(OOOOO00OOO0O0O00O ['GE4_EG_TC1_AirIntakeTemp'] + 273.15)
            OOO000OO0OO00OOOO .set_POut(OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutPrs'] * 1000000)
            OO0O00OOOO00OO000 .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutTemp'] + 273.15)
            O0OOO0000000000O0 .SetPressure(OOOOO00OOO0O0O00O ['GE4_CS_LTCFW_AirClrInPrs'] * 1000000)
            O0OOO0000000000O0 .SetTemperature(OOOOO00OOO0O0O00O ['GE4_CS_LTCFW_AirClrInTemp'] + 273.15)
            O0O0O0OO00000O00O .set_OutletTemperature(OOOOO00OOO0O0O00O ['GE4_CS_LTCFW_AirClrOutTemp'] + 273.15)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .GE4_sim)
            OOO0O00OO00O0OO00 ['GE4_Suction_volumetric_flow'] = OOOOO00OOO0O0O00O ['GE4_Suction_volumetric_flow']
            OOO0O00OO00O0OO00 ['GE4_Combustion_air_flow'] = OOOOO0O00OO0O00O0 .GetMassFlow() * 3600
            OOO0O00OO00O0OO00 ['GE4_Total_fuel_flow'] = OOOOO00OOO0O0O00O ['GE4_Total_fuel_flow']
            OOO0O00OO00O0OO00 ['GE4_AirFuel_ratio'] = OOO0O00OO00O0OO00 ['GE4_Combustion_air_flow'] / OOO0O00OO00O0OO00 ['GE4_Total_fuel_flow']
            OOO0O00OO00O0OO00 ['GE4_Heat_added'] = OOOOO00OOO0O0O00O ['GE4_Heat_added']
            OOO0O00OO00O0OO00 ['GE4_Isentropic_compression_power'] = abs(OO0000O0OO0000OOO .GetPowerGeneratedOrConsumed())
            OOO0O00OO00O0OO00 ['GE4_Maximum_pressure'] = OOOOO00OOO0O0O00O ['GE4_CylAvg_CompressionPrs'] * 10
            OOO0O00OO00O0OO00 ['GE4_CylTemperature_after_isentropic_compression'] = O0O00OO0OO00O0OO0 .GetTemperature() - 273.15
            OOO0O00OO00O0OO00 ['GE4_CylTemperature_after_combustion'] = O0000OOO0O0O0O000 .GetTemperature() - 273.15
            OOO0O00OO00O0OO00 ['GE4_Total_ideal_brake_power'] = abs(OOO0O0O0OOOOOO0OO .GetPowerGeneratedOrConsumed())
            OOO0O00OO00O0OO00 ['GE4_Net_ideal_brake_power'] = OOO0O00OO00O0OO00 ['GE4_Total_ideal_brake_power'] - OOO0O00OO00O0OO00 ['GE4_Isentropic_compression_power']
            OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power'] = OOOOO00OOO0O0O00O ['GE4_Misc_Pwr']
            if OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power'] == 0.0:
                OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power'] = 1.0
            OOO0O00OO00O0OO00 ['GE4_Ideal_brake_thermal_efficiency'] = OOO0O00OO00O0OO00 ['GE4_Net_ideal_brake_power'] / OOO0O00OO00O0OO00 ['GE4_Heat_added'] * 100
            OOO0O00OO00O0OO00 ['GE4_Actual_brake_thermal_efficiency'] = OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power'] / OOO0O00OO00O0OO00 ['GE4_Heat_added'] * 100
            OOO0O00OO00O0OO00 ['GE4_Relative_efficiency'] = OOO0O00OO00O0OO00 ['GE4_Actual_brake_thermal_efficiency'] / OOO0O00OO00O0OO00 ['GE4_Ideal_brake_thermal_efficiency'] * 100
            OOO0O00OO00O0OO00 ['GE4_Ideal_brake_specific_fuel_consumption'] = OOO0O00OO00O0OO00 ['GE4_Total_fuel_flow'] / OOO0O00OO00O0OO00 ['GE4_Net_ideal_brake_power']
            OOO0O00OO00O0OO00 ['GE4_Actual_brake_specific_fuel_consumption'] = OOO0O00OO00O0OO00 ['GE4_Total_fuel_flow'] / OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power']
            OOO0O00OO00O0OO00 ['GE4_Actual_brake_mean_effective_pressure'] = OOO0O00OO00O0OO00 ['GE4_Net_actual_brake_power'] / OOOOO00OOO0O0O00O ['GE4_Suction_volumetric_flow'] * 36
            OOO0O00OO00O0OO00 ['GE4_Ideal_brake_mean_effective_pressure'] = OOO0O00OO00O0OO00 ['GE4_Net_ideal_brake_power'] / OOOOO00OOO0O0O00O ['GE4_Suction_volumetric_flow'] * 36
            OOO0O00OO00O0OO00 ['GE4_Compression_pressure_ratio'] = OOO0O00OO00O0OO00 ['GE4_Maximum_pressure'] / (OOOOO00OOO0O0O00O ['GE4_CS_AirClr_ChAirOutPrs'] * 10)
            OOO0O00OO00O0OO00 ['GE4_TC_compression_power'] = abs(OOO000OO0OO00OOOO .GetPowerGeneratedOrConsumed())
            O0O0O0O00O000O0OO ['GE4_SAC_air_in_temperature'] = OOOO00OOOO0OO0O0O .GetTemperature() - 273.15
            O0O0O0O00O000O0OO ['GE4_SAC_scav_air_in_SpecificEnthalpy'] = OOOO00OOOO0OO0O0O .GetMassEnthalpy()
            O0O0O0O00O000O0OO ['GE4_SAC_scav_air_out_SpecificEnthalpy'] = O0OOO0000O00OOO0O .GetMassEnthalpy()
            O0O0O0O00O000O0OO ['GE4_SAC_cw_duty'] = OO0O00OOOO00OO000 .GetPowerGeneratedOrConsumed()
            O0O0O0O00O000O0OO ['GE4_SAC_cw_flow_required'] = O0OOO0000000000O0 .GetMassFlow() * 3600
            OOO0O00OO00O0OO00  = OOO0O00OO00O0OO00  | O0O0O0O00O000O0OO 
            for key in OOO0O00OO00O0OO00 .keys():
                OOO0O00OO00O0OO00 [key] = float('{0:.3f}'.format(OOO0O00OO00O0OO00 [key]))
        if OOO0000O00000OOOO ['NG1'] == 1:
            print('starting dwsim NG1')
            if O00OO00O00OO00O00 ['NS_NG1-40101_PV'] == 1 and O00OO00O00OO00O00 ['NS_NG1-40102_PV'] == 1 and (O00OO00O00OO00O00 ['NS_NG1-40103_PV'] == 1):
                O00OO000O0O00OOOO  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_air_comp').GetAsObject()
                OO000OO000OOOOO0O  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_Air').GetAsObject()
                O0OOO0000O00O0OO0  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_comp_out').GetAsObject()
                O0O00O00OO00O0000  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_clr').GetAsObject()
                OOOOO0O0OO0OOOO0O  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_htr_in').GetAsObject()
                O0O0O0000O000000O  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_htr').GetAsObject()
                OOOOO00O0O000OO0O  = O0000OOO0OOO0OO00 .NG1_sim.GetFlowsheetSimulationObject('NG1_sep_in').GetAsObject()
                OO000OO000OOOOO0O .SetTemperature(OOOOO00OOO0O0O00O ['Nav_Atm_AmbTemp'] + 273.15)
                OO000OO000OOOOO0O .SetVolumetricFlow(OOOOO00OOO0O0O00O ['Elec_NGen1_Flow'] / 0.78 / 3600)
                O00OO000O0O00OOOO .set_POut(OOOOO00OOO0O0O00O ['NS_NG1-40101_PV'] * 1000000)
                O0O00O00OO00O0000 .set_OutletTemperature(OOOOO00OOO0O0O00O ['NS_NG1-40102_PV'] + 273.15)
                O0O0O0000O000000O .set_OutletTemperature(OOOOO00OOO0O0O00O ['NS_NG1-40103_PV'] + 273.15)
                from DWSIM.GlobalSettings import Settings
                Settings.SolverMode = 0
                O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .NG1_sim)
                OOOOO0OO00OO0OO0O ['NG1_Air_flow_estimated'] = OO000OO000OOOOO0O .GetMassFlow() * 3600
                OOOOO0OO00OO0OO0O ['NG1_Air_comp_in_SpecificEnthalpy'] = OO000OO000OOOOO0O .GetMassEnthalpy()
                OOOOO0OO00OO0OO0O ['NG1_Air_comp_out_SpecificEnthalpy'] = O0OOO0000O00O0OO0 .GetMassEnthalpy()
                OOOOO0OO00OO0OO0O ['NG1_air_comp_polytropic_power'] = abs(O00OO000O0O00OOOO .GetPowerGeneratedOrConsumed())
                OOOOO0OO00OO0OO0O ['NG1_air_comp_out_temperature'] = O0OOO0000O00O0OO0 .GetTemperature() - 273.15
                OOOOO0OO00OO0OO0O ['NG1_cooling_duty'] = O0O00O00OO00O0000 .GetPowerGeneratedOrConsumed()
                OOOOO0OO00OO0OO0O ['NG1_heating_duty'] = abs(O0O0O0000O000000O .GetPowerGeneratedOrConsumed())
                OOOOO0OO00OO0OO0O ['NG1_htr_in_SpecificEnthalpy'] = OOOOO0O0OO0OOOO0O .GetMassEnthalpy()
                OOOOO0OO00OO0OO0O ['NG1_htr_out_SpecificEnthalpy'] = OOOOO00O0O000OO0O .GetMassEnthalpy()
                for key in OOOOO0OO00OO0OO0O .keys():
                    OOOOO0OO00OO0OO0O [key] = float('{0:.3f}'.format(OOOOO0OO00OO0OO0O [key]))
        if OOO0000O00000OOOO ['NG2'] == 1:
            print('starting dwsim NG2')
            if O00OO00O00OO00O00 ['NS_NG2-40101_PV'] == 1 and O00OO00O00OO00O00 ['NS_NG2-40102_PV'] == 1 and (O00OO00O00OO00O00 ['NS_NG2-40103_PV'] == 1):
                OOOOOOOO000000O0O  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_air_comp').GetAsObject()
                OO0O0O0OO00OO0O0O  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_Air').GetAsObject()
                OO0OOO00OOO0OO00O  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_comp_out').GetAsObject()
                OOO0O00OOOOO0OOO0  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_clr').GetAsObject()
                O0OOO000O00000OO0  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_htr_in').GetAsObject()
                O0000OO00OO0OO0OO  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_htr').GetAsObject()
                O0OOOO00OOOOOO0OO  = O0000OOO0OOO0OO00 .NG2_sim.GetFlowsheetSimulationObject('NG2_sep_in').GetAsObject()
                OO0O0O0OO00OO0O0O .SetTemperature(OOOOO00OOO0O0O00O ['Nav_Atm_AmbTemp'] + 273.15)
                OO0O0O0OO00OO0O0O .SetVolumetricFlow(OOOOO00OOO0O0O00O ['Elec_NGen2_Flow'] / 0.78 / 3600)
                OOOOOOOO000000O0O .set_POut(OOOOO00OOO0O0O00O ['NS_NG2-40101_PV'] * 1000000)
                OOO0O00OOOOO0OOO0 .set_OutletTemperature(OOOOO00OOO0O0O00O ['NS_NG2-40102_PV'] + 273.15)
                O0000OO00OO0OO0OO .set_OutletTemperature(OOOOO00OOO0O0O00O ['NS_NG2-40103_PV'] + 273.15)
                from DWSIM.GlobalSettings import Settings
                Settings.SolverMode = 0
                O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .NG2_sim)
                O00OO0O000O000O0O ['NG2_Air_flow_estimated'] = OO0O0O0OO00OO0O0O .GetMassFlow() * 3600
                O00OO0O000O000O0O ['NG2_Air_comp_in_SpecificEnthalpy'] = OO0O0O0OO00OO0O0O .GetMassEnthalpy()
                O00OO0O000O000O0O ['NG2_Air_comp_out_SpecificEnthalpy'] = OO0OOO00OOO0OO00O .GetMassEnthalpy()
                O00OO0O000O000O0O ['NG2_air_comp_polytropic_power'] = abs(OOOOOOOO000000O0O .GetPowerGeneratedOrConsumed())
                O00OO0O000O000O0O ['NG2_air_comp_out_temperature'] = OO0OOO00OOO0OO00O .GetTemperature() - 273.15
                O00OO0O000O000O0O ['NG2_cooling_duty'] = OOO0O00OOOOO0OOO0 .GetPowerGeneratedOrConsumed()
                O00OO0O000O000O0O ['NG2_heating_duty'] = abs(O0000OO00OO0OO0OO .GetPowerGeneratedOrConsumed())
                O00OO0O000O000O0O ['NG2_htr_in_SpecificEnthalpy'] = O0OOO000O00000OO0 .GetMassEnthalpy()
                O00OO0O000O000O0O ['NG2_htr_out_SpecificEnthalpy'] = O0OOOO00OOOOOO0OO .GetMassEnthalpy()
                for key in O00OO0O000O000O0O .keys():
                    O00OO0O000O000O0O [key] = float('{0:.3f}'.format(O00OO0O000O000O0O [key]))
        O0O0O000OO00O000O  = 50000
        if OOO0000O00000OOOO ['AB_AB1'] == 1 and OOO0000O00000OOOO ['AB_AB2'] == 1:
            O00O0000OOOOO0O0O  = OOOOO00OOO0O0O00O ['Blr_AuxBlr_FO_Flow_InstMass'] * 50000 / 3600 / 2
            O0OO00O0O0OOO00OO  = OOOOO00OOO0O0O00O ['Blr_AuxBlr_FO_Flow_InstMass'] * 50000 / 3600 / 2
        elif OOO0000O00000OOOO ['AB_AB1'] == 1:
            O00O0000OOOOO0O0O  = OOOOO00OOO0O0O00O ['Blr_AuxBlr_FO_Flow_InstMass'] * 50000 / 3600
            O0OO00O0O0OOO00OO  = 0
        elif OOO0000O00000OOOO ['AB_AB2'] == 1:
            O0OO00O0O0OOO00OO  = OOOOO00OOO0O0O00O ['Blr_AuxBlr_FO_Flow_InstMass'] * 50000 / 3600
            O00O0000OOOOO0O0O  = 0
        if OOO0000O00000OOOO ['AB_AB1'] == 1:
            print('starting dwsim AB1')
            OOO000O0O0O0O0O0O  = O0000OOO0OOO0OO00 .AB1_sim.GetFlowsheetSimulationObject('AB1_steam').GetAsObject()
            OOO000O0O0O0O0O0O .SetPressure(OOOOO00OOO0O0O00O ['Blr_AuxBlr1_StmPrs'] * 1000000)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .AB1_sim)
            O0OOO0O000OO00OO0 ['AB1_Heat_added'] = O00O0000OOOOO0O0O 
            O0OOO0O000OO00OO0 ['AB1_Steam_temp'] = OOO000O0O0O0O0O0O .GetTemperature() - 273.15
            O0OOO0O000OO00OO0 ['AB1_Steam_SpecificEnthalpy'] = OOO000O0O0O0O0O0O .GetMassEnthalpy()
            O0OOO0O000OO00OO0 ['AB1_Steam_flow'] = O0OOO0O000OO00OO0 ['AB1_Heat_added'] / O0OOO0O000OO00OO0 ['AB1_Steam_SpecificEnthalpy'] * 3600 * 0.8
        if OOO0000O00000OOOO ['AB_AB2'] == 1:
            print('starting dwsim AB2')
            O0OO00O0OO000OOOO  = O0000OOO0OOO0OO00 .AB2_sim.GetFlowsheetSimulationObject('AB2_steam').GetAsObject()
            O0OO00O0OO000OOOO .SetPressure(OOOOO00OOO0O0O00O ['Blr_AuxBlr2_StmPrs'] * 1000000)
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            O00O000OOO00000O0  = O0000OOO0OOO0OO00 .interf.CalculateFlowsheet2(O0000OOO0OOO0OO00 .AB2_sim)
            OO0O00OO000O0000O ['AB2_Heat_added'] = O0OO00O0O0OOO00OO 
            OO0O00OO000O0000O ['AB2_Steam_temp'] = O0OO00O0OO000OOOO .GetTemperature() - 273.15
            OO0O00OO000O0000O ['AB2_Steam_SpecificEnthalpy'] = O0OO00O0OO000OOOO .GetMassEnthalpy()
            OO0O00OO000O0000O ['AB2_Steam_flow'] = OO0O00OO000O0000O ['AB2_Heat_added'] / OO0O00OO000O0000O ['AB2_Steam_SpecificEnthalpy'] * 3600 * 0.8
        O0000O000O0O0OOOO  = {}
        OOO0OOO0OOOOOOOO0  = {}
        O00O0OO000OOO0OOO  = {}
        OO00OO0OO0OOO0O0O  = {}
        if OOO0000O00000OOOO ['LNGV'] == 1:
            O0OOOO00O0OOOOOOO  = OO0OOO00O00OOO0O0 ['LNGV_Qc']
        else:
            O0OOOO00O0OOOOOOO  = 0
        if OOO0000O00000OOOO ['WUH'] == 1:
            OOO0O00OOO0OO00O0  = OO0O0O00O00O00O00 ['WUH_Qc']
        else:
            OOO0O00OOO0OO00O0  = 0
        O0000O000O0O0OOOO ['Cargo_vapor_total_duty'] = O0OOOO00O0OOOOOOO  + OOO0O00OOO0OO00O0 
        if OOO0000O00000OOOO ['FV'] == 1:
            O00O0OOO0000OO0O0  = OO0O00O0O0OO000O0 ['FV_Qc']
        else:
            O00O0OOO0000OO0O0  = 0
        if OOO0000O00000OOOO ['BOGH'] == 1:
            O000OOO0O00OOOOO0  = O00OO00O0OOOOO0OO ['BOGH_Qc']
        else:
            O000OOO0O00OOOOO0  = 0
        O00O0OO000OOO0OOO ['FBOG_total_duty'] = O00O0OOO0000OO0O0  + O000OOO0O00OOOOO0 
        if OOO0000O00000OOOO ['FV'] == 1:
            O000OOOO00OO0O000  = OO0O00O0O0OO000O0 ['FV_steam_required']
        else:
            O000OOOO00OO0O000  = 0
        if OOO0000O00000OOOO ['BOGH'] == 1:
            O000O0OO0000000OO  = O00OO00O0OOOOO0OO ['BOGH_steam_required']
        else:
            O000O0OO0000000OO  = 0
        O00O0OO000OOO0OOO ['FBOG_total_steam'] = O000OOOO00OO0O000  + O000O0OO0000000OO 
        if OOO0000O00000OOOO ['HD1'] == 1 and OOO0000O00000OOOO ['HD2'] == 0:
            OOO0OOO0OOOOOOOO0 ['HD_polytropic_efficiency'] = OOO0O0OOO0OOOO0OO ['HD1_polytropic_efficiency']
        elif OOO0000O00000OOOO ['HD1'] == 0 and OOO0000O00000OOOO ['HD2'] == 1:
            OOO0OOO0OOOOOOOO0 ['HD_polytropic_efficiency'] = OOOOOO00O000OO0OO ['HD2_polytropic_efficiency']
        elif OOO0000O00000OOOO ['HD1'] == 1 and OOO0000O00000OOOO ['HD2'] == 1:
            OOO0OOO0OOOOOOOO0 ['HD_polytropic_efficiency'] = (OOO0O0OOO0OOOO0OO ['HD1_polytropic_efficiency'] + OOOOOO00O000OO0OO ['HD2_polytropic_efficiency']) / 2
        if OOO0000O00000OOOO ['LD1'] == 1 and OOO0000O00000OOOO ['LD2'] == 0:
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_efficiency'] = (O0OO000OOO0000O00 ['LD1_S1_polytropic_efficiency'] + O0OO000OOO0000O00 ['LD1_S2_polytropic_efficiency']) / 2
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_power'] = (O0OO000OOO0000O00 ['LD1_S1_polytropic_power'] + O0OO000OOO0000O00 ['LD1_S2_polytropic_power']) / 2
        elif OOO0000O00000OOOO ['LD1'] == 0 and OOO0000O00000OOOO ['LD2'] == 1:
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_efficiency'] = (O00O0O00000O0O0OO ['LD2_S1_polytropic_efficiency'] + O00O0O00000O0O0OO ['LD2_S2_polytropic_efficiency']) / 2
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_power'] = (O00O0O00000O0O0OO ['LD2_S1_polytropic_power'] + O00O0O00000O0O0OO ['LD2_S2_polytropic_power']) / 2
        elif OOO0000O00000OOOO ['LD1'] == 1 and OOO0000O00000OOOO ['LD2'] == 1:
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_efficiency'] = (O0OO000OOO0000O00 ['LD1_S1_polytropic_efficiency'] + O0OO000OOO0000O00 ['LD1_S2_polytropic_efficiency'] + O00O0O00000O0O0OO ['LD2_S1_polytropic_efficiency'] + O00O0O00000O0O0OO ['LD2_S2_polytropic_efficiency']) / 4
            OO00OO0OO0OOO0O0O ['NBOG_polytropic_power'] = (O0OO000OOO0000O00 ['LD1_S1_polytropic_power'] + O0OO000OOO0000O00 ['LD1_S2_polytropic_power'] + O00O0O00000O0O0OO ['LD2_S1_polytropic_power'] + O00O0O00000O0O0OO ['LD2_S2_polytropic_power']) / 4
        O000OOOO0O0OOOOOO  = {}
        O000OOOO0O0OOOOOO ['FG_Consumption_ME'] = OOOOO00OOO0O0O00O ['ME1_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME2_FG_Flow_InstMass']
        O000OOOO0O0OOOOOO ['FG_Consumption_GE'] = OOOOO00OOO0O0O00O ['GE1_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE2_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE3_FG_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE4_FG_Flow_InstMass']
        O000OOOO0O0OOOOOO ['FO_Consumption_Aux_Boiler'] = OOOOO00OOO0O0O00O ['Blr_AuxBlr_FO_Flow_InstMass']
        if O00OO00O00OO00O00 ['NS_GPS_019_PV'] == 1:
            O000OOOO0O0OOOOOO ['Speed'] = OOOOO00OOO0O0O00O ['NS_GPS_019_PV']
        else:
            O000OOOO0O0OOOOOO ['Speed'] = 9.9
        O000OOOO0O0OOOOOO ['FG_Consumption_GCU'] = OOOOO00OOO0O0O00O ['FG_GCU1_Flow']
        O000OOOO0O0OOOOOO ['FO_Consumption_ME'] = OOOOO00OOO0O0O00O ['ME1_FO_Flow_InstMass'] + OOOOO00OOO0O0O00O ['ME2_FO_Flow_InstMass']
        O000OOOO0O0OOOOOO ['FO_Consumption_GE'] = OOOOO00OOO0O0O00O ['GE_FO_GE1GE2_Flow_InstMass'] + OOOOO00OOO0O0O00O ['GE_FO_GE3GE4_Flow_InstMass']
        O000OOOO0O0OOOOOO ['Total_FG_Consumption'] = O000OOOO0O0OOOOOO ['FG_Consumption_ME'] + O000OOOO0O0OOOOOO ['FG_Consumption_GE'] + O000OOOO0O0OOOOOO ['FG_Consumption_GCU']
        O000OOOO0O0OOOOOO ['PF_Consumption_ME_FG'] = O000OOOO0O0OOOOOO ['FG_Consumption_ME'] * 0.01
        O000OOOO0O0OOOOOO ['PF_Consumption_ME_FO'] = O000OOOO0O0OOOOOO ['FO_Consumption_ME'] * 0.005
        O000OOOO0O0OOOOOO ['PF_Consumption_GE_FG'] = O000OOOO0O0OOOOOO ['FG_Consumption_GE'] * 0.01
        O000OOOO0O0OOOOOO ['PF_Consumption_GE_FO'] = O000OOOO0O0OOOOOO ['FO_Consumption_GE'] * 0.005
        O000OOOO0O0OOOOOO ['Total_FO_Consumption'] = O000OOOO0O0OOOOOO ['FO_Consumption_ME'] + O000OOOO0O0OOOOOO ['FO_Consumption_GE'] + O000OOOO0O0OOOOOO ['FO_Consumption_Aux_Boiler'] + O000OOOO0O0OOOOOO ['PF_Consumption_ME_FO'] + O000OOOO0O0OOOOOO ['PF_Consumption_GE_FO']
        O000OOOO0O0OOOOOO ['Total_Fuel_Consumption'] = O000OOOO0O0OOOOOO ['Total_FG_Consumption'] + O000OOOO0O0OOOOOO ['Total_FO_Consumption'] + O000OOOO0O0OOOOOO ['PF_Consumption_ME_FG'] + O000OOOO0O0OOOOOO ['PF_Consumption_GE_FG']
        O0O0O0000OO0000O0  = {}
        if OOO0000O00000OOOO ['Fuel_Economy'] == 1:
            if O000OOOO0O0OOOOOO ['Speed'] == 0:
                O0O0O0000OO0000O0 ['Fuel_Economy'] = 0
            else:
                O0O0O0000OO0000O0 ['Fuel_Economy'] = O000OOOO0O0OOOOOO ['Total_Fuel_Consumption'] / O000OOOO0O0OOOOOO ['Speed']
        OO0OO0OO000O00000  = {}
        O0O0O0O000O00O00O  = ['FV_outputs', 'LNGV_outputs', 'BOGH_outputs', 'WUH_outputs', 'GWH_Stm_outputs', 'LD1_outputs', 'LD2_outputs', 'HD1_outputs', 'HD2_outputs', 'SC_outputs', 'Cargo_vapor_outputs', 'HD_outputs', 'NBOG_outputs', 'FBOG_outputs', 'Fuel_Consumption_outputs', 'Fuel_Economy_outputs', 'ME1_outputs', 'ME2_outputs', 'GE1_outputs', 'GE2_outputs', 'GE3_outputs', 'GE4_outputs', 'NG1_outputs', 'NG2_outputs', 'AB_AB1_outputs', 'AB_AB2_outputs']
        OO0000OO00OOOO0O0  = [OO0O00O0O0OO000O0 , OO0OOO00O00OOO0O0 , O00OO00O0OOOOO0OO , OO0O0O00O00O00O00 , OOOOOO0O0O0O0O0OO , O0OO000OOO0000O00 , O00O0O00000O0O0OO , OOO0O0OOO0OOOO0OO , OOOOOO00O000OO0OO , O00OO0O000O0OO0O0 , O0000O000O0O0OOOO , OOO0OOO0OOOOOOOO0 , OO00OO0OO0OOO0O0O , O00O0OO000OOO0OOO , O000OOOO0O0OOOOOO , O0O0O0000OO0000O0 , OO0000OOOOOO00OO0 , OOO0OO0O00OO0O0OO , OO0OOO00O00OO00OO , O00O0O00OO0OO0O0O , O00O0OOO0OOOOOOO0 , OOO0O00OO00O0OO00 , OOOOO0OO00OO0OO0O , O00OO0O000O000O0O , O0OOO0O000OO00OO0 , OO0O00OO000O0000O ]
        for i in range(len(O0O0O0O000O00O00O )):
            OO0OO0OO000O00000 [O0O0O0O000O00O00O [i]] = OO0000OO00OOOO0O0 [i]
        OOO00OO00O0OO000O  = OO0O00O0O0OO000O0  | OO0OOO00O00OOO0O0  | O00OO00O0OOOOO0OO  | OO0O0O00O00O00O00  | OOOOOO0O0O0O0O0OO  | O0OO000OOO0000O00  | O00O0O00000O0O0OO  | OOO0O0OOO0OOOO0OO  | OOOOOO00O000OO0OO  | O00OO0O000O0OO0O0  | O0000O000O0O0OOOO  | OOO0OOO0OOOOOOOO0  | OO00OO0OO0OOO0O0O  | O00O0OO000OOO0OOO  | O000OOOO0O0OOOOOO  | O0O0O0000OO0000O0  | OO0000OOOOOO00OO0  | OOO0OO0O00OO0O0OO  | OO0OOO00O00OO00OO  | O00O0O00OO0OO0O0O  | O00O0OOO0OOOOOOO0  | OOO0O00OO00O0OO00  | OOOOO0OO00OO0OO0O  | O00OO0O000O000O0O  | O0OOO0O000OO00OO0  | OO0O00OO000O0000O 
        return (OO0OO0OO000O00000 , OOO00OO00O0OO000O )
    def outputsLogging(OO0O0O00O000OO0OO , O0OO00OO0O0OO0000 , O00OO0O000OO000OO , OO00O0O00000OO0O0 , O000OOOOOO0OOO000 ):
        O00OO00OOO0O00000  = ['FV', 'LNGV', 'BOGH', 'WUH', 'GWH_Stm', 'LD1', 'LD2', 'HD1', 'HD2', 'SC', 'Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy', 'ME1', 'ME2', 'GE1', 'GE2', 'GE3', 'GE4', 'AB_AB1', 'AB_AB2']
        if O000OOOOOO0OOO000 ['NS_NG1-40101_PV'] == 1 and O000OOOOOO0OOO000 ['NS_NG2-40101_PV'] == 1:
            O00OO00OOO0O00000  = O00OO00OOO0O00000  + ['NG1', 'NG2']
        for asset in O00OO00OOO0O00000 :
            if O00OO0O000OO000OO [asset] == 1:
                O0O00O000OO000OO0  = asset + '_output_history'
                OO0O0O00O000OO0OO .cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [O0O00O000OO000OO0 ])
                OOOO00O0O00000O0O  = OO0O0O00O000OO0OO .cursor.fetchall()
                OO0O0O00O000OO0OO .conn.commit()
                OOOOO00O0OO0OO0OO  = [item[0] for item in OOOO00O0O00000O0O ]
                OOOOO00O0OO0OO0OO .remove('TimeStamp_onboard')
                O00O0O0OOOOOOO00O  = O00O0O0OOOOOOO00O  + '_outputs'
                for output_tag in OOOOO00O0OO0OO0OO :
                    if 'Performance_health' not in output_tag:
                        if np.isnan(O0OO00OO0O0OO0000 [O00O0O0OOOOOOO00O ][output_tag]):
                            print(output_tag)
                            print('this is nan, setting to temporary value 0')
                            O0OO00OO0O0OO0000 [O00O0O0OOOOOOO00O ][output_tag] = 0.0
                        OO0O0O00O000OO0OO .cursor.execute('update public."Output_Tags" set "Value" = %s where "TagName" = %s', [float(O0OO00OO0O0OO0000 [O00O0O0OOOOOOO00O ][output_tag]), output_tag])
                        OO0O0O00O000OO0OO .conn.commit()
                O00OOO0OOOO0OO0O0  = f"'{OO00O0O00000OO0O0 }', "
                for output_tag in OOOOO00O0OO0OO0OO :
                    if 'Performance_health' not in output_tag:
                        O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0  + f'{O0OO00OO0O0OO0000 [O00O0O0OOOOOOO00O ][output_tag]}, '
                if O00O0O0OOOOOOO00O [:-8] in ['Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy', 'ME1', 'ME2', 'GE1', 'GE2', 'GE3', 'GE4', 'NG1', 'NG2', 'AB_AB1', 'AB_AB2']:
                    O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0 [:-2]
                else:
                    O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0  + f'{100}'
                O00OOO0OOOO0OO0O0  = f'insert into public."{O0O00O000OO000OO0 }" values({O00OOO0OOOO0OO0O0 })'
                OO0O0O00O000OO0OO .cursor.execute(O00OOO0OOOO0OO0O0 )
                OO0O0O00O000OO0OO .conn.commit()
    def runningStatus(OO00OO0O0OO00OOOO , OO0O0O0000000OOO0 , OO0OO000OOOO00O00 ):
        O00OO0O000OO000OO  = {}
        if OO0O0O0000000OOO0 ['FG_FV_DischFlow'] > 100:
            O00OO0O000OO000OO ['FV'] = 1
        else:
            O00OO0O000OO000OO ['FV'] = 0
        if OO0O0O0000000OOO0 ['CM_LNGVapr_Stop'] == 0 and OO0O0O0000000OOO0 ['FG_Flow_VaprToAtm'] > 100:
            O00OO0O000OO000OO ['LNGV'] = 1
        else:
            O00OO0O000OO000OO ['LNGV'] = 0
        if OO0O0O0000000OOO0 ['FG_FV_DischFlow'] > 100:
            O00OO0O000OO000OO ['BOGH'] = 1
        else:
            O00OO0O000OO000OO ['BOGH'] = 0
        if OO0O0O0000000OOO0 ['FG_FBOG_WuHtr_OutTempInd'] - OO0O0O0000000OOO0 ['FG_FBOG_WuHtr_InTempInd'] > 10 and OO0O0O0000000OOO0 ['FG_FBOG_WuHtr_CondWtrTempInd'] - OO0O0O0000000OOO0 ['FG_FBOG_WuHtr_OutTempInd'] > 0:
            O00OO0O000OO000OO ['WUH'] = 1
        else:
            O00OO0O000OO000OO ['WUH'] = 0
        if OO0O0O0000000OOO0 ['FG_GW_MainHtr_OutTemp'] - OO0O0O0000000OOO0 ['FG_GW_MainHtr_RtnTemp'] > 5 and OO0O0O0000000OOO0 ['CM_GwCircPp1_Run'] == 1:
            O00OO0O000OO000OO ['GWH_Stm'] = 1
        else:
            O00OO0O000OO000OO ['GWH_Stm'] = 0
        if OO0O0O0000000OOO0 ['CM_LD1_Flow'] > 100:
            O00OO0O000OO000OO ['LD1'] = 1
        else:
            O00OO0O000OO000OO ['LD1'] = 0
        if OO0O0O0000000OOO0 ['CM_LD2_Flow'] > 100:
            O00OO0O000OO000OO ['LD2'] = 1
        else:
            O00OO0O000OO000OO ['LD2'] = 0
        if OO0O0O0000000OOO0 ['CM_HD1_Run'] == 1 and OO0O0O0000000OOO0 ['CM_HD1_DischPrs'] - OO0O0O0000000OOO0 ['CM_HD1_InPrsAlrmCtrl'] > 30 and (OO0O0O0000000OOO0 ['CM_HD1_IGVPosCtrl'] > 5):
            O00OO0O000OO000OO ['HD1'] = 1
        else:
            O00OO0O000OO000OO ['HD1'] = 0
        if OO0O0O0000000OOO0 ['CM_HD2_Run'] == 1 and OO0O0O0000000OOO0 ['CM_HD2_DischPrs'] - OO0O0O0000000OOO0 ['CM_HD2_InPrsAlrmCtrl'] > 30 and (OO0O0O0000000OOO0 ['CM_HD2_IGVPosCtrl'] > 5):
            O00OO0O000OO000OO ['HD2'] = 1
        else:
            O00OO0O000OO000OO ['HD2'] = 0
        if OO0O0O0000000OOO0 ['CM_LNGSubClr_CoolDownMode'] == 1 and OO0O0O0000000OOO0 ['CM_LNGSubClr_Run'] == 1:
            O00OO0O000OO000OO ['SC'] = 1
        else:
            O00OO0O000OO000OO ['SC'] = 0
        if OO0O0O0000000OOO0 ['CM_GwHtr1_Run'] == 1 or OO0O0O0000000OOO0 ['CM_GwHtr2_Run'] == 1 or OO0O0O0000000OOO0 ['CM_GwHtr3_Run'] == 1 or (OO0O0O0000000OOO0 ['CM_GwHtr4_Run'] == 1):
            O00OO0O000OO000OO ['GWH_Elec'] = 1
        else:
            O00OO0O000OO000OO ['GWH_Elec'] = 0
        if OO0O0O0000000OOO0 ['CM_GwCircPp1_Run'] == 1:
            O00OO0O000OO000OO ['GWH_StmPP'] = 1
        else:
            O00OO0O000OO000OO ['GWH_StmPP'] = 0
        if OO0O0O0000000OOO0 ['CM_GwCircPp2_Run'] == 1:
            O00OO0O000OO000OO ['GWH_ElecPP'] = 1
        else:
            O00OO0O000OO000OO ['GWH_ElecPP'] = 0
        if O00OO0O000OO000OO ['LNGV'] == 1 or O00OO0O000OO000OO ['WUH'] == 1:
            O00OO0O000OO000OO ['Cargo_vapor'] = 1
        else:
            O00OO0O000OO000OO ['Cargo_vapor'] = 0
        if O00OO0O000OO000OO ['HD1'] == 1 or O00OO0O000OO000OO ['HD2'] == 1:
            O00OO0O000OO000OO ['HD'] = 1
        else:
            O00OO0O000OO000OO ['HD'] = 0
        if O00OO0O000OO000OO ['FV'] == 1 or O00OO0O000OO000OO ['BOGH'] == 1:
            O00OO0O000OO000OO ['FBOG'] = 1
        else:
            O00OO0O000OO000OO ['FBOG'] = 0
        if O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1:
            O00OO0O000OO000OO ['NBOG'] = 1
        else:
            O00OO0O000OO000OO ['NBOG'] = 0
        O00OO0O000OO000OO ['Fuel_Consumption'] = 1
        if OO0OO000OOOO00O00 ['NS_GPS_019_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_GPS_019_PV'] > 1:
                O00OO0O000OO000OO ['Fuel_Economy'] = 1
            else:
                O00OO0O000OO000OO ['Fuel_Economy'] = 0
        else:
            O00OO0O000OO000OO ['Fuel_Economy'] = 0
        if O00OO0O000OO000OO ['GWH_Stm'] == 1 or O00OO0O000OO000OO ['GWH_Elec'] == 1:
            O00OO0O000OO000OO ['GWH'] = 1
            O00OO0O000OO000OO ['GWH_ExpTank'] = 1
        else:
            O00OO0O000OO000OO ['GWH'] = 0
            O00OO0O000OO000OO ['GWH_ExpTank'] = 0
        if OO0OO000OOOO00O00 ['NS_IG-00531_PV'] == 1:
            if OO0O0O0000000OOO0 ['FG_IG_SystemRun'] == 1 and OO0O0O0000000OOO0 ['NS_IG-00531_PV'] == 1:
                O00OO0O000OO000OO ['IG'] = 1
            else:
                O00OO0O000OO000OO ['IG'] = 0
        elif OO0O0O0000000OOO0 ['FG_IG_SystemRun'] == 1:
            O00OO0O000OO000OO ['IG'] = 1
        else:
            O00OO0O000OO000OO ['IG'] = 0
        if OO0O0O0000000OOO0 ['Elec_NGen1_SystemRun'] == 1:
            O00OO0O000OO000OO ['NG1'] = 1
        else:
            O00OO0O000OO000OO ['NG1'] = 0
        if OO0O0O0000000OOO0 ['Elec_NGen2_SystemRun'] == 1:
            O00OO0O000OO000OO ['NG2'] = 1
        else:
            O00OO0O000OO000OO ['NG2'] = 0
        if OO0O0O0000000OOO0 ['ME1_FG_Flow_InstMass'] > 100 or OO0O0O0000000OOO0 ['ME1_FO_Flow_InstMass'] > 100:
            O00OO0O000OO000OO ['ME1'] = 1
        else:
            O00OO0O000OO000OO ['ME1'] = 0
        if OO0O0O0000000OOO0 ['ME2_FG_Flow_InstMass'] > 100 or OO0O0O0000000OOO0 ['ME2_FO_Flow_InstMass'] > 100:
            O00OO0O000OO000OO ['ME2'] = 1
        else:
            O00OO0O000OO000OO ['ME2'] = 0
        if O00OO0O000OO000OO ['ME1'] == 1:
            O00OO0O000OO000OO ['MEEG_ECO1'] = 1
        else:
            O00OO0O000OO000OO ['MEEG_ECO1'] = 0
        if O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['MEEG_ECO2'] = 1
        else:
            O00OO0O000OO000OO ['MEEG_ECO2'] = 0
        if OO0O0O0000000OOO0 ['GE1_Misc_Run'] == 1:
            O00OO0O000OO000OO ['GE1'] = 1
        else:
            O00OO0O000OO000OO ['GE1'] = 0
        if OO0O0O0000000OOO0 ['GE2_Misc_Run'] == 1:
            O00OO0O000OO000OO ['GE2'] = 1
        else:
            O00OO0O000OO000OO ['GE2'] = 0
        if OO0O0O0000000OOO0 ['GE3_Misc_Run'] == 1:
            O00OO0O000OO000OO ['GE3'] = 1
        else:
            O00OO0O000OO000OO ['GE3'] = 0
        if OO0O0O0000000OOO0 ['GE4_Misc_Run'] == 1:
            O00OO0O000OO000OO ['GE4'] = 1
        else:
            O00OO0O000OO000OO ['GE4'] = 0
        if O00OO0O000OO000OO ['GE1'] == 1 or O00OO0O000OO000OO ['GE2'] == 1:
            O00OO0O000OO000OO ['GEEG_ECO1'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_ECO1'] = 0
        if O00OO0O000OO000OO ['GE3'] == 1 or O00OO0O000OO000OO ['GE4'] == 1:
            O00OO0O000OO000OO ['GEEG_ECO4'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_ECO4'] = 0
        if O00OO0O000OO000OO ['ME1'] == 1 or O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['MEEG'] = 1
        else:
            O00OO0O000OO000OO ['MEEG'] = 0
        if O00OO0O000OO000OO ['GE1'] == 1 or O00OO0O000OO000OO ['GE2'] == 1 or O00OO0O000OO000OO ['GE3'] == 1 or (O00OO0O000OO000OO ['GE4'] == 1):
            O00OO0O000OO000OO ['GEEG'] = 1
        else:
            O00OO0O000OO000OO ['GEEG'] = 0
        if OO0OO000OOOO00O00 ['NS_MM048-XI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_MM648-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM048-XI_PV'] == 1:
                O00OO0O000OO000OO ['AB_AB1'] = 1
            else:
                O00OO0O000OO000OO ['AB_AB1'] = 0
            if OO0O0O0000000OOO0 ['NS_MM648-XI_PV'] == 1:
                O00OO0O000OO000OO ['AB_AB2'] = 1
            else:
                O00OO0O000OO000OO ['AB_AB2'] = 0
        else:
            if OO0O0O0000000OOO0 ['Blr_AuxBlr1_Run'] == 1 and OO0O0O0000000OOO0 ['Blr_AuxBlr_FO_Flow_InstMass'] > 5:
                O00OO0O000OO000OO ['AB_AB1'] = 1
            else:
                O00OO0O000OO000OO ['AB_AB1'] = 0
            if OO0O0O0000000OOO0 ['Blr_AuxBlr2_Run'] == 1 and OO0O0O0000000OOO0 ['Blr_AuxBlr_FO_Flow_InstMass'] > 5:
                O00OO0O000OO000OO ['AB_AB2'] = 1
            else:
                O00OO0O000OO000OO ['AB_AB2'] = 0
        if O00OO0O000OO000OO ['AB_AB1'] == 1 or O00OO0O000OO000OO ['AB_AB2'] == 1:
            O00OO0O000OO000OO ['AB'] = 1
        else:
            O00OO0O000OO000OO ['AB'] = 0
        if OO0OO000OOOO00O00 ['NS_MM018-XI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_MM618-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM018-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriME1'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriME1'] = 0
            if OO0O0O0000000OOO0 ['NS_MM618-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriME2'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriME2'] = 0
        else:
            if OO0O0O0000000OOO0 ['ME1_LO_Puri1_InTemp'] > 78:
                O00OO0O000OO000OO ['LO_PuriME1'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriME1'] = 0
            if OO0O0O0000000OOO0 ['ME2_LO_Puri1_InTemp'] > 78:
                O00OO0O000OO000OO ['LO_PuriME2'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriME2'] = 0
        if OO0OO000OOOO00O00 ['NS_MM023-XI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_MM021-XI_PV'] == 1 and (OO0OO000OOOO00O00 ['NS_MM623-XI_PV'] == 1) and (OO0OO000OOOO00O00 ['NS_MM621-XI_PV'] == 1):
            if OO0O0O0000000OOO0 ['NS_MM021-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriGE1'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE1'] = 0
            if OO0O0O0000000OOO0 ['NS_MM023-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriGE2'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE2'] = 0
            if OO0O0O0000000OOO0 ['NS_MM621-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriGE3'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE3'] = 0
            if OO0O0O0000000OOO0 ['NS_MM623-XI_PV'] == 1:
                O00OO0O000OO000OO ['LO_PuriGE4'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE4'] = 0
        else:
            if OO0O0O0000000OOO0 ['GE_LO_GE1GE2_Puri_InTemp'] > 83 or OO0O0O0000000OOO0 ['GE_LO_GE1GE2_Puri2_InTemp'] > 83:
                O00OO0O000OO000OO ['LO_PuriGE1'] = 1
                O00OO0O000OO000OO ['LO_PuriGE2'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE1'] = 0
                O00OO0O000OO000OO ['LO_PuriGE2'] = 0
            if OO0O0O0000000OOO0 ['GE_LO_GE3GE4_Puri_InTemp'] > 83 or OO0O0O0000000OOO0 ['GE_LO_GE3GE4_Puri2_InTemp'] > 83:
                O00OO0O000OO000OO ['LO_PuriGE3'] = 1
                O00OO0O000OO000OO ['LO_PuriGE4'] = 1
            else:
                O00OO0O000OO000OO ['LO_PuriGE3'] = 0
                O00OO0O000OO000OO ['LO_PuriGE4'] = 0
        if OO0OO000OOOO00O00 ['NS_PP004-03MI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_PP043-03MI_PV'] == 1 and (OO0OO000OOOO00O00 ['NS_PP009-03MI_PV'] == 1) and (OO0OO000OOOO00O00 ['NS_PP044-03MI_PV'] == 1):
            if OO0O0O0000000OOO0 ['NS_PP004-03MI_PV'] == 1 or OO0O0O0000000OOO0 ['NS_PP043-03MI_PV'] == 1:
                O00OO0O000OO000OO ['LO_StrnTube1'] = 1
            else:
                O00OO0O000OO000OO ['LO_StrnTube1'] = 0
            if OO0O0O0000000OOO0 ['NS_PP009-03MI_PV'] == 1 or OO0O0O0000000OOO0 ['NS_PP044-03MI_PV'] == 1:
                O00OO0O000OO000OO ['LO_StrnTube2'] = 1
            else:
                O00OO0O000OO000OO ['LO_StrnTube2'] = 0
        elif O00OO0O000OO000OO ['ME1'] == 1 or O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['LO_StrnTube1'] = 1
            O00OO0O000OO000OO ['LO_StrnTube2'] = 1
        else:
            O00OO0O000OO000OO ['LO_StrnTube1'] = 0
            O00OO0O000OO000OO ['LO_StrnTube2'] = 0
        O00OO0O000OO000OO ['VA'] = 1
        if OO0OO000OOOO00O00 ['NS_PP036-03XI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_PP037-03AXI_PV'] == 1 and (OO0OO000OOOO00O00 ['NS_PP038-03AXI_PV'] == 1) and (OO0OO000OOOO00O00 ['NS_PP038-03XC_PV'] == 1):
            if OO0O0O0000000OOO0 ['NS_PP036-03XI_PV'] == 1:
                O00OO0O000OO000OO ['BLST_PP1'] = 1
            else:
                O00OO0O000OO000OO ['BLST_PP1'] = 0
            if OO0O0O0000000OOO0 ['NS_PP037-03AXI_PV'] == 1:
                O00OO0O000OO000OO ['BLST_PP2'] = 1
            else:
                O00OO0O000OO000OO ['BLST_PP2'] = 0
            if OO0O0O0000000OOO0 ['NS_PP038-03AXI_PV'] == 1 or OO0O0O0000000OOO0 ['NS_PP038-03XC_PV'] == 1:
                O00OO0O000OO000OO ['BLST_PP3'] = 1
            else:
                O00OO0O000OO000OO ['BLST_PP3'] = 0
        else:
            O00OO0O000OO000OO ['BLST_PP1'] = 1
            O00OO0O000OO000OO ['BLST_PP2'] = 1
            O00OO0O000OO000OO ['BLST_PP3'] = 1
        O00OO0O000OO000OO ['BLST'] = 1
        O00OO0O000OO000OO ['BLG'] = 1
        O00OO0O000OO000OO ['CT1'] = 1
        O00OO0O000OO000OO ['CT2'] = 1
        O00OO0O000OO000OO ['CT3'] = 1
        O00OO0O000OO000OO ['CT4'] = 1
        if O00OO0O000OO000OO ['ME1'] == 1:
            O00OO0O000OO000OO ['FW_ME1SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME1SAC'] = 0
        if O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['FW_ME2SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME2SAC'] = 0
        if O00OO0O000OO000OO ['GE1'] == 1:
            O00OO0O000OO000OO ['FW_GE1SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_GE1SAC'] = 0
        if O00OO0O000OO000OO ['GE2'] == 1:
            O00OO0O000OO000OO ['FW_GE2SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_GE2SAC'] = 0
        if O00OO0O000OO000OO ['GE3'] == 1:
            O00OO0O000OO000OO ['FW_GE3SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_GE3SAC'] = 0
        if O00OO0O000OO000OO ['GE4'] == 1:
            O00OO0O000OO000OO ['FW_GE4SAC'] = 1
        else:
            O00OO0O000OO000OO ['FW_GE4SAC'] = 0
        if OO0OO000OOOO00O00 ['NS_PP040-03MI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_PP045-03MI_PV'] == 1 and (OO0OO000OOOO00O00 ['NS_PP046-03MI_PV'] == 1):
            if OO0O0O0000000OOO0 ['NS_PP040-03MI_PV'] == 1:
                O00OO0O000OO000OO ['FW_GEwtrCircPP1'] = 1
            else:
                O00OO0O000OO000OO ['FW_GEwtrCircPP1'] = 0
            if OO0O0O0000000OOO0 ['NS_PP045-03MI_PV'] == 1:
                O00OO0O000OO000OO ['FW_GEwtrCircPP2'] = 1
            else:
                O00OO0O000OO000OO ['FW_GEwtrCircPP2'] = 0
            if OO0O0O0000000OOO0 ['NS_PP046-03MI_PV'] == 1:
                O00OO0O000OO000OO ['FW_GEwtrCircPP3'] = 1
            else:
                O00OO0O000OO000OO ['FW_GEwtrCircPP3'] = 0
        elif O00OO0O000OO000OO ['GE1'] == 1 or O00OO0O000OO000OO ['GE2'] == 1 or O00OO0O000OO000OO ['GE3'] == 1 or (O00OO0O000OO000OO ['GE4'] == 1):
            O00OO0O000OO000OO ['FW_GEwtrCircPP1'] = 1
            O00OO0O000OO000OO ['FW_GEwtrCircPP2'] = 1
            O00OO0O000OO000OO ['FW_GEwtrCircPP3'] = 1
        else:
            O00OO0O000OO000OO ['FW_GEwtrCircPP1'] = 0
            O00OO0O000OO000OO ['FW_GEwtrCircPP2'] = 0
            O00OO0O000OO000OO ['FW_GEwtrCircPP3'] = 0
        if OO0O0O0000000OOO0 ['Mach_CfwPp1_Run'] == 1:
            O00OO0O000OO000OO ['FW_CentralPP1'] = 1
        else:
            O00OO0O000OO000OO ['FW_CentralPP1'] = 0
        if OO0O0O0000000OOO0 ['Mach_CfwPp2_Run'] == 1:
            O00OO0O000OO000OO ['FW_CentralPP2'] = 1
        else:
            O00OO0O000OO000OO ['FW_CentralPP2'] = 0
        if OO0O0O0000000OOO0 ['Mach_CfwPp3_Run'] == 1:
            O00OO0O000OO000OO ['FW_CentralPP3'] = 1
        else:
            O00OO0O000OO000OO ['FW_CentralPP3'] = 0
        O00OO0O000OO000OO ['FW_BoosterPP'] = 1
        if O00OO0O000OO000OO ['ME1'] == 1:
            O00OO0O000OO000OO ['FW_ME1CFWPP1'] = 1
            O00OO0O000OO000OO ['FW_ME1CFWPP2'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME1CFWPP1'] = 0
            O00OO0O000OO000OO ['FW_ME1CFWPP2'] = 0
        if O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['FW_ME2CFWPP1'] = 1
            O00OO0O000OO000OO ['FW_ME2CFWPP2'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME2CFWPP1'] = 0
            O00OO0O000OO000OO ['FW_ME2CFWPP2'] = 0
        if OO0O0O0000000OOO0 ['Mach_CswPp1_Run'] == 1:
            O00OO0O000OO000OO ['FW_CSWPP1'] = 1
        else:
            O00OO0O000OO000OO ['FW_CSWPP1'] = 0
        if OO0O0O0000000OOO0 ['Mach_CswPp2_Run'] == 1:
            O00OO0O000OO000OO ['FW_CSWPP2'] = 1
        else:
            O00OO0O000OO000OO ['FW_CSWPP2'] = 0
        if OO0O0O0000000OOO0 ['Mach_CswPp3_Run'] == 1:
            O00OO0O000OO000OO ['FW_CSWPP3'] = 1
        else:
            O00OO0O000OO000OO ['FW_CSWPP3'] = 0
        if OO0O0O0000000OOO0 ['ME1_FO_Flow_InstMass'] > 30 or OO0O0O0000000OOO0 ['ME2_FO_Flow_InstMass'] > 30 or OO0O0O0000000OOO0 ['GE_FO_GE1GE2_Flow_InstMass'] > 30 or (OO0O0O0000000OOO0 ['GE_FO_GE3GE4_Flow_InstMass'] > 30) or (OO0O0O0000000OOO0 ['Blr_AuxBlr_FO_Flow_InstMass'] > 10):
            O00OO0O000OO000OO ['FO'] = 1
        else:
            O00OO0O000OO000OO ['FO'] = 0
        if OO0O0O0000000OOO0 ['Mach_HFOPuri1_Run'] == 1 and OO0O0O0000000OOO0 ['Mach_HFOPuri1_InTemp'] > 50 or (OO0O0O0000000OOO0 ['Mach_HFOPuri2_Run'] == 1 and OO0O0O0000000OOO0 ['Mach_HFOPuri2_InTemp'] > 50):
            O00OO0O000OO000OO ['FO_Puri'] = 1
        else:
            O00OO0O000OO000OO ['FO_Puri'] = 0
        if OO0OO000OOOO00O00 ['NS_MM944-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM944-XI_PV'] == 1:
                O00OO0O000OO000OO ['INCIN'] = 1
            else:
                O00OO0O000OO000OO ['INCIN'] = 0
        else:
            O00OO0O000OO000OO ['INCIN'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['ME1'] == 1:
            O00OO0O000OO000OO ['MEFG_ME1'] = 1
        else:
            O00OO0O000OO000OO ['MEFG_ME1'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['MEFG_ME2'] = 1
        else:
            O00OO0O000OO000OO ['MEFG_ME2'] = 0
        if O00OO0O000OO000OO ['MEFG_ME1'] == 1 or O00OO0O000OO000OO ['MEFG_ME2'] == 1:
            O00OO0O000OO000OO ['MEFG'] = 1
        else:
            O00OO0O000OO000OO ['MEFG'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['GE1'] == 1:
            O00OO0O000OO000OO ['GEFG_GE1'] = 1
        else:
            O00OO0O000OO000OO ['GEFG_GE1'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['GE2'] == 1:
            O00OO0O000OO000OO ['GEFG_GE2'] = 1
        else:
            O00OO0O000OO000OO ['GEFG_GE2'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['GE3'] == 1:
            O00OO0O000OO000OO ['GEFG_GE3'] = 1
        else:
            O00OO0O000OO000OO ['GEFG_GE3'] = 0
        if (O00OO0O000OO000OO ['LD1'] == 1 or O00OO0O000OO000OO ['LD2'] == 1) and O00OO0O000OO000OO ['GE4'] == 1:
            O00OO0O000OO000OO ['GEFG_GE4'] = 1
        else:
            O00OO0O000OO000OO ['GEFG_GE4'] = 0
        if OO0OO000OOOO00O00 ['NS_MF001-03MI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MF001-03MI_PV'] == 1:
                O00OO0O000OO000OO ['GEFG_Fan1'] = 1
            else:
                O00OO0O000OO000OO ['GEFG_Fan1'] = 0
        else:
            O00OO0O000OO000OO ['GEFG_Fan1'] = 0
        if OO0OO000OOOO00O00 ['NS_MF010-03MI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MF010-03MI_PV'] == 1:
                O00OO0O000OO000OO ['GEFG_Fan2'] = 1
            else:
                O00OO0O000OO000OO ['GEFG_Fan2'] = 0
        else:
            O00OO0O000OO000OO ['GEFG_Fan2'] = 0
        if O00OO0O000OO000OO ['GEFG_GE1'] == 1 or O00OO0O000OO000OO ['GEFG_GE2'] or O00OO0O000OO000OO ['GEFG_GE3'] or O00OO0O000OO000OO ['GEFG_GE4']:
            O00OO0O000OO000OO ['GEFG'] = 1
        else:
            O00OO0O000OO000OO ['GEFG'] = 0
        if OO0O0O0000000OOO0 ['FG_GCU1_Run'] == 1:
            O00OO0O000OO000OO ['GCU'] = 1
        else:
            O00OO0O000OO000OO ['GCU'] = 0
        if O00OO0O000OO000OO ['GE1'] == 1:
            O00OO0O000OO000OO ['GEEG_SCR1'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_SCR1'] = 0
        if O00OO0O000OO000OO ['GE2'] == 1:
            O00OO0O000OO000OO ['GEEG_SCR2'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_SCR2'] = 0
        if O00OO0O000OO000OO ['GE3'] == 1:
            O00OO0O000OO000OO ['GEEG_SCR3'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_SCR3'] = 0
        if O00OO0O000OO000OO ['GE4'] == 1:
            O00OO0O000OO000OO ['GEEG_SCR4'] = 1
        else:
            O00OO0O000OO000OO ['GEEG_SCR4'] = 0
        if OO0OO000OOOO00O00 ['NS_MM002-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM002-XI_PV'] == 1:
                O00OO0O000OO000OO ['FW_Gen1'] = 1
            else:
                O00OO0O000OO000OO ['FW_Gen1'] = 0
        else:
            O00OO0O000OO000OO ['FW_Gen1'] = 1
        if OO0OO000OOOO00O00 ['NS_MM602-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM602-XI_PV'] == 1:
                O00OO0O000OO000OO ['FW_Gen2'] = 1
            else:
                O00OO0O000OO000OO ['FW_Gen2'] = 0
        else:
            O00OO0O000OO000OO ['FW_Gen2'] = 1
        if OO0OO000OOOO00O00 ['NS_MM933-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM933-XI_PV'] == 1:
                O00OO0O000OO000OO ['FW_VFD_hydro_unit'] = 1
            else:
                O00OO0O000OO000OO ['FW_VFD_hydro_unit'] = 0
        else:
            O00OO0O000OO000OO ['FW_VFD_hydro_unit'] = 1
        if OO0OO000OOOO00O00 ['NS_MM908-03XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM908-03XI_PV'] == 1:
                O00OO0O000OO000OO ['FW_Hot_water_pp'] = 1
            else:
                O00OO0O000OO000OO ['FW_Hot_water_pp'] = 0
        else:
            O00OO0O000OO000OO ['FW_Hot_water_pp'] = 1
        if OO0OO000OOOO00O00 ['NS_MM066-XI_PV'] == 1 and OO0OO000OOOO00O00 ['NS_MM666-XI_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_MM066-XI_PV'] == 1 and OO0O0O0000000OOO0 ['NS_MM666-XI_PV'] == 1:
                O00OO0O000OO000OO ['FW_Ref'] = 1
            else:
                O00OO0O000OO000OO ['FW_Ref'] = 0
        else:
            O00OO0O000OO000OO ['FW_Ref'] = 1
        if OO0OO000OOOO00O00 ['NS_CF013-03MC_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_CF013-03MC_PV'] == 1:
                O00OO0O000OO000OO ['FW_CFW_PP1'] = 1
            else:
                O00OO0O000OO000OO ['FW_CFW_PP1'] = 0
        else:
            O00OO0O000OO000OO ['FW_CFW_PP1'] = 1
        if OO0OO000OOOO00O00 ['NS_CF014-03MC_PV'] == 1:
            if OO0O0O0000000OOO0 ['NS_CF014-03MC_PV'] == 1:
                O00OO0O000OO000OO ['FW_CFW_PP2'] = 1
            else:
                O00OO0O000OO000OO ['FW_CFW_PP2'] = 0
        else:
            O00OO0O000OO000OO ['FW_CFW_PP2'] = 1
        if O00OO0O000OO000OO ['ME1'] == 1:
            O00OO0O000OO000OO ['FW_ME1bearings'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME1bearings'] = 0
        if O00OO0O000OO000OO ['ME2'] == 1:
            O00OO0O000OO000OO ['FW_ME2bearings'] = 1
        else:
            O00OO0O000OO000OO ['FW_ME2bearings'] = 0
        if O00OO0O000OO000OO ['LO_PuriME1'] == 1 or O00OO0O000OO000OO ['LO_PuriME2'] == 1 or O00OO0O000OO000OO ['LO_PuriGE1'] == 1 or (O00OO0O000OO000OO ['LO_PuriGE2'] == 1) or (O00OO0O000OO000OO ['LO_PuriGE3'] == 1) or (O00OO0O000OO000OO ['LO_PuriGE4'] == 1) or (O00OO0O000OO000OO ['LO_StrnTube1'] == 1) or (O00OO0O000OO000OO ['LO_StrnTube2'] == 1):
            O00OO0O000OO000OO ['LO'] = 1
        else:
            O00OO0O000OO000OO ['LO'] = 0
        O00OO0O000OO000OO ['FW'] = 0
        OO0OO0OOO00OO000O  = []
        for key in O00OO0O000OO000OO .keys():
            if key[:3] == 'FW_':
                OO0OO0OOO00OO000O .append(key)
        for item in OO0OO0OOO00OO000O :
            if O00OO0O000OO000OO [item] == 1:
                O00OO0O000OO000OO ['FW'] = 1
                break
        if OO00OO0O0OO00OOOO .test_run == 1:
            for key in O00OO0O000OO000OO .keys():
                O00OO0O000OO000OO [key] = 1
        return O00OO0O000OO000OO 
    def cloudDataLogging(O0O0OO0OO0O0OO0O0 ):
        O0O0OO0OO0O0OO0O0 .cursor.execute('select "Value" from public."Application_status" where "Item" = \'Input_file\';')
        OOOO00O0O00000O0O  = O0O0OO0OO0O0OO0O0 .cursor.fetchall()
        O0O0OO0OO0O0OO0O0 .conn.commit()
        O0OOO0O00000OO000  = OOOO00O0O00000O0O [0][0]
        O00O0O000OOO0O0OO  = O0OOO0O00000OO000 [-19:-11]
        O0OO0O0O0OOO0O00O  = O0O0OO0OO0O0OO0O0 .simfiles_path + '/' + O00O0O000OOO0O0OO 
        OO00OOOOOOO0O0O00  = natsorted(os.listdir(O0OO0O0O0OOO0O00O ))
        for i in range(len(OO00OOOOOOO0O0O00 )):
            if OO00OOOOOOO0O0O00 [i] == O0OOO0O00000OO000 :
                print('previously flagged file is:', O0OOO0O00000OO000 )
                if i == len(OO00OOOOOOO0O0O00 ) - 1:
                    print('no more file available')
                    O0O000O000OOO0000  = natsorted(os.listdir(O0O0OO0OO0O0OO0O0 .simfiles_path))
                    for j in range(len(O0O000O000OOO0000 )):
                        if O0O000O000OOO0000 [j] == O00O0O000OOO0O0OO :
                            if j == len(O0O000O000OOO0000 ) - 1:
                                print('no more folder is available')
                                OO0O00OOOO0OO0000  = 'Holding'
                                print('switch to:', OO0O00OOOO0OO0000 )
                            else:
                                O00O0O000OOO0O0OO  = O0O000O000OOO0000 [j + 1]
                                print('next day folder is:', O00O0O000OOO0O0OO )
                                O0OO0O0O0OOO0O00O  = O0O0OO0OO0O0OO0O0 .simfiles_path + '/' + O00O0O000OOO0O0OO 
                                OO00OOOOOOO0O0O00  = natsorted(os.listdir(O0OO0O0O0OOO0O00O ))
                                if len(OO00OOOOOOO0O0O00 ) == 0:
                                    print('new folder is empty')
                                    OO0O00OOOO0OO0000  = 'Holding'
                                    print('switch to:', OO0O00OOOO0OO0000 )
                                else:
                                    O0OOO0O00000OO000  = OO00OOOOOOO0O0O00 [0]
                                    print('sim file in next day folder:', O0OOO0O00000OO000 )
                                    print('next file to read is:', O0OOO0O00000OO000 )
                                    if len(OO00OOOOOOO0O0O00 ) > 1:
                                        OO0O00OOOO0OO0000  = 'Playback'
                                        print('switch to :', OO0O00OOOO0OO0000 )
                                    else:
                                        OO0O00OOOO0OO0000  = 'Normal'
                                        print('switch to:', OO0O00OOOO0OO0000 )
                                    break
                else:
                    O0OOO0O00000OO000  = OO00OOOOOOO0O0O00 [i + 1]
                    print('next file to read is:', O0OOO0O00000OO000 )
                    OOOOOO00000O000O0  = len(OO00OOOOOOO0O0O00 ) - i
                    if OOOOOO00000O000O0  > 2:
                        OO0O00OOOO0OO0000  = 'Playback'
                        print('switch to :', OO0O00OOOO0OO0000 )
                    else:
                        OO0O00OOOO0OO0000  = 'Normal'
                    break
        if OO0O00OOOO0OO0000  == 'Normal':
            O0OO00000OOOOO00O  = 60
        elif OO0O00OOOO0OO0000  == 'Playback':
            O0OO00000OOOOO00O  = 0.01
        elif OO0O00OOOO0OO0000  == 'Holding':
            O0OO00000OOOOO00O  = 5
        else:
            O0OO00000OOOOO00O  = 5
        O0O0OO0OO0O0OO0O0 .cursor.execute(f"""update public."Application_status" set "Value" = %s where "Item" = 'Input_file';""", [O0OOO0O00000OO000 ])
        O0O0OO0OO0O0OO0O0 .conn.commit()
        O0O0OO0OO0O0OO0O0 .cursor.execute('update public."Application_status" set "Value" = %s where "Item" = \'Status\';', [OO0O00OOOO0OO0000 ])
        O0O0OO0OO0O0OO0O0 .conn.commit()
        O0O0OO0OO0O0OO0O0 .cursor.execute('update public."Application_status" set "Value" = %s where "Item" = \'Frequency\';', [str(O0OO00000OOOOO00O )])
        O0O0OO0OO0O0OO0O0 .conn.commit()
        if OO0O00OOOO0OO0000  == 'Normal' or OO0O00OOOO0OO0000  == 'Playback':
            print('proceeding with status:', OO0O00OOOO0OO0000 )
            OO0000OO00OO00OO0  = O0O0OO0OO0O0OO0O0 .simfiles_path + '/' + O00O0O000OOO0O0OO  + '/' + O0OOO0O00000OO000 
            with open(OO0000OO00OO00OO0 ) as f:
                O0O0000O0O00O00O0  = f.readlines()
            print('len of lines:', len(O0O0000O0O00O00O0 ))
            if len(O0O0000O0O00O00O0 ) == 2:
                OOOO00O0OO00OOO00  = O0O0000O0O00O00O0 [0]
                OOOO0OO00O00O00OO  = O0O0000O0O00O00O0 [1]
                OOO00O000OOOOOOO0  = OOOO00O0OO00OOO00 .split(',')
                O0OO00OOOOO00O0OO  = OOOO0OO00O00O00OO .split(',')
                OO0OOO00000000OO0  = ['names', 'sample1']
                OOOO0O0OOO00O00O0  = [OOO00O000OOOOOOO0 , O0OO00OOOOO00O0OO ]
                if len(OOO00O000OOOOOOO0 ) == len(O0OO00OOOOO00O0OO ):
                    OO000OO0OO0O00000  = {}
                    for i in range(len(OOO00O000OOOOOOO0 )):
                        OO000OO0OO0O00000 [OOO00O000OOOOOOO0 [i]] = [O0OO00OOOOO00O0OO [i]]
                else:
                    print('tags and samples size not same')
            elif len(O0O0000O0O00O00O0 ) == 3:
                OOOO00O0OO00OOO00  = O0O0000O0O00O00O0 [0]
                OOOO0OO00O00O00OO  = O0O0000O0O00O00O0 [1]
                O0O00000OO0000000  = O0O0000O0O00O00O0 [2]
                OOO00O000OOOOOOO0  = OOOO00O0OO00OOO00 .split(',')
                O0OO00OOOOO00O0OO  = OOOO0OO00O00O00OO .split(',')
                OOO0O00O0O0OO00OO  = O0O00000OO0000000 .split(',')
                OO0OOO00000000OO0  = ['names', 'sample1', 'sample2']
                OOOO0O0OOO00O00O0  = [OOO00O000OOOOOOO0 , O0OO00OOOOO00O0OO , OOO0O00O0O0OO00OO ]
                if len(OOO00O000OOOOOOO0 ) == len(O0OO00OOOOO00O0OO ) == len(OOO0O00O0O0OO00OO ):
                    OO000OO0OO0O00000  = {}
                    for i in range(len(OOO00O000OOOOOOO0 )):
                        OO000OO0OO0O00000 [OOO00O000OOOOOOO0 [i]] = [O0OO00OOOOO00O0OO [i], OOO0O00O0O0OO00OO [i]]
                else:
                    print('tags and samples size not same')
            elif len(O0O0000O0O00O00O0 ) == 4:
                OOOO00O0OO00OOO00  = O0O0000O0O00O00O0 [0]
                OOOO0OO00O00O00OO  = O0O0000O0O00O00O0 [1]
                O0O00000OO0000000  = O0O0000O0O00O00O0 [2]
                OOOOOOOOOO000O000  = O0O0000O0O00O00O0 [3]
                OOO00O000OOOOOOO0  = OOOO00O0OO00OOO00 .split(',')
                O0OO00OOOOO00O0OO  = OOOO0OO00O00O00OO .split(',')
                OOO0O00O0O0OO00OO  = O0O00000OO0000000 .split(',')
                O0O00OOO0O0000O0O  = OOOOOOOOOO000O000 .split(',')
                OO0OOO00000000OO0  = ['names', 'sample1', 'sample2', 'sample3']
                OOOO0O0OOO00O00O0  = [OOO00O000OOOOOOO0 , O0OO00OOOOO00O0OO , OOO0O00O0O0OO00OO , O0O00OOO0O0000O0O ]
                if len(OOO00O000OOOOOOO0 ) == len(O0OO00OOOOO00O0OO ) == len(OOO0O00O0O0OO00OO ) == len(O0O00OOO0O0000O0O ):
                    OO000OO0OO0O00000  = {}
                    for i in range(len(OOO00O000OOOOOOO0 )):
                        OO000OO0OO0O00000 [OOO00O000OOOOOOO0 [i]] = [O0OO00OOOOO00O0OO [i], OOO0O00O0O0OO00OO [i], O0O00OOO0O0000O0O [i]]
                else:
                    print('tags and samples size not same')
            elif len(O0O0000O0O00O00O0 ) == 5:
                OOOO00O0OO00OOO00  = O0O0000O0O00O00O0 [0]
                OOOO0OO00O00O00OO  = O0O0000O0O00O00O0 [1]
                O0O00000OO0000000  = O0O0000O0O00O00O0 [2]
                OOOOOOOOOO000O000  = O0O0000O0O00O00O0 [3]
                O00O0O000O0O0O0O0  = O0O0000O0O00O00O0 [4]
                OOO00O000OOOOOOO0  = OOOO00O0OO00OOO00 .split(',')
                O0OO00OOOOO00O0OO  = OOOO0OO00O00O00OO .split(',')
                OOO0O00O0O0OO00OO  = O0O00000OO0000000 .split(',')
                O0O00OOO0O0000O0O  = OOOOOOOOOO000O000 .split(',')
                OOO00O000O0O0OOO0  = O00O0O000O0O0O0O0 .split(',')
                OO0OOO00000000OO0  = ['names', 'sample1', 'sample2', 'sample3', 'sample4']
                OOOO0O0OOO00O00O0  = [OOO00O000OOOOOOO0 , O0OO00OOOOO00O0OO , OOO0O00O0O0OO00OO , O0O00OOO0O0000O0O , OOO00O000O0O0OOO0 ]
                if len(OOO00O000OOOOOOO0 ) == len(O0OO00OOOOO00O0OO ) == len(OOO0O00O0O0OO00OO ) == len(O0O00OOO0O0000O0O ) == len(OOO00O000O0O0OOO0 ):
                    OO000OO0OO0O00000  = {}
                    for i in range(len(OOO00O000OOOOOOO0 )):
                        OO000OO0OO0O00000 [OOO00O000OOOOOOO0 [i]] = [O0OO00OOOOO00O0OO [i], OOO0O00O0O0OO00OO [i], O0O00OOO0O0000O0O [i], OOO00O000O0O0OOO0 [i]]
                else:
                    print('tags and samples size not same')
            elif len(O0O0000O0O00O00O0 ) == 6:
                OOOO00O0OO00OOO00  = O0O0000O0O00O00O0 [0]
                OOOO0OO00O00O00OO  = O0O0000O0O00O00O0 [1]
                O0O00000OO0000000  = O0O0000O0O00O00O0 [2]
                OOOOOOOOOO000O000  = O0O0000O0O00O00O0 [3]
                O00O0O000O0O0O0O0  = O0O0000O0O00O00O0 [4]
                O0OO0000OO0OOO0OO  = O0O0000O0O00O00O0 [5]
                OOO00O000OOOOOOO0  = OOOO00O0OO00OOO00 .split(',')
                O0OO00OOOOO00O0OO  = OOOO0OO00O00O00OO .split(',')
                OOO0O00O0O0OO00OO  = O0O00000OO0000000 .split(',')
                O0O00OOO0O0000O0O  = OOOOOOOOOO000O000 .split(',')
                OOO00O000O0O0OOO0  = O00O0O000O0O0O0O0 .split(',')
                OO0000OO000000000  = O0OO0000OO0OOO0OO .split(',')
                OO0OOO00000000OO0  = ['names', 'sample1', 'sample2', 'sample3', 'sample4', 'sample5']
                OOOO0O0OOO00O00O0  = [OOO00O000OOOOOOO0 , O0OO00OOOOO00O0OO , OOO0O00O0O0OO00OO , O0O00OOO0O0000O0O , OOO00O000O0O0OOO0 , OO0000OO000000000 ]
                if len(OOO00O000OOOOOOO0 ) == len(O0OO00OOOOO00O0OO ) == len(OOO0O00O0O0OO00OO ) == len(O0O00OOO0O0000O0O ) == len(OOO00O000O0O0OOO0 ) == len(OO0000OO000000000 ):
                    OO000OO0OO0O00000  = {}
                    for i in range(len(OOO00O000OOOOOOO0 )):
                        OO000OO0OO0O00000 [OOO00O000OOOOOOO0 [i]] = [O0OO00OOOOO00O0OO [i], OOO0O00O0O0OO00OO [i], O0O00OOO0O0000O0O [i], OOO00O000O0O0OOO0 [i], OO0000OO000000000 [i]]
                else:
                    print('tags and samples size not same')
            OO000O0O0OO0OO0O0  = len(O0O0000O0O00O00O0 ) - 1
            return (OO000OO0OO0O00000 , OO000O0O0OO0OO0O0 , OO0O00OOOO0OO0000 , O0OO00000OOOOO00O )
        else:
            OO000OO0OO0O00000  = {}
            OO000O0O0OO0OO0O0  = 0
            return (OO000OO0OO0O00000 , OO000O0O0OO0OO0O0 , OO0O00OOOO0OO0000 , O0OO00000OOOOO00O )
    def inputsLogging(OOO00OOOOOO00O00O , O00O0O00O000OOO00 , O0OO0O0OOOOOO00OO , O00000O0000O0O00O , O000O00O0O0OOO00O ):
        OO00O0O00000OO0O0  = O00000O0000O0O00O ['Nav_GPS1_UTC']
        OOO00OOOOOO00O00O .cursor.execute('update public."Application_status" set "Value" = %s where "Item" = \'TimeStamp_onboard\';', [OO00O0O00000OO0O0 ])
        OOO00OOOOOO00O00O .conn.commit()
        O00O00OO00OO0OOO0  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if OOO00OOOOOO00O00O .log_inputs_realtime == 1:
            for tag in O0OO0O0OOOOOO00OO :
                if tag == 'Nav_GPS1_UTC':
                    OOO00OOOOOO00O00O .cursor.execute('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s', [OO00O0O00000OO0O0 , tag])
                    OOO00OOOOOO00O00O .conn.commit()
                elif O000O00O0O0OOO00O [tag] == 1:
                    OOOOOOOO00000O000  = str(O00000O0000O0O00O [tag])
                    O0O0O0O0O00000O00  = True
                    if len(OOOOOOOO00000O000 ) == 0:
                        OOOOOOOO00000O000  = 999
                        O0O0O0O0O00000O00  = False
                    OOO00OOOOOO00O00O .cursor.execute('update public."Input_Tags" set "Value" = %s where "Standard_Key" = %s', [float(OOOOOOOO00000O000 ), tag])
                    OOO00OOOOOO00O00O .conn.commit()
                    OOO00OOOOOO00O00O .cursor.execute('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s', [O00O00OO00OO0OOO0 , tag])
                    OOO00OOOOOO00O00O .conn.commit()
        print('value no. ', O00O0O00O000OOO00 , ' is done. TimeStamp is :', O00000O0000O0O00O ['Nav_GPS1_UTC'])
        if OOO00OOOOOO00O00O .log_inputs_history == 1:
            OO000O0O000O000OO  = ['Input_history1', 'Input_history2', 'Input_history3', 'Input_history4', 'Input_history5', 'Input_history6']
            O000000OOO0OO0000  = {}
            for key in O00000O0000O0O00O .keys():
                OOOOOOOO00000O000  = O00000O0000O0O00O [key]
                O00OO0OO0OO0O0O0O  = O00OO0OO0OO0O0O0O .replace('-', '_')
                O000000OOO0OO0000 [O00OO0OO0OO0O0O0O ] = OOOOOOOO00000O000 
            for O0O00O000OO000OO0  in OO000O0O000O000OO :
                OOO00OOOOOO00O00O .cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [O0O00O000OO000OO0 ])
                OOOO00O0O00000O0O  = OOO00OOOOOO00O00O .cursor.fetchall()
                OOO00OOOOOO00O00O .conn.commit()
                OO0O0OOO0OOO0OO00  = [item[0] for item in OOOO00O0O00000O0O ]
                OO0O0OOO0OOO0OO00 .remove('Nav_GPS1_UTC')
                OO0O0OOO0OOO0OO00 .remove('TimeStamp')
                O00OOO0OOOO0OO0O0  = f"""insert into public."{O0O00O000OO000OO0 }" values('{O00O00OO00OO0OOO0 }', '{OO00O0O00000OO0O0 }',"""
                for col in OO0O0OOO0OOO0OO00 :
                    O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0  + f'{O000000OOO0OO0000 [col]}, '
                O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0 [:-2] + ')'
                OOO00OOOOOO00O00O .cursor.execute(O00OOO0OOOO0OO0O0 )
                OOO00OOOOOO00O00O .conn.commit()
        return OO00O0O00000OO0O0 
    def findConditionsStatus(O0OO00OO00O000OO0 , O00OO0000O0O0O00O , OO00O0O0O00O0OO0O ):
        O0OOOO0O0OO0OO0O0  = False
        OO0O0OO0OOO00O0O0  = False
        OOO00O000O000O0OO  = False
        O00O00O00O00OO0O0  = False
        O00000O0OOOOOO000  = False
        OOOO0O000OOOO0OO0  = False
        OO0O00O0O0000OO0O  = 0
        OO00OO000OO0O00O0  = 0
        O0O0OO000O0000OO0  = True
        if len(O00OO0000O0O0O00O ) == 2:
            if 'standard deviation' in O00OO0000O0O0O00O [0]:
                O0OOOO0O0OO0OO0O0  = True
                OO0O00O0O0000OO0O  = int(O00OO0000O0O0O00O [1])
            elif 'moving average' in O00OO0000O0O0O00O [0]:
                OO0O0OO0OOO00O0O0  = True
                OO0O00O0O0000OO0O  = int(O00OO0000O0O0O00O [1])
            elif 'delta' in O00OO0000O0O0O00O [0]:
                OOO00O000O000O0OO  = True
                OO0O00O0O0000OO0O  = int(O00OO0000O0O0O00O [1])
            elif 'subtract' in O00OO0000O0O0O00O [0]:
                O00000O0OOOOOO000  = True
            elif 'sum' in O00OO0000O0O0O00O [0]:
                OOOO0O000OOOO0OO0  = True
            else:
                O0O0OO000O0000OO0  = False
        elif len(O00OO0000O0O0O00O ) > 2 and ('subtract' in O00OO0000O0O0O00O [0] or 'sum' in O00OO0000O0O0O00O [0]):
            if 'subtract' in O00OO0000O0O0O00O [0]:
                O00000O0OOOOOO000  = True
            elif 'sum' in O00OO0000O0O0O00O [0]:
                OOOO0O000OOOO0OO0  = True
            else:
                O0O0OO000O0000OO0  = False
        elif len(O00OO0000O0O0O00O ) == 4:
            if 'moving average' in O00OO0000O0O0O00O [0] and 'delta' in O00OO0000O0O0O00O [2]:
                O00O00O00O00OO0O0  = True
                OO0O00O0O0000OO0O  = int(O00OO0000O0O0O00O [1])
                OO00OO000OO0O00O0  = int(O00OO0000O0O0O00O [3])
            else:
                O0O0OO000O0000OO0  = False
        else:
            O0O0OO000O0000OO0  = False
        if OO00O0O0O00O0OO0O  == O0OO00OO00O000OO0 .for_test:
            print('condition exists=>', O0O0OO000O0000OO0 )
            print('condition list=>', O00OO0000O0O0O00O )
        return (O0OOOO0O0OO0OO0O0 , OO0O0OO0OOO00O0O0 , OOO00O000O000O0OO , O00000O0OOOOOO000 , OOOO0O000OOOO0OO0 , O00O00O00O00OO0O0 , OO0O00O0O0000OO0O , OO00OO000OO0O00O0 , O0O0OO000O0000OO0 )
    def calcAggregate(O00O00O00OOOOO0OO , O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O00000000OO0000O0 , OO00O0OO0O0000O00 ):
        O00O0OOO00OO0O000  = OO00O0OO0O0000O00  + '__' + O00000000OO0000O0 
        if O00OO0O0000O0OOO0 :
            O0OOOO00000O0O00O  = sum(O00O00O00OOOOO0OO .agg[O00O0OOO00OO0O000 ]) / len(O00O00O00OOOOO0OO .agg[O00O0OOO00OO0O000 ])
        elif O0OOO000O00OO0OOO :
            O0OOOO00000O0O00O  = np.std(O00O00O00OOOOO0OO .agg[O00O0OOO00OO0O000 ])
        return O0OOOO00000O0O00O 
    def tagNotExists_inSampleList(O000O000O000O0O0O , O0O0OOO00O000OOOO , O000OO0OO0O0OOOOO , OO00OO0O00OOO0OO0 , OO0O00O0OOOOO00OO ):
        O000O000O000O0O0O .agg[OO00OO0O00OOO0OO0 ] = [O000OO0OO0O0OOOOO [O0O0OOO00O000OOOO ]]
        O0OOO00OO000OOOOO  = False
        if OO0O00O0OOOOO00OO  == O000O000O000O0O0O .for_test:
            print('fell into function: tagNotExists_inSampleList(). latest samples are: ', O000O000O000O0O0O .agg[OO00OO0O00OOO0OO0 ])
        return O0OOO00OO000OOOOO 
    def tagExists_butSampleSizeTooShort(O0OO0O0O00O0O0OOO , OOOO00OO000000000 , O00O00O0OOOOOO00O , OOOO0OOO00OOO0O0O , OOOOOOO00OO00OOOO ):
        O0OO0O0O00O0O0OOO .agg[OOOO0OOO00OOO0O0O ].append(O00O00O0OOOOOO00O [OOOO00OO000000000 ])
        O0OOO00OO000OOOOO  = False
        if OOOOOOO00OO00OOOO  == O0OO0O0O00O0O0OOO .for_test:
            print('fell into function: tagExists_butSampleSizeTooShort(). latest samples are: ', O0OO0O0O00O0O0OOO .agg[OOOO0OOO00OOO0O0O ])
        return O0OOO00OO000OOOOO 
    def SampleSizeOneShort(OOO000OOOO00OOO00 , OOO0O0O00O000O00O , O000OO0OOO0O0000O , O0OO0OOOOOOO0OOO0 , O0OOO00O0OO0OO0O0 ):
        OOO000OOOO00OOO00 .agg[O0OO0OOOOOOO0OOO0 ].append(O000OO0OOO0O0000O [OOO0O0O00O000O00O ])
        O0OOO00OO000OOOOO  = True
        if O0OOO00O0OO0OO0O0  == OOO000OOOO00OOO00 .for_test:
            print('fell into function: SampleSizeOneShort(). 1 is added now and latest samples are okay for calculation: ', OOO000OOOO00OOO00 .agg[O0OO0OOOOOOO0OOO0 ])
        return O0OOO00OO000OOOOO 
    def SampleSizeOK(OO0OO0O00O0OO000O , O0OO00OOOO00000OO , O0000O0O00000OOO0 , O0O0OO000OO00O000 , OOOO0O00O000O00OO ):
        OO0OO0O00O0OO000O .agg[O0O0OO000OO00O000 ].pop(0)
        OO0OO0O00O0OO000O .agg[O0O0OO000OO00O000 ].append(O0000O0O00000OOO0 [O0OO00OOOO00000OO ])
        O0OOO00OO000OOOOO  = True
        if OOOO0O00O000O00OO  == OO0OO0O00O0OO000O .for_test:
            print('fell into function: SampleSizeOK(). latest is appended now and oldest is popped, and latest samples are okay for calculation: ', OO0OO0O00O0OO000O .agg[O0O0OO000OO00O000 ])
        return O0OOO00OO000OOOOO 
    def tagNotExists_inMAvgList(O00OOOO00OO000O00 , OO00OOOOOOOO0O000 , OO0OOOO0000OO00OO , OOOO00000OOO0O00O ):
        O000000OOO00OOO0O  = sum(O00OOOO00OO000O00 .agg[OO0OOOO0000OO00OO ]) / len(O00OOOO00OO000O00 .agg[OO0OOOO0000OO00OO ])
        O00OOOO00OO000O00 .mavg_samples[OO0OOOO0000OO00OO ] = [O000000OOO00OOO0O ]
        O0OOO00OO000OOOOO  = False
        if OOOO00000OOO0O00O  == O00OOOO00OO000O00 .for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', OO0OOOO0000OO00OO , ' are ', O00OOOO00OO000O00 .mavg_samples, 'it ended up in tagNotExists_inMAvgList()')
        return O0OOO00OO000OOOOO 
    def MAvgSampleSizeTooShort(OO00OO0O0O0O0OO00 , O0O00OO0O0O00O000 , OO0OO0OO0OO0O0OOO , O0O0O000OOOO0O00O ):
        O000000OOO00OOO0O  = sum(OO00OO0O0O0O0OO00 .agg[OO0OO0OO0OO0O0OOO ]) / len(OO00OO0O0O0O0OO00 .agg[OO0OO0OO0OO0O0OOO ])
        OO00OO0O0O0O0OO00 .mavg_samples[OO0OO0OO0OO0O0OOO ].append(O000000OOO00OOO0O )
        O0OOO00OO000OOOOO  = False
        if O0O0O000OOOO0O00O  == OO00OO0O0O0O0OO00 .for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', OO0OO0OO0OO0O0OOO , ' are ', OO00OO0O0O0O0OO00 .mavg_samples, 'it ended up in MAvgSampleSizeTooShort()')
        return O0OOO00OO000OOOOO 
    def MAvgSampleSizeOneShort(O0000O00OO00OO0OO , OOOO0OO0O0000OOO0 , O0O0O00000O000O0O , O0O00O0OO0O0O0O0O ):
        O000000OOO00OOO0O  = sum(O0000O00OO00OO0OO .agg[O0O0O00000O000O0O ]) / len(O0000O00OO00OO0OO .agg[O0O0O00000O000O0O ])
        O0000O00OO00OO0OO .mavg_samples[O0O0O00000O000O0O ].append(O000000OOO00OOO0O )
        O0OOO00OO000OOOOO  = True
        if O0O00O0OO0O0O0O0O  == O0000O00OO00OO0OO .for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', O0O0O00000O000O0O , ' are ', O0000O00OO00OO0OO .mavg_samples, 'it ended up in MAvgSampleSizeOneShort()')
        return O0OOO00OO000OOOOO 
    def MAvgSampleSizeOK(OOO000O0O00O00O00 , OO0O0O0O00OOOO000 , O00000O0OO000OOO0 , OO0O0OO0O00OOO0OO ):
        OOO000O0O00O00O00 .mavg_samples[O00000O0OO000OOO0 ].pop(0)
        O000000OOO00OOO0O  = sum(OOO000O0O00O00O00 .agg[O00000O0OO000OOO0 ]) / len(OOO000O0O00O00O00 .agg[O00000O0OO000OOO0 ])
        OOO000O0O00O00O00 .mavg_samples[O00000O0OO000OOO0 ].append(O000000OOO00OOO0O )
        O0OOO00OO000OOOOO  = True
        if OO0O0OO0O00OOO0OO  == OOO000O0O00O00O00 .for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', O00000O0OO000OOO0 , ' are ', OOO000O0O00O00O00 .mavg_samples, 'it ended up in MAvgSampleSizeOK()')
        return O0OOO00OO000OOOOO 
    def checkSamplesStatus(O0OO00O000000OOO0 , OOO000O000OOO0O0O , OOOOO00OOO0O00000 , O0OO00OOO0000O000 , OO00O0O0O000OOO0O , OOOOO000O0OO000O0 , OO0OOOOOOOOOOOO00 , O0OOOO00OO0OO0OOO , O0O0OOO0000OOO0O0 ):
        O00000O0OO000OOO0  = O0O0OOO0000OOO0O0  + '__' + OOO000O000OOO0O0O 
        if O00000O0OO000OOO0  not in O0OO00O000000OOO0 .agg.keys():
            OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .tagNotExists_inSampleList(OOO000O000OOO0O0O , OOOOO00OOO0O00000 , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
        elif O00000O0OO000OOO0  in O0OO00O000000OOO0 .agg.keys():
            if len(O0OO00O000000OOO0 .agg[O00000O0OO000OOO0 ]) + 1 < O0OO00OOO0000O000 :
                OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .tagExists_butSampleSizeTooShort(OOO000O000OOO0O0O , OOOOO00OOO0O00000 , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
            elif len(O0OO00O000000OOO0 .agg[O00000O0OO000OOO0 ]) + 1 == O0OO00OOO0000O000 :
                OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .SampleSizeOneShort(OOO000O000OOO0O0O , OOOOO00OOO0O00000 , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
            elif len(O0OO00O000000OOO0 .agg[O00000O0OO000OOO0 ]) + 1 > O0OO00OOO0000O000 :
                OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .SampleSizeOK(OOO000O000OOO0O0O , OOOOO00OOO0O00000 , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
        if O0O0OOO0000OOO0O0  == O0OO00O000000OOO0 .for_test:
            print('samples_ok: ', OO00O0O0O000OOO0O )
        if OOOOO000O0OO000O0 :
            if OO00O0O0O000OOO0O :
                if O0O0OOO0000OOO0O0  == O0OO00O000000OOO0 .for_test:
                    print('raw samples are collected well at point', 'point+1(point NA now)')
                if O00000O0OO000OOO0  not in O0OO00O000000OOO0 .mavg_samples.keys():
                    OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .tagNotExists_inMAvgList(OOO000O000OOO0O0O , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
                elif O00000O0OO000OOO0  in O0OO00O000000OOO0 .mavg_samples.keys():
                    if len(O0OO00O000000OOO0 .mavg_samples[O00000O0OO000OOO0 ]) + 1 < OO0OOOOOOOOOOOO00 :
                        OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .MAvgSampleSizeTooShort(OOO000O000OOO0O0O , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
                    elif len(O0OO00O000000OOO0 .mavg_samples[O00000O0OO000OOO0 ]) + 1 == OO0OOOOOOOOOOOO00 :
                        OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .MAvgSampleSizeOneShort(OOO000O000OOO0O0O , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
                    elif len(O0OO00O000000OOO0 .mavg_samples[O00000O0OO000OOO0 ]) + 1 > OO0OOOOOOOOOOOO00 :
                        OO00O0O0O000OOO0O  = O0OO00O000000OOO0 .MAvgSampleSizeOK(OOO000O000OOO0O0O , O00000O0OO000OOO0 , O0O0OOO0000OOO0O0 )
            if O0O0OOO0000OOO0O0  == O0OO00O000000OOO0 .for_test:
                if OO00O0O0O000OOO0O :
                    print('mavg samples are collected well at point', 'point+1(point NA now)')
        return OO00O0O0O000OOO0O 
    def moreThan(O00O0OO0OOOOO00OO , OO0O0O00O0O0OO000 , OOOO000OOO0O0O0O0 , OOO0OO00OOOOO0000 , OOOO0OO0O000OOO0O , OO0O00OO0O0OOO00O , OOOOOO0O000OO00O0 , O000OOO000O00O0O0 ):
        OO0O00OO0O0OOO00O  = float(OO0O00OO0O0OOO00O )
        O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , OOO00O000O000O0OO , O00000O0OOOOOO000 , OOOO0O000OOOO0OO0 , OOOOO000O0OO000O0 , O0OO00OOO0000O000 , OO0OOOOOOOOOOOO00 , O0O0OO000O0000OO0  = O00O0OO0OOOOO00OO .findConditionsStatus(OOOO000OOO0O0O0O0 , O000OOO000O00O0O0 )
        OOOOO0OO0O0O00O00  = 1
        if O0O0OO000O0000OO0 :
            if OOOO0O000OOOO0OO0  == True or O00000O0OOOOOO000  == True:
                OO00O0O0O000OOO0O  = True
            else:
                OO00O0O0O000OOO0O  = False
                OO00O0O0O000OOO0O  = O00O0OO0OOOOO00OO .checkSamplesStatus(OOO0OO00OOOOO0000 , OOOO0OO0O000OOO0O , O0OO00OOO0000O000 , OO00O0O0O000OOO0O , OOOOO000O0OO000O0 , OO0OOOOOOOOOOOO00 , OOOO000OOO0O0O0O0 , O000OOO000O00O0O0 )
            if OO00O0O0O000OOO0O  == False:
                O00OOO0OO0OO000OO  = 'Unknown'
            elif OO00O0O0O000OOO0O :
                O00O0OOO00OO0O000  = O000OOO000O00O0O0  + '__' + OOO0OO00OOOOO0000 
                if O0OOO000O00OO0OOO  == True or O00OO0O0000O0OOO0  == True:
                    O0OOOO00000O0O00O  = O00O0OO0OOOOO00OO .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , OOO0OO00OOOOO0000 , O000OOO000O00O0O0 )
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print('collected raw samples are: ', O00O0OO0OOOOO00OO .agg[O000OOO000O00O0O0  + '__' + OOO0OO00OOOOO0000 ], 'threshold is: ', OO0O00OO0O0OOO00O , 'calculated agg value:', O0OOOO00000O0O00O )
                    if O0OOOO00000O0O00O  > OO0O00OO0O0OOO00O :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOO00O000O000O0OO :
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print('collected raw samples are: ', O00O0OO0OOOOO00OO .agg[O00O0OOO00OO0O000 ], 'threshold is: ', OO0O00OO0O0OOO00O )
                    if 'absolute' in OOOO000OOO0O0O0O0 [0]:
                        if abs(OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ] - O00O0OO0OOOOO00OO .agg[O00O0OOO00OO0O000 ][0]) > OO0O00OO0O0OOO00O :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ] - O00O0OO0OOOOO00OO .agg[O00O0OOO00OO0O000 ][0] > OO0O00OO0O0OOO00O :
                        if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                            print('current point', OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ])
                            print('point in sample', O00O0OO0OOOOO00OO .agg[O00O0OOO00OO0O000 ][0])
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOOO000O0OO000O0 :
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print('collected mavg samples are: ', O00O0OO0OOOOO00OO .mavg_samples[O00O0OOO00OO0O000 ], 'threshold is: ', OO0O00OO0O0OOO00O )
                    if 'absolute' in OOOO000OOO0O0O0O0 [2]:
                        if abs(O00O0OO0OOOOO00OO .mavg_samples[O00O0OOO00OO0O000 ][-1] - O00O0OO0OOOOO00OO .mavg_samples[O00O0OOO00OO0O000 ][0]) > OO0O00OO0O0OOO00O :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif O00O0OO0OOOOO00OO .mavg_samples[O00O0OOO00OO0O000 ][-1] - O00O0OO0OOOOO00OO .mavg_samples[O00O0OOO00OO0O000 ][0] > OO0O00OO0O0OOO00O :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif O00000O0OOOOOO000 :
                    OOOOOOOO00000O000  = OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ]
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print(OOOOOOOO00000O000 )
                    for O00O0O00O000OOO00  in range(1, len(OOOO000OOO0O0O0O0 )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  - OOOO0OO0O000OOO0O [OOOO000OOO0O0O0O0 [O00O0O00O000OOO00 ]]
                        if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print('value after subtracting given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in OO0O0O00O0O0OO000 :
                        if abs(OOOOOOOO00000O000 ) > OO0O00OO0O0OOO00O :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  > OO0O00OO0O0OOO00O :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOO0O000OOOO0OO0 :
                    OOOOOOOO00000O000  = OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ]
                    for O00O0O00O000OOO00  in range(1, len(OOOO000OOO0O0O0O0 )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  + OOOO0OO0O000OOO0O [OOOO000OOO0O0O0O0 [O00O0O00O000OOO00 ]]
                        if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if O000OOO000O00O0O0  == O00O0OO0OOOOO00OO .for_test:
                        print('value after adding given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in OO0O0O00O0O0OO000 :
                        if abs(OOOOOOOO00000O000 ) > OO0O00OO0O0OOO00O :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  > OO0O00OO0O0OOO00O :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
        elif OOOO0OO0O000OOO0O [OOO0OO00OOOOO0000 ] > OO0O00OO0O0OOO00O :
            O00OOO0OO0OO000OO  = True
        else:
            O00OOO0OO0OO000OO  = False
        return (O00OOO0OO0OO000OO , OOOOOO0O000OO00O0 )
    def lessThan(OO0OOO00000O00OO0 , OOOOOOO000OO0OO0O , O00O0O00OOO0000OO , O0OOO0OOOO0O00OO0 , O0O0000OOO0O0O00O , OOO00O0O00O0O0OOO , O0OO00OOOOOO0OOOO , O00OO0OOO00OO0OO0 ):
        OOO00O0O00O0O0OOO  = float(OOO00O0O00O0O0OOO )
        O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , OOO00O000O000O0OO , O00000O0OOOOOO000 , OOOO0O000OOOO0OO0 , OOOOO000O0OO000O0 , O0OO00OOO0000O000 , OO0OOOOOOOOOOOO00 , O0O0OO000O0000OO0  = OO0OOO00000O00OO0 .findConditionsStatus(O00O0O00OOO0000OO , O00OO0OOO00OO0OO0 )
        OOOOO0OO0O0O00O00  = 1
        if O0O0OO000O0000OO0 :
            if OOOO0O000OOOO0OO0  == True or O00000O0OOOOOO000  == True:
                OO00O0O0O000OOO0O  = True
            else:
                OO00O0O0O000OOO0O  = False
                OO00O0O0O000OOO0O  = OO0OOO00000O00OO0 .checkSamplesStatus(O0OOO0OOOO0O00OO0 , O0O0000OOO0O0O00O , O0OO00OOO0000O000 , OO00O0O0O000OOO0O , OOOOO000O0OO000O0 , OO0OOOOOOOOOOOO00 , O00O0O00OOO0000OO , O00OO0OOO00OO0OO0 )
            if OO00O0O0O000OOO0O  == False:
                O00OOO0OO0OO000OO  = 'Unknown'
            elif OO00O0O0O000OOO0O :
                O00O0OOO00OO0O000  = O00OO0OOO00OO0OO0  + '__' + O0OOO0OOOO0O00OO0 
                if O0OOO000O00OO0OOO  == True or O00OO0O0000O0OOO0  == True:
                    O0OOOO00000O0O00O  = OO0OOO00000O00OO0 .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O0OOO0OOOO0O00OO0 , O00OO0OOO00OO0OO0 )
                    if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                        print('points', OO0OOO00000O00OO0 .agg[O00O0OOO00OO0O000 ])
                        print('agg value:', O0OOOO00000O0O00O )
                    if O0OOOO00000O0O00O  < OOO00O0O00O0O0OOO :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOO00O000O000O0OO :
                    if 'absolute' in O00O0O00OOO0000OO [0]:
                        if abs(O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ] - OO0OOO00000O00OO0 .agg[O00O0OOO00OO0O000 ][0]) < OOO00O0O00O0O0OOO :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ] - OO0OOO00000O00OO0 .agg[O00O0OOO00OO0O000 ][0] < OOO00O0O00O0O0OOO :
                        if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                            print('current point', O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ])
                            print('point in sample', OO0OOO00000O00OO0 .agg[O00O0OOO00OO0O000 ][0])
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOOO000O0OO000O0 :
                    if 'absolute' in O00O0O00OOO0000OO [2]:
                        if abs(OO0OOO00000O00OO0 .mavg_samples[O00O0OOO00OO0O000 ][-1] - OO0OOO00000O00OO0 .mavg_samples[O00O0OOO00OO0O000 ][0]) < OOO00O0O00O0O0OOO :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OO0OOO00000O00OO0 .mavg_samples[O00O0OOO00OO0O000 ][-1] - OO0OOO00000O00OO0 .mavg_samples[O00O0OOO00OO0O000 ][0] < OOO00O0O00O0O0OOO :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif O00000O0OOOOOO000 :
                    OOOOOOOO00000O000  = O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ]
                    for O00O0O00O000OOO00  in range(1, len(O00O0O00OOO0000OO )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  - O0O0000OOO0O0O00O [O00O0O00OOO0000OO [O00O0O00O000OOO00 ]]
                        if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                        print('value after subtracting given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in OOOOOOO000OO0OO0O :
                        if abs(OOOOOOOO00000O000 ) < OOO00O0O00O0O0OOO :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  < OOO00O0O00O0O0OOO :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOO0O000OOOO0OO0 :
                    OOOOOOOO00000O000  = O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ]
                    for O00O0O00O000OOO00  in range(1, len(O00O0O00OOO0000OO )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  + O0O0000OOO0O0O00O [O00O0O00OOO0000OO [O00O0O00O000OOO00 ]]
                        if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if O00OO0OOO00OO0OO0  == OO0OOO00000O00OO0 .for_test:
                        print('value after adding given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in OOOOOOO000OO0OO0O :
                        if abs(OOOOOOOO00000O000 ) < OOO00O0O00O0O0OOO :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  < OOO00O0O00O0O0OOO :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
        elif O0O0000OOO0O0O00O [O0OOO0OOOO0O00OO0 ] < OOO00O0O00O0O0OOO :
            O00OOO0OO0OO000OO  = True
        else:
            O00OOO0OO0OO000OO  = False
        return (O00OOO0OO0OO000OO , O0OO00OOOOOO0OOOO )
    def equalTo(OO000OOO0OOO0OOOO , O0OOO0O00O000OOO0 , OOO00OOOOO0O00OOO , O000OOO0OO0O0O0O0 , OO00OOO0OO0000O0O , O0O00O0000OOOOO00 , OO00O0OOOO0000OO0 , OOO0OO00OO00O0OO0 ):
        O0O00O0000OOOOO00  = float(O0O00O0000OOOOO00 )
        O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , OOO00O000O000O0OO , O00000O0OOOOOO000 , OOOO0O000OOOO0OO0 , OOOOO000O0OO000O0 , O0OO00OOO0000O000 , OO0OOOOOOOOOOOO00 , O0O0OO000O0000OO0  = OO000OOO0OOO0OOOO .findConditionsStatus(OOO00OOOOO0O00OOO , OOO0OO00OO00O0OO0 )
        OOOOO0OO0O0O00O00  = 1
        if O0O0OO000O0000OO0 :
            if OOOO0O000OOOO0OO0  == True or O00000O0OOOOOO000  == True:
                OO00O0O0O000OOO0O  = True
            else:
                OO00O0O0O000OOO0O  = False
                OO00O0O0O000OOO0O  = OO000OOO0OOO0OOOO .checkSamplesStatus(O000OOO0OO0O0O0O0 , OO00OOO0OO0000O0O , O0OO00OOO0000O000 , OO00O0O0O000OOO0O , OOOOO000O0OO000O0 , OO0OOOOOOOOOOOO00 , OOO00OOOOO0O00OOO , OOO0OO00OO00O0OO0 )
            if OO00O0O0O000OOO0O  == False:
                O00OOO0OO0OO000OO  = 'Unknown'
            elif OO00O0O0O000OOO0O :
                O00O0OOO00OO0O000  = OOO0OO00OO00O0OO0  + '__' + O000OOO0OO0O0O0O0 
                if O0OOO000O00OO0OOO  == True or O00OO0O0000O0OOO0  == True:
                    O0OOOO00000O0O00O  = OO000OOO0OOO0OOOO .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O000OOO0OO0O0O0O0 , OOO0OO00OO00O0OO0 )
                    if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                        print('points', OO000OOO0OOO0OOOO .agg[O00O0OOO00OO0O000 ])
                        print('agg value:', O0OOOO00000O0O00O )
                    if O0OOOO00000O0O00O  == O0O00O0000OOOOO00 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOO00O000O000O0OO :
                    if 'absolute' in OOO00OOOOO0O00OOO [0]:
                        if abs(OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] - OO000OOO0OOO0OOOO .agg[O00O0OOO00OO0O000 ][0]) == O0O00O0000OOOOO00 :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] - OO000OOO0OOO0OOOO .agg[O00O0OOO00OO0O000 ][0] == O0O00O0000OOOOO00 :
                        if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                            print('current point', OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ])
                            print('point in sample', OO000OOO0OOO0OOOO .agg[O00O0OOO00OO0O000 ][0])
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOOO000O0OO000O0 :
                    if 'absolute' in OOO00OOOOO0O00OOO [2]:
                        if abs(OO000OOO0OOO0OOOO .mavg_samples[O00O0OOO00OO0O000 ][-1] - OO000OOO0OOO0OOOO .mavg_samples[O00O0OOO00OO0O000 ][0]) == O0O00O0000OOOOO00 :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OO000OOO0OOO0OOOO .mavg_samples[O00O0OOO00OO0O000 ][-1] - OO000OOO0OOO0OOOO .mavg_samples[O00O0OOO00OO0O000 ][0] == O0O00O0000OOOOO00 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif O00000O0OOOOOO000 :
                    OOOOOOOO00000O000  = OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ]
                    for O00O0O00O000OOO00  in range(1, len(OOO00OOOOO0O00OOO )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  - OO00OOO0OO0000O0O [OOO00OOOOO0O00OOO [O00O0O00O000OOO00 ]]
                        if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                        print('value after subtracting given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in O0OOO0O00O000OOO0 :
                        if abs(OOOOOOOO00000O000 ) == O0O00O0000OOOOO00 :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  == O0O00O0000OOOOO00 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOO0O000OOOO0OO0 :
                    OOOOOOOO00000O000  = OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ]
                    for O00O0O00O000OOO00  in range(1, len(OOO00OOOOO0O00OOO )):
                        OOOOOOOO00000O000  = OOOOOOOO00000O000  + OO00OOO0OO0000O0O [OOO00OOOOO0O00OOO [O00O0O00O000OOO00 ]]
                        if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                            print('after loop value: ', OOOOOOOO00000O000 )
                    if OOO0OO00OO00O0OO0  == OO000OOO0OOO0OOOO .for_test:
                        print('value after adding given keys: ', OOOOOOOO00000O000 )
                    if 'absolute' in O0OOO0O00O000OOO0 :
                        if abs(OOOOOOOO00000O000 ) == O0O00O0000OOOOO00 :
                            O00OOO0OO0OO000OO  = True
                        else:
                            O00OOO0OO0OO000OO  = False
                    elif OOOOOOOO00000O000  == O0O00O0000OOOOO00 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
        elif 'Intermediate' in O000OOO0OO0O0O0O0 :
            if OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] == 0:
                O00OOO0OO0OO000OO  = False
            elif OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] == 1:
                O00OOO0OO0OO000OO  = True
            elif OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] == 2:
                O00OOO0OO0OO000OO  = 'Unknown'
        elif OO00OOO0OO0000O0O [O000OOO0OO0O0O0O0 ] == O0O00O0000OOOOO00 :
            O00OOO0OO0OO000OO  = True
        else:
            O00OOO0OO0OO000OO  = False
        return (O00OOO0OO0OO000OO , OO00O0OOOO0000OO0 )
    def outOfRange(O0OOO0OO0O0O0O0O0 , OO0O000OOOOOOO000 , O0O0O00OOO00O00OO , O0OO0OOOOO0OOOOOO , O0O0000O0OO000O00 , OOO00OO0O0OOO00OO , O0O00000O000OO0O0 , O0OOOOO00O0O0OOO0 ):
        OOO00OO0O0OOO00OO  = OOO00OO0O0OOO00OO .replace(']', '')
        OOO00OO0O0OOO00OO  = OOO00OO0O0OOO00OO .replace('[', '')
        OOO00OO0O0OOO00OO  = OOO00OO0O0OOO00OO .replace("'", '')
        OOO00OO0O0OOO00OO  = OOO00OO0O0OOO00OO .split(',')
        O000OOO00O0OO00O0  = float(OOO00OO0O0OOO00OO [0])
        OOOOO0000OOO0O000  = float(OOO00OO0O0OOO00OO [1])
        if 'standard deviation' in OO0O000OOOOOOO000  or 'moving average' in OO0O000OOOOOOO000 :
            OOOO0OOOO000O0OO0  = O0O0O00OOO00O00OO [0]
            if 'standard deviation' in OO0O000OOOOOOO000 :
                O0OOO000O00OO0OOO  = True
            else:
                O0OOO000O00OO0OOO  = False
            if 'moving average' in OO0O000OOOOOOO000 :
                O00OO0O0000O0OOO0  = True
            else:
                O00OO0O0000O0OOO0  = False
            O0OO00OOO0000O000  = int(O0O0O00OOO00O00OO [1])
            OOOOO0OO0O0O00O00  = 1
            O00000O0OO000OOO0  = O0OOOOO00O0O0OOO0  + '__' + O0OO0OOOOO0OOOOOO 
            if O00000O0OO000OOO0  not in O0OOO0OO0O0O0O0O0 .agg.keys():
                O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ] = [O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ]]
                O00OOO0OO0OO000OO  = 'Unknown'
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('samples exist, but too short, appending one for now')
                    print('points', O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ])
            elif O00000O0OO000OOO0  in O0OOO0OO0O0O0O0O0 .agg.keys() and len(O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ]) + 1 < O0OO00OOO0000O000 :
                O00OOO0OO0OO000OO  = 'Unknown'
                O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ].append(O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ])
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('samples exist, but too short, appending one for now')
                    print('points', O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ])
                O0O00000O000OO0O0  == False
            elif O00000O0OO000OOO0  in O0OOO0OO0O0O0O0O0 .agg.keys() and len(O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ]) + 1 == O0OO00OOO0000O000 :
                O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ].append(O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ])
                O0OOOO00000O0O00O  = O0OOO0OO0O0O0O0O0 .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O0OOO0OO0O0O0O0O0 .agg, O0OO0OOOOO0OOOOOO , O0OOOOO00O0O0OOO0 )
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('samples exist, but one short, appended one now and samples are OK for calculation')
                    print('points', O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ])
                    print('agg value:', O0OOOO00000O0O00O )
                    print('low val:', O000OOO00O0OO00O0 )
                    print('high val:', OOOOO0000OOO0O000 )
                if O0OOOO00000O0O00O  < O000OOO00O0OO00O0  or O0OOOO00000O0O00O  > OOOOO0000OOO0O000 :
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
            elif O00000O0OO000OOO0  in O0OOO0OO0O0O0O0O0 .agg.keys() and len(O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ]) + 1 > O0OO00OOO0000O000 :
                O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ].pop(0)
                O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ].append(O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ])
                O0OOOO00000O0O00O  = O0OOO0OO0O0O0O0O0 .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O0OO0OOOOO0OOOOOO , O0OOOOO00O0O0OOO0 )
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('samples more than sample size, appended latest and popped oldest and samples are OK for calculation')
                    print('points', O0OOO0OO0O0O0O0O0 .agg[O00000O0OO000OOO0 ])
                    print('agg value:', O0OOOO00000O0O00O )
                    print('low val:', O000OOO00O0OO00O0 )
                    print('high val:', OOOOO0000OOO0O000 )
                if O0OOOO00000O0O00O  < O000OOO00O0OO00O0  or O0OOOO00000O0O00O  > OOOOO0000OOO0O000 :
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
        elif 'subtract' in OO0O000OOOOOOO000  or 'sum' in OO0O000OOOOOOO000 :
            if 'subtract' in OO0O000OOOOOOO000 :
                OOOOOOOO00000O000  = O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ]
                for O00O0O00O000OOO00  in range(1, len(O0O0O00OOO00O00OO )):
                    OOOOOOOO00000O000  = OOOOOOOO00000O000  - O0O0000O0OO000O00 [O0O0O00OOO00O00OO [O00O0O00O000OOO00 ]]
                    if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                        print('after loop value: ', OOOOOOOO00000O000 )
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('value after subtracting given keys: ', OOOOOOOO00000O000 )
                if 'absolute' in OO0O000OOOOOOO000 :
                    if abs(OOOOOOOO00000O000 ) < O000OOO00O0OO00O0  or abs(OOOOOOOO00000O000 ) > OOOOO0000OOO0O000 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOOOOOO00000O000  < O000OOO00O0OO00O0  or OOOOOOOO00000O000  > OOOOO0000OOO0O000 :
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
            elif 'sum' in OO0O000OOOOOOO000 :
                OOOOOOOO00000O000  = O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ]
                for O00O0O00O000OOO00  in range(1, len(O0O0O00OOO00O00OO )):
                    OOOOOOOO00000O000  = OOOOOOOO00000O000  + O0O0000O0OO000O00 [O0O0O00OOO00O00OO [O00O0O00O000OOO00 ]]
                    if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                        print('after loop value: ', OOOOOOOO00000O000 )
                if O0OOOOO00O0O0OOO0  == O0OOO0OO0O0O0O0O0 .for_test:
                    print('value after adding given keys: ', OOOOOOOO00000O000 )
                if 'absolute' in OO0O000OOOOOOO000 :
                    if abs(OOOOOOOO00000O000 ) < O000OOO00O0OO00O0  or abs(OOOOOOOO00000O000 ) > OOOOO0000OOO0O000 :
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif OOOOOOOO00000O000  < O000OOO00O0OO00O0  or OOOOOOOO00000O000  > OOOOO0000OOO0O000 :
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
        elif O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ] < O000OOO00O0OO00O0  or O0O0000O0OO000O00 [O0OO0OOOOO0OOOOOO ] > OOOOO0000OOO0O000 :
            O00OOO0OO0OO000OO  = True
        else:
            O00OOO0OO0OO000OO  = False
        return (O00OOO0OO0OO000OO , O0O00000O000OO0O0 )
    def inRange(O0OOOOO000OOOOOOO , OO00OO000O00O00O0 , O00O00O000O0000OO , O0000O0OO0O0000OO , OO0000O0OO0OO00O0 , O0OOO00OOO0OO00OO , O0OO0OOO00000O000 , OO0O0O0O000O00OOO ):
        O0OOO00OOO0OO00OO  = O0OOO00OOO0OO00OO .replace(']', '')
        O0OOO00OOO0OO00OO  = O0OOO00OOO0OO00OO .replace('[', '')
        O0OOO00OOO0OO00OO  = O0OOO00OOO0OO00OO .replace("'", '')
        O0OOO00OOO0OO00OO  = O0OOO00OOO0OO00OO .split(',')
        O000OOO00O0OO00O0  = float(O0OOO00OOO0OO00OO [0])
        OOOOO0000OOO0O000  = float(O0OOO00OOO0OO00OO [1])
        if 'standard deviation' in OO00OO000O00O00O0  or 'moving average' in OO00OO000O00O00O0 :
            OOOO0OOOO000O0OO0  = O00O00O000O0000OO [0]
            if 'standard deviation' in OO00OO000O00O00O0 :
                O0OOO000O00OO0OOO  = True
            else:
                O0OOO000O00OO0OOO  = False
            if 'moving average' in OO00OO000O00O00O0 :
                O00OO0O0000O0OOO0  = True
            else:
                O00OO0O0000O0OOO0  = False
            O0OO00OOO0000O000  = int(O00O00O000O0000OO [1])
            OOOOO0OO0O0O00O00  = 1
            O00000O0OO000OOO0  = OO0O0O0O000O00OOO  + '__' + O0000O0OO0O0000OO 
            if O00000O0OO000OOO0  not in O0OOOOO000OOOOOOO .agg.keys():
                O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ] = [OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ]]
                O00OOO0OO0OO000OO  = 'Unknown'
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('samples exist, but too short, appending one for now')
                    print('points', O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ])
            elif O00000O0OO000OOO0  in O0OOOOO000OOOOOOO .agg.keys() and len(O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ]) + 1 < O0OO00OOO0000O000 :
                O00OOO0OO0OO000OO  = 'Unknown'
                O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ].append(OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ])
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('samples exist, but too short, appending one for now')
                    print('points', O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ])
                O0OO0OOO00000O000  == False
            elif O00000O0OO000OOO0  in O0OOOOO000OOOOOOO .agg.keys() and len(O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ]) + 1 == O0OO00OOO0000O000 :
                O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ].append(OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ])
                O0OOOO00000O0O00O  = O0OOOOO000OOOOOOO .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O0000O0OO0O0000OO , OO0O0O0O000O00OOO )
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('samples exist, but one short, appended one now and samples are OK for calculation')
                    print('points', O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ])
                    print('agg value:', O0OOOO00000O0O00O )
                    print('low val:', O000OOO00O0OO00O0 )
                    print('high val:', OOOOO0000OOO0O000 )
                if (O0OOOO00000O0O00O  > O000OOO00O0OO00O0  or O0OOOO00000O0O00O  == O000OOO00O0OO00O0 ) and (O0OOOO00000O0O00O  < OOOOO0000OOO0O000  or O0OOOO00000O0O00O  == OOOOO0000OOO0O000 ):
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
            elif O00000O0OO000OOO0  in O0OOOOO000OOOOOOO .agg.keys() and len(O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ]) + 1 > O0OO00OOO0000O000 :
                O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ].pop(0)
                O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ].append(OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ])
                O0OOOO00000O0O00O  = O0OOOOO000OOOOOOO .calcAggregate(O0OOO000O00OO0OOO , O00OO0O0000O0OOO0 , O0000O0OO0O0000OO , OO0O0O0O000O00OOO )
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('samples more than sample size, appended latest and popped oldest and samples are OK for calculation')
                    print('points', O0OOOOO000OOOOOOO .agg[O00000O0OO000OOO0 ])
                    print('agg value:', O0OOOO00000O0O00O )
                    print('low val:', O000OOO00O0OO00O0 )
                    print('high val:', OOOOO0000OOO0O000 )
                if (O0OOOO00000O0O00O  > O000OOO00O0OO00O0  or O0OOOO00000O0O00O  == O000OOO00O0OO00O0 ) and (O0OOOO00000O0O00O  < OOOOO0000OOO0O000  or O0OOOO00000O0O00O  == OOOOO0000OOO0O000 ):
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
        elif 'subtract' in OO00OO000O00O00O0  or 'sum' in OO00OO000O00O00O0 :
            if 'subtract' in OO00OO000O00O00O0 :
                OOOOOOOO00000O000  = OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ]
                for O00O0O00O000OOO00  in range(1, len(O00O00O000O0000OO )):
                    OOOOOOOO00000O000  = OOOOOOOO00000O000  - OO0000O0OO0OO00O0 [O00O00O000O0000OO [O00O0O00O000OOO00 ]]
                    if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                        print('after loop value: ', OOOOOOOO00000O000 )
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('value after subtracting given keys: ', OOOOOOOO00000O000 )
                if 'absolute' in OO00OO000O00O00O0 :
                    if (abs(OOOOOOOO00000O000 ) > O000OOO00O0OO00O0  or abs(OOOOOOOO00000O000 ) == O000OOO00O0OO00O0 ) and (abs(OOOOOOOO00000O000 ) < OOOOO0000OOO0O000  or abs(OOOOOOOO00000O000 ) == OOOOO0000OOO0O000 ):
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif (OOOOOOOO00000O000  > O000OOO00O0OO00O0  or OOOOOOOO00000O000  == O000OOO00O0OO00O0 ) and (OOOOOOOO00000O000  < OOOOO0000OOO0O000  or OOOOOOOO00000O000  == OOOOO0000OOO0O000 ):
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
            elif 'sum' in OO00OO000O00O00O0 :
                OOOOOOOO00000O000  = OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ]
                for O00O0O00O000OOO00  in range(1, len(O00O00O000O0000OO )):
                    OOOOOOOO00000O000  = OOOOOOOO00000O000  + OO0000O0OO0OO00O0 [O00O00O000O0000OO [O00O0O00O000OOO00 ]]
                    if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                        print('after loop value: ', OOOOOOOO00000O000 )
                if OO0O0O0O000O00OOO  == O0OOOOO000OOOOOOO .for_test:
                    print('value after adding given keys: ', OOOOOOOO00000O000 )
                if 'absolute' in OO00OO000O00O00O0 :
                    if (abs(OOOOOOOO00000O000 ) > O000OOO00O0OO00O0  or abs(OOOOOOOO00000O000 ) == O000OOO00O0OO00O0 ) and (abs(OOOOOOOO00000O000 ) < OOOOO0000OOO0O000  or abs(OOOOOOOO00000O000 ) == OOOOO0000OOO0O000 ):
                        O00OOO0OO0OO000OO  = True
                    else:
                        O00OOO0OO0OO000OO  = False
                elif (OOOOOOOO00000O000  > O000OOO00O0OO00O0  or OOOOOOOO00000O000  == O000OOO00O0OO00O0 ) and (OOOOOOOO00000O000  < OOOOO0000OOO0O000  or OOOOOOOO00000O000  == OOOOO0000OOO0O000 ):
                    O00OOO0OO0OO000OO  = True
                else:
                    O00OOO0OO0OO000OO  = False
        elif (OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ] > O000OOO00O0OO00O0  or OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ] == O000OOO00O0OO00O0 ) and (OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ] < OOOOO0000OOO0O000  or OO0000O0OO0OO00O0 [O0000O0OO0O0000OO ] == OOOOO0000OOO0O000 ):
            O00OOO0OO0OO000OO  = True
        else:
            O00OOO0OO0OO000OO  = False
        return (O00OOO0OO0OO000OO , O0OO0OOO00000O000 )
    def eventSoFar(OOOO00OO0O00O0O00 , OO0OOOOOO0OO00O0O , OOOO0O00OOOO0OO00 , OO00O0OO00O0O00OO , O00OOOO0OOOOOO0OO ):
        if OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 1 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'AND' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 2 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == False and OOOO0O00OOOO0OO00  == 'AND' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = False
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 3 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'AND' and (OO00O0OO00O0O00OO  == 'Unknown'):
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 4 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == 'Unknown' and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 5 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == 'Unknown'):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 6 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == 'Unknown' and OOOO0O00OOOO0OO00  == 'AND' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 7 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 8 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == False and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == True):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 9 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'OR' and (OO00O0OO00O0O00OO  == False):
            OO00O0OO00O0O00OO  = True
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 10 of eventsofar func')
        elif OO0OOOOOO0OO00O0O  == True and OOOO0O00OOOO0OO00  == 'AND' and (OO00O0OO00O0O00OO  == False):
            OO00O0OO00O0O00OO  = False
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 11 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == 'Unknown' and OO00O0OO00O0O00OO  == False) and OOOO0O00OOOO0OO00  == 'AND':
            OO00O0OO00O0O00OO  = False
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 12 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == 'Unknown' and OO00O0OO00O0O00OO  == False) and OOOO0O00OOOO0OO00  == 'OR':
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 13 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == False and OO00O0OO00O0O00OO  == 'Unknown') and OOOO0O00OOOO0OO00  == 'OR':
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 14 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == False and OO00O0OO00O0O00OO  == 'Unknown') and OOOO0O00OOOO0OO00  == 'AND':
            OO00O0OO00O0O00OO  = False
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 15 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == 'Unknown' and OO00O0OO00O0O00OO  == 'Unknown') and (OOOO0O00OOOO0OO00  == 'OR' or OOOO0O00OOOO0OO00  == 'AND'):
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 16 of eventsofar func')
        elif (OO0OOOOOO0OO00O0O  == False and OO00O0OO00O0O00OO  == False) and (OOOO0O00OOOO0OO00  == 'OR' or OOOO0O00OOOO0OO00  == 'AND'):
            OO00O0OO00O0O00OO  = False
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into condition 17 of eventsofar func')
        else:
            OO00O0OO00O0O00OO  = 'Unknown'
            if O00OOOO0OOOOOO0OO  == OOOO00OO0O00O0O00 .for_test:
                print('fell into last else condition of eventsofar func')
        return OO00O0OO00O0O00OO 
    def lineStatus(O0O0OO0O0OO0OOO00 , OO000000O0000OOOO , O00O000OOOOO0O0OO , O0OOO0O0O000000OO , O0O0OOO0OO00OOOO0 , O0O00O00OO0O00OO0 , OOOOOOOOOOO00OOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 ):
        if OO000000O0000OOOO  == True:
            if str(O0OO0OO0O00O0OO00 ) == '0.0':
                print('implement is 0, so event of this line is Unknown')
                O00O000OOOOO0O0OO  = 'Unknown'
                OO000000O0000OOOO  = True
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print('this line is not implemented, event is: ', O00O000OOOOO0O0OO )
                    print('-------------')
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
            elif O0OOO00O0O0OOOO00  == '>':
                O00O000OOOOO0O0OO , OO000000O0000OOOO  = O0O0OO0O0OO0OOO00 .moreThan(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OOOOOOOOOOO00OOO0 , O0O0OOO0OO00OOOO0 , OOO000000O0000OOO , OO000000O0000OOOO , OO00OOO0OO0O0O0O0 )
                if 'True' in OO00O0OOO0OOOOOOO :
                    O00O000OOOOO0O0OO  = O0O0OO0O0OO0OOO00 .persistenceCheck(O00O000OOOOO0O0OO , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 , OOOOOOOOOOO00OOO0 )
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print("this line's status:", O00O000OOOOO0O0OO , 'logic:', O00O00OO0O000O0OO , 'status comes from above:', O0OOO0O0O000000OO )
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
            elif O0OOO00O0O0OOOO00  == '<':
                O00O000OOOOO0O0OO , OO000000O0000OOOO  = O0O0OO0O0OO0OOO00 .lessThan(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OOOOOOOOOOO00OOO0 , O0O0OOO0OO00OOOO0 , OOO000000O0000OOO , OO000000O0000OOOO , OO00OOO0OO0O0O0O0 )
                if 'True' in OO00O0OOO0OOOOOOO :
                    O00O000OOOOO0O0OO  = O0O0OO0O0OO0OOO00 .persistenceCheck(O00O000OOOOO0O0OO , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 , OOOOOOOOOOO00OOO0 )
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print("this line's status:", O00O000OOOOO0O0OO , 'logic:', O00O00OO0O000O0OO , 'status comes from above:', O0OOO0O0O000000OO )
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
            elif O0OOO00O0O0OOOO00  == '=':
                O00O000OOOOO0O0OO , OO000000O0000OOOO  = O0O0OO0O0OO0OOO00 .equalTo(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OOOOOOOOOOO00OOO0 , O0O0OOO0OO00OOOO0 , OOO000000O0000OOO , OO000000O0000OOOO , OO00OOO0OO0O0O0O0 )
                if 'True' in OO00O0OOO0OOOOOOO :
                    O00O000OOOOO0O0OO  = O0O0OO0O0OO0OOO00 .persistenceCheck(O00O000OOOOO0O0OO , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 , OOOOOOOOOOO00OOO0 )
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print("this line's status:", O00O000OOOOO0O0OO , 'logic:', O00O00OO0O000O0OO , 'status comes from above:', O0OOO0O0O000000OO )
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
            elif O0OOO00O0O0OOOO00  == '][':
                O00O000OOOOO0O0OO , OO000000O0000OOOO  = O0O0OO0O0OO0OOO00 .outOfRange(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OOOOOOOOOOO00OOO0 , O0O0OOO0OO00OOOO0 , OOO000000O0000OOO , OO000000O0000OOOO , OO00OOO0OO0O0O0O0 )
                if 'True' in OO00O0OOO0OOOOOOO :
                    O00O000OOOOO0O0OO  = O0O0OO0O0OO0OOO00 .persistenceCheck(O00O000OOOOO0O0OO , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 , OOOOOOOOOOO00OOO0 )
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print("this line's status:", O00O000OOOOO0O0OO , 'logic:', O00O00OO0O000O0OO , 'status comes from above:', O0OOO0O0O000000OO )
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
            elif O0OOO00O0O0OOOO00  == '[]' or O0OOO00O0O0OOOO00  == 'NOT ][':
                O00O000OOOOO0O0OO , OO000000O0000OOOO  = O0O0OO0O0OO0OOO00 .inRange(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OOOOOOOOOOO00OOO0 , O0O0OOO0OO00OOOO0 , OOO000000O0000OOO , OO000000O0000OOOO , OO00OOO0OO0O0O0O0 )
                if 'True' in OO00O0OOO0OOOOOOO :
                    O00O000OOOOO0O0OO  = O0O0OO0O0OO0OOO00 .persistenceCheck(O00O000OOOOO0O0OO , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O , OO00OOO0OO0O0O0O0 , OOOOOOOOOOO00OOO0 )
                if OO00OOO0OO0O0O0O0  == O0O0OO0O0OO0OOO00 .for_test:
                    print("this line's status:", O00O000OOOOO0O0OO , 'logic:', O00O00OO0O000O0OO , 'status comes from above:', O0OOO0O0O000000OO )
                O0OOO0O0O000000OO  = O0O0OO0O0OO0OOO00 .eventSoFar(O00O000OOOOO0O0OO , O00O00OO0O000O0OO , O0OOO0O0O000000OO , OO00OOO0OO0O0O0O0 )
        else:
            OO000000O0000OOOO  = False
        return (O0OOO0O0O000000OO , OO000000O0000OOOO )
    def createVariables(OO0O0O0OOO000O00O , O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 ):
        O0O00O00OO0O00OO0  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Problem_Name']
        OOOOOOOOOOO00OOO0  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Standard_Key']
        O0O000O0O00O0OO0O  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Additional condition']
        OO00000OO00OOOOO0  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Additional condition'].split(',')
        O0OOO00O0O0OOOO00  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Condition']
        OOO000000O0000OOO  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Threshold']
        O00O00OO0O000O0OO  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0  - 1]['Logic']
        O0OO0OO0O00O0OO00  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Implement']
        if OO0O0O0OOO000O00O .test_run == 1:
            if OOOOOOOOOOO00OOO0  == 'NS_IG010-XA_PV' or OOOOOOOOOOO00OOO0  == 'NS_AN_NG2-00273_PV':
                O0OO0OO0O00O0OO00  = 0
            else:
                O0OO0OO0O00O0OO00  = 1
        OO00O0OOO0OOOOOOO  = O0OOO00O0000O00O0 .loc[O0O00O0OOOO000OO0 ]['Persistence'].split(',')
        O000O0OO0OO0OO00O  = 1
        if 'True' in OO00O0OOO0OOOOOOO :
            O000O0OO0OO0OO00O  = int(OO00O0OOO0OOOOOOO [1])
        return (O0O00O00OO0O00OO0 , OOOOOOOOOOO00OOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO00O0OOO0OOOOOOO , O000O0OO0OO0OO00O )
    def persistenceCheck(O00O00O0O00O00O00 , O0O0O0O000OO00O0O , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O , OO0OO00OO0OOOOOO0 ):
        O00000O00O000OO00  = O0000OO0OO00OOO0O  + '__' + OO0OO00OO0OOOOOO0 
        if O0O0O0O000OO00O0O  == True and 'True' in OO0OO0O00000OOOOO :
            if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                print('persistence to apply')
            if O0O0O0O000OO00O0O  == True and O00000O00O000OO00  not in O00O00O0O00O00O00 .persistence.keys():
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ] = [O0O0O0O000OO00O0O ]
                O0O0O0O000OO00O0O  = 'Unknown'
                if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                    print('fell into 1st condition of persistence (no samples present). event is: ', O0O0O0O000OO00O0O )
            elif O00000O00O000OO00  in O00O00O0O00O00O00 .persistence.keys() and len(O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ]) + 1 < OO0OO0O00OO0OO0O0 :
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ].append(O0O0O0O000OO00O0O )
                O0O0O0O000OO00O0O  = 'Unknown'
                if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                    print('fell into 2nd condition of persistence (sample exist but short). event is: ', O0O0O0O000OO00O0O )
            elif O00000O00O000OO00  in O00O00O0O00O00O00 .persistence.keys() and len(O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ]) + 1 == OO0OO0O00OO0OO0O0 :
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ].append(O0O0O0O000OO00O0O )
                O0O0O0O000OO00O0O  = True
                if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                    print('fell into 3rd condition of persistence (samples are one short, but appended one now and now equal to persistence duration). event is: ', O0O0O0O000OO00O0O )
            elif O00000O00O000OO00  in O00O00O0O00O00O00 .persistence.keys() and len(O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ]) + 1 > OO0OO0O00OO0OO0O0 :
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ].pop(0)
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ].append(O0O0O0O000OO00O0O )
                O0O0O0O000OO00O0O  = True
                if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                    print('fell into 4th condition of persistence (samples more than persistence duration, latest is appended and oldest is popped). event is: ', O0O0O0O000OO00O0O )
        elif 'True' in OO0OO0O00000OOOOO  and O0O0O0O000OO00O0O  != True:
            if O00000O00O000OO00  in O00O00O0O00O00O00 .persistence.keys():
                O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ] = []
                if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
                    print('fell into 5th condition of persistence (persistence is reset as event is not active). event is: ', O0O0O0O000OO00O0O )
        if O0000OO0OO00OOO0O  == O00O00O0O00O00O00 .for_test:
            if O00000O00O000OO00  in O00O00O0O00O00O00 .persistence.keys():
                print('persistence stored for ', O00000O00O000OO00 , ' are: ', O00O00O0O00O00O00 .persistence[O00000O00O000OO00 ])
            else:
                print('persistence check => ', O00000O00O000OO00 , ' is yet not available in persistence dict because it has not been triggered yet, probably due to additional condition.')
        return O0O0O0O000OO00O0O 
    def rcaTemplatesReader(OOOO0OO00OOO0000O , O00OO0O0OO0000O0O , OOOO0O0O00O0OO0OO , OOO0OO0OOOOO000O0 , O00000O00O00O00OO ):
        OO0000O0OO0OOO0OO  = {}
        O0000O0O00OOO000O  = {}
        O00OO00OOO0O00000  = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 'GCU', 'INCIN']
        for itr in range(len(O00OO0O0OO0000O0O )):
            if OOO0OO0OOOOO000O0 [O00OO00OOO0O00000 [itr]] == 1:
                print(f'starting rca template: {O00OO00OOO0O00000 [itr]}')
                O0OOO00O0000O00O0  = O00OO0O0OO0000O0O [itr]
                O0OOO00O0000O00O0  = O0OOO00O0000O00O0 .loc[:, :'Implement']
                O0OOO00O0000O00O0 .fillna('blank', inplace=True)
                OOOO00OO00O0OOO00  = O0OOO00O0000O00O0 ['Implement'] == 1.0
                O0OOO00O0000O00O0  = O0OOO00O0000O00O0 [OOOO00OO00O0OOO00 ].reset_index()
                O0OOO00O0000O00O0  = O0OOO00O0000O00O0 .drop(columns=['index'], axis=1)
                OO0O000O0O0OOOO00  = 'start_of_sheet'
                O0OO00O0OO0O00OOO  = True
                O0O0O0OOO00O0O0O0  = 'none'
                for O00O0O00O000OOO00  in range(len(O0OOO00O0000O00O0 .index)):
                    O0000OO0OO00OOO0O  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Problem_Name']
                    OO0OO00OO0OOOOOO0  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Standard_Key']
                    O0O000O0O00O0OO0O  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Additional condition']
                    OO00000OO00OOOOO0  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Additional condition'].split(',')
                    O0OOO00O0O0OOOO00  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Condition']
                    OOO000000O0000OOO  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Threshold']
                    OO0OO0O00000OOOOO  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Persistence'].split(',')
                    OO0OO0O00OO0OO0O0  = 1
                    if 'True' in OO0OO0O00000OOOOO :
                        OO0OO0O00OO0OO0O0  = int(OO0OO0O00000OOOOO [1])
                    O0OO0OO0O00O0OO00  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Implement']
                    if OOOO0OO00OOO0000O .test_run == 1:
                        if OO0OO00OO0OOOOOO0  == 'NS_IG010-XA_PV' or OO0OO00OO0OOOOOO0  == 'NS_AN_NG2-00273_PV':
                            O0OO0OO0O00O0OO00  = 0
                        else:
                            O0OO0OO0O00O0OO00  = 1
                    OO0O0O000000O0OO0  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Level']
                    OOOOOOO00OO00OOO0  = str(O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Run Check'])
                    if OO0O0O000000O0OO0  == 'COMPONENT':
                        if OOOOOOO00OO00OOO0  == '1.0':
                            if OOO0OO0OOOOO000O0 [O0000OO0OO00OOO0O ] == 1:
                                O0OO00O0OO0O00OOO  = True
                            else:
                                O0OO00O0OO0O00OOO  = False
                        else:
                            O0OO00O0OO0O00OOO  = True
                    if O0OO00O0OO0O00OOO :
                        if O0000OO0OO00OOO0O  != OO0O000O0O0OOOO00  and O00000O00O00O00OO [O0000OO0OO00OOO0O ] == 1:
                            OO0O000O0O0OOOO00  = O0000OO0OO00OOO0O 
                            O0000O0O00OOO000O [O0000OO0OO00OOO0O ] = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Parent_Node']
                            OO000000O0000OOOO  = True
                            if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                print(O0000OO0OO00OOO0O , 'started')
                            if O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Standard_Key'] == 'blank':
                                O0O0O0O000OO00O0O  = 'Unknown'
                                OO000000O0000OOOO  = False
                            else:
                                O0O0O0O000OO00O0O  = False
                            if str(O0OO0OO0O00O0OO00 ) == '0.0':
                                O0O0O0O000OO00O0O  = 'Unknown'
                                OO000000O0000OOOO  = True
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('this line is not implemented, event is: ', O0O0O0O000OO00O0O )
                            elif O0OOO00O0O0OOOO00  == '>':
                                O0O0O0O000OO00O0O , OO000000O0000OOOO  = OOOO0OO00OOO0000O .moreThan(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OO0OO00OO0OOOOOO0 , OOOO0O0O00O0OO0OO , OOO000000O0000OOO , OO000000O0000OOOO , O0000OO0OO00OOO0O )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('data of 1st line: ', OO0OO00OO0OOOOOO0 , ' ', O0OOO00O0O0OOOO00 , ' ', OOO000000O0000OOO , ' ', OO00000OO00OOOOO0 )
                                    print('event of 1st line: ', O0O0O0O000OO00O0O )
                            elif O0OOO00O0O0OOOO00  == '<':
                                O0O0O0O000OO00O0O , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lessThan(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OO0OO00OO0OOOOOO0 , OOOO0O0O00O0OO0OO , OOO000000O0000OOO , OO000000O0000OOOO , O0000OO0OO00OOO0O )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('data of 1st line: ', OO0OO00OO0OOOOOO0 , ' ', O0OOO00O0O0OOOO00 , ' ', OOO000000O0000OOO , ' ', OO00000OO00OOOOO0 )
                                    print('event of 1st line: ', O0O0O0O000OO00O0O )
                            elif O0OOO00O0O0OOOO00  == '=':
                                O0O0O0O000OO00O0O , OO000000O0000OOOO  = OOOO0OO00OOO0000O .equalTo(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OO0OO00OO0OOOOOO0 , OOOO0O0O00O0OO0OO , OOO000000O0000OOO , OO000000O0000OOOO , O0000OO0OO00OOO0O )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('data of 1st line: ', OO0OO00OO0OOOOOO0 , ' ', O0OOO00O0O0OOOO00 , ' ', OOO000000O0000OOO , ' ', OO00000OO00OOOOO0 )
                                    print('event of 1st line: ', O0O0O0O000OO00O0O )
                            elif O0OOO00O0O0OOOO00  == '][':
                                O0O0O0O000OO00O0O , OO000000O0000OOOO  = OOOO0OO00OOO0000O .outOfRange(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OO0OO00OO0OOOOOO0 , OOOO0O0O00O0OO0OO , OOO000000O0000OOO , OO000000O0000OOOO , O0000OO0OO00OOO0O )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('data of 1st line: ', OO0OO00OO0OOOOOO0 , ' ', O0OOO00O0O0OOOO00 , ' ', OOO000000O0000OOO , ' ', OO00000OO00OOOOO0 )
                                    print('event of 1st line: ', O0O0O0O000OO00O0O )
                            elif O0OOO00O0O0OOOO00  == '[]' or O0OOO00O0O0OOOO00  == 'NOT ][':
                                O0O0O0O000OO00O0O , OO000000O0000OOOO  = OOOO0OO00OOO0000O .inRange(O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , OO0OO00OO0OOOOOO0 , OOOO0O0O00O0OO0OO , OOO000000O0000OOO , OO000000O0000OOOO , O0000OO0OO00OOO0O )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('data of 1st line: ', OO0OO00OO0OOOOOO0 , ' ', O0OOO00O0O0OOOO00 , ' ', OOO000000O0000OOO , ' ', OO00000OO00OOOOO0 )
                                    print('event of 1st line: ', O0O0O0O000OO00O0O )
                            if 'True' in OO0OO0O00000OOOOO :
                                O0O0O0O000OO00O0O  = OOOO0OO00OOO0000O .persistenceCheck(O0O0O0O000OO00O0O , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O , OO0OO00OO0OOOOOO0 )
                            O0OOO0O0O000000OO  = O0O0O0O000OO00O0O 
                            if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                print(O0000OO0OO00OOO0O , '=> after line 1 event so far =>', O0OOO0O0O000000OO , ', and it will go to the lines below')
                                print('-------------')
                            if O00O0O00O000OOO00  + 1 < len(O0OOO00O0000O00O0 .index) and OO000000O0000OOOO  == True:
                                O0O00O0OOOO000OO0  = O00O0O00O000OOO00  + 1
                                O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0  = OOOO0OO00OOO0000O .createVariables(O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('line 2 data =>', O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO )
                                if O0O00O00OO0O00OO0  != OO0O000O0O0OOOO00 :
                                    OO000000O0000OOOO  = False
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print('********* end of rule *********')
                                        print('this line has another scenario started, so this line will not be processed')
                                if OO000000O0000OOOO  == True:
                                    O0OOO0O0O000000OO , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lineStatus(OO000000O0000OOOO , O0O0O0O000OO00O0O , O0OOO0O0O000000OO , OOOO0O0O00O0OO0OO , O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O )
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print(O0000OO0OO00OOO0O , 'after line 2 =>', O0OOO0O0O000000OO )
                                        print('-------------')
                            if O00O0O00O000OOO00  + 2 < len(O0OOO00O0000O00O0 .index) and OO000000O0000OOOO  == True:
                                O0O00O0OOOO000OO0  = O00O0O00O000OOO00  + 2
                                O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0  = OOOO0OO00OOO0000O .createVariables(O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('line 3 data =>', O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO )
                                if O0O00O00OO0O00OO0  != OO0O000O0O0OOOO00 :
                                    OO000000O0000OOOO  = False
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print('********* end of rule *********')
                                        print('this line has another scenario started, this line will not be processed')
                                if OO000000O0000OOOO  == True:
                                    O0OOO0O0O000000OO , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lineStatus(OO000000O0000OOOO , O0O0O0O000OO00O0O , O0OOO0O0O000000OO , OOOO0O0O00O0OO0OO , O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O )
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print(O0000OO0OO00OOO0O , 'after line 3 =>', O0OOO0O0O000000OO )
                                        print('-------------')
                            if O00O0O00O000OOO00  + 3 < len(O0OOO00O0000O00O0 .index) and OO000000O0000OOOO  == True:
                                O0O00O0OOOO000OO0  = O00O0O00O000OOO00  + 3
                                O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0  = OOOO0OO00OOO0000O .createVariables(O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('line 4 data =>', O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO )
                                if O0O00O00OO0O00OO0  != OO0O000O0O0OOOO00 :
                                    OO000000O0000OOOO  = False
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print('********* end of rule *********')
                                        print('this line has another scenario started, this line will not be processed')
                                if OO000000O0000OOOO  == True:
                                    O0OOO0O0O000000OO , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lineStatus(OO000000O0000OOOO , O0O0O0O000OO00O0O , O0OOO0O0O000000OO , OOOO0O0O00O0OO0OO , O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O )
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print(O0000OO0OO00OOO0O , 'after line 4 =>', O0OOO0O0O000000OO )
                                        print('-------------')
                            if O00O0O00O000OOO00  + 4 < len(O0OOO00O0000O00O0 .index) and OO000000O0000OOOO  == True:
                                O0O00O0OOOO000OO0  = O00O0O00O000OOO00  + 4
                                O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0  = OOOO0OO00OOO0000O .createVariables(O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('line 5 data =>', O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO )
                                if O0O00O00OO0O00OO0  != OO0O000O0O0OOOO00 :
                                    OO000000O0000OOOO  = False
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print('********* end of rule *********')
                                        print('this line has another scenario started, this line will not be processed')
                                if OO000000O0000OOOO  == True:
                                    O0OOO0O0O000000OO , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lineStatus(OO000000O0000OOOO , O0O0O0O000OO00O0O , O0OOO0O0O000000OO , OOOO0O0O00O0OO0OO , O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O )
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print(O0000OO0OO00OOO0O , 'after line 5 =>', O0OOO0O0O000000OO )
                                        print('-------------')
                            if O00O0O00O000OOO00  + 5 < len(O0OOO00O0000O00O0 .index) and OO000000O0000OOOO  == True:
                                O0O00O0OOOO000OO0  = O00O0O00O000OOO00  + 5
                                O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0  = OOOO0OO00OOO0000O .createVariables(O0O00O0OOOO000OO0 , O0OOO00O0000O00O0 )
                                if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                    print('line 6 data =>', O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO )
                                if O0O00O00OO0O00OO0  != OO0O000O0O0OOOO00 :
                                    OO000000O0000OOOO  = False
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print('********* end of rule *********')
                                        print('this line has another scenario started, this line will not be processed')
                                if OO000000O0000OOOO  == True:
                                    O0OOO0O0O000000OO , OO000000O0000OOOO  = OOOO0OO00OOO0000O .lineStatus(OO000000O0000OOOO , O0O0O0O000OO00O0O , O0OOO0O0O000000OO , OOOO0O0O00O0OO0OO , O0O00O00OO0O00OO0 , OO0OO00OO0OOOOOO0 , O0O000O0O00O0OO0O , OO00000OO00OOOOO0 , O0OOO00O0O0OOOO00 , OOO000000O0000OOO , O00O00OO0O000O0OO , O0OO0OO0O00O0OO00 , OO0OO0O00000OOOOO , OO0OO0O00OO0OO0O0 , O0000OO0OO00OOO0O )
                                    if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                        print(O0000OO0OO00OOO0O , 'after line 6 =>', O0OOO0O0O000000OO )
                                        print('-------------')
                            if 'Intermediate' in O0000OO0OO00OOO0O :
                                if O0OOO0O0O000000OO  == True:
                                    O00OOO00OO000O00O  = 1
                                elif O0OOO0O0O000000OO  == False:
                                    O00OOO00OO000O00O  = 0
                                elif O0OOO0O0O000000OO  == 'Unknown':
                                    O00OOO00OO000O00O  = 2
                                OOOO0O0O00O0OO0OO [O0000OO0OO00OOO0O ] = O00OOO00OO000O00O 
                                OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ] = O00OOO00OO000O00O 
                            else:
                                OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ] = O0OOO0O0O000000OO 
                            if O0000OO0OO00OOO0O  == OOOO0OO00OOO0000O .for_test:
                                if OOOO0OO00OOO0000O .agg_test in OOOO0OO00OOO0000O .agg:
                                    print(OOOO0OO00OOO0000O .agg[OOOO0OO00OOO0000O .agg_test])
                                print('final result of ', OOOO0OO00OOO0000O .for_test, 'is =>', OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ])
                                print('----------------------------------')
                        elif O00000O00O00O00OO [O0000OO0OO00OOO0O ] == 0:
                            OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ] = 'Unknown_TagNA'
                            O0000O0O00OOO000O [O0000OO0OO00OOO0O ] = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Parent_Node']
                    else:
                        if 'Intermediate' not in O0000OO0OO00OOO0O  and O0000OO0OO00OOO0O  != O0O0O0OOO00O0O0O0 :
                            O0000O0O00OOO000O [O0000OO0OO00OOO0O ] = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Parent_Node']
                            OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ] = 'Unknown_ComponentNotRunning'
                        O0O0O0OOO00O0O0O0  = O0000OO0OO00OOO0O 
            elif OOO0OO0OOOOO000O0 [O00OO00OOO0O00000 [itr]] == 0:
                O0OOO00O0000O00O0  = O00OO0O0OO0000O0O [itr]
                O0O0O0OOO00O0O0O0  = 'none'
                for O00O0O00O000OOO00  in range(len(O0OOO00O0000O00O0 .index)):
                    O0000OO0OO00OOO0O  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Problem_Name']
                    if 'Intermediate' not in O0000OO0OO00OOO0O  and O0000OO0OO00OOO0O  != O0O0O0OOO00O0O0O0 :
                        OO0000O0OO0OOO0OO [O0000OO0OO00OOO0O ] = 'Unknown_AssetNotRunning'
                        O0000O0O00OOO000O [O0000OO0OO00OOO0O ] = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Parent_Node']
                    O0O0O0OOO00O0O0O0  = O0000OO0OO00OOO0O 
        for O00OO0OO0OO0O0O0O  in OO0000O0OO0OOO0OO .keys():
            OO0000O0OO0OOO0OO [O00OO0OO0OO0O0O0O ] = str(OO0000O0OO0OOO0OO [O00OO0OO0OO0O0O0O ])
        return (OO0000O0OO0OOO0OO , O0000O0O00OOO000O )
    def logStatusandParentNode(O0O000OO00000OO00 , OO00OOO0O0OO00000 , O0OO0OOOO0000OOOO ):
        O0O000OO00000OO00 .cursor.execute('truncate table public."RCA_update"')
        O0O000OO00000OO00 .conn.commit()
        OO0O0O0OOOOOOO00O  = {}
        for O00OO0OO0OO0O0O0O  in OO00OOO0O0OO00000 .keys():
            OO0O0O0OOOOOOO00O [O00OO0OO0OO0O0O0O ] = [str(OO00OOO0O0OO00000 [O00OO0OO0OO0O0O0O ]), O0OO0OOOO0000OOOO [O00OO0OO0OO0O0O0O ]]
        for O00OO0OO0OO0O0O0O  in OO0O0O0OOOOOOO00O .keys():
            O0O000OO00000OO00 .cursor.execute('insert into public."RCA_update" values(%s, %s, %s, %s)', [datetime.now(), O00OO0OO0OO0O0O0O , OO0O0O0OOOOOOO00O [O00OO0OO0OO0O0O0O ][0], OO0O0O0OOOOOOO00O [O00OO0OO0OO0O0O0O ][1]])
            O0O000OO00000OO00 .conn.commit()
        return OO0O0O0OOOOOOO00O 
    def RCAlevels(OOO000OO000O00000 , O00O00OOO0O00O0O0 ):
        OOO000OO000O00000 .cursor.execute('truncate table public."RCA_levels"')
        OOO000OO000O00000 .conn.commit()
        OOO000OO000O00000 .cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = \'None\';')
        OOOO00O0O00000O0O  = OOO000OO000O00000 .cursor.fetchall()
        OOO000OO000O00000 .conn.commit()
        OO0OOOO0O000O0000  = []
        for item in OOOO00O0O00000O0O :
            OO0OOOO0O000O0000 .append(item[0])
        OO0OOO0O00000OOO0  = {}
        OO0O0OO000O00O00O  = {}
        for Equipment in OO0OOOO0O000O0000 :
            if Equipment in O00O00OOO0O00O0O0 .keys():
                OO0OOO0O00000OOO0 [Equipment] = []
            O0OO00OO0OO000O00  = Equipment
            O00OOOOO000OOO0O0  = []
            OOO000OO000O00000 .cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Equipment])
            OOOO00O0O00000O0O  = OOO000OO000O00000 .cursor.fetchall()
            OOO000OO000O00000 .conn.commit()
            for item in OOOO00O0O00000O0O :
                O00OOOOO000OOO0O0 .append(item[0])
                if item[0] in O00O00OOO0O00O0O0 .keys():
                    OO0OOO0O00000OOO0 [Equipment].append(item[0])
            for Component in O00OOOOO000OOO0O0 :
                OO00OOOO0O0OO00O0  = Component
                O00O00OO0OOOOO00O  = []
                OOO000OO000O00000 .cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Component])
                OOOO00O0O00000O0O  = OOO000OO000O00000 .cursor.fetchall()
                OOO000OO000O00000 .conn.commit()
                for item in OOOO00O0O00000O0O :
                    O00O00OO0OOOOO00O .append(item[0])
                for Scenario in O00O00OO0OOOOO00O :
                    O0O00OOO000OO0O00  = Scenario
                    O0O00O0000000OOO0  = []
                    OOO000OO000O00000 .cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Scenario])
                    OOOO00O0O00000O0O  = OOO000OO000O00000 .cursor.fetchall()
                    OOO000OO000O00000 .conn.commit()
                    for item in OOOO00O0O00000O0O :
                        O0O00O0000000OOO0 .append(item[0])
                    if len(O0O00O0000000OOO0 ) > 0:
                        O0O0000OOO000OOO0  = O0O00O0000000OOO0 [0]
                        for O00O0O00O000OOO00  in range(1, len(O0O00O0000000OOO0 )):
                            O0O0000OOO000OOO0  = O0O0000OOO000OOO0  + ',' + O0O00O0000000OOO0 [O00O0O00O000OOO00 ]
                    else:
                        O0O0000OOO000OOO0  = ''
                    O000OO00O00O00000  = ['LDC1', 'LDC2', 'HDC1', 'HDC2', 'FVAP', 'LNGVAP', 'BOGHTR', 'WUHTR', 'GWHSTM', 'SCLR']
                    O0000000O00OO0OOO  = ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'BOGH', 'WUH', 'GWHS', 'SC']
                    for O00O0O00O000OOO00  in range(len(O000OO00O00O00000 )):
                        O0OO00OO0OO000O00  = O0OO00OO0OO000O00 .replace(O000OO00O00O00000 [O00O0O00O000OOO00 ] + '_', O0000000O00OO0OOO [O00O0O00O000OOO00 ] + '_')
                        OO00OOOO0O0OO00O0  = OO00OOOO0O0OO00O0 .replace(O000OO00O00O00000 [O00O0O00O000OOO00 ] + '_', O0000000O00OO0OOO [O00O0O00O000OOO00 ] + '_')
                    OOO000OO000O00000 .cursor.execute('insert into public."RCA_levels" values(%s, %s, %s, %s)', [O0OO00OO0OO000O00 , OO00OOOO0O0OO00O0 , O0O00OOO000OO0O00 , O0O0000OOO000OOO0 ])
                    OOO000OO000O00000 .conn.commit()
                    OO0O0OO000O00O00O [O0O00OOO000OO0O00 ] = O0O0000OOO000OOO0 
        return (OO0OOO0O00000OOO0 , OO0O0OO000O00O00O )
    def applyInferredStatus(OO0000O0O00OOO0OO , OO0O0O00O00O00000 ):
        OO0000O0O00OOO0OO .cursor.execute('select "Level3_Scenario", "Level4_RootCauses" from public."RCA_levels"')
        OOOO00O0O00000O0O  = OO0000O0O00OOO0OO .cursor.fetchall()
        OO0000O0O00OOO0OO .conn.commit()
        O0000O00O0O0O0OOO  = {}
        for item in OOOO00O0O00000O0O :
            O0000O00O0O0O0OOO [item[0]] = item[1].split(',')
        for O00OO0OO0OO0O0O0O  in O0000O00O0O0O0OOO .keys():
            if len(O0000O00O0O0O0OOO [O00OO0OO0OO0O0O0O ]) > 1:
                for rootcause in O0000O00O0O0O0OOO [O00OO0OO0OO0O0O0O ]:
                    if rootcause in OO0O0O00O00O00000 .keys():
                        if str(OO0O0O00O00O00000 [rootcause]) == 'True' and (str(OO0O0O00O00O00000 [O00OO0OO0OO0O0O0O ]) == 'False' or str(OO0O0O00O00O00000 [O00OO0OO0OO0O0O0O ]) == 'Unknown'):
                            OO0000O0O00OOO0OO .cursor.execute('update public."RCA_update" set "Status" = \'InferredTrue\' where "scenarioName" = %s', [O00OO0OO0OO0O0O0O ])
                            OO0000O0O00OOO0OO .conn.commit()
                            OO0O0O00O00O00000 [O00OO0OO0OO0O0O0O ] = 'InferredTrue'
        return OO0O0O00O00O00000 
    def updateRCAstatus(O00OO0O0OOOO00O0O , O0000O00O000OO0OO , OO00000O0O000O0OO , OOO0OO0O00O00OOO0 , OOO0OOOOO0O0O0O00 , OO0O0OOO0OOO0OOOO , OO0O0OOOO00O0OO0O , O0O0OO00OO00O0O00 ):
        O00OO00OOO0O00000  = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 'GCU', 'INCIN']
        if O00OO0O0OOOO00O0O .compare_pre_and_curr_status == 1:
            for scenario in O0000O00O000OO0OO .keys():
                if scenario not in OOO0OO0O00O00OOO0 .keys():
                    OOO0OO0O00O00OOO0 [scenario] = 'NAnow_Modified'
            for scenario in OO0O0OOO0OOO0OOOO :
                if scenario not in O0000O00O000OO0OO .keys():
                    if scenario in OOO0OO0O00O00OOO0 :
                        O0000O00O000OO0OO [scenario] = [OOO0OOOOO0O0O0O00 , OOO0OO0O00O00OOO0 [scenario]]
                    else:
                        O0000O00O000OO0OO [scenario] = [OOO0OOOOO0O0O0O00 , 'NAnow_Modified']
                    O00OO0O0OOOO00O0O .cursor.execute('insert into public."Prestatus" values(%s,%s,%s)', [scenario, O0000O00O000OO0OO [scenario][0], O0000O00O000OO0OO [scenario][1]])
        for scenario in OO0O0OOO0OOO0OOOO :
            O00O0O0OOOOOOO00O  = scenario.split('_')[0]
            OO0OO0O0O000O0000  = OOO0OO0O00O00OOO0 [scenario]
            if O00OO0O0OOOO00O0O .test_run == 1:
                OO0OO0O0O000O0000  = 'True'
            if OO0OO0O0O000O0000  == 'True' or OO0OO0O0O000O0000  == 'InferredTrue':
                OOO000O00OOOO0OO0  = O0O0OO00OO00O0O00 [scenario]
                O0000O0OO0O0O0000  = {}
                OO000000O0OO0O0O0  = {}
                if len(OOO000O00OOOO0OO0 ) == 0:
                    OOO000O0OO00000OO  = 'None'
                    O0O00O00O00OO000O  = 'None'
                else:
                    OOO000O00OOOO0OO0  = OOO000O00OOOO0OO0 .split(',')
                    O0000O0OO0O0O0000  = {}
                    OO000000O0OO0O0O0  = {}
                    for rootcause in OOO000O00OOOO0OO0 :
                        if rootcause in OOO0OO0O00O00OOO0 .keys():
                            OOOOOO00O00O0OO0O  = str(OOO0OO0O00O00OOO0 [rootcause])
                        else:
                            OOOOOO00O00O0OO0O  = 'Unknown'
                        OO000OO00000OOO0O  = OO000OO00000OOO0O .split('_')
                        OO000OO00000OOO0O  = '_'.join(OO000OO00000OOO0O [1:])
                        if OOOOOO00O00O0OO0O  == 'True':
                            O0000O0OO0O0O0000 [OO000OO00000OOO0O ] = OOOOOO00O00O0OO0O 
                        elif OOOOOO00O00O0OO0O  == 'Unknown':
                            OO000000O0OO0O0O0 [OO000OO00000OOO0O ] = OOOOOO00O00O0OO0O 
                        else:
                            OOOOOO00O00O0OO0O  = 'False'
                            OO000000O0OO0O0O0 [OO000OO00000OOO0O ] = OOOOOO00O00O0OO0O 
                    if len(O0000O0OO0O0O0000 ) == 0:
                        OOO000O0OO00000OO  = 'None'
                    else:
                        OOO000O0OO00000OO  = json.dumps(O0000O0OO0O0O0000 )
                    if len(OO000000O0OO0O0O0 ) == 0:
                        O0O00O00O00OO000O  = 'None'
                    else:
                        O0O00O00O00OO000O  = json.dumps(OO000000O0OO0O0O0 )
                    OO0O00000O0O0OOO0  = '{}"'
                    for item in OO0O00000O0O0OOO0 :
                        OOO000O0OO00000OO  = OOO000O0OO00000OO .replace(item, '')
                        OOO000O0OO00000OO  = OOO000O0OO00000OO .replace(',', '   ---   ')
                        O0O00O00O00OO000O  = O0O00O00O00OO000O .replace(item, '')
                        O0O00O00O00OO000O  = O0O00O00O00OO000O .replace(',', '   ---   ')
                O0O0OO0OOO0OOO00O  = scenario.split('_')
                O0O0OO0OOO0OOO00O  = '_'.join(O0O0OO0OOO0OOO00O [1:])
                O00OO0O0OOOO00O0O .cursor.execute('select "Level3_Scenario", "ScenarioStatus", "Level4_ActiveRootCauses", "Level4_OtherRootCauses" from public."RCA_Active" where "ScenarioID" = %s', [scenario])
                OOOO00O0O00000O0O  = O00OO0O0OOOO00O0O .cursor.fetchall()
                O00OO0O0OOOO00O0O .conn.commit()
                OOOO0O0OOOOOO00O0  = '%d/%m/%Y %H:%M:%S'
                O0OO000000O0OOO0O  = pd.to_datetime(datetime.now(), format=OOOO0O0OOOOOO00O0 )
                O0O00O000OO00O0O0  = scenario + ' => ' + OO0O0OOOO00O0OO0O [scenario] + ' --- '
                if len(O0000O0OO0O0O0000 .keys()) > 0:
                    for O00OO0OO0OO0O0O0O  in O0000O0OO0O0O0000 .keys():
                        O00OO0OO0OO0O0O0O  = O00O0O0OOOOOOO00O  + '_' + O00OO0OO0OO0O0O0O 
                        O0O00O000OO00O0O0  = O0O00O000OO00O0O0  + O00OO0OO0OO0O0O0O  + ' => ' + OO0O0OOOO00O0OO0O [O00OO0OO0OO0O0O0O ] + ' --- '
                O0O00O000OO00O0O0  = O0O00O000OO00O0O0 [:-5]
                if O00OO0O0OOOO00O0O .hide_rules == 1:
                    O0O00O000OO00O0O0  = 'NA'
                if len(OOOO00O0O00000O0O ) == 0:
                    O00OO0O0OOOO00O0O .cursor.execute('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)', [str(O0OO000000O0OOO0O ), O0O0OO0OOO0OOO00O , OO0OO0O0O000O0000 , OOO000O0OO00000OO , O0O00O00O00OO000O , scenario, OOO0OOOOO0O0O0O00 , O0O00O000OO00O0O0 ])
                    O00OO0O0OOOO00O0O .conn.commit()
                    O0OO0O0OOO0O0O000  = O0000O00O000OO0OO [scenario][1]
                    OO0OOO0OOO000O0OO  = O0000O00O000OO0OO [scenario][0]
                    OO0OOO0OOO000O0OO  = pd.to_datetime(OO0OOO0OOO000O0OO )
                    O000OOO00O0000OO0  = pd.to_datetime(OOO0OOOOO0O0O0O00 )
                    O0O0OO0000OOO0OO0  = (O000OOO00O0000OO0  - OO0OOO0OOO000O0OO ).total_seconds() / 60
                    O0O0OO0000OOO0OO0  = float('{0:.2f}'.format(O0O0OO0000OOO0OO0 ))
                    O00OO0O0OOOO00O0O .cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(OO0OOO0OOO000O0OO ), str(O000OOO00O0000OO0 ), int(O0O0OO0000OOO0OO0 ), O0O0OO0OOO0OOO00O , O0OO0O0OOO0O0O000 , OO0OO0O0O000O0000 , OOO000O0OO00000OO , O0O00O00O00OO000O , scenario, str(O0OO000000O0OOO0O ), O0O00O000OO00O0O0 , 'Open', 'None'])
                    O00OO0O0OOOO00O0O .conn.commit()
                    O0000O00O000OO0OO [scenario] = [str(O000OOO00O0000OO0 ), OO0OO0O0O000O0000 ]
                else:
                    OOO00OOO0O0O00O00  = OOOO00O0O00000O0O [0]
                    O0O00OOOO000OO0O0  = OOO00OOO0O0O00O00 [0]
                    O0OO0O0OOO0O0O000  = OOO00OOO0O0O00O00 [1]
                    O0O0O0O000O0O0O00  = OOO00OOO0O0O00O00 [2]
                    OO00O00O0OO0OO0OO  = OOO00OOO0O0O00O00 [3]
                    OO0OOO0OOO000O0OO  = O0000O00O000OO0OO [scenario][0]
                    OO0OOO0OOO000O0OO  = pd.to_datetime(OO0OOO0OOO000O0OO )
                    O000OOO00O0000OO0  = pd.to_datetime(OOO0OOOOO0O0O0O00 )
                    O0000O00O000OO0OO [scenario] = [str(OO0OOO0OOO000O0OO ), OO0OO0O0O000O0000 ]
                    if O0O0OO0OOO0OOO00O  != O0O00OOOO000OO0O0  or OO0OO0O0O000O0000  != O0OO0O0OOO0O0O000  or OOO000O0OO00000OO  != O0O0O0O000O0O0O00  or (O0O00O00O00OO000O  != OO00O00O0OO0OO0OO ):
                        O00OO0O0OOOO00O0O .cursor.execute('delete from public."RCA_Active" where "ScenarioID" = %s', [scenario])
                        O00OO0O0OOOO00O0O .conn.commit()
                        O00OO0O0OOOO00O0O .cursor.execute('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)', [str(O0OO000000O0OOO0O ), O0O0OO0OOO0OOO00O , OO0OO0O0O000O0000 , OOO000O0OO00000OO , O0O00O00O00OO000O , scenario, OOO0OOOOO0O0O0O00 , O0O00O000OO00O0O0 ])
                        O00OO0O0OOOO00O0O .conn.commit()
                        O0O0OO0000OOO0OO0  = (O000OOO00O0000OO0  - OO0OOO0OOO000O0OO ).total_seconds() / 60
                        O0O0OO0000OOO0OO0  = float('{0:.2f}'.format(O0O0OO0000OOO0OO0 ))
                        O00OO0O0OOOO00O0O .cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(OO0OOO0OOO000O0OO ), str(O000OOO00O0000OO0 ), int(O0O0OO0000OOO0OO0 ), O0O0OO0OOO0OOO00O , O0OO0O0OOO0O0O000 , OO0OO0O0O000O0000 , OOO000O0OO00000OO , O0O00O00O00OO000O , scenario, str(O0OO000000O0OOO0O ), O0O00O000OO00O0O0 , 'Open', 'None'])
                        O00OO0O0OOOO00O0O .conn.commit()
                        O0000O00O000OO0OO [scenario] = [str(O000OOO00O0000OO0 ), OO0OO0O0O000O0000 ]
            elif OO0OO0O0O000O0000  == 'False' or OO0OO0O0O000O0000  == 'Unknown' or OO0OO0O0O000O0000  == 'Unknown_AssetNotRunning' or (OO0OO0O0O000O0000  == 'NAnow_Modified') or (OO0OO0O0O000O0000  == 'Unknown_ComponentNotRunning'):
                O00OO0O0OOOO00O0O .cursor.execute('delete from public."RCA_Active" where "ScenarioID" = %s', [scenario])
                O00OO0O0OOOO00O0O .conn.commit()
                O0OO0O0OOO0O0O000  = O0000O00O000OO0OO [scenario][1]
                OOOO0O0OOOOOO00O0  = '%d/%m/%Y %H:%M:%S'
                O0OO000000O0OOO0O  = pd.to_datetime(datetime.now(), format=OOOO0O0OOOOOO00O0 )
                OO0OOO0OOO000O0OO  = O0000O00O000OO0OO [scenario][0]
                OO0OOO0OOO000O0OO  = pd.to_datetime(OO0OOO0OOO000O0OO )
                O000OOO00O0000OO0  = pd.to_datetime(OOO0OOOOO0O0O0O00 )
                O0O0OO0OOO0OOO00O  = scenario.replace(O00O0O0OOOOOOO00O  + '_', '')
                if O0OO0O0OOO0O0O000  != OO0OO0O0O000O0000 :
                    O0O0OO0000OOO0OO0  = (O000OOO00O0000OO0  - OO0OOO0OOO000O0OO ).total_seconds() / 60
                    O0O0OO0000OOO0OO0  = float('{0:.2f}'.format(O0O0OO0000OOO0OO0 ))
                    OOO000O0OO00000OO  = 'None'
                    O0O00O00O00OO000O  = 'None'
                    O00OO0O0OOOO00O0O .cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(OO0OOO0OOO000O0OO ), str(O000OOO00O0000OO0 ), int(O0O0OO0000OOO0OO0 ), O0O0OO0OOO0OOO00O , O0OO0O0OOO0O0O000 , OO0OO0O0O000O0000 , OOO000O0OO00000OO , O0O00O00O00OO000O , scenario, str(O0OO000000O0OOO0O ), 'NA', 'Open', 'None'])
                    O00OO0O0OOOO00O0O .conn.commit()
                    O0000O00O000OO0OO [scenario] = [str(O000OOO00O0000OO0 ), OO0OO0O0O000O0000 ]
        for scenario in O0000O00O000OO0OO .keys():
            O00OO0O0OOOO00O0O .cursor.execute('update public."Prestatus" set "TimeStamp" = %s where "Scenario" = %s', [O0000O00O000OO0OO [scenario][0], scenario])
            O00OO0O0OOOO00O0O .conn.commit()
            O00OO0O0OOOO00O0O .cursor.execute('update public."Prestatus" set "Status" = %s where "Scenario" = %s', [O0000O00O000OO0OO [scenario][1], scenario])
            O00OO0O0OOOO00O0O .conn.commit()
        return O0000O00O000OO0OO 
    def saveHOS(OOOOO000000000OOO , O0O00O0000O00000O , OOO0O00000O000O00 , O0OOO00OO0O00000O , O000000O000OOOO00 , OO0OO000OO0000OO0 , OO00O0O0O0O000OO0 , O0OOOOO0O0O00O00O ):
        O0O00O0000O00000O  = pd.to_datetime(O0O00O0000O00000O , format='%Y-%m-%d %H:%M:%S')
        O000000O000OOOO00  = pd.to_datetime(O000000O000OOOO00 , format='%Y-%m-%d %H:%M:%S')
        O000OO0000O0O00O0  = []
        for O00OO0OO0OO0O0O0O  in OO00O0O0O0O000OO0 .keys():
            O000OO0000O0O00O0 .append(O00OO0OO0OO0O0O0O )
            O000OO0000O0O00O0  = O000OO0000O0O00O0  + OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]
        for item in O0OOO00OO0O00000O .keys():
            if item not in O000OO0000O0O00O0 :
                print(item, '=> not present in hierarchy')
        O0000OOO0O00O0OO0  = False
        OOO00O0OOO00O0OOO  = {}
        for O00OO0OO0OO0O0O0O  in OO00O0O0O0O000OO0 .keys():
            if OOO0O00000O000O00 [O00OO0OO0OO0O0O0O ] == 1 and OO0OO000OO0000OO0 [O00OO0OO0OO0O0O0O ] == 1:
                O00OOOOO0OO0O0OOO  = O000000O000OOOO00  - O0O00O0000O00000O 
                O00OOOOO0OO0O0OOO  = O00OOOOO0OO0O0OOO .total_seconds()
                if O00OOOOO0OO0O0OOO  > 180.0:
                    O00OOOOO0OO0O0OOO  = 60.0
                O00OOOOO0OO0O0OOO  = O00OOOOO0OO0O0OOO  / 3600
                OOO00O0OOO00O0OOO [O00OO0OO0OO0O0O0O ] = O0OOOOO0O0O00O00O [O00OO0OO0OO0O0O0O ] + O00OOOOO0OO0O0OOO 
            else:
                OOO00O0OOO00O0OOO [O00OO0OO0OO0O0O0O ] = O0OOOOO0O0O00O00O [O00OO0OO0OO0O0O0O ]
            if len(OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]) > 0:
                for OOOOOOOO00000O000  in OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]:
                    if OOO0O00000O000O00 [OOOOOOOO00000O000 ] == 1 and OO0OO000OO0000OO0 [OOOOOOOO00000O000 ] == 1:
                        O00OOOOO0OO0O0OOO  = O000000O000OOOO00  - O0O00O0000O00000O 
                        O00OOOOO0OO0O0OOO  = O00OOOOO0OO0O0OOO .total_seconds()
                        if O00OOOOO0OO0O0OOO  > 180.0:
                            O00OOOOO0OO0O0OOO  = 60.0
                        O00OOOOO0OO0O0OOO  = O00OOOOO0OO0O0OOO  / 3600
                        OOO00O0OOO00O0OOO [OOOOOOOO00000O000 ] = O0OOOOO0O0O00O00O [OOOOOOOO00000O000 ] + O00OOOOO0OO0O0OOO 
                    else:
                        OOO00O0OOO00O0OOO [OOOOOOOO00000O000 ] = O0OOOOO0O0O00O00O [OOOOOOOO00000O000 ]
        if O0O00O0000O00000O .date() != O000000O000OOOO00 .date():
            O0000OOO0O00O0OO0  = True
            print('new day started, so dailyHOS to write')
        if O0000OOO0O00O0OO0 :
            for O00OO0OO0OO0O0O0O  in OO00O0O0O0O000OO0 .keys():
                OO00OOO0O000O00O0  = OOO00O0OOO00O0OOO [O00OO0OO0OO0O0O0O ]
                if OO00OOO0O000O00O0  > 24.0 and OO00OOO0O000O00O0  < 24.3:
                    OO00OOO0O000O00O0  = 24.0
                OO00OOO0O000O00O0  = '{0:.3f}'.format(OO00OOO0O000O00O0 )
                OOOOO000000000OOO .cursor.execute('insert into public."DailyHOS" values(%s,%s,%s,%s)', [str(O0O00O0000O00000O .date()), O00OO0OO0OO0O0O0O , '-', OO00OOO0O000O00O0 ])
                OOOOO000000000OOO .conn.commit()
                OOOOO000000000OOO .cursor.execute('update public."HOS" set "DailyHOS" = %s where "Asset" = %s', [OO00OOO0O000O00O0 , O00OO0OO0OO0O0O0O ])
                OOOOO000000000OOO .conn.commit()
                O0OOOOO0O0O00O00O [O00OO0OO0OO0O0O0O ] = 0
                if len(OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]) > 0:
                    for OOOOOOOO00000O000  in OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]:
                        OO00OOO0O000O00O0  = OOO00O0OOO00O0OOO [OOOOOOOO00000O000 ]
                        if OO00OOO0O000O00O0  > 24.0 and OO00OOO0O000O00O0  < 24.3:
                            OO00OOO0O000O00O0  = 24.0
                        OO00OOO0O000O00O0  = '{0:.3f}'.format(OO00OOO0O000O00O0 )
                        OOOOO000000000OOO .cursor.execute('insert into public."DailyHOS" values(%s,%s,%s,%s)', [str(O0O00O0000O00000O .date()), O00OO0OO0OO0O0O0O , OOOOOOOO00000O000 , OO00OOO0O000O00O0 ])
                        OOOOO000000000OOO .conn.commit()
                        OOOOO000000000OOO .cursor.execute('update public."HOS" set "DailyHOS" = %s where "Asset" = %s', [OO00OOO0O000O00O0 , OOOOOOOO00000O000 ])
                        OOOOO000000000OOO .conn.commit()
                        O0OOOOO0O0O00O00O [OOOOOOOO00000O000 ] = 0
            OOOOO000000000OOO .cursor.execute('update public."HOS" set "TodaySoFar" = 0')
            OOOOO000000000OOO .conn.commit()
        else:
            for O00OO0OO0OO0O0O0O  in OO00O0O0O0O000OO0 .keys():
                OO00OOO0O000O00O0  = '{0:.3f}'.format(OOO00O0OOO00O0OOO [O00OO0OO0OO0O0O0O ])
                OOOOO000000000OOO .cursor.execute('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s', [OO00OOO0O000O00O0 , O00OO0OO0OO0O0O0O ])
                OOOOO000000000OOO .conn.commit()
                O0OOOOO0O0O00O00O [O00OO0OO0OO0O0O0O ] = float(OO00OOO0O000O00O0 )
                if len(OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]) > 0:
                    for OOOOOOOO00000O000  in OO00O0O0O0O000OO0 [O00OO0OO0OO0O0O0O ]:
                        OO00OOO0O000O00O0  = '{0:.3f}'.format(OOO00O0OOO00O0OOO [OOOOOOOO00000O000 ])
                        OOOOO000000000OOO .cursor.execute('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s', [OO00OOO0O000O00O0 , OOOOOOOO00000O000 ])
                        OOOOO000000000OOO .conn.commit()
                        O0OOOOO0O0O00O00O [OOOOOOOO00000O000 ] = float(OO00OOO0O000O00O0 )
        for O00O0O0OOOOOOO00O  in O0OOO00OO0O00000O .keys():
            O0O0O0OO000OOO000  = O0OOO00OO0O00000O [O00O0O0OOOOOOO00O ]
            O0O000OO00O00000O  = OO0OO000OO0000OO0 [O00O0O0OOOOOOO00O ]
            if OOO0O00000O000O00 [O00O0O0OOOOOOO00O ] == 1 and O0O000OO00O00000O  == 1:
                O0O00O0O00000OOOO  = O000000O000OOOO00  - O0O00O0000O00000O 
                O0O00O0O00000OOOO  = O0O00O0O00000OOOO .total_seconds()
                if O0O00O0O00000OOOO  > 180.0:
                    O0O00O0O00000OOOO  = 60.0
                O0O00O0O00000OOOO  = O0O00O0O00000OOOO  / 3600
                O0OO000OOO00O00OO  = O0O0O0OO000OOO000  + O0O00O0O00000OOOO 
                if O0OO000OOO00O00OO  < 0:
                    O0OO000OOO00O00OO  = 0
            else:
                O0OO000OOO00O00OO  = O0O0O0OO000OOO000 
            O0OOO00OO0O00000O [O00O0O0OOOOOOO00O ] = O0OO000OOO00O00OO 
            OOO0O00000O000O00 [O00O0O0OOOOOOO00O ] = O0O000OO00O00000O 
        for O00O0O0OOOOOOO00O  in O0OOO00OO0O00000O .keys():
            OOOOO000000000OOO .cursor.execute('update public."HOS" set "HOS" = %s where "Asset" = %s', ['{0:.3f}'.format(O0OOO00OO0O00000O [O00O0O0OOOOOOO00O ]), O00O0O0OOOOOOO00O ])
            OOOOO000000000OOO .conn.commit()
            OOOOO000000000OOO .cursor.execute('update public."HOS" set "TimeStamp" = %s where "Asset" = %s', [str(O000000O000OOOO00 ), O00O0O0OOOOOOO00O ])
            OOOOO000000000OOO .conn.commit()
        O0O00O0000O00000O  = O000000O000OOOO00 
        return (O0O00O0000O00000O , OOO0O00000O000O00 , O0OOO00OO0O00000O , O0OOOOO0O0O00O00O )
    def maintenanceAlarm(OOOOO0O00000O00O0 , O0OOOO0O000OOO0O0 , O0O0O0O0OOOO00O0O ):
        O00OOOOOOOO000O00  = 24 * 7
        OOOO0O0O0OOOO0OOO  = np.array([720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200, 7920, 8640, 9360, 10080, 10800, 11520, 12240, 12960, 13680, 14400, 15120, 15840, 16560, 17280, 18000, 18720, 19440, 20160, 20880, 21600, 22320, 23040, 23760, 24480, 25200, 25920, 26640, 27360, 28080, 28800, 29520, 30240, 30960, 31680, 32400, 33120, 33840, 34560, 35280, 36000, 36720, 37440, 38160, 38880, 39600, 40320, 41040, 41760, 42480, 43200])
        O00OOOO00O0O00O0O  = np.array([2160, 4320, 6480, 8640, 10800, 12960, 15120, 17280, 19440, 21600, 23760, 25920, 28080, 30240, 32400, 34560, 36720, 38880, 41040, 43200])
        OOO000O0OOO0OO00O  = np.array([4320, 8640, 12960, 17280, 21600, 25920, 30240, 34560, 38880, 43200])
        O000O00O00OOOO00O  = np.array([8640, 17280, 25920, 34560, 43200])
        OOOO0O00OO00OOOOO  = np.array([10000, 20000, 30000, 40000, 50000])
        O0OO00OO00OOO0O0O  = np.array([21600, 43200])
        OO0O0O0O00000O00O  = np.array([43200])
        O0O00O0O0O0000O00  = np.array([86400])
        OO000OOOOOO000OOO  = OOOO0O0O0OOOO0OOO  + O00OOOOOOOO000O00 
        OOOOOOO0OO0O000OO  = O00OOOO00O0O00O0O  + O00OOOOOOOO000O00 
        OOOOO00OO00OO0OOO  = OOO000O0OOO0OO00O  + O00OOOOOOOO000O00 
        O00O00O0OO00OOOOO  = O000O00O00OOOO00O  + O00OOOOOOOO000O00 
        O00O00OOOOOO000O0  = OOOO0O00OO00OOOOO  + O00OOOOOOOO000O00 
        O0OO0000000OO0OO0  = OO0O0O0O00000O00O  + O00OOOOOOOO000O00 
        O0OO0OOO0O00O00OO  = O0O00O0O0O0000O00  + O00OOOOOOOO000O00 
        O00O0O0O0O0OO0OO0  = O0OO00OO00OOO0O0O  + O00OOOOOOOO000O00 
        OOO000O00000O0OO0  = datetime.now()
        OOO000O00000O0OO0  = pd.to_datetime(OOO000O00000O0OO0 , format='%d/%m/%Y %H:%M:%S')
        O0OOOO0O000OOO0O0  = pd.to_datetime(O0OOOO0O000OOO0O0 )
        OO0O00000000OO000  = OOO000O00000O0OO0  - O0OOOO0O000OOO0O0 
        O00000OOO0O00O0O0  = OO0O00000000OO000 .total_seconds() / 3600
        OOOOO0O00000O00O0 .cursor.execute('update public."Calender_time" set "TimeStamp" = %s where "Kind" = \'Elapsed_time\';', [str(OOO000O00000O0OO0 )])
        OOOOO0O00000O00O0 .conn.commit()
        OOOOO0O00000O00O0 .cursor.execute('update public."Calender_time" set "Value" = %s where "Kind" = \'Elapsed_time\';', [O00000OOO0O00O0O0 ])
        OOOOO0O00000O00O0 .conn.commit()
        OO000O0O00O00OO00  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        O0OO00O0O00O0OO00  = ['LD1_half_year_HOS', 'LD1_year_HOS', 'LD1_5years_HOS', 'LD2_half_year_HOS', 'LD2_year_HOS', 'LD2_5years_HOS', 'HD1_3months_HOS', 'HD1_half_year_HOS', 'HD1_year_HOS', 'HD1_5years_HOS', 'HD1_10years_HOS', 'HD2_3months_HOS', 'HD2_half_year_HOS', 'HD2_year_HOS', 'HD2_5years_HOS', 'HD2_10years_HOS', 'SC_10000hrs_HOS', 'SC_3months_HOS', 'SC_year_HOS', 'SC_5years_HOS', 'FV_half_year_HOS', 'FV_year_HOS', 'FV_30months_HOS', 'FV_5years_HOS', 'LNGV_half_year_HOS', 'LNGV_year_HOS', 'LNGV_30months_HOS', 'LNGV_5years_HOS', 'GWHS_month_HOS', 'GWHS_year_HOS', 'GWHS_5years_HOS']
        for O00O0O0OOOOOOO00O  in O0O0O0O0OOOO00O0O .keys():
            if O00O0O0OOOOOOO00O  in ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'GWHS', 'SC']:
                OO0000OOOOO000OOO  = [O00O0O0OOOOOOO00O  + '_month_HOS', O00O0O0OOOOOOO00O  + '_3months_HOS', O00O0O0OOOOOOO00O  + '_half_year_HOS', O00O0O0OOOOOOO00O  + '_year_HOS', O00O0O0OOOOOOO00O  + '_10000hrs_HOS', O00O0O0OOOOOOO00O  + '_30months_HOS', O00O0O0OOOOOOO00O  + '_5years_HOS', O00O0O0OOOOOOO00O  + '_10years_HOS']
                OOO000OOOO00O0OO0  = {O00O0O0OOOOOOO00O  + '_month_HOS': OOOO0O0O0OOOO0OOO , O00O0O0OOOOOOO00O  + '_3months_HOS': O00OOOO00O0O00O0O , O00O0O0OOOOOOO00O  + '_half_year_HOS': OOO000O0OOO0OO00O , O00O0O0OOOOOOO00O  + '_year_HOS': O000O00O00OOOO00O , O00O0O0OOOOOOO00O  + '_10000hrs_HOS': OOOO0O00OO00OOOOO , O00O0O0OOOOOOO00O  + '_30months_HOS': O0OO00OO00OOO0O0O , O00O0O0OOOOOOO00O  + '_5years_HOS': OO0O0O0O00000O00O , O00O0O0OOOOOOO00O  + '_10years_HOS': O0O00O0O0O0000O00 }
                O00OOO00OO0O0OOO0  = {O00O0O0OOOOOOO00O  + '_month_HOS': OO000OOOOOO000OOO , O00O0O0OOOOOOO00O  + '_3months_HOS': OOOOOOO0OO0O000OO , O00O0O0OOOOOOO00O  + '_half_year_HOS': OOOOO00OO00OO0OOO , O00O0O0OOOOOOO00O  + '_year_HOS': O00O00O0OO00OOOOO , O00O0O0OOOOOOO00O  + '_10000hrs_HOS': O00O00OOOOOO000O0 , O00O0O0OOOOOOO00O  + '_30months_HOS': O00O0O0O0O0OO0OO0 , O00O0O0OOOOOOO00O  + '_5years_HOS': O0OO0000000OO0OO0 , O00O0O0OOOOOOO00O  + '_10years_HOS': O0OO0OOO0O00O00OO }
                O0OO00OOO0O000O00  = ['half_year_calender', 'year_calender', '5years_calender']
                OOOOOO0000OO0OOO0  = {'half_year_calender': OOO000O0OOO0OO00O , 'year_calender': O000O00O00OOOO00O , '5years_calender': OO0O0O0O00000O00O }
                OO0O00O0OOO00OO0O  = {'half_year_calender': OOOOO00OO00OO0OOO , 'year_calender': O00O00O0OO00OOOOO , '5years_calender': O0OO0000000OO0OO0 }
                for item in OO0000OOOOO000OOO :
                    if item in O0OO00O0O00O0OO00 :
                        for O00O0O00O000OOO00  in range(len(OOO000OOOO00O0OO0 [item])):
                            if int(O0O0O0O0OOOO00O0O [O00O0O0OOOOOOO00O ]) >= OOO000OOOO00O0OO0 [item][O00O0O00O000OOO00 ] and int(O0O0O0O0OOOO00O0O [O00O0O0OOOOOOO00O ]) <= O00OOO00OO0O0OOO0 [item][O00O0O00O000OOO00 ]:
                                OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [1, item])
                                OOOOO0O00000O00O0 .conn.commit()
                                OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [OO000O0O00O00OO00 , item])
                                OOOOO0O00000O00O0 .conn.commit()
                                break
                            else:
                                OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [0, item])
                                OOOOO0O00000O00O0 .conn.commit()
                                OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [OO000O0O00O00OO00 , item])
                                OOOOO0O00000O00O0 .conn.commit()
                for item in O0OO00OOO0O000O00 :
                    for O00O0O00O000OOO00  in range(len(OOOOOO0000OO0OOO0 [item])):
                        if int(O00000OOO0O00O0O0 ) >= OOOOOO0000OO0OOO0 [item][O00O0O00O000OOO00 ] and int(O00000OOO0O00O0O0 ) <= OO0O00O0OOO00OO0O [item][O00O0O00O000OOO00 ]:
                            OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [1, item])
                            OOOOO0O00000O00O0 .conn.commit()
                            OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [OO000O0O00O00OO00 , item])
                            OOOOO0O00000O00O0 .conn.commit()
                            break
                        else:
                            OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [0, item])
                            OOOOO0O00000O00O0 .conn.commit()
                            OOOOO0O00000O00O0 .cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [OO000O0O00O00OO00 , item])
                            OOOOO0O00000O00O0 .conn.commit()
    def saveAlertCount(OO0OO00O0OO000OOO ):
        OOOOOOO0OO0OOO0O0  = {}
        O0000OO0O0O00O0O0  = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 'GCU', 'INCIN']
        for O00O0O0OOOOOOO00O  in O0000OO0O0O00O0O0 :
            OO0OO00O0OO000OOO .cursor.execute(f"""select "ScenarioID" from public."RCA_Active" where "ScenarioID" like '{O00O0O0OOOOOOO00O }%';""")
            OOOO00O0O00000O0O  = OO0OO00O0OO000OOO .cursor.fetchall()
            OO0OO00O0OO000OOO .conn.commit()
            OOOOOOO0OO0OOO0O0 [O00O0O0OOOOOOO00O ] = len(OOOO00O0O00000O0O )
        for O00OO0OO0OO0O0O0O  in OOOOOOO0OO0OOO0O0 .keys():
            O00O0O0OOOOOOO00O  = O00OO0OO0OO0O0O0O 
            O00000O0O000O00O0  = OOOOOOO0OO0OOO0O0 [O00OO0OO0OO0O0O0O ]
            OO0OO00O0OO000OOO .cursor.execute('update public."Active_count" set "Alert_count" = %s where "Asset" = %s', [O00000O0O000O00O0 , O00O0O0OOOOOOO00O ])
            OO0OO00O0OO000OOO .conn.commit()
            OO0OO00O0OO000OOO .cursor.execute('update public."Active_count" set "TimeStamp" = %s where "Asset" = %s', [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), O00O0O0OOOOOOO00O ])
            OO0OO00O0OO000OOO .conn.commit()
    def totalAvailableScenarios(O0000O0O0OOO00000 ):
        O0OOO00OOO0O00O00  = {}
        O0000OO0O0O00O0O0  = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 'GCU', 'INCIN']
        for O00O0O0OOOOOOO00O  in O0000OO0O0O00O0O0 :
            O0000O0O0OOO00000 .cursor.execute(f"""select "Level3_ScenarioName" from public."RCA_ID" where "Level3_ScenarioName" like '{O00O0O0OOOOOOO00O }%';""")
            OOOO00O0O00000O0O  = O0000O0O0OOO00000 .cursor.fetchall()
            O0000O0O0OOO00000 .conn.commit()
            O0OOO00OOO0O00O00 [O00O0O0OOOOOOO00O ] = len(OOOO00O0O00000O0O )
        for O00OO0OO0OO0O0O0O  in O0OOO00OOO0O00O00 .keys():
            O00O0O0OOOOOOO00O  = O00OO0OO0OO0O0O0O 
            O00000O0O000O00O0  = O0OOO00OOO0O00O00 [O00OO0OO0OO0O0O0O ]
            O0000O0O0OOO00000 .cursor.execute('update public."Active_count" set "Total_count" = %s where "Asset" = %s', [O00000O0O000O00O0 , O00O0O0OOOOOOO00O ])
            O0000O0O0OOO00000 .conn.commit()
    def runningStatusLogging(O00000000O00OO0OO , O00O0O0O000OO0O0O , OOO00O00OO0O00O0O ):
        OO0O000OO000O00OO  = ['Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy']
        for O00O0O0OOOOOOO00O  in O00O0O0O000OO0O0O .keys():
            O00OOO0OOOO0OO0O0  = f"""update public."Running_status_update" set "Status" = {O00O0O0O000OO0O0O [O00O0O0OOOOOOO00O ]} where "Asset" = '{O00O0O0OOOOOOO00O }';"""
            O00000000O00OO0OO .cursor.execute(O00OOO0OOOO0OO0O0 )
            O00000000O00OO0OO .conn.commit()
        O0O00O000OO000OO0  = 'Running_status_history'
        O00000000O00OO0OO .cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [O0O00O000OO000OO0 ])
        OOOO00O0O00000O0O  = O00000000O00OO0OO .cursor.fetchall()
        O00000000O00OO0OO .conn.commit()
        OO0O0OOO0OOO0OO00  = [item[0].replace('_running_status', '') for item in OOOO00O0O00000O0O ][1:]
        O00OOO0OOOO0OO0O0  = f"'{OOO00O00OO0O00O0O }', "
        for col in OO0O0OOO0OOO0OO00 :
            O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0  + f'{O00O0O0O000OO0O0O [col]}, '
        O00OOO0OOOO0OO0O0  = O00OOO0OOOO0OO0O0 [:-2] + ')'
        O00OOO0OOOO0OO0O0  = f'insert into public."Running_status_history" values({O00OOO0OOOO0OO0O0 }'
        O00000000O00OO0OO .cursor.execute(O00OOO0OOOO0OO0O0 )
        O00000000O00OO0OO .conn.commit()
    def importRCAtemplates(O00OOO00OO0OOO00O ):
        O0OO0O0O0OOOOO0O0  = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 'GCU', 'INCIN']
        O00OO000OOO0OO000  = O00OOO00OO0OOO00O .RCA_mastersheet_path
        OOOO0OO000O000O00  = io.BytesIO()
        with open(O00OO000OOO0OO000 , 'rb') as file:
            OO0O0O0OO0OOOOO00  = msoffcrypto.OfficeFile(file)
            OO0O0O0OO0OOOOO00 .load_key(O00OOO00OO0OOO00O .ent)
            OO0O0O0OO0OOOOO00 .decrypt(OOOO0OO000O000O00 )
        O00OO0O0OO0000O0O  = []
        for sheet in O0OO0O0O0OOOOO0O0 :
            O00OO0O0OO0000O0O .append(pd.read_excel(OOOO0OO000O000O00 , sheet_name=sheet))
        for O0OOO00O0000O00O0  in O00OO0O0OO0000O0O :
            O0OOO00O0000O00O0 .at[0, 'Parent_Node'] = 'None'
        return O00OO0O0OO0000O0O 
    def rcaID(OO00OO0000OOOO000 , OO000OOOOO0O00O0O ):
        OO00OO00O0OO00O0O  = {}
        for O00O0O00O000OOO00  in range(len(OO000OOOOO0O00O0O )):
            O0OOO00O0000O00O0  = OO000OOOOO0O00O0O [O00O0O00O000OOO00 ]
            O0OOO00O0000O00O0  = O0OOO00O0000O00O0 .loc[:, ['Problem_Name', 'Level', 'Implement', 'Priority', 'AdviceMessage']]
            O0OOO00O0000O00O0 .rename(columns={'Problem_Name': 'Level3_ScenarioName'}, inplace=True)
            OOOO00OOO000OO00O  = O0OOO00O0000O00O0 ['Level'] == 'SCENARIO'
            O0OOO00O0000O00O0  = O0OOO00O0000O00O0 [OOOO00OOO000OO00O ]
            OOOO00OOO000OO00O  = O0OOO00O0000O00O0 ['Implement'] == 1.0
            O0OOO00O0000O00O0  = O0OOO00O0000O00O0 [OOOO00OOO000OO00O ]
            if O00O0O00O000OOO00  == 0:
                OO000OOO0OOOOOOOO  = O0OOO00O0000O00O0 .copy()
            else:
                OO000OOO0OOOOOOOO  = pd.concat([OO000OOO0OOOOOOOO , O0OOO00O0000O00O0 ], axis=0)
        OO000OOO0OOOOOOOO  = OO000OOO0OOOOOOOO .drop_duplicates('Level3_ScenarioName', keep='first').reset_index()
        OO00OO0000OOOO000 .cursor.execute('truncate table public."RCA_ID"')
        OO00OO0000OOOO000 .conn.commit()
        for O00O0O00O000OOO00  in range(len(OO000OOO0OOOOOOOO .index)):
            O000OOO0000OO0OOO  = OO000OOO0OOOOOOOO .loc[O00O0O00O000OOO00 ]['Level3_ScenarioName']
            OOO000O0OO00OO000  = OO000OOO0OOOOOOOO .loc[O00O0O00O000OOO00 ]['Level']
            OOO0OOO00O000000O  = OO000OOO0OOOOOOOO .loc[O00O0O00O000OOO00 ]['Implement']
            O0OO0OOOOO00O0000  = OO000OOO0OOOOOOOO .loc[O00O0O00O000OOO00 ]['Priority']
            O0O00OOO0OO00O0O0  = OO000OOO0OOOOOOOO .loc[O00O0O00O000OOO00 ]['AdviceMessage']
            OO00OO0000OOOO000 .cursor.execute('insert into public."RCA_ID" values (%s, %s, %s, %s, %s)', [O000OOO0000OO0OOO , OOO000O0OO00OO000 , int(OOO0OOO00O000000O ), float(O0OO0OOOOO00O0000 ), O0O00OOO0OO00O0O0 ])
            OO00OO0000OOOO000 .conn.commit()
        OO0O0OOO0OOO0OOOO  = OO000OOO0OOOOOOOO ['Level3_ScenarioName'].values.tolist()
        return OO0O0OOO0OOO0OOOO 
    def updateSignal(OOOO000O0O00O0OO0 ):
        OOOO000O0O00O0OO0 .cursor.execute('select * from public."Templates_update"')
        OOOO00O0O00000O0O  = OOOO000O0O00O0OO0 .cursor.fetchall()
        OOOO000O0O00O0OO0 .conn.commit()
        O0O0OO00O0OOOOO0O  = OOOO00O0O00000O0O [0][1]
        return O0O0OO00O0OOOOO0O 
    def findRules(O000OO0OO0OO00O00 , OO0OO000O0O0O0000 ):
        O000OO0OO0OO00O00 .cursor.execute('truncate public."RCA_rules"')
        O000OO0OO0OO00O00 .conn.commit()
        OO0O0OOOO00O0OO0O  = {}
        O0O0O0O000O00O00O  = {}
        for O0OOO00O0000O00O0  in OO0OO000O0O0O0000 :
            O0OOO00O0000O00O0 .fillna('blank', inplace=True)
            O00OOO0OOOO00O0O0  = 'none'
            for O00O0O00O000OOO00  in range(len(O0OOO00O0000O00O0 .index)):
                OO0000OO0OO0O0OOO  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Problem_Name']
                if OO0000OO0OO0O0OOO  != O00OOO0OOOO00O0O0 :
                    OO0OO00OO0OOOOOO0  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Standard_Key']
                    O0O000O0O00O0OO0O  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Additional condition']
                    O0OOO00O0O0OOOO00  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Condition']
                    OOO000000O0000OOO  = str(O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Threshold'])
                    O00O00OO0O000O0OO  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Logic']
                    if OO0OO00OO0OOOOOO0  != 'blank':
                        if 'Intermediate' in OO0OO00OO0OOOOOO0 :
                            O0O00O000OO00O0O0  = f' ({OO0O0OOOO00O0OO0O [OO0OO00OO0OOOOOO0 ]}) {O00O00OO0O000O0OO } '
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('blank', '')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .strip()
                            OO0O0OOOO00O0OO0O [OO0000OO0OO0O0OOO ] = O0O00O000OO00O0O0 
                            O00OO0OO0OO0O0O0O  = O0O0O0O000O00O00O [OO0OO00OO0OOOOOO0 ]
                            O0O0O0O000O00O00O [OO0000OO0OO0O0OOO ] = O00OO0OO0OO0O0O0O 
                        else:
                            O0O00O000OO00O0O0  = f' {OO0OO00OO0OOOOOO0 } {O0OOO00O0O0OOOO00 } {OOO000000O0000OOO } {O0O000O0O00O0OO0O } {O00O00OO0O000O0OO } '
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('blank', '')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .strip()
                            OO0O0OOOO00O0OO0O [OO0000OO0OO0O0OOO ] = O0O00O000OO00O0O0 
                            O00OO0OO0OO0O0O0O  = OO0OO00OO0OOOOOO0 
                            O0O0O0O000O00O00O [OO0000OO0OO0O0OOO ] = O00OO0OO0OO0O0O0O 
                    elif OO0OO00OO0OOOOOO0  == 'blank':
                        OO0O0OOOO00O0OO0O [OO0000OO0OO0O0OOO ] = 'None'
                        O0O0O0O000O00O00O [OO0000OO0OO0O0OOO ] = 'None'
                    O00OOO0OOOO00O0O0  = OO0000OO0OO0O0OOO 
                elif OO0000OO0OO0O0OOO  == O00OOO0OOOO00O0O0 :
                    OO0OO00OO0OOOOOO0  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Standard_Key']
                    O0O000O0O00O0OO0O  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Additional condition']
                    O0OOO00O0O0OOOO00  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Condition']
                    OOO000000O0000OOO  = str(O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Threshold'])
                    O00O00OO0O000O0OO  = O0OOO00O0000O00O0 .loc[O00O0O00O000OOO00 ]['Logic']
                    if OO0OO00OO0OOOOOO0  != 'blank':
                        if 'Intermediate' in OO0OO00OO0OOOOOO0 :
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0  + f' ({OO0O0OOOO00O0OO0O [OO0OO00OO0OOOOOO0 ]}) {O00O00OO0O000O0OO } '
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('blank', '')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('  ', ' ')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .strip()
                            OO0O0OOOO00O0OO0O [OO0000OO0OO0O0OOO ] = O0O00O000OO00O0O0 
                            O00OO0OO0OO0O0O0O  = O00OO0OO0OO0O0O0O  + ', ' + O0O0O0O000O00O00O [OO0OO00OO0OOOOOO0 ]
                            O0O0O0O000O00O00O [OO0000OO0OO0O0OOO ] = O00OO0OO0OO0O0O0O 
                        else:
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0  + f' {OO0OO00OO0OOOOOO0 } {O0OOO00O0O0OOOO00 } {OOO000000O0000OOO } {O0O000O0O00O0OO0O } {O00O00OO0O000O0OO } '
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('blank', '')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .replace('  ', ' ')
                            O0O00O000OO00O0O0  = O0O00O000OO00O0O0 .strip()
                            OO0O0OOOO00O0OO0O [OO0000OO0OO0O0OOO ] = O0O00O000OO00O0O0 
                            O00OO0OO0OO0O0O0O  = O00OO0OO0OO0O0O0O  + ', ' + OO0OO00OO0OOOOOO0 
                            O0O0O0O000O00O00O [OO0000OO0OO0O0OOO ] = O00OO0OO0OO0O0O0O 
                    O00OOO0OOOO00O0O0  = OO0000OO0OO0O0OOO 
        for O0O00O00OO0O00OO0  in OO0O0OOOO00O0OO0O .keys():
            if O000OO0OO0OO00O00 .hide_rules == 1:
                OO0O0OOOO00O0OO0O [O0O00O00OO0O00OO0 ] = 'NA'
            O000OO0OO0OO00O00 .cursor.execute('insert into public."RCA_rules" values(%s,%s,%s)', [O0O00O00OO0O00OO0 , OO0O0OOOO00O0OO0O [O0O00O00OO0O00OO0 ], O0O0O0O000O00O00O [O0O00O00OO0O00OO0 ]])
            O000OO0OO0OO00O00 .conn.commit()
        return (OO0O0OOOO00O0OO0O , O0O0O0O000O00O00O )
    def alarmLoggingforNoKPIassets(OO0OOO0O0O0O0O000 , O00OOO0OO00OO0O00 , O0OO000OO0OOOO0OO ):
        for OO0OO00OO0OOOOOO0  in O00OOO0OO00OO0O00 :
            OO0OOO0O0O0O0O000 .cursor.execute('update public."Output_Tags" set "Value" = %s where "TagName" = %s', [float(O0OO000OO0OOOO0OO [OO0OO00OO0OOOOOO0 ]), OO0OO00OO0OOOOOO0 ])
            OO0OOO0O0O0O0O000 .conn.commit()
    def findtargetScenarios(OOO000OO000O0O0O0 , OOOOO0O00OO0000OO , OO0O00O0O0O0O0OOO ):
        O00000O00O00O00OO  = {}
        for O0O00O00OO0O00OO0  in OOOOO0O00OO0000OO .keys():
            OO00O000000O0000O  = True
            if OOOOO0O00OO0000OO [O0O00O00OO0O00OO0 ] == 'None':
                OO00O000000O0000O  = True
            else:
                O0OOOO0OOOO0OO0OO  = OOOOO0O00OO0000OO [O0O00O00OO0O00OO0 ].split(', ')
                for OO0OO00OO0OOOOOO0  in O0OOOO0OOOO0OO0OO :
                    if OO0OO00OO0OOOOOO0  in OO0O00O0O0O0O0OOO .keys():
                        if OO0O00O0O0O0O0OOO [OO0OO00OO0OOOOOO0 ] == 0:
                            OO00O000000O0000O  = False
                            break
            if OO00O000000O0000O :
                O00000O00O00O00OO [O0O00O00OO0O00OO0 ] = 1
            else:
                O00000O00O00O00OO [O0O00O00OO0O00OO0 ] = 0
        return O00000O00O00O00OO 
def main():
    import argparse
    OOOOO0OO00O0O0OOO  = argparse.ArgumentParser(description='Enter arguments')
    OOOOO0OO00O0O0OOO .add_argument('-H', '--host', required=True, help='Hostname or IP address')
    OOOOO0OO00O0O0OOO .add_argument('-U', '--user', required=True, help='Username')
    OOOOO0OO00O0O0OOO .add_argument('-P', '--password', required=True, help='Password')
    OOOOO0OO00O0O0OOO .add_argument('-p', '--port', required=True, help='port')
    OOOOO0OO00O0O0OOO .add_argument('-D', '--database', required=True, help='PostgreSQL database')
    OOOOO0OO00O0O0OOO .add_argument('-X', '--excelpwd', required=True, help='Excel sheet password')
    OOOOO0OO00O0O0OOO .add_argument('-d', '--dwsimpath', required=False, help='DWSIM Path')
    O0000O0000O00OO0O  = OOOOO0OO00O0O0OOO .parse_args()
    O00O0OOOO000O0000  = O0000O0000O00OO0O .host
    O00000000OO0O00O0  = O0000O0000O00OO0O .user
    OOO0OOOOO00OOOOO0  = O0000O0000O00OO0O .password
    O0000OOOOO0O0OOO0  = O0000O0000O00OO0O .database
    OOO0OOO00OOOOO00O  = O0000O0000O00OO0O .port
    OOOOOO00O00OOOO0O  = O0000O0000O00OO0O .excelpwd
    OO0OO00000000OO0O  = O0000O0000O00OO0O .dwsimpath
    if OO0OO00000000OO0O  == None:
        OO0OO00000000OO0O  = ''
    print(f'Host: {O00O0OOOO000O0000 }')
    print(f'Database: {O0000OOOOO0O0OOO0 }')
    print(f'User: {O00000000OO0O00O0 }')
    O0O00O0000OO00000  = slmApplication(O00000000OO0O00O0 , OOO0OOOOO00OOOOO0 , OOOOOO00O00OOOO0O , O00O0OOOO000O0000 , O0000OOOOO0O0OOO0 , OOO0OOO00OOOOO00O , OO0OO00000000OO0O )
    OO0OO000O0O0O0000  = O0O00O0000OO00000 .importRCAtemplates()
    OO0O0OOO0OOO0OOOO  = O0O00O0000OO00000 .rcaID(OO0OO000O0O0O0000 )
    O0O00O0000OO00000 .cursor.execute('select "TimeStamp" from public."Calender_time" where "Kind" = \'Start_of_run\';')
    OOOO00O0O00000O0O  = O0O00O0000OO00000 .cursor.fetchall()
    O0O00O0000OO00000 .conn.commit()
    O0OOOO0O000OOO0O0  = OOOO00O0O00000O0O [0][0]
    O0000O00O000OO0OO  = {}
    O0O00O0000OO00000 .cursor.execute('select * from public."Prestatus"')
    OOOO00O0O00000O0O  = O0O00O0000OO00000 .cursor.fetchall()
    O0O00O0000OO00000 .conn.commit()
    O0000O00O000OO0OO  = {}
    for item in OOOO00O0O00000O0O :
        O0000O00O000OO0OO [item[0]] = [item[1], item[2]]
    O0O0O0O0OOOO00O0O  = {}
    O0OOOOO0O0O00O00O  = {}
    O0O00O0000OO00000 .cursor.execute('select "Asset", "HOS", "TodaySoFar" from public."HOS"')
    OO00OOOO0000OOO00  = O0O00O0000OO00000 .cursor.fetchall()
    O0O00O0000OO00000 .conn.commit()
    for item in OO00OOOO0000OOO00 :
        O0O0O0O0OOOO00O0O [item[0]] = item[1]
        O0OOOOO0O0O00O00O [item[0]] = item[2]
    OOO0O00000O000O00  = {}
    for item in O0O0O0O0OOOO00O0O .keys():
        OOO0O00000O000O00 [item] = 1
    O000OO0OOOOOOO0O0  = True
    O0O00O0000OO00000 .cursor.execute('select "Standard_Key" from public."Input_Tags"')
    OOOO00O0O00000O0O  = O0O00O0000OO00000 .cursor.fetchall()
    O0O00O0000OO00000 .conn.commit()
    O0OO0O0OOOOOO00OO  = []
    for item in OOOO00O0O00000O0O :
        O0OO0O0OOOOOO00OO .append(item[0])
    O0O00O0000OO00000 .cursor.execute('select "TagName" from public."Output_Tags" where "Description" = \'To display instead of KPI\';')
    OOOO00O0O00000O0O  = O0O00O0000OO00000 .cursor.fetchall()
    O0O00O0000OO00000 .conn.commit()
    O00OOO0OO00OO0O00  = []
    for item in OOOO00O0O00000O0O :
        O00OOO0OO00OO0O00 .append(item[0])
    OO00OOO0000OOO0O0  = 1
    while O000OO0OOOOOOO0O0 :
        OO000OO0OO0O00000 , OO000O0O0OO0OO0O0 , OO0O00OOOO0OO0000 , O0OO00000OOOOO00O  = O0O00O0000OO00000 .cloudDataLogging()
        print('no. of total tags in simfile: ', len(OO000OO0OO0O00000 .keys()))
        if OO0O00OOOO0OO0000  == 'Playback' or OO0O00OOOO0OO0000  == 'Normal':
            for O00O0O00O000OOO00  in range(OO000O0O0OO0OO0O0 ):
                O0OO000OO0OOOO0OO  = {}
                OO0O00O0O0O0O0OOO  = {}
                for OO0OO00OO0OOOOOO0  in O0OO0O0OOOOOO00OO :
                    if OO0OO00OO0OOOOOO0  == 'Nav_GPS1_UTC':
                        O0OO000OO0OOOO0OO [OO0OO00OO0OOOOOO0 ] = OO000OO0OO0O00000 [OO0OO00OO0OOOOOO0 ][O00O0O00O000OOO00 ]
                    elif OO0OO00OO0OOOOOO0  in OO000OO0OO0O00000 .keys():
                        OO0O00O0O0O0O0OOO [OO0OO00OO0OOOOOO0 ] = 1
                        OOOOOOOO00000O000  = OO000OO0OO0O00000 [OO0OO00OO0OOOOOO0 ][O00O0O00O000OOO00 ]
                        if len(OOOOOOOO00000O000 ) == 0:
                            OOOOOOOO00000O000  = 99
                        O0OO000OO0OOOO0OO [OO0OO00OO0OOOOOO0 ] = float(OOOOOOOO00000O000 )
                    else:
                        OO0O00O0O0O0O0OOO [OO0OO00OO0OOOOOO0 ] = 0
                        O0OO000OO0OOOO0OO [OO0OO00OO0OOOOOO0 ] = 99
                OOO00O00OO0O00O0O  = O0O00O0000OO00000 .inputsLogging(O00O0O00O000OOO00 , O0OO0O0OOOOOO00OO , O0OO000OO0OOOO0OO , OO0O00O0O0O0O0OOO )
                if OO00OOO0000OOO0O0  == 1 or OO00OOO0000OOO0O0  == 0:
                    OO0OO000OOOO00O00  = {}
                    O0O0O00O00O000000  = ['NS_GPS_019_PV', 'NS_PP004-03MI_PV', 'NS_PP043-03MI_PV', 'NS_PP009-03MI_PV', 'NS_PP044-03MI_PV', 'NS_PP036-03XI_PV', 'NS_PP037-03AXI_PV', 'NS_PP038-03AXI_PV', 'NS_PP038-03XC_PV', 'NS_PP040-03MI_PV', 'NS_PP045-03MI_PV', 'NS_PP046-03MI_PV', 'NS_PP061-03MI_PV', 'NS_PP030-03MI_PV', 'NS_PP058-03MI_PV', 'NS_PP033-03MI_PV', 'NS_PP059-03MI_PV', 'NS_MM048-XI_PV', 'NS_MM648-XI_PV', 'NS_MM018-XI_PV', 'NS_MM618-XI_PV', 'NS_MM023-XI_PV', 'NS_MM021-XI_PV', 'NS_MM623-XI_PV', 'NS_MM621-XI_PV', 'NS_NG1-40101_PV', 'NS_NG1-40102_PV', 'NS_NG1-40103_PV', 'NS_NG2-40101_PV', 'NS_NG2-40102_PV', 'NS_NG2-40103_PV', 'NS_MM944-XI_PV', 'NS_MF001-03MI_PV', 'NS_MF010-03MI_PV', 'NS_IG-00531_PV', 'NS_CF013-03MC_PV', 'NS_CF014-03MC_PV', 'NS_MM002-XI_PV', 'NS_MM602-XI_PV', 'NS_MM908-03XI_PV', 'NS_MM066-XI_PV', 'NS_MM666-XI_PV', 'NS_MM933-XI_PV']
                    for item in O0O0O00O00O000000 :
                        if item in O0OO000OO0OOOO0OO .keys():
                            O00OOO00OOO0OO000  = True
                        else:
                            O00OOO00OOO0OO000  = False
                        if O00OOO00OOO0OO000  == True and O0OO000OO0OOOO0OO [item] == 99:
                            OO0OO000OOOO00O00 [item] = 0
                        elif O00OOO00OOO0OO000  == True:
                            OO0OO000OOOO00O00 [item] = 1
                        else:
                            OO0OO000OOOO00O00 [item] = 0
                O00O0O0O000OO0O0O  = O0O00O0000OO00000 .runningStatus(O0OO000OO0OOOO0OO , OO0OO000OOOO00O00 )
                O0O00O0000OO00000 .runningStatusLogging(O00O0O0O000OO0O0O , OOO00O00OO0O00O0O )
                print('running status logged')
                print('---------')
                O0OO00OO0O0OO0000 , OOO00OO00O0OO000O  = O0O00O0000OO00000 .dwsimSimulation(O0OO000OO0OOOO0OO , O00O0O0O000OO0O0O , OOO00O00OO0O00O0O , OO0OO000OOOO00O00 )
                print('dwsim outputs are calculated')
                print('---------')
                O0O00O0000OO00000 .outputsLogging(O0OO00OO0O0OO0000 , O00O0O0O000OO0O0O , OOO00O00OO0O00O0O , OO0OO000OOOO00O00 )
                if 'NS_IG004-XA_PV' in O0OO000OO0OOOO0OO .keys():
                    O0O00O0000OO00000 .alarmLoggingforNoKPIassets(O00OOO0OO00OO0O00 , O0OO000OO0OOOO0OO )
                O0OO000OO0OOOO0OO  = O0OO000OO0OOOO0OO  | OOO00OO00O0OO000O 
                O0O0OO00O0OOOOO0O  = O0O00O0000OO00000 .updateSignal()
                if O0O0OO00O0OOOOO0O  == '1':
                    OO0OO000O0O0O0000  = O0O00O0000OO00000 .importRCAtemplates()
                    OO0O0OOO0OOO0OOOO  = O0O00O0000OO00000 .rcaID(OO0OO000O0O0O0000 )
                    print('rca templates and rca id were re-read after templates were updated by user')
                if OO00OOO0000OOO0O0  == 1:
                    OO0O0OOOO00O0OO0O , OOOOO0O00OO0000OO  = O0O00O0000OO00000 .findRules(OO0OO000O0O0O0000 )
                if OO00OOO0000OOO0O0  == 1 or '2023-07-09 00:0' in OOO00O00OO0O00O0O :
                    print('finding target scenarios at start of program in case of simfiles updated after 0709')
                    O00000O00O00O00OO  = O0O00O0000OO00000 .findtargetScenarios(OOOOO0O00OO0000OO , OO0O00O0O0O0O0OOO )
                OOO0OO0O00O00OOO0 , O0OO0OOOO0000OOOO  = O0O00O0000OO00000 .rcaTemplatesReader(OO0OO000O0O0O0000 , O0OO000OO0OOOO0OO , O00O0O0O000OO0O0O , O00000O00O00O00OO )
                print('status and parent node are read')
                print('---------')
                OO0O0O0OOOOOOO00O  = O0O00O0000OO00000 .logStatusandParentNode(OOO0OO0O00O00OOO0 , O0OO0OOOO0000OOOO )
                print('rca update history is logged')
                if OO00OOO0000OOO0O0  == 1:
                    OO00O0O0O0O000OO0 , O0O0OO00OO00O0O00  = O0O00O0000OO00000 .RCAlevels(O0O0O0O0OOOO00O0O )
                    print('rca levels done')
                    O0O00O0000OO00000 .totalAvailableScenarios()
                    O0O00O0000O00000O  = OOO00O00OO0O00O0O 
                    OO00OOO0000OOO0O0  = 0
                if O0O0OO00O0OOOOO0O  == '1':
                    OO00O0O0O0O000OO0 , O0O0OO00OO00O0O00  = O0O00O0000OO00000 .RCAlevels(O0O0O0O0OOOO00O0O )
                    print('rca levels done')
                    O0O00O0000OO00000 .totalAvailableScenarios()
                    O0O00O0000OO00000 .cursor.execute('update public."Templates_update" set "Status" = \'0\' where "Activity" = \'RCA_templates_updated\';')
                    O0O00O0000OO00000 .conn.commit()
                    print('rca levels and no. of scenarios updated after templates were updated by user')
                    OO0O0OOOO00O0OO0O  = O0O00O0000OO00000 .findRules(OO0OO000O0O0O0000 )
                OOO0OO0O00O00OOO0  = O0O00O0000OO00000 .applyInferredStatus(OOO0OO0O00O00OOO0 )
                print('inferred status applied')
                O0000O00O000OO0OO  = O0O00O0000OO00000 .updateRCAstatus(O0000O00O000OO0OO , O00O0O0O000OO0O0O , OOO0OO0O00O00OOO0 , OOO00O00OO0O00O0O , OO0O0OOO0OOO0OOOO , OO0O0OOOO00O0OO0O , O0O0OO00OO00O0O00 )
                print('rca status is done')
                O0O00O0000O00000O , OOO0O00000O000O00 , O0O0O0O0OOOO00O0O , O0OOOOO0O0O00O00O  = O0O00O0000OO00000 .saveHOS(O0O00O0000O00000O , OOO0O00000O000O00 , O0O0O0O0OOOO00O0O , OOO00O00OO0O00O0O , O00O0O0O000OO0O0O , OO00O0O0O0O000OO0 , O0OOOOO0O0O00O00O )
                print('HOS are saved')
                O0O00O0000OO00000 .maintenanceAlarm(O0OOOO0O000OOO0O0 , O0O0O0O0OOOO00O0O )
                print('maintenance alarms checked')
                O0O00O0000OO00000 .saveAlertCount()
                print('Alert count updated')
                print('All done! Time_onboard: ', OOO00O00OO0O00O0O , '--- Time_now:', datetime.now())
                print('================================================')
                time.sleep(O0OO00000OOOOO00O )
                if O00O0O00O000OOO00  == OO000O0O0OO0OO0O0  - 1:
                    print('reading new cloud inputs. TimeStamp is :', datetime.now())
                    O000OO0OOOOOOO0O0  = True
        else:
            print('Holding mode')
            time.sleep(O0OO00000OOOOO00O )
            O000OO0OOOOOOO0O0  = True
if __name__ == '__main__':
    main()