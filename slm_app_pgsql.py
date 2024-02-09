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
import psycopg2 #updated for PostgreSQL
# import math
class slmApplication():
    def __init__(self,user_id,pwd,excel_pwd,db_address,pg_database,pg_port,dwsim_path):
        try:
            self.excel_pwd=excel_pwd
            if dwsim_path =='':
                dwsim_path='/usr/local/lib/dwsim/'   
                
            # self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMERSON\SQLEXPRESS01;DATABASE=SLM-Project;UID=user1;PWD=1234'
            self.conn_string = f'dbname ={pg_database} user={user_id} password={pwd} host={db_address} port={pg_port}' #updated for PostgreSQL #postgres is test db, test1 is main db
            # self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LPPLVAI\SQLEXPRESS2019;DATABASE=S-Project;UID=sa;PWD=Welcome1'
            # self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMERSON\SQLEXPRESS01;DATABASE=S-Project;UID=user1;PWD=1234'
            # self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O74IH9F\SPARTA;DATABASE=S-Project;UID=sa;PWD=1234'
            self.conn = psycopg2.connect(self.conn_string) #updated for PostgreSQL
            self.cursor = self.conn.cursor()

            quoted = urllib.parse.quote_plus(self.conn_string)
            # self.engine = create_engine('postgresql://postgres:1234@127.0.0.1:5432/postgres') #updated for PostgreSQL #updated on 12042023

            print("SQL connected!")
            # return conn_string

        except:
            print("SQL not connected!")
        dwsimpath = dwsim_path #on server
        #dwsimpath = "C:\\Users\\iu\\AppData\\Local\\DWSIM8\\" #on server
        # dwsimpath = "C:\\Users\\okfar\\AppData\\Local\\DWSIM\\" #my notebook
        
        self.test_run = 0 #updated on 12062023 #confirm it before delivery
        production = True # True for production (site deployment). change it to False for development(office) run #confirm it before delivery
        if production:
            self.log_inputs_realtime = 0
            self.log_inputs_history = 0
            self.hide_rules = 1
        else:
            self.log_inputs_realtime = 1
            self.log_inputs_history = 1
            self.hide_rules = 0

        self.compare_pre_and_curr_status = 1  #updated on 11292023
        self.log_less_priority_items = 0 #updated on 11292023


        clr.AddReference(dwsimpath + "CapeOpen.dll")
        clr.AddReference(dwsimpath + "DWSIM.Automation.dll")
        clr.AddReference(dwsimpath + "DWSIM.Interfaces.dll")
        clr.AddReference(dwsimpath + "DWSIM.GlobalSettings.dll")
        clr.AddReference(dwsimpath + "DWSIM.SharedClasses.dll")
        clr.AddReference(dwsimpath + "DWSIM.Thermodynamics.dll")
        clr.AddReference(dwsimpath + "DWSIM.UnitOperations.dll")
        clr.AddReference(dwsimpath + "DWSIM.Inspector.dll")
        clr.AddReference(dwsimpath + "System.Buffers.dll")

        from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
        from DWSIM.Thermodynamics import Streams, PropertyPackages
        from DWSIM.UnitOperations import UnitOperations
        from DWSIM.Automation import Automation3
        from DWSIM.GlobalSettings import Settings

        #Directory.SetCurrentDirectory(dwsimpath)

        self.interf = Automation3()
        # print([item for item in dir(interf)])

        assets_folder = 'assets/' #in the same directory as py file
        
        dwsim_flowsheets_folder = 'assets/py_conn/'
        current_file = os.path.abspath(os.path.dirname(__file__))
        self.RCA_mastersheet_path = os.path.join(current_file, assets_folder+'SHI Rules Master sheet_12142023_rev3.7') #updated on 12122023
        
        # simfiles_folder = 'assets/simfiles/'  #in case of simfiles within asset folder
        # self.simfiles_path = os.path.join(current_file, simfiles_folder)

        #but if some other folder, use following format:
        simfiles_folder=assets_folder+'simfiles'
        self.simfiles_path=os.path.join(current_file,simfiles_folder)          
        #self.simfiles_path = r"C:\Users\iu\Downloads\9929106\9929106"
        # self.simfiles_path = r"C:\Users\okfar\Downloads\simfiles" #my notebook for feb2013 to april2023
        # self.simfiles_path = r"D:\Panocean_simfiles_07082023-08142023\Panocean_simfiles_07082023-08142023" #my notebook
        # self.simfiles_path = r"C:\Users\apstp\OneDrive\문서\SLM clone\assets\simfiles" # test notebook

        dwsim_files_path = os.path.join(current_file, dwsim_flowsheets_folder)
        self.ent = '@@@LD2_S2_out_actual_specific_enthalpy@@@'
       
        # dwsim_files_path = "C:\\Users\\iu\\Documents\\SLM clone\\py_conn\\"
        

        self.sim1 = self.interf.LoadFlowsheet(dwsim_files_path + "sclr_py_conn.dwxmz")
        print("sim1-SC interface ready")
        self.sim2 = self.interf.LoadFlowsheet(dwsim_files_path + "fv_py_conn.dwxmz")
        print("sim2-FV interface ready")
        self.sim3 = self.interf.LoadFlowsheet(dwsim_files_path + "lngv_py_conn.dwxmz")
        print("sim3-LNGV interface ready")
        self.sim4 = self.interf.LoadFlowsheet(dwsim_files_path + "bogh_py_conn.dwxmz")
        print("sim4-BOGH interface ready")
        self.sim5 = self.interf.LoadFlowsheet(dwsim_files_path + "wuh_py_conn.dwxmz")
        print("sim5-WUH interface ready")
        self.sim6 = self.interf.LoadFlowsheet(dwsim_files_path + "gwhs_py_conn.dwxmz")
        print("sim6-GWHStm interface ready")
        self.sim7 = self.interf.LoadFlowsheet(dwsim_files_path + "LD1_py_conn.dwxmz")
        print("sim7-LD1 interface ready")
        self.sim8 = self.interf.LoadFlowsheet(dwsim_files_path + "LD2_py_conn.dwxmz")
        print("sim8-LD2 interface ready")
        self.sim9 = self.interf.LoadFlowsheet(dwsim_files_path + "HD1_py_conn.dwxmz")
        print("sim9-HD1 interface ready")
        self.sim10 = self.interf.LoadFlowsheet(dwsim_files_path + "HD2_py_conn.dwxmz")
        print("sim10-HD2 interface ready")
        self.ME1_sim = self.interf.LoadFlowsheet(dwsim_files_path + "ME1_py_conn.dwxmz")
        self.ME2_sim = self.interf.LoadFlowsheet(dwsim_files_path + "ME2_py_conn.dwxmz")
        self.GE1_sim = self.interf.LoadFlowsheet(dwsim_files_path + "GE1_py_conn.dwxmz")
        self.GE2_sim = self.interf.LoadFlowsheet(dwsim_files_path + "GE2_py_conn.dwxmz")
        self.GE3_sim = self.interf.LoadFlowsheet(dwsim_files_path + "GE3_py_conn.dwxmz")
        self.GE4_sim = self.interf.LoadFlowsheet(dwsim_files_path + "GE4_py_conn.dwxmz")
        print("ME1/2 and GE1/2/3/4 interface ready")
        self.NG1_sim = self.interf.LoadFlowsheet(dwsim_files_path + "NG1_py_conn.dwxmz")
        self.NG2_sim = self.interf.LoadFlowsheet(dwsim_files_path + "NG2_py_conn.dwxmz")
        print("NG1/2 interface ready")
        self.AB1_sim = self.interf.LoadFlowsheet(dwsim_files_path + "AB1_py_conn.dwxmz") # updated for AB simulation
        self.AB2_sim = self.interf.LoadFlowsheet(dwsim_files_path + "AB2_py_conn.dwxmz") # updated for AB simulation
        print("AB1/2 interface ready") # updated for AB simulation

        self.agg = {} #for collecting samples for aggregation in template reader
        self.persistence = {} #for collecting samples for persistence in template reader
        self.mavg_samples = {} #for trend counter, collection of mavg samples (smoothed values)

        # self.for_test = 'LD2_Overtemp_of_bearings'
        self.for_test = 'none_for_test'
        # self.for_test = 'LD1_Overspeed'
        # self.for_test = 'LD1_Little_or_no_oil'
        # self.for_test = 'LD1_Intermediate_1'
        # self.for_test = 'none'

        # self.agg_test = 'CM_LD1_OilFilterAlrmCtrlTemp'
        self.agg_test = 'none'

    def validateInputs(self, tags, to_validate, onboard_timestamp):
        
        out_of_range_keys = {} #out of range key and its temporary value
        for key in to_validate.keys():
            current_val = tags[key]
            normal_range = to_validate[key][0]
            temporary_val = to_validate[key][1]
            low = normal_range[0]
            high = normal_range[1]
            message = 'normal range of '+ key + ': ['+str(low)+","+str(high)+"]. Current value of "+key+ ": "+str(current_val)+". Temporary value of "+str(temporary_val)+" will be used in dwsim to avoid non-convergence of flowsheet."

            self.cursor.execute('select "Tag" from public."Log_messages"') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()
            keys = [item[0] for item in row]
            
            if current_val < low or current_val > high:
                print(key, 'is out of range, so using temporary value which is: ',temporary_val)
                out_of_range_keys[key] = temporary_val
                if key not in keys:
                    self.cursor.execute('insert into public."Log_messages" values(%s, %s, %s, %s)', [onboard_timestamp, key, 'dwsimSimulation', message]) #updated for PostgreSQL
                    self.conn.commit()
            else:
                # print(key, 'is in normal range')
                pass
        
        return out_of_range_keys #sample--> {'out_of_range_key': temporary_value}

    def dwsimSimulation(self, tags, running_status, onboard_timestamp, tags_av_check):
        SC_outputs = {}
        FV_outputs = {}
        LNGV_outputs = {}
        BOGH_outputs = {}
        WUH_outputs = {}
        GWH_Stm_outputs = {}
        LD1_outputs = {}
        LD2_outputs = {}
        HD1_outputs = {}
        HD2_outputs = {}
        ME1_outputs = {}
        ME1_SAC_outputs = {}
        ME2_outputs = {}
        ME2_SAC_outputs = {}
        GE1_outputs = {}
        GE1_SAC_outputs = {}
        GE2_outputs = {}
        GE2_SAC_outputs = {}
        GE3_outputs = {}
        GE3_SAC_outputs = {}
        GE4_outputs = {}
        GE4_SAC_outputs = {}
        NG1_outputs = {}
        NG2_outputs = {}
        AB_AB1_outputs = {} # updated for AB simulation
        AB_AB2_outputs = {} # updated for AB simulation

        #inputs_validation
        #add desired inputs to this dict below
        to_validate = {'CM_LNGSubClr_Flow': [[3, 10], 5], 'ME1_EG_ScavAirMeanPrs': [[0.1, 0.5], 0.26], 'ME2_EG_ScavAirMeanPrs': [[0.1, 0.5], 0.26]} 
        #sample--> {'key': [[normal_range], temporary_value]
        out_of_range_keys = self.validateInputs(tags, to_validate, onboard_timestamp)
        #now make logic below, during setting to dwsim, to check if the tag in 'to_validate' is present in 'out_of_range_keys' as well? 
        #if present it means it is out of range. and we should use its temporary value which is given in 'out_of_range_keys', not the value from tags

        if running_status['SC'] == 1:
            # print("**************")
            print("starting dwsim SC")
            # print("**************")

            #HX2
            LNG_in = self.sim1.GetFlowsheetSimulationObject('LNG_in').GetAsObject()
            LNG_out = self.sim1.GetFlowsheetSimulationObject('LNG_out').GetAsObject()
            HX2_LNG_cooling = self.sim1.GetFlowsheetSimulationObject('HX2_LNG_cooling').GetAsObject()

            #MTC_comp
            MTC_comp_in = self.sim1.GetFlowsheetSimulationObject('MTC_comp_in').GetAsObject()
            MTC_comp = self.sim1.GetFlowsheetSimulationObject('MTC_comp').GetAsObject()
            MTC_comp_out_ideal = self.sim1.GetFlowsheetSimulationObject('MTC_comp_out_ideal').GetAsObject()
            MTC_comp_out_actual = self.sim1.GetFlowsheetSimulationObject('MTC_comp_out_actual').GetAsObject()
            HX300 = self.sim1.GetFlowsheetSimulationObject('HX300').GetAsObject()

            #MTC_exp
            MTC_exp = self.sim1.GetFlowsheetSimulationObject('MTC_exp').GetAsObject()
            MTC_exp_in = self.sim1.GetFlowsheetSimulationObject('MTC_exp_in').GetAsObject()
            MTC_exp_out_ideal = self.sim1.GetFlowsheetSimulationObject('MTC_exp_out_ideal').GetAsObject()
            MTC_exp_out_actual = self.sim1.GetFlowsheetSimulationObject('MTC_exp_out_actual').GetAsObject()

            #MC_comp
            MC_comp_in = self.sim1.GetFlowsheetSimulationObject('MC_comp_in').GetAsObject()
            MC_comp = self.sim1.GetFlowsheetSimulationObject('MC_comp').GetAsObject()
            MC_comp_out_ideal = self.sim1.GetFlowsheetSimulationObject('MC_comp_out_ideal').GetAsObject()
            MC_comp_out_actual = self.sim1.GetFlowsheetSimulationObject('MC_comp_out_actual').GetAsObject()
            HX200 = self.sim1.GetFlowsheetSimulationObject('HX200').GetAsObject()
            HX200_out = self.sim1.GetFlowsheetSimulationObject('HX200_out').GetAsObject()

            #Regenerator (HX1-2)
            HX1_ref_cooling = self.sim1.GetFlowsheetSimulationObject('HX1_ref_cooling').GetAsObject()
            HX12_ref_heating = self.sim1.GetFlowsheetSimulationObject('HX1-2_ref_heating').GetAsObject()
            HX12_out = self.sim1.GetFlowsheetSimulationObject('HX1-2_out').GetAsObject()
            HX12_ideal = self.sim1.GetFlowsheetSimulationObject('HX1-2_ideal').GetAsObject()


            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")
            ten_r_5 = 100000.0

            # #HX2

            HX2_dP = tags['CM_LNGSubClr_DropPrs']/1000.0  #it comes in mbar. converted to bar
            LNG_out_pres = (tags['CM_LNGSubClr_OutPrs']) #it comes in bar
            LNG_in_pres = LNG_out_pres + HX2_dP # in bar
            LNG_in.SetPressure(LNG_in_pres * ten_r_5) #write in Pa
            HX2_LNG_cooling.set_DeltaP(HX2_dP* ten_r_5) #dp was coverted to bar above. write in Pa
            LNG_in.SetTemperature(tags['CM_LNGSubClr_InTemp']+273.15) #write in K TBF-TI-800
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            if 'CM_LNGSubClr_Flow' in out_of_range_keys: #if it is out of range
                CM_LNGSubClr_Flow = out_of_range_keys['CM_LNGSubClr_Flow'] #temporary value
            else:
                CM_LNGSubClr_Flow = tags['CM_LNGSubClr_Flow'] #original value
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # LNG_in.SetMassFlow(tags['CM_LNGSubClr_Flow']/3600.0) #write in kg/s TBF-FI-800
            LNG_in.SetMassFlow(CM_LNGSubClr_Flow/3600.0) #write in kg/s TBF-FI-800
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            HX2_LNG_cooling.set_OutletTemperature(tags['CM_LNGSubClr_OutTemp']+273.15) # write out temp TBF-TI-801

            # #MTC_comp
            MTC_comp_in.SetPressure(tags['CM_LNGSubClr_MTC_CompInPrs'] * ten_r_5) #write in Pa TBF-PI-100
            MTC_comp_in.SetTemperature(tags['CM_LNGSubClr_MTC_CompInTemp']+273.15) #write in K TBF-TI-100

            MTC_comp.set_POut(tags['CM_LNGSubClr_MTC_CompOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-300
            MTC_comp_out_actual.SetPressure(tags['CM_LNGSubClr_MTC_CompOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-300
            MTC_comp_out_actual.SetTemperature(tags['CM_LNGSubClr_MTC_CompOutTemp']+273.15) # write out temp act TBF-TI-300
            HX300.set_OutletTemperature(tags['CM_LNGSubClr_Hx300_OutTemp']+273.15) # write out temp TBF-TI-310
            HX300_dP = tags['CM_LNGSubClr_MTC_CompOutPrs'] - tags['CM_LNGSubClr_Hx300_OutPrs'] #calculate dP
            HX300.set_DeltaP(HX300_dP * ten_r_5) #write in Pa #pressure drop calculated above #update the coversion factor after review

            # #MC_comp
            MC_comp.set_POut(tags['CM_LNGSubClr_MC_CompOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-200
            MC_comp_out_actual.SetPressure(tags['CM_LNGSubClr_MC_CompOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-200
            MC_comp_out_actual.SetTemperature(tags['CM_LNGSubClr_MC_CompOutTemp']+273.15) # write out temp act TBF-TI-200
            HX200.set_OutletTemperature(tags['CM_LNGSubClr_Hx1_InTemp']+273.15) # write out temp TBF-TI-201

            # #Regenerator (HX1-2)
            HX1_ref_cooling.set_OutletTemperature(tags['CM_LNGSubClr_MTC_TurbineInTemp']+273.15) # write out temp act TBF-TI-203
            HX1_ref_cooling_dP = tags['CM_LNGSubClr_MC_CompOutPrs'] - tags['CM_LNGSubClr_MTC_TurbineInPrs'] #calculate dP
            HX1_ref_cooling.set_DeltaP(HX1_ref_cooling_dP * ten_r_5) #write in Pa #pressure drop calculated above #update the coversion factor after review

            # # MTC_exp
            MTC_exp.set_POut(tags['CM_LNGSubClr_MTC_TurbineOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-120
            MTC_exp_out_actual.SetPressure(tags['CM_LNGSubClr_MTC_TurbineOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-120
            MTC_exp_out_actual.SetTemperature(tags['CM_LNGSubClr_MTC_TurbineOutTemp']+273.15) # write out temp act TBF-TI-102

            # # HX1-2_out
            HX12_ideal.SetPressure(tags['CM_LNGSubClr_MTC_TurbineOutPrs'] * ten_r_5) #write in Pa #write out pres act TBF-PI-120
            HX12_ideal.SetTemperature(tags['CM_LNGSubClr_Hx1_InTemp']+273.15) #write in K TBF-TI-201

            #solve
            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim1)


            SC_inputs = {}

            #HX2
            LNG_in_temp = LNG_in.GetTemperature() - 273.15 #degC
            LNG_out_pres = LNG_out.GetPressure() / ten_r_5 #dwsim gives in Pa. but tags are in bar. so converted to bar
            LNG_out_flow = LNG_out.GetMassFlow() * 3600 #kg/h
            #MTC_comp
            MTC_comp_in_pres = MTC_comp_in.GetPressure() / ten_r_5
            MTC_comp_in_temp = MTC_comp_in.GetTemperature() - 273.15
            MTC_comp_out_pres = MTC_comp_out_actual.GetPressure() / ten_r_5
            MTC_comp_out_temp = MTC_comp_out_actual.GetTemperature() - 273.15
            #MC_comp
            MC_comp_in_pres = MC_comp_in.GetPressure() / ten_r_5
            MC_comp_in_temp = MC_comp_in.GetTemperature() - 273.15
            MC_comp_out_pres = MC_comp_out_actual.GetPressure() / ten_r_5
            MC_comp_out_temp = MC_comp_out_actual.GetTemperature() - 273.15
            HX200_out_temp = HX200_out.GetTemperature() - 273.15
            # MTC_exp
            MTC_exp_in_pres = MTC_exp_in.GetPressure() / ten_r_5
            MTC_exp_in_temp = MTC_exp_in.GetTemperature() - 273.15
            MTC_exp_out_pres = MTC_exp_out_actual.GetPressure() / ten_r_5
            MTC_exp_out_temp = MTC_exp_out_actual.GetTemperature() - 273.15
            #Regenerator (HX1-2)
            HX12_out_temp = HX12_out.GetTemperature() - 273.15

            SC_inputs['LNG_in_temp'] = LNG_in_temp
            SC_inputs['LNG_out_pres'] = LNG_out_pres
            SC_inputs['LNG_out_flow'] = LNG_out_flow
            SC_inputs['MTC_comp_in_pres'] = MTC_comp_in_pres
            SC_inputs['MTC_comp_in_temp'] = MTC_comp_in_temp
            SC_inputs['MTC_comp_out_pres'] = MTC_comp_out_pres
            SC_inputs['MTC_comp_out_temp'] = MTC_comp_out_temp
            SC_inputs['MC_comp_in_pres'] = MC_comp_in_pres
            SC_inputs['MC_comp_in_temp'] = MC_comp_in_temp
            SC_inputs['MC_comp_out_pres'] = MC_comp_out_pres
            SC_inputs['MC_comp_out_temp'] = MC_comp_out_temp
            SC_inputs['HX200_out_temp'] = HX200_out_temp
            SC_inputs['MTC_exp_in_pres'] = MTC_exp_in_pres
            SC_inputs['MTC_exp_in_temp'] = MTC_exp_in_temp
            SC_inputs['MTC_exp_out_pres'] = MTC_exp_out_pres
            SC_inputs['MTC_exp_out_temp'] = MTC_exp_out_temp
            SC_inputs['HX12_out_temp'] = HX12_out_temp
            # print(SC_inputs)

            #MTC_comp
            MTC_comp_in_specific_enthalpy = MTC_comp_in.GetMassEnthalpy()
            MTC_comp_pressure_ratio = MTC_comp_out_pres/MTC_comp_in_pres
            MTC_comp_polytropic_power = abs(MTC_comp.GetPowerGeneratedOrConsumed())
            MTC_comp_polytropic_head = MTC_comp.get_PolytropicHead() # m
            MTC_comp_out_adiabatic_temp = MTC_comp_out_ideal.GetTemperature() - 273.15
            MTC_comp_in_specific_enthalpy = MTC_comp_in.GetMassEnthalpy()
            MTC_comp_out_ideal_specific_enthalpy = MTC_comp_out_ideal.GetMassEnthalpy()
            MTC_comp_out_actual_specific_enthalpy = MTC_comp_out_actual.GetMassEnthalpy()
            MTC_comp_ideal_ethalpy_change = MTC_comp_out_ideal_specific_enthalpy - MTC_comp_in_specific_enthalpy
            MTC_comp_actual_ethalpy_change = MTC_comp_out_actual_specific_enthalpy - MTC_comp_in_specific_enthalpy
            MTC_comp_polytropic_efficiency = (MTC_comp_ideal_ethalpy_change / MTC_comp_actual_ethalpy_change) * 100
            HX300_deltaT = HX300.get_DeltaT() # comes in degC
            HX300_duty = HX300.GetPowerGeneratedOrConsumed()

            SC_outputs['SC_MTC_comp_in_specific_enthalpy'] = MTC_comp_in_specific_enthalpy
            SC_outputs['SC_MTC_comp_pressure_ratio'] = MTC_comp_pressure_ratio
            SC_outputs['SC_MTC_comp_polytropic_power'] = MTC_comp_polytropic_power
            SC_outputs['SC_MTC_comp_polytropic_head'] = MTC_comp_polytropic_head
            SC_outputs['SC_MTC_comp_in_specific_enthalpy'] = MTC_comp_in_specific_enthalpy
            SC_outputs['SC_MTC_comp_out_actual_specific_enthalpy'] = MTC_comp_out_actual_specific_enthalpy
            SC_outputs['SC_MTC_comp_polytropic_efficiency'] = MTC_comp_polytropic_efficiency
            SC_outputs['SC_HX300_deltaT'] = HX300_deltaT
            SC_outputs['SC_HX300_duty'] = HX300_duty

            #MC_comp
            MC_comp_in_specific_enthalpy = MC_comp_in.GetMassEnthalpy()
            MC_comp_pressure_ratio = MC_comp_out_pres/MC_comp_in_pres
            MC_comp_polytropic_power = abs(MC_comp.GetPowerGeneratedOrConsumed())
            MC_comp_polytropic_head = MC_comp.get_PolytropicHead() # m
            MC_comp_out_adiabatic_temp = MC_comp_out_ideal.GetTemperature() - 273.15
            MC_comp_in_specific_enthalpy = MC_comp_in.GetMassEnthalpy()
            MC_comp_out_ideal_specific_enthalpy = MC_comp_out_ideal.GetMassEnthalpy()
            MC_comp_out_actual_specific_enthalpy = MC_comp_out_actual.GetMassEnthalpy()
            MC_comp_ideal_ethalpy_change = MC_comp_out_ideal_specific_enthalpy - MC_comp_in_specific_enthalpy
            MC_comp_actual_ethalpy_change = MC_comp_out_actual_specific_enthalpy - MC_comp_in_specific_enthalpy
            MC_comp_polytropic_efficiency = (MC_comp_ideal_ethalpy_change / MC_comp_actual_ethalpy_change) * 100
            HX200_deltaT = HX200.get_DeltaT() # comes in degC
            HX200_duty = HX200.GetPowerGeneratedOrConsumed()

            SC_outputs['SC_MC_comp_in_specific_enthalpy'] = MC_comp_in_specific_enthalpy
            SC_outputs['SC_MC_comp_pressure_ratio'] = MC_comp_pressure_ratio
            SC_outputs['SC_MC_comp_polytropic_power'] = MC_comp_polytropic_power
            SC_outputs['SC_MC_comp_polytropic_head'] = MC_comp_polytropic_head
            SC_outputs['SC_MC_comp_in_specific_enthalpy'] = MC_comp_in_specific_enthalpy
            SC_outputs['SC_MC_comp_out_actual_specific_enthalpy'] = MC_comp_out_actual_specific_enthalpy
            SC_outputs['SC_MC_comp_polytropic_efficiency'] = MC_comp_polytropic_efficiency
            SC_outputs['SC_HX200_deltaT'] = HX200_deltaT
            SC_outputs['SC_HX200_duty'] = HX200_duty

            #MTC_exp
            MTC_exp_in_specific_enthalpy = MTC_exp_in.GetMassEnthalpy()
            MTC_exp_pressure_ratio = MTC_exp_in_pres/MTC_exp_out_pres
            MTC_exp_polytropic_power = abs(MTC_exp.GetPowerGeneratedOrConsumed())
            MTC_exp_polytropic_head = MTC_exp.get_PolytropicHead() # m
            MTC_exp_out_adiabatic_temp = MTC_exp_out_ideal.GetTemperature() - 273.15
            MTC_exp_in_specific_enthalpy = MTC_exp_in.GetMassEnthalpy()
            MTC_exp_out_ideal_specific_enthalpy = MTC_exp_out_ideal.GetMassEnthalpy()
            MTC_exp_out_actual_specific_enthalpy = MTC_exp_out_actual.GetMassEnthalpy()
            MTC_exp_ideal_ethalpy_change = MTC_exp_out_ideal_specific_enthalpy - MTC_exp_in_specific_enthalpy
            MTC_exp_actual_ethalpy_change = MTC_exp_out_actual_specific_enthalpy - MTC_exp_in_specific_enthalpy
            MTC_exp_polytropic_efficiency = (MTC_exp_actual_ethalpy_change / MTC_exp_ideal_ethalpy_change) * 100

            SC_outputs['SC_MTC_exp_in_specific_enthalpy'] = MTC_exp_in_specific_enthalpy
            SC_outputs['SC_MTC_exp_pressure_ratio'] = MTC_exp_pressure_ratio
            SC_outputs['SC_MTC_exp_polytropic_power'] = MTC_exp_polytropic_power
            SC_outputs['SC_MTC_exp_polytropic_head'] = MTC_exp_polytropic_head
            SC_outputs['SC_MTC_exp_in_specific_enthalpy'] = MTC_exp_in_specific_enthalpy
            SC_outputs['SC_MTC_exp_out_actual_specific_enthalpy'] = MTC_exp_out_actual_specific_enthalpy
            SC_outputs['SC_MTC_exp_polytropic_efficiency'] = MTC_exp_polytropic_efficiency

            #Regenerator (HX1-2)
            HX2_deltaT = HX2_LNG_cooling.get_DeltaT() # comes in degC
            HX2_duty = HX2_LNG_cooling.GetPowerGeneratedOrConsumed()
            HX1_deltaT = HX1_ref_cooling.get_DeltaT()
            HX1_duty = HX1_ref_cooling.GetPowerGeneratedOrConsumed()
            HX12_regenerator_deltaT = HX12_ref_heating.get_DeltaT()
            HX12_regenerator_duty = HX12_ref_heating.GetPowerGeneratedOrConsumed()

            SC_outputs['SC_HX2_deltaT'] = HX2_deltaT
            SC_outputs['SC_HX2_LNG_cold_power'] = HX2_duty
            SC_outputs['SC_HX1_deltaT'] = HX1_deltaT
            SC_outputs['SC_HX1_duty'] = HX1_duty
            SC_outputs['SC_HX12_regenerator_deltaT'] = HX12_regenerator_deltaT
            SC_outputs['SC_HX12_regenerator_duty'] = HX12_regenerator_duty

            #others
            SC_min_temp = MTC_exp_out_temp
            SC_max_temp = MC_comp_out_temp

            MTC_actual_power_opr = tags['CM_LNGSubClr_MTC1_Pwr'] + tags['CM_LNGSubClr_MTC2_Pwr'] + tags['CM_LNGSubClr_MTC3_Pwr']
            MC_actual_power_opr = tags['CM_LNGSubClr_MC1_Pwr'] + tags['CM_LNGSubClr_MC2_Pwr'] + tags['CM_LNGSubClr_MC3_Pwr'] + tags['CM_LNGSubClr_MC4_Pwr']

            COP = HX2_duty / (MTC_actual_power_opr + MC_actual_power_opr)
            # print("************ COP => ", COP)

            SC_outputs['SC_SC_min_temp'] = SC_min_temp
            SC_outputs['SC_SC_max_temp'] = SC_max_temp
            SC_outputs['SC_MTC_actual_power'] = MTC_actual_power_opr
            SC_outputs['SC_MC_actual_power'] = MC_actual_power_opr

            SC_outputs['SC_COP'] = COP
            for key in SC_outputs.keys():
                SC_outputs[key] = float("{0:.2f}".format(SC_outputs[key]))

            # print(SC_outputs)

        if running_status['FV'] == 1:
            # print("**************")
            print("starting dwsim FV")
            # print("**************")

            FV_cold_in = self.sim2.GetFlowsheetSimulationObject('FV_cold_in').GetAsObject()
            FV_cold_out = self.sim2.GetFlowsheetSimulationObject('FV_cold_out').GetAsObject()
            FV_HT_1 = self.sim2.GetFlowsheetSimulationObject('FV_HT_1').GetAsObject()
            FV_stm_in = self.sim2.GetFlowsheetSimulationObject('FV_stm_in').GetAsObject()
            FV_stm_out = self.sim2.GetFlowsheetSimulationObject('FV_stm_out').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            FV_cold_in.SetTemperature(tags['FG_FV_InTempInd']+273.15) #write in K
            FV_cold_in.SetPressure(tags['FG_FV_InPrs'] * 1000.0) #write in Pa
            FV_cold_in.SetMassFlow(tags['FG_FV_DischFlow']/3600.0) #write in kg/s
            FV_HT_1.set_OutletTemperature(tags['FG_FV_OutTemp2Ind']+273.15)
            FV_HT_1_dP = tags['FG_FV_InPrs'] - tags['FG_FV_OutPrs']
            FV_HT_1.set_DeltaP(FV_HT_1_dP * 1000.0)
            FV_stm_in.SetTemperature(tags['FG_FV_CondWtrTempInd'] + 273.15) #set steam out/condensate temp here

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim2)

            FV_inputs = {}

            FV_cold_in_temp = FV_cold_in.GetTemperature() - 273.15
            # print(FV_cold_in_temp) #degC
            FV_cold_in_pres = FV_cold_in.GetPressure() / 1000.0
            # print(FV_cold_in_pres) #MPa
            FV_inputs['FV_cold_in_temp'] = FV_cold_in_temp
            FV_inputs['FV_cold_in_pres'] = FV_cold_in_pres

            FV_cold_mass_flow = FV_cold_in.GetMassFlow() * 3600.0
            FV_inputs['FV_mass_flow'] = FV_cold_mass_flow

            FV_cold_out_temp = FV_cold_out.GetTemperature() - 273.15
            # print(FV_cold_out_temp) #degC
            FV_cold_out_pres = FV_cold_out.GetPressure() / 1000.0
            # print(FV_cold_out_pres) #MPa
            FV_inputs['FV_cold_out_temp'] = FV_cold_out_temp
            FV_inputs['FV_cold_out_pres'] = FV_cold_out_pres

            FV_stm_in_temp = FV_stm_in.GetTemperature() - 273.15
            # FV_stm_out_temp = FV_stm_out.GetTemperature() - 273.15

            FV_stm_out_temp = FV_stm_in_temp
            # print(FV_stm_in_temp) #degC
            # print(FV_stm_out_temp) #degC
            FV_inputs['FV_stm_in_temp'] = FV_stm_in_temp
            FV_inputs['FV_stm_out_temp'] = FV_stm_out_temp

            # print(FV_inputs)

            FV_Qc = abs(FV_HT_1.GetPowerGeneratedOrConsumed())
            FV_outputs['FV_Qc'] = FV_Qc
            # FV_Qc

            FV_LMTD = ((FV_stm_in_temp - FV_cold_out_temp) - (FV_stm_out_temp - FV_cold_in_temp)) / np.log((FV_stm_in_temp - FV_cold_out_temp) / (FV_stm_out_temp - FV_cold_in_temp))
            FV_outputs['FV_LMTD'] = FV_LMTD
            # FV_LMTD

            FV_area = 6.1
            FV_U = FV_Qc/(FV_area*FV_LMTD) * 1000
            FV_outputs['FV_U'] = FV_U
            # FV_U

            FV_U_clean = 424.0

            #read previous fouling factor value
            self.cursor.execute('''select "Value" from public."Output_Tags" where "TagName" = 'FV_fouling_factor';''') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()
            ff = row[0][0]

            if tags['FG_FV_DischFlow'] > 2500: #calculate newly if flow is in design range
                FV_fouling_factor = (1/FV_U) - (1/FV_U_clean)
                FV_fouling_factor = (1-FV_fouling_factor) * 100
            elif ff < 100.0: #if its already been calculated and less than 100, then keep it as it is
                FV_fouling_factor = ff
            else: #if flow never been in design range and ff is never calculated earlier, keep it 100
                FV_fouling_factor = 100

            FV_outputs['FV_fouling_factor'] = FV_fouling_factor
            # FV_fouling_factor

            FV_cold_in_specific_enthalpy = FV_cold_in.GetMassEnthalpy()
            FV_outputs['FV_cold_in_specific_enthalpy'] = FV_cold_in_specific_enthalpy
            # print(FV_cold_in_specific_enthalpy)

            FV_cold_out_specific_enthalpy = FV_cold_out.GetMassEnthalpy()
            FV_outputs['FV_cold_out_specific_enthalpy'] = FV_cold_out_specific_enthalpy
            # print(FV_cold_out_specific_enthalpy)

            FV_cold_temp_rise = FV_cold_out_temp - FV_cold_in_temp #C
            FV_outputs['FV_cold_temp_rise'] = FV_cold_temp_rise
            # FV_cold_temp_rise

            FV_minimum_approach = FV_stm_in_temp - FV_cold_out_temp #C
            FV_outputs['FV_minimum_approach'] = FV_minimum_approach
            # FV_minimum_approach

            FV_steam_required = FV_stm_in.GetMassFlow() * 3600 #kg/h
            FV_outputs['FV_steam_required'] = FV_steam_required
            # FV_steam_required_theoretically

            # FV_cold_specific_heat = (FV_Qc / FV_cold_temp_rise) * 3600 #kJ/h.C
            # FV_outputs['FV_cold_specific_heat'] = FV_cold_specific_heat

            FV_cold_in_energy_flow = FV_cold_in.GetEnergyFlow()
            FV_outputs['FV_cold_in_energy_flow'] = FV_cold_in_energy_flow

            FV_cold_out_energy_flow = FV_cold_out.GetEnergyFlow()
            FV_outputs['FV_cold_out_energy_flow'] = FV_cold_out_energy_flow

            for key in FV_outputs.keys():
                FV_outputs[key] = float("{0:.2f}".format(FV_outputs[key]))
            # print(FV_outputs)

        if running_status['LNGV'] == 1:
            # print("**************")
            print("starting dwsim LNGV")
            # print("**************")

            LNGV_cold_in = self.sim3.GetFlowsheetSimulationObject('LNGV_cold_in').GetAsObject()
            LNGV_cold_out = self.sim3.GetFlowsheetSimulationObject('LNGV_cold_out').GetAsObject()
            LNGV_HT_1 = self.sim3.GetFlowsheetSimulationObject('LNGV_HT_1').GetAsObject()
            LNGV_stm_in = self.sim3.GetFlowsheetSimulationObject('LNGV_stm_in').GetAsObject()
            LNGV_stm_out = self.sim3.GetFlowsheetSimulationObject('LNGV_stm_out').GetAsObject()


            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")
            
            LNGV_cold_in.SetTemperature(tags['CM_LNGVapr_InTempInd']+273.15) #write in K
            LNGV_cold_in.SetPressure(tags['CM_LNGVapr_InPrs'] * 1000.0) #write in Pa
            LNGV_cold_in.SetMassFlow(tags['FG_Flow_VaprToAtm']/3600.0) #write in kg/s
            LNGV_HT_1.set_OutletTemperature(tags['CM_LNGVapr_OutTempInd']+273.15)
            LNGV_HT_1_dP = tags['CM_LNGVapr_InPrs'] - tags['CM_LNGVapr_OutPrs']
            LNGV_HT_1.set_DeltaP(LNGV_HT_1_dP * 1000.0)
            LNGV_stm_in.SetTemperature(tags['CM_LNGVapr_CondWtrTempInd']+273.15) #set steam out/condensate temp here

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim3)

            LNGV_inputs = {}

            LNGV_cold_in_temp = LNGV_cold_in.GetTemperature() - 273.15
            # print(LNGV_cold_in_temp) #degC
            LNGV_cold_in_pres = LNGV_cold_in.GetPressure() / 1000.0
            # print(LNGV_cold_in_pres) #MPa
            LNGV_inputs['LNGV_cold_in_temp'] = LNGV_cold_in_temp
            LNGV_inputs['LNGV_cold_in_pres'] = LNGV_cold_in_pres

            LNGV_cold_mass_flow = LNGV_cold_in.GetMassFlow() * 3600.0
            LNGV_inputs['LNGV_mass_flow'] = LNGV_cold_mass_flow

            LNGV_cold_out_temp = LNGV_cold_out.GetTemperature() - 273.15
            # print(LNGV_cold_out_temp) #degC
            LNGV_cold_out_pres = LNGV_cold_out.GetPressure() / 1000.0
            # print(LNGV_cold_out_pres) #MPa
            LNGV_inputs['LNGV_cold_out_temp'] = LNGV_cold_out_temp
            LNGV_inputs['LNGV_cold_out_pres'] = LNGV_cold_out_pres

            LNGV_stm_in_temp = LNGV_stm_in.GetTemperature() - 273.15
            # LNGV_stm_out_temp = LNGV_stm_out.GetTemperature() - 273.15

            LNGV_stm_out_temp = LNGV_stm_in_temp
            # print(LNGV_stm_in_temp) #degC
            # print(LNGV_stm_out_temp) #degC
            LNGV_inputs['LNGV_stm_in_temp'] = LNGV_stm_in_temp
            LNGV_inputs['LNGV_stm_out_temp'] = LNGV_stm_out_temp

            # print(LNGV_inputs)

            LNGV_Qc = abs(LNGV_HT_1.GetPowerGeneratedOrConsumed())
            LNGV_outputs['LNGV_Qc'] = LNGV_Qc
            # LNGV_Qc

            LNGV_LMTD = ((LNGV_stm_in_temp - LNGV_cold_out_temp) - (LNGV_stm_out_temp - LNGV_cold_in_temp)) / np.log((LNGV_stm_in_temp - LNGV_cold_out_temp) / (LNGV_stm_out_temp - LNGV_cold_in_temp))
            LNGV_outputs['LNGV_LMTD'] = LNGV_LMTD
            # LNGV_LMTD

            LNGV_area = 71.0
            LNGV_U = LNGV_Qc/(LNGV_area*LNGV_LMTD) * 1000
            LNGV_outputs['LNGV_U'] = LNGV_U
            # LNGV_U

            LNGV_U_clean = 183.8
            
            #read previous fouling factor value
            self.cursor.execute('''select "Value" from public."Output_Tags" where "TagName" = 'LNGV_fouling_factor';''') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()
            ff = row[0][0]

            if tags['FG_Flow_VaprToAtm'] > 20000: #calculate newly if flow is in design range
                LNGV_fouling_factor = (1/LNGV_U) - (1/LNGV_U_clean)
                LNGV_fouling_factor = (1-LNGV_fouling_factor) * 100
            elif ff < 100.0: #if its already been calculated and less than 100, then keep it as it is
                LNGV_fouling_factor = ff
            else: #if flow never been in design range and ff is never calculated earlier, keep it 100
                LNGV_fouling_factor = 100

            LNGV_outputs['LNGV_fouling_factor'] = LNGV_fouling_factor
            # LNGV_fouling_factor

            LNGV_cold_in_specific_enthalpy = LNGV_cold_in.GetMassEnthalpy()
            LNGV_outputs['LNGV_cold_in_specific_enthalpy'] = LNGV_cold_in_specific_enthalpy
            # print(LNGV_cold_in_specific_enthalpy)

            LNGV_cold_out_specific_enthalpy = LNGV_cold_out.GetMassEnthalpy()
            LNGV_outputs['LNGV_cold_out_specific_enthalpy'] = LNGV_cold_out_specific_enthalpy
            # print(LNGV_cold_out_specific_enthalpy)

            LNGV_cold_temp_rise = LNGV_cold_out_temp - LNGV_cold_in_temp #C
            LNGV_outputs['LNGV_cold_temp_rise'] = LNGV_cold_temp_rise
            # LNGV_cold_temp_rise

            LNGV_minimum_approach = LNGV_stm_in_temp - LNGV_cold_out_temp #C
            LNGV_outputs['LNGV_minimum_approach'] = LNGV_minimum_approach
            # LNGV_minimum_approach

            LNGV_steam_required = LNGV_stm_in.GetMassFlow() * 3600 #kg/h
            LNGV_outputs['LNGV_steam_required'] = LNGV_steam_required
            # LNGV_steam_required_theoretically

            # LNGV_cold_specific_heat = (LNGV_Qc / LNGV_cold_temp_rise) * 3600 #kJ/h.C
            # LNGV_outputs['LNGV_cold_specific_heat'] = LNGV_cold_specific_heat

            LNGV_cold_in_energy_flow = LNGV_cold_in.GetEnergyFlow()
            LNGV_outputs['LNGV_cold_in_energy_flow'] = LNGV_cold_in_energy_flow

            LNGV_cold_out_energy_flow = LNGV_cold_out.GetEnergyFlow()
            LNGV_outputs['LNGV_cold_out_energy_flow'] = LNGV_cold_out_energy_flow

            for key in LNGV_outputs.keys():
                LNGV_outputs[key] = float("{0:.2f}".format(LNGV_outputs[key]))
            # print(LNGV_outputs)

        if running_status['BOGH'] == 1:
        
            # print("**************")
            print("starting dwsim BOGH")
            # print("**************")


            BOGH_cold_in = self.sim4.GetFlowsheetSimulationObject('BOGH_cold_in').GetAsObject()
            BOGH_cold_out = self.sim4.GetFlowsheetSimulationObject('BOGH_cold_out').GetAsObject()
            BOGH_HT_1 = self.sim4.GetFlowsheetSimulationObject('BOGH_HT_1').GetAsObject()
            BOGH_stm_in = self.sim4.GetFlowsheetSimulationObject('BOGH_stm_in').GetAsObject()
            BOGH_stm_out = self.sim4.GetFlowsheetSimulationObject('BOGH_stm_out').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            BOGH_cold_in.SetTemperature(tags['FG_FV_OutTempInd']+273.15) #write in K
            BOGH_cold_in.SetPressure(tags['FG_FV_OutPrs'] * 1000.0) #write in Pa
            BOGH_cold_in.SetMassFlow(tags['FG_FV_DischFlow']/3600.0) #write in kg/s
            BOGH_HT_1.set_OutletTemperature(tags['FG_FBOG_BogHtr_OutTempInd']+273.15)
            BOGH_HT_1_dP = tags['FG_FV_OutPrs'] - tags['FG_FBOG_BogHtr_OutPrs']
            BOGH_HT_1.set_DeltaP(BOGH_HT_1_dP * 1000.0)
            BOGH_stm_in.SetTemperature(tags['FG_FBOG_BogHtr_CondWtrTempInd']+273.15) #set steam out/condensate temp here

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim4)


            BOGH_inputs = {}

            BOGH_cold_in_temp = BOGH_cold_in.GetTemperature() - 273.15
            # print(BOGH_cold_in_temp) #degC
            BOGH_cold_in_pres = BOGH_cold_in.GetPressure() / 1000.0
            # print(BOGH_cold_in_pres) #MPa
            BOGH_inputs['BOGH_cold_in_temp'] = BOGH_cold_in_temp
            BOGH_inputs['BOGH_cold_in_pres'] = BOGH_cold_in_pres

            BOGH_cold_mass_flow = BOGH_cold_in.GetMassFlow() * 3600.0
            BOGH_inputs['BOGH_mass_flow'] = BOGH_cold_mass_flow

            BOGH_cold_out_temp = BOGH_cold_out.GetTemperature() - 273.15
            # print(BOGH_cold_out_temp) #degC
            BOGH_cold_out_pres = BOGH_cold_out.GetPressure() / 1000.0
            # print(BOGH_cold_out_pres) #MPa
            BOGH_inputs['BOGH_cold_out_temp'] = BOGH_cold_out_temp
            BOGH_inputs['BOGH_cold_out_pres'] = BOGH_cold_out_pres

            BOGH_stm_in_temp = BOGH_stm_in.GetTemperature() - 273.15
            # BOGH_stm_out_temp = BOGH_stm_out.GetTemperature() - 273.15

            BOGH_stm_out_temp = BOGH_stm_in_temp
            # print(BOGH_stm_in_temp) #degC
            # print(BOGH_stm_out_temp) #degC
            BOGH_inputs['BOGH_stm_in_temp'] = BOGH_stm_in_temp
            BOGH_inputs['BOGH_stm_out_temp'] = BOGH_stm_out_temp

            # print(BOGH_inputs)

            BOGH_Qc = abs(BOGH_HT_1.GetPowerGeneratedOrConsumed())
            BOGH_outputs['BOGH_Qc'] = BOGH_Qc
            # BOGH_Qc

            BOGH_LMTD = ((BOGH_stm_in_temp - BOGH_cold_out_temp) - (BOGH_stm_out_temp - BOGH_cold_in_temp)) / np.log((BOGH_stm_in_temp - BOGH_cold_out_temp) / (BOGH_stm_out_temp - BOGH_cold_in_temp))
            BOGH_outputs['BOGH_LMTD'] = BOGH_LMTD
            # BOGH_LMTD

            BOGH_area = 15.5
            BOGH_U = BOGH_Qc/(BOGH_area*BOGH_LMTD) * 1000
            BOGH_outputs['BOGH_U'] = BOGH_U
            # BOGH_U

            BOGH_U_clean = 145.0

            #read previous fouling factor value
            self.cursor.execute('''select "Value" from public."Output_Tags" where "TagName" = 'BOGH_fouling_factor';''') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()
            ff = row[0][0]

            if tags['FG_FV_DischFlow'] > 2500: #calculate newly if flow is in design range
                BOGH_fouling_factor = (1/BOGH_U) - (1/BOGH_U_clean)
                BOGH_fouling_factor = (1-BOGH_fouling_factor) * 100
            elif ff < 100.0: #if its already been calculated and less than 100, then keep it as it is
                BOGH_fouling_factor = ff
            else: #if flow never been in design range and ff is never calculated earlier, keep it 100
                BOGH_fouling_factor = 100

            BOGH_outputs['BOGH_fouling_factor'] = BOGH_fouling_factor
            # BOGH_fouling_factor

            BOGH_cold_in_specific_enthalpy = BOGH_cold_in.GetMassEnthalpy()
            BOGH_outputs['BOGH_cold_in_specific_enthalpy'] = BOGH_cold_in_specific_enthalpy
            # print(BOGH_cold_in_specific_enthalpy)

            BOGH_cold_out_specific_enthalpy = BOGH_cold_out.GetMassEnthalpy()
            BOGH_outputs['BOGH_cold_out_specific_enthalpy'] = BOGH_cold_out_specific_enthalpy
            # print(BOGH_cold_out_specific_enthalpy)

            BOGH_cold_temp_rise = BOGH_cold_out_temp - BOGH_cold_in_temp #C
            BOGH_outputs['BOGH_cold_temp_rise'] = BOGH_cold_temp_rise
            # BOGH_cold_temp_rise

            BOGH_minimum_approach = BOGH_stm_in_temp - BOGH_cold_out_temp #C
            BOGH_outputs['BOGH_minimum_approach'] = BOGH_minimum_approach
            # BOGH_minimum_approach

            BOGH_steam_required = BOGH_stm_in.GetMassFlow() * 3600 #kg/h
            BOGH_outputs['BOGH_steam_required'] = BOGH_steam_required
            # BOGH_steam_required_theoretically

            # BOGH_cold_specific_heat = (BOGH_Qc / BOGH_cold_temp_rise) * 3600 #kJ/h.C
            # BOGH_outputs['BOGH_cold_specific_heat'] = BOGH_cold_specific_heat

            BOGH_cold_in_energy_flow = BOGH_cold_in.GetEnergyFlow()
            BOGH_outputs['BOGH_cold_in_energy_flow'] = BOGH_cold_in_energy_flow

            BOGH_cold_out_energy_flow = BOGH_cold_out.GetEnergyFlow()
            BOGH_outputs['BOGH_cold_out_energy_flow'] = BOGH_cold_out_energy_flow

            for key in BOGH_outputs.keys():
                BOGH_outputs[key] = float("{0:.2f}".format(BOGH_outputs[key]))
            # print(BOGH_outputs)

        if running_status['WUH'] == 1:
            # print("**************")
            print("starting dwsim WUH")
            # print("**************")

            WUH_cold_in = self.sim5.GetFlowsheetSimulationObject('WUH_cold_in').GetAsObject()
            WUH_cold_out = self.sim5.GetFlowsheetSimulationObject('WUH_cold_out').GetAsObject()
            WUH_HT_1 = self.sim5.GetFlowsheetSimulationObject('WUH_HT_1').GetAsObject()
            WUH_stm_in = self.sim5.GetFlowsheetSimulationObject('WUH_stm_in').GetAsObject()
            WUH_stm_out = self.sim5.GetFlowsheetSimulationObject('WUH_stm_out').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            WUH_cold_in.SetTemperature(tags['FG_FBOG_WuHtr_InTempInd']+273.15) #write in K
            WUH_cold_in.SetPressure(tags['FG_FBOG_WuHtr_InPrs'] * 1000.0) #write in Pa
            # WUH_cold_in.SetMassFlow(tags['yet_to_add'][i]/3600.0) #write in kg/s
            WUH_HT_1.set_OutletTemperature(tags['FG_FBOG_WuHtr_OutTempInd']+273.15)
            WUH_HT_1_dP = tags['FG_FBOG_WuHtr_InPrs'] - tags['FG_FBOG_WuHtr_OutPrs']
            WUH_HT_1.set_DeltaP(WUH_HT_1_dP * 1000.0)
            WUH_stm_in.SetTemperature(tags['FG_FBOG_WuHtr_CondWtrTempInd']+273.15) #set steam out/condensate temp here

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim5)

            WUH_inputs = {}

            WUH_cold_in_temp = WUH_cold_in.GetTemperature() - 273.15
            # print(WUH_cold_in_temp) #degC
            WUH_cold_in_pres = WUH_cold_in.GetPressure() / 1000.0
            # print(WUH_cold_in_pres) #MPa
            WUH_inputs['WUH_cold_in_temp'] = WUH_cold_in_temp
            WUH_inputs['WUH_cold_in_pres'] = WUH_cold_in_pres

            WUH_cold_mass_flow = WUH_cold_in.GetMassFlow() * 3600.0
            WUH_inputs['WUH_mass_flow'] = WUH_cold_mass_flow

            WUH_cold_out_temp = WUH_cold_out.GetTemperature() - 273.15
            # print(WUH_cold_out_temp) #degC
            WUH_cold_out_pres = WUH_cold_out.GetPressure() / 1000.0
            # print(WUH_cold_out_pres) #MPa
            WUH_inputs['WUH_cold_out_temp'] = WUH_cold_out_temp
            WUH_inputs['WUH_cold_out_pres'] = WUH_cold_out_pres

            WUH_stm_in_temp = WUH_stm_in.GetTemperature() - 273.15
            # WUH_stm_out_temp = WUH_stm_out.GetTemperature() - 273.15

            WUH_stm_out_temp = WUH_stm_in_temp
            # print(WUH_stm_in_temp) #degC
            # print(WUH_stm_out_temp) #degC
            WUH_inputs['WUH_stm_in_temp'] = WUH_stm_in_temp
            WUH_inputs['WUH_stm_out_temp'] = WUH_stm_out_temp

            # print(WUH_inputs)

            WUH_Qc = abs(WUH_HT_1.GetPowerGeneratedOrConsumed())
            WUH_outputs['WUH_Qc'] = WUH_Qc
            # WUH_Qc

            WUH_LMTD = ((WUH_stm_in_temp - WUH_cold_out_temp) - (WUH_stm_out_temp - WUH_cold_in_temp)) / np.log((WUH_stm_in_temp - WUH_cold_out_temp) / (WUH_stm_out_temp - WUH_cold_in_temp))
            WUH_outputs['WUH_LMTD'] = WUH_LMTD
            # WUH_LMTD

            WUH_area = 38.2
            WUH_U = WUH_Qc/(WUH_area*WUH_LMTD) * 1000
            WUH_outputs['WUH_U'] = WUH_U
            # WUH_U

            WUH_U_clean = 394.6
            #flow tag yet not available, so deactivating it for now
            # WUH_fouling_factor = (1/WUH_U) - (1/WUH_U_clean)
            # WUH_fouling_factor = (1-WUH_fouling_factor) * 100
            WUH_fouling_factor = 100
            WUH_outputs['WUH_fouling_factor'] = WUH_fouling_factor
            # WUH_fouling_factor

            WUH_cold_in_specific_enthalpy = WUH_cold_in.GetMassEnthalpy()
            WUH_outputs['WUH_cold_in_specific_enthalpy'] = WUH_cold_in_specific_enthalpy
            # print(WUH_cold_in_specific_enthalpy)

            WUH_cold_out_specific_enthalpy = WUH_cold_out.GetMassEnthalpy()
            WUH_outputs['WUH_cold_out_specific_enthalpy'] = WUH_cold_out_specific_enthalpy
            # print(WUH_cold_out_specific_enthalpy)

            WUH_cold_temp_rise = WUH_cold_out_temp - WUH_cold_in_temp #C
            WUH_outputs['WUH_cold_temp_rise'] = WUH_cold_temp_rise
            # WUH_cold_temp_rise

            WUH_minimum_approach = WUH_stm_in_temp - WUH_cold_out_temp #C
            WUH_outputs['WUH_minimum_approach'] = WUH_minimum_approach
            # WUH_minimum_approach

            WUH_steam_required = WUH_stm_in.GetMassFlow() * 3600 #kg/h
            WUH_outputs['WUH_steam_required'] = WUH_steam_required
            # WUH_steam_required_theoretically

            # WUH_cold_specific_heat = (WUH_Qc / WUH_cold_temp_rise) * 3600 #kJ/h.C
            # WUH_outputs['WUH_cold_specific_heat'] = WUH_cold_specific_heat

            WUH_cold_in_energy_flow = WUH_cold_in.GetEnergyFlow()
            WUH_outputs['WUH_cold_in_energy_flow'] = WUH_cold_in_energy_flow

            WUH_cold_out_energy_flow = WUH_cold_out.GetEnergyFlow()
            WUH_outputs['WUH_cold_out_energy_flow'] = WUH_cold_out_energy_flow

            for key in WUH_outputs.keys():
                WUH_outputs[key] = float("{0:.2f}".format(WUH_outputs[key]))
            # print(WUH_outputs)

        if running_status['GWH_Stm'] == 1:
            # print("**************")
            print("starting dwsim GWH_Stm")
            # print("**************")

            GWHS_cold_in = self.sim6.GetFlowsheetSimulationObject('GWHS_cold_in').GetAsObject()
            GWHS_cold_out = self.sim6.GetFlowsheetSimulationObject('GWHS_cold_out').GetAsObject()
            GWHS_HT_1 = self.sim6.GetFlowsheetSimulationObject('GWHS_HT_1').GetAsObject()
            GWHS_stm_in = self.sim6.GetFlowsheetSimulationObject('GWHS_stm_in').GetAsObject()
            GWHS_stm_out = self.sim6.GetFlowsheetSimulationObject('GWHS_stm_out').GetAsObject()


            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")


            GWHS_cold_in.SetTemperature(tags['FG_GW_MainHtr_RtnTemp']+273.15) #write in K
            GWHS_cold_in.SetPressure(tags['FG_GW_MainHtr_InPrs'] * 1000.0) #write in Pa
            # GWHS_cold_in.SetMassFlow(tags['nan'][i]/3600.0) #write in kg/s
            GWHS_HT_1.set_OutletTemperature(tags['FG_GW_MainHtr_OutTempCtrl']+273.15)
            # GWHS_stm_in.SetTemperature(tags['nan'][i]+273.15) #set steam out/condensate temp here

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim6)

            GWHS_inputs = {}

            GWHS_cold_in_temp = GWHS_cold_in.GetTemperature() - 273.15
            # print(GWHS_cold_in_temp) #degC
            GWHS_cold_in_pres = GWHS_cold_in.GetPressure() / 1000.0
            # print(GWHS_cold_in_pres) #MPa
            GWHS_inputs['GWHS_cold_in_temp'] = GWHS_cold_in_temp
            GWHS_inputs['GWHS_cold_in_pres'] = GWHS_cold_in_pres

            GWHS_cold_mass_flow = GWHS_cold_in.GetMassFlow() * 3600.0
            GWHS_inputs['GWHS_mass_flow'] = GWHS_cold_mass_flow

            GWHS_cold_out_temp = GWHS_cold_out.GetTemperature() - 273.15
            # print(GWHS_cold_out_temp) #degC
            GWHS_cold_out_pres = GWHS_cold_out.GetPressure() / 1000.0
            # print(GWHS_cold_out_pres) #MPa
            GWHS_inputs['GWHS_cold_out_temp'] = GWHS_cold_out_temp
            GWHS_inputs['GWHS_cold_out_pres'] = GWHS_cold_out_pres

            GWHS_stm_in_temp = GWHS_stm_in.GetTemperature() - 273.15
            GWHS_stm_out_temp = GWHS_stm_out.GetTemperature() - 273.15

            GWHS_stm_out_temp = GWHS_stm_in_temp
            # print(GWHS_stm_in_temp) #degC
            # print(GWHS_stm_out_temp) #degC
            GWHS_inputs['GWHS_stm_in_temp'] = GWHS_stm_in_temp
            GWHS_inputs['GWHS_stm_out_temp'] = GWHS_stm_out_temp

            # print(GWHS_inputs)

            GWHS_Qc = abs(GWHS_HT_1.GetPowerGeneratedOrConsumed())
            GWH_Stm_outputs['GWHS_Qc'] = GWHS_Qc
            # GWHS_Qc

            GWHS_LMTD = ((GWHS_stm_in_temp - GWHS_cold_out_temp) - (GWHS_stm_out_temp - GWHS_cold_in_temp)) / np.log((GWHS_stm_in_temp - GWHS_cold_out_temp) / (GWHS_stm_out_temp - GWHS_cold_in_temp))
            GWH_Stm_outputs['GWHS_LMTD'] = GWHS_LMTD
            # GWHS_LMTD

            GWHS_area = 4.59
            GWHS_U = GWHS_Qc/(GWHS_area*GWHS_LMTD) * 1000
            GWH_Stm_outputs['GWHS_U'] = GWHS_U
            # GWHS_U

            GWHS_U_clean = 3375.8

            #flow tag yet not available, so deactivating it for now
            # GWHS_fouling_factor = (1/GWHS_U) - (1/GWHS_U_clean)
            # GWHS_fouling_factor = (1-GWHS_fouling_factor) * 100

            GWHS_fouling_factor = 100
            GWH_Stm_outputs['GWHS_fouling_factor'] = GWHS_fouling_factor
            # GWHS_fouling_factor

            GWHS_cold_in_specific_enthalpy = GWHS_cold_in.GetMassEnthalpy()
            GWH_Stm_outputs['GWHS_cold_in_specific_enthalpy'] = GWHS_cold_in_specific_enthalpy
            # print(GWHS_cold_in_specific_enthalpy)

            GWHS_cold_out_specific_enthalpy = GWHS_cold_out.GetMassEnthalpy()
            GWH_Stm_outputs['GWHS_cold_out_specific_enthalpy'] = GWHS_cold_out_specific_enthalpy
            # print(GWHS_cold_out_specific_enthalpy)

            GWHS_cold_temp_rise = GWHS_cold_out_temp - GWHS_cold_in_temp #C
            GWH_Stm_outputs['GWHS_cold_temp_rise'] = GWHS_cold_temp_rise
            # GWHS_cold_temp_rise

            GWHS_minimum_approach = GWHS_stm_in_temp - GWHS_cold_out_temp #C
            GWH_Stm_outputs['GWHS_minimum_approach'] = GWHS_minimum_approach
            # GWHS_minimum_approach

            GWHS_steam_required = GWHS_stm_in.GetMassFlow() * 3600 #kg/h
            GWH_Stm_outputs['GWHS_steam_required'] = GWHS_steam_required
            # GWHS_steam_required_theoretically

            # GWHS_cold_specific_heat = (GWHS_Qc / GWHS_cold_temp_rise) * 3600 #kJ/h.C
            # GWHS_outputs['GWHS_cold_specific_heat'] = GWHS_cold_specific_heat

            GWHS_cold_in_energy_flow = GWHS_cold_in.GetEnergyFlow()
            GWH_Stm_outputs['GWHS_cold_in_energy_flow'] = GWHS_cold_in_energy_flow

            GWHS_cold_out_energy_flow = GWHS_cold_out.GetEnergyFlow()
            GWH_Stm_outputs['GWHS_cold_out_energy_flow'] = GWHS_cold_out_energy_flow
            # print("before formatting:", type(GWHS_outputs['GWHS_fouling_factor']))
            for key in GWH_Stm_outputs.keys():
                GWH_Stm_outputs[key] = float("{0:.2f}".format(GWH_Stm_outputs[key]))
            # print(GWHS_outputs)
            # print("after formatting:", type(GWHS_outputs['GWHS_fouling_factor']))

        if running_status['LD1'] == 1:
            # print("**************")
            print("starting dwsim LD1")
            # print("**************")

            LD1_S1_in = self.sim7.GetFlowsheetSimulationObject('LD1_S1_in').GetAsObject()
            LD1_S1 = self.sim7.GetFlowsheetSimulationObject('LD1_S1').GetAsObject()
            LD1_S1_out_ideal = self.sim7.GetFlowsheetSimulationObject('LD1_S1_out_ideal').GetAsObject()
            LD1_S1_out_actual = self.sim7.GetFlowsheetSimulationObject('LD1_S1_out_actual').GetAsObject()

            LD1_interclr = self.sim7.GetFlowsheetSimulationObject('LD1_interclr').GetAsObject()

            LD1_S2_in = self.sim7.GetFlowsheetSimulationObject('LD1_S2_in').GetAsObject()
            LD1_S2 = self.sim7.GetFlowsheetSimulationObject('LD1_S2').GetAsObject()
            LD1_S2_out_ideal = self.sim7.GetFlowsheetSimulationObject('LD1_S2_out_ideal').GetAsObject()
            LD1_S2_out_actual = self.sim7.GetFlowsheetSimulationObject('LD1_S2_out_actual').GetAsObject()

            LD1_afterclr = self.sim7.GetFlowsheetSimulationObject('LD1_afterclr').GetAsObject()
            LD1_out = self.sim7.GetFlowsheetSimulationObject('LD1_out').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            #S1
            LD1_S1_in.SetPressure(tags['CM_LD1_CtrlPrs'] * 1000.0) #write in Pa
            LD1_S1_in.SetTemperature(tags['CM_LD1_CtrlTemp']+273.15) #write in K
            LD1_S1_in.SetMassFlow(tags['CM_LD1_Flow']/3600.0) #write in kg/s
            LD1_S1_out_actual.SetPressure(tags['CM_LD1_Stage2InPrs'] * 1000.0) #write in Pa #write out pres act
            LD1_S1_out_actual.SetTemperature(tags['CM_LD1_Stage1DischAlrmTemp']+273.15) #write in K #write out temp act
            LD1_S1_out_actual.SetMassFlow(tags['CM_LD1_Flow']/3600.0) #write in kg/s
            LD1_S1.set_POut(tags['CM_LD1_Stage2InPrs'] * 1000.0) #write in Pa #write out pres act
            LD1_interclr.set_OutletTemperature(tags['CM_LD1_Stage2InTemp']+273.15)
            # LD1_S1.get_POut() / 1000

            #S2
            LD1_S2.set_POut(tags['CM_LD1_Stage2DischAlrmCtrlPrs'] * 1000.0) #write in Pa #write out pres act
            LD1_S2_out_actual.SetPressure(tags['CM_LD1_Stage2DischAlrmCtrlPrs'] * 1000.0) #write in Pa #write out pres act
            LD1_S2_out_actual.SetTemperature(tags['CM_LD1_Stage2DischAlrmTemp']+273.15) #write in K #write out temp act
            LD1_S2_out_actual.SetMassFlow(tags['CM_LD1_Flow']/3600.0) #write in kg/s
            LD1_afterclr.set_OutletTemperature(tags['CM_LD1_DischTemp']+273.15)
            # LD1_S2.get_POut() / 1000

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim7)

            LD1_inputs = {}

            #S1
            LD1_S1_in_pres = LD1_S1_in.GetPressure() / 1000.0 #KPa
            LD1_inputs['LD1_S1_in_pres'] = LD1_S1_in_pres

            LD1_S1_in_temp = LD1_S1_in.GetTemperature() - 273.15
            LD1_inputs['LD1_S1_in_temp'] = LD1_S1_in_temp

            LD1_mass_flow = LD1_S1_in.GetMassFlow() * 3600.0
            LD1_inputs['LD1_mass_flow'] = LD1_mass_flow

            LD1_S1_out_pres = LD1_S1_out_ideal.GetPressure() / 1000.0 #KPa
            LD1_inputs['LD1_S1_out_pres'] = LD1_S1_out_pres

            LD1_S1_out_temp = LD1_S1_out_actual.GetTemperature() - 273.15
            LD1_inputs['LD1_S1_out_temp'] = LD1_S1_out_temp

            #S2

            LD1_S2_in_pres = LD1_S2_in.GetPressure() / 1000.0 #KPa
            LD1_inputs['LD1_S2_in_pres'] = LD1_S2_in_pres

            LD1_S2_in_temp = LD1_S2_in.GetTemperature() - 273.15
            LD1_inputs['LD1_S2_in_temp'] = LD1_S2_in_temp

            LD1_S2_out_pres = LD1_S2_out_ideal.GetPressure() / 1000.0 #KPa
            LD1_inputs['LD1_S2_out_pres'] = LD1_S2_out_pres

            LD1_S2_out_temp = LD1_S2_out_actual.GetTemperature() - 273.15
            LD1_inputs['LD1_S2_out_temp'] = LD1_S2_out_temp

            LD1_out_temp = LD1_out.GetTemperature() - 273.15
            LD1_inputs['LD1_out_temp'] = LD1_out_temp

            # print(LD1_inputs)

            #S1
            LD1_S1_in_specific_enthalpy = LD1_S1_in.GetMassEnthalpy()
            LD1_outputs['LD1_S1_in_specific_enthalpy'] = LD1_S1_in_specific_enthalpy

            LD1_S1_pressure_ratio = LD1_S1_out_pres/LD1_S1_in_pres
            LD1_outputs['LD1_S1_pressure_ratio'] = LD1_S1_pressure_ratio

            # LD1_S1_out_adiabatic_temp = LD1_S1_out_ideal.GetTemperature() - 273.15
            # LD1_outputs['LD1_S1_out_adiabatic_temp'] = LD1_S1_out_adiabatic_temp

            LD1_S1_polytropic_power = abs(LD1_S1.GetPowerGeneratedOrConsumed())
            LD1_outputs['LD1_S1_polytropic_power'] = LD1_S1_polytropic_power

            LD1_S1_polytropic_head = LD1_S1.get_PolytropicHead() # m
            LD1_outputs['LD1_S1_polytropic_head'] = LD1_S1_polytropic_head

            # LD1_S1_polytropic_coeff = LD1_S1.get_PolytropicCoefficient() # m
            # LD1_outputs['LD1_S1_polytropic_coeff'] = LD1_S1_polytropic_coeff

            # LD1_S1_in_energy_flow = LD1_S1_in.GetEnergyFlow()
            # LD1_outputs['LD1_S1_in_energy_flow'] = LD1_S1_in_energy_flow

            # LD1_S1_out_energy_flow = LD1_S1_out_actual.GetEnergyFlow()
            # LD1_outputs['LD1_S1_out_energy_flow'] = LD1_S1_out_energy_flow


            LD1_S1_out_ideal_specific_enthalpy = LD1_S1_out_ideal.GetMassEnthalpy()
            # LD1_outputs['LD1_S1_out_ideal_specific_enthalpy'] = LD1_S1_out_ideal_specific_enthalpy


            LD1_S1_out_actual_specific_enthalpy = LD1_S1_out_actual.GetMassEnthalpy()
            LD1_outputs['LD1_S1_out_actual_specific_enthalpy'] = LD1_S1_out_actual_specific_enthalpy

            LD1_S1_ideal_ethalpy_change = LD1_S1_out_ideal_specific_enthalpy - LD1_S1_in_specific_enthalpy
            # LD1_outputs['LD1_S1_ideal_ethalpy_change'] = LD1_S1_ideal_ethalpy_change

            LD1_S1_actual_ethalpy_change = LD1_S1_out_actual_specific_enthalpy - LD1_S1_in_specific_enthalpy
            LD1_outputs['LD1_S1_actual_ethalpy_change'] = LD1_S1_actual_ethalpy_change
            if LD1_S1_actual_ethalpy_change == 0:
                LD1_S1_actual_ethalpy_change = 1
            LD1_S1_polytropic_efficiency = (LD1_S1_ideal_ethalpy_change / LD1_S1_actual_ethalpy_change) * 100
            LD1_outputs['LD1_S1_polytropic_efficiency'] = LD1_S1_polytropic_efficiency

            LD1_interclr_deltaT = LD1_interclr.get_DeltaT() # comes in degC
            LD1_outputs['LD1_interclr_deltaT'] = LD1_interclr_deltaT

            LD1_interclr_duty = LD1_interclr.GetPowerGeneratedOrConsumed()
            LD1_outputs['LD1_interclr_duty'] = LD1_interclr_duty

            #S2

            LD1_S2_in_specific_enthalpy = LD1_S2_in.GetMassEnthalpy()
            LD1_outputs['LD1_S2_in_specific_enthalpy'] = LD1_S2_in_specific_enthalpy

            LD1_S2_pressure_ratio = LD1_S2_out_pres/LD1_S2_in_pres
            LD1_outputs['LD1_S2_pressure_ratio'] = LD1_S2_pressure_ratio

            # LD1_S2_out_adiabatic_temp = LD1_S2_out_ideal.GetTemperature() - 273.15
            # LD1_outputs['LD1_S2_out_adiabatic_temp'] = LD1_S2_out_adiabatic_temp

            LD1_S2_polytropic_power = abs(LD1_S2.GetPowerGeneratedOrConsumed())
            LD1_outputs['LD1_S2_polytropic_power'] = LD1_S2_polytropic_power

            LD1_S2_polytropic_head = LD1_S2.get_PolytropicHead() # m
            LD1_outputs['LD1_S2_polytropic_head'] = LD1_S2_polytropic_head

            # LD1_S2_polytropic_coeff = LD1_S2.get_PolytropicCoefficient() # m
            # LD1_outputs['LD1_S2_polytropic_coeff'] = LD1_S2_polytropic_coeff

            # LD1_S2_in_energy_flow = LD1_S2_in.GetEnergyFlow()
            # LD1_outputs['LD1_S2_in_energy_flow'] = LD1_S2_in_energy_flow

            # LD1_S2_out_energy_flow = LD1_S2_out_actual.GetEnergyFlow()
            # LD1_outputs['LD1_S2_out_energy_flow'] = LD1_S2_out_energy_flow


            LD1_S2_out_ideal_specific_enthalpy = LD1_S2_out_ideal.GetMassEnthalpy()
            # LD1_outputs['LD1_S2_out_ideal_specific_enthalpy'] = LD1_S2_out_ideal_specific_enthalpy


            LD1_S2_out_actual_specific_enthalpy = LD1_S2_out_actual.GetMassEnthalpy()
            LD1_outputs['LD1_S2_out_actual_specific_enthalpy'] = LD1_S2_out_actual_specific_enthalpy

            LD1_S2_ideal_ethalpy_change = LD1_S2_out_ideal_specific_enthalpy - LD1_S2_in_specific_enthalpy
            # LD1_outputs['LD1_S2_ideal_ethalpy_change'] = LD1_S2_ideal_ethalpy_change

            LD1_S2_actual_ethalpy_change = LD1_S2_out_actual_specific_enthalpy - LD1_S2_in_specific_enthalpy
            LD1_outputs['LD1_S2_actual_ethalpy_change'] = LD1_S2_actual_ethalpy_change

            if LD1_S2_actual_ethalpy_change == 0:
                LD1_S2_actual_ethalpy_change = 1

            LD1_S2_polytropic_efficiency = (LD1_S2_ideal_ethalpy_change / LD1_S2_actual_ethalpy_change) * 100
            LD1_outputs['LD1_S2_polytropic_efficiency'] = LD1_S2_polytropic_efficiency

            LD1_afterclr_deltaT = LD1_afterclr.get_DeltaT() # comes in degC
            LD1_outputs['LD1_afterclr_deltaT'] = LD1_afterclr_deltaT

            LD1_afterclr_duty = LD1_afterclr.GetPowerGeneratedOrConsumed()
            LD1_outputs['LD1_afterclr_duty'] = LD1_afterclr_duty


            #LD1 out
            LD1_out_specific_enthalpy = LD1_out.GetMassEnthalpy()
            LD1_outputs['LD1_out_specific_enthalpy'] = LD1_out_specific_enthalpy

            # LD1_out_energy_flow = LD1_out.GetEnergyFlow()
            # LD1_outputs['LD1_out_energy_flow'] = LD1_out_energy_flow

            LD1_outputs['LD1_polytropic_efficiency'] = (LD1_S1_polytropic_efficiency + LD1_S2_polytropic_efficiency)/2

            for key in LD1_outputs.keys():
                LD1_outputs[key] = float("{0:.2f}".format(LD1_outputs[key]))
            # print(LD1_outputs)

        if running_status['LD2'] == 1:
            # print("**************")
            print("starting dwsim LD2")
            # print("**************")


            LD2_S1_in = self.sim8.GetFlowsheetSimulationObject('LD2_S1_in').GetAsObject()
            LD2_S1 = self.sim8.GetFlowsheetSimulationObject('LD2_S1').GetAsObject()
            LD2_S1_out_ideal = self.sim8.GetFlowsheetSimulationObject('LD2_S1_out_ideal').GetAsObject()
            LD2_S1_out_actual = self.sim8.GetFlowsheetSimulationObject('LD2_S1_out_actual').GetAsObject()

            LD2_interclr = self.sim8.GetFlowsheetSimulationObject('LD2_interclr').GetAsObject()

            LD2_S2_in = self.sim8.GetFlowsheetSimulationObject('LD2_S2_in').GetAsObject()
            LD2_S2 = self.sim8.GetFlowsheetSimulationObject('LD2_S2').GetAsObject()
            LD2_S2_out_ideal = self.sim8.GetFlowsheetSimulationObject('LD2_S2_out_ideal').GetAsObject()
            LD2_S2_out_actual = self.sim8.GetFlowsheetSimulationObject('LD2_S2_out_actual').GetAsObject()

            LD2_afterclr = self.sim8.GetFlowsheetSimulationObject('LD2_afterclr').GetAsObject()
            LD2_out = self.sim8.GetFlowsheetSimulationObject('LD2_out').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            #S1
            LD2_S1_in.SetPressure(tags['CM_LD2_CtrlPrs'] * 1000.0) #write in Pa
            LD2_S1_in.SetTemperature(tags['CM_LD2_CtrlTemp']+273.15) #write in K
            LD2_S1_in.SetMassFlow(tags['CM_LD2_Flow']/3600.0) #write in kg/s
            LD2_S1_out_actual.SetPressure(tags['CM_LD2_Stage2InPrs'] * 1000.0) #write in Pa #write out pres act
            LD2_S1_out_actual.SetTemperature(tags['CM_LD2_Stage1DischAlrmTemp']+273.15) #write in K #write out temp act
            LD2_S1_out_actual.SetMassFlow(tags['CM_LD2_Flow']/3600.0) #write in kg/s
            LD2_S1.set_POut(tags['CM_LD2_Stage2InPrs'] * 1000.0) #write in Pa #write out pres act
            LD2_interclr.set_OutletTemperature(tags['CM_LD2_Stage2InTemp']+273.15)
            # LD2_S1.get_POut() / 1000

            #S2
            LD2_S2.set_POut(tags['CM_LD2_Stage2DischAlrmCtrlPrs'] * 1000.0) #write in Pa #write out pres act
            LD2_S2_out_actual.SetPressure(tags['CM_LD2_Stage2DischAlrmCtrlPrs'] * 1000.0) #write in Pa #write out pres act
            LD2_S2_out_actual.SetTemperature(tags['CM_LD2_Stage2DischAlrmTemp']+273.15) #write in K #write out temp act
            LD2_S2_out_actual.SetMassFlow(tags['CM_LD2_Flow']/3600.0) #write in kg/s
            LD2_afterclr.set_OutletTemperature(tags['CM_LD2_DischTemp']+273.15)
            # LD2_S2.get_POut() / 1000

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim8)

            LD2_inputs = {}

            #S1
            LD2_S1_in_pres = LD2_S1_in.GetPressure() / 1000.0 #KPa
            LD2_inputs['LD2_S1_in_pres'] = LD2_S1_in_pres

            LD2_S1_in_temp = LD2_S1_in.GetTemperature() - 273.15
            LD2_inputs['LD2_S1_in_temp'] = LD2_S1_in_temp

            LD2_mass_flow = LD2_S1_in.GetMassFlow() * 3600.0
            LD2_inputs['LD2_mass_flow'] = LD2_mass_flow

            LD2_S1_out_pres = LD2_S1_out_ideal.GetPressure() / 1000.0 #KPa
            LD2_inputs['LD2_S1_out_pres'] = LD2_S1_out_pres

            LD2_S1_out_temp = LD2_S1_out_actual.GetTemperature() - 273.15
            LD2_inputs['LD2_S1_out_temp'] = LD2_S1_out_temp

            #S2

            LD2_S2_in_pres = LD2_S2_in.GetPressure() / 1000.0 #KPa
            LD2_inputs['LD2_S2_in_pres'] = LD2_S2_in_pres

            LD2_S2_in_temp = LD2_S2_in.GetTemperature() - 273.15
            LD2_inputs['LD2_S2_in_temp'] = LD2_S2_in_temp

            LD2_S2_out_pres = LD2_S2_out_ideal.GetPressure() / 1000.0 #KPa
            LD2_inputs['LD2_S2_out_pres'] = LD2_S2_out_pres

            LD2_S2_out_temp = LD2_S2_out_actual.GetTemperature() - 273.15
            LD2_inputs['LD2_S2_out_temp'] = LD2_S2_out_temp

            LD2_out_temp = LD2_out.GetTemperature() - 273.15
            LD2_inputs['LD2_out_temp'] = LD2_out_temp

            # print(LD2_inputs)

            #S1
            LD2_S1_in_specific_enthalpy = LD2_S1_in.GetMassEnthalpy()
            LD2_outputs['LD2_S1_in_specific_enthalpy'] = LD2_S1_in_specific_enthalpy

            LD2_S1_pressure_ratio = LD2_S1_out_pres/LD2_S1_in_pres
            LD2_outputs['LD2_S1_pressure_ratio'] = LD2_S1_pressure_ratio

            # LD2_S1_out_adiabatic_temp = LD2_S1_out_ideal.GetTemperature() - 273.15
            # LD2_outputs['LD2_S1_out_adiabatic_temp'] = LD2_S1_out_adiabatic_temp

            LD2_S1_polytropic_power = abs(LD2_S1.GetPowerGeneratedOrConsumed())
            LD2_outputs['LD2_S1_polytropic_power'] = LD2_S1_polytropic_power

            LD2_S1_polytropic_head = LD2_S1.get_PolytropicHead() # m
            LD2_outputs['LD2_S1_polytropic_head'] = LD2_S1_polytropic_head

            # LD2_S1_polytropic_coeff = LD2_S1.get_PolytropicCoefficient() # m
            # LD2_outputs['LD2_S1_polytropic_coeff'] = LD2_S1_polytropic_coeff

            # LD2_S1_in_energy_flow = LD2_S1_in.GetEnergyFlow()
            # LD2_outputs['LD2_S1_in_energy_flow'] = LD2_S1_in_energy_flow

            # LD2_S1_out_energy_flow = LD2_S1_out_actual.GetEnergyFlow()
            # LD2_outputs['LD2_S1_out_energy_flow'] = LD2_S1_out_energy_flow


            LD2_S1_out_ideal_specific_enthalpy = LD2_S1_out_ideal.GetMassEnthalpy()
            # LD2_outputs['LD2_S1_out_ideal_specific_enthalpy'] = LD2_S1_out_ideal_specific_enthalpy


            LD2_S1_out_actual_specific_enthalpy = LD2_S1_out_actual.GetMassEnthalpy()
            LD2_outputs['LD2_S1_out_actual_specific_enthalpy'] = LD2_S1_out_actual_specific_enthalpy

            LD2_S1_ideal_ethalpy_change = LD2_S1_out_ideal_specific_enthalpy - LD2_S1_in_specific_enthalpy
            # LD2_outputs['LD2_S1_ideal_ethalpy_change'] = LD2_S1_ideal_ethalpy_change

            LD2_S1_actual_ethalpy_change = LD2_S1_out_actual_specific_enthalpy - LD2_S1_in_specific_enthalpy
            LD2_outputs['LD2_S1_actual_ethalpy_change'] = LD2_S1_actual_ethalpy_change

            if LD2_S1_actual_ethalpy_change == 0:
                LD2_S1_actual_ethalpy_change = 1
            LD2_S1_polytropic_efficiency = (LD2_S1_ideal_ethalpy_change / LD2_S1_actual_ethalpy_change) * 100
            LD2_outputs['LD2_S1_polytropic_efficiency'] = LD2_S1_polytropic_efficiency

            LD2_interclr_deltaT = LD2_interclr.get_DeltaT() # comes in degC
            LD2_outputs['LD2_interclr_deltaT'] = LD2_interclr_deltaT

            LD2_interclr_duty = LD2_interclr.GetPowerGeneratedOrConsumed()
            LD2_outputs['LD2_interclr_duty'] = LD2_interclr_duty

            #S2

            LD2_S2_in_specific_enthalpy = LD2_S2_in.GetMassEnthalpy()
            LD2_outputs['LD2_S2_in_specific_enthalpy'] = LD2_S2_in_specific_enthalpy

            LD2_S2_pressure_ratio = LD2_S2_out_pres/LD2_S2_in_pres
            LD2_outputs['LD2_S2_pressure_ratio'] = LD2_S2_pressure_ratio

            # LD2_S2_out_adiabatic_temp = LD2_S2_out_ideal.GetTemperature() - 273.15
            # LD2_outputs['LD2_S2_out_adiabatic_temp'] = LD2_S2_out_adiabatic_temp

            LD2_S2_polytropic_power = abs(LD2_S2.GetPowerGeneratedOrConsumed())
            LD2_outputs['LD2_S2_polytropic_power'] = LD2_S2_polytropic_power

            LD2_S2_polytropic_head = LD2_S2.get_PolytropicHead() # m
            LD2_outputs['LD2_S2_polytropic_head'] = LD2_S2_polytropic_head

            # LD2_S2_polytropic_coeff = LD2_S2.get_PolytropicCoefficient() # m
            # LD2_outputs['LD2_S2_polytropic_coeff'] = LD2_S2_polytropic_coeff

            # LD2_S2_in_energy_flow = LD2_S2_in.GetEnergyFlow()
            # LD2_outputs['LD2_S2_in_energy_flow'] = LD2_S2_in_energy_flow

            # LD2_S2_out_energy_flow = LD2_S2_out_actual.GetEnergyFlow()
            # LD2_outputs['LD2_S2_out_energy_flow'] = LD2_S2_out_energy_flow


            LD2_S2_out_ideal_specific_enthalpy = LD2_S2_out_ideal.GetMassEnthalpy()
            # LD2_outputs['LD2_S2_out_ideal_specific_enthalpy'] = LD2_S2_out_ideal_specific_enthalpy


            LD2_S2_out_actual_specific_enthalpy = LD2_S2_out_actual.GetMassEnthalpy()
            LD2_outputs['LD2_S2_out_actual_specific_enthalpy'] = LD2_S2_out_actual_specific_enthalpy

            LD2_S2_ideal_ethalpy_change = LD2_S2_out_ideal_specific_enthalpy - LD2_S2_in_specific_enthalpy
            # LD2_outputs['LD2_S2_ideal_ethalpy_change'] = LD2_S2_ideal_ethalpy_change

            LD2_S2_actual_ethalpy_change = LD2_S2_out_actual_specific_enthalpy - LD2_S2_in_specific_enthalpy
            LD2_outputs['LD2_S2_actual_ethalpy_change'] = LD2_S2_actual_ethalpy_change
            if LD2_S2_actual_ethalpy_change == 0:
                LD2_S2_actual_ethalpy_change = 1
            LD2_S2_polytropic_efficiency = (LD2_S2_ideal_ethalpy_change / LD2_S2_actual_ethalpy_change) * 100
            LD2_outputs['LD2_S2_polytropic_efficiency'] = LD2_S2_polytropic_efficiency

            LD2_afterclr_deltaT = LD2_afterclr.get_DeltaT() # comes in degC
            LD2_outputs['LD2_afterclr_deltaT'] = LD2_afterclr_deltaT

            LD2_afterclr_duty = LD2_afterclr.GetPowerGeneratedOrConsumed()
            LD2_outputs['LD2_afterclr_duty'] = LD2_afterclr_duty


            #LD2 out
            LD2_out_specific_enthalpy = LD2_out.GetMassEnthalpy()
            LD2_outputs['LD2_out_specific_enthalpy'] = LD2_out_specific_enthalpy

            # LD2_out_energy_flow = LD2_out.GetEnergyFlow()
            # LD2_outputs['LD2_out_energy_flow'] = LD2_out_energy_flow

            LD2_outputs['LD2_polytropic_efficiency'] = (LD2_S1_polytropic_efficiency + LD2_S2_polytropic_efficiency)/2

            for key in LD2_outputs.keys():
                LD2_outputs[key] = float("{0:.2f}".format(LD2_outputs[key]))
            # print(LD2_outputs)

        if running_status['HD1'] == 1:
            # print("**************")
            print("starting dwsim HD1")
            # print("**************")


            HD1_in = self.sim9.GetFlowsheetSimulationObject('HD1_in').GetAsObject()
            HD1 = self.sim9.GetFlowsheetSimulationObject('HD1').GetAsObject()
            HD1_out_ideal = self.sim9.GetFlowsheetSimulationObject('HD1_out_ideal').GetAsObject()
            HD1_out_actual = self.sim9.GetFlowsheetSimulationObject('HD1_out_actual').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            HD1_in.SetPressure(tags['CM_HD1_InPrsAlrmCtrl'] * 1000.0) #write in Pa
            HD1_in.SetTemperature(tags['CM_HD1_InTemp']+273.15) #write in K
            # HD1_in.SetMassFlow(tags['not_yet_added']/3600.0) #write in kg/s
            HD1_out_actual.SetPressure(tags['CM_HD1_DischPrs'] * 1000.0) #write in Pa #write out pres act
            HD1_out_actual.SetTemperature(tags['CM_HD1_CtrlTemp']+273.15) #write in K #write out temp act
            # HD1_out_actual.SetMassFlow(tags['not_yet_added']/3600.0) #write in kg/s
            HD1.set_POut(tags['CM_HD1_DischPrs'] * 1000.0) #write in Pa #write out pres act
            # HD1.get_POut() / 1000

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim9)

            HD1_inputs = {}


            HD1_in_pres = HD1_in.GetPressure() / 1000.0 #KPa
            HD1_inputs['HD1_in_pres'] = HD1_in_pres

            HD1_in_temp = HD1_in.GetTemperature() - 273.15
            HD1_inputs['HD1_in_temp'] = HD1_in_temp

            HD1_mass_flow = HD1_in.GetMassFlow() * 3600.0
            HD1_inputs['HD1_mass_flow'] = HD1_mass_flow

            HD1_out_pres = HD1_out_ideal.GetPressure() / 1000.0 #KPa
            HD1_inputs['HD1_out_pres'] = HD1_out_pres

            HD1_out_temp = HD1_out_actual.GetTemperature() - 273.15
            HD1_inputs['HD1_out_temp'] = HD1_out_temp

            # print(HD1_inputs)

            HD1_in_specific_enthalpy = HD1_in.GetMassEnthalpy()
            HD1_outputs['HD1_in_specific_enthalpy'] = HD1_in_specific_enthalpy

            HD1_pressure_ratio = HD1_out_pres/HD1_in_pres
            HD1_outputs['HD1_pressure_ratio'] = HD1_pressure_ratio

            # HD1_out_adiabatic_temp = HD1_out_ideal.GetTemperature() - 273.15
            # HD1_outputs['HD1_out_adiabatic_temp'] = HD1_out_adiabatic_temp

            HD1_polytropic_power = abs(HD1.GetPowerGeneratedOrConsumed())
            HD1_outputs['HD1_polytropic_power'] = HD1_polytropic_power

            HD1_polytropic_head = HD1.get_PolytropicHead() # m
            HD1_outputs['HD1_polytropic_head'] = HD1_polytropic_head

            # HD1_polytropic_coeff = HD1.get_PolytropicCoefficient() # m
            # HD1_outputs['HD1_polytropic_coeff'] = HD1_polytropic_coeff

            # HD1_in_energy_flow = HD1_in.GetEnergyFlow()
            # HD1_outputs['HD1_in_energy_flow'] = HD1_in_energy_flow

            # HD1_out_energy_flow = HD1_out_actual.GetEnergyFlow()
            # HD1_outputs['HD1_out_energy_flow'] = HD1_out_energy_flow

            HD1_out_ideal_specific_enthalpy = HD1_out_ideal.GetMassEnthalpy()
            HD1_outputs['HD1_out_ideal_specific_enthalpy'] = HD1_out_ideal_specific_enthalpy


            HD1_out_actual_specific_enthalpy = HD1_out_actual.GetMassEnthalpy()
            HD1_outputs['HD1_out_actual_specific_enthalpy'] = HD1_out_actual_specific_enthalpy

            HD1_ideal_ethalpy_change = HD1_out_ideal_specific_enthalpy - HD1_in_specific_enthalpy
            # HD1_outputs['HD1_ideal_ethalpy_change'] = HD1_ideal_ethalpy_change

            HD1_actual_ethalpy_change = HD1_out_actual_specific_enthalpy - HD1_in_specific_enthalpy
            # HD1_outputs['HD1_actual_ethalpy_change'] = HD1_actual_ethalpy_change

            if HD1_actual_ethalpy_change == 0:
                HD1_actual_ethalpy_change = 1
            HD1_polytropic_efficiency = (HD1_ideal_ethalpy_change / HD1_actual_ethalpy_change) * 100
            HD1_outputs['HD1_polytropic_efficiency'] = HD1_polytropic_efficiency

            for key in HD1_outputs.keys():
                HD1_outputs[key] = float("{0:.2f}".format(HD1_outputs[key]))
            # print(HD1_outputs)

        if running_status['HD2'] == 1:
            # print("**************")
            print("starting dwsim HD2")
            # print("**************")

            HD2_in = self.sim10.GetFlowsheetSimulationObject('HD2_in').GetAsObject()
            HD2 = self.sim10.GetFlowsheetSimulationObject('HD2').GetAsObject()
            HD2_out_ideal = self.sim10.GetFlowsheetSimulationObject('HD2_out_ideal').GetAsObject()
            HD2_out_actual = self.sim10.GetFlowsheetSimulationObject('HD2_out_actual').GetAsObject()

            # print("--------------------")
            # print("setting inputs")
            # print("--------------------")

            HD2_in.SetPressure(tags['CM_HD2_InPrsAlrmCtrl'] * 1000.0) #write in Pa
            HD2_in.SetTemperature(tags['CM_HD2_InTemp']+273.15) #write in K
            # HD2_in.SetMassFlow(tags['not_yet_added'][i]/3600.0) #write in kg/s
            HD2_out_actual.SetPressure(tags['CM_HD2_DischPrs'] * 1000.0) #write in Pa #write out pres act
            HD2_out_actual.SetTemperature(tags['CM_HD2_CtrlTemp']+273.15) #write in K #write out temp act
            # HD2_out_actual.SetMassFlow(tags['not_yet_added']/3600.0) #write in kg/s
            HD2.set_POut(tags['CM_HD2_DischPrs'] * 1000.0) #write in Pa #write out pres act
            # HD2.get_POut() / 1000

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.sim10)

            HD2_inputs = {}


            HD2_in_pres = HD2_in.GetPressure() / 1000.0 #KPa
            HD2_inputs['HD2_in_pres'] = HD2_in_pres

            HD2_in_temp = HD2_in.GetTemperature() - 273.15
            HD2_inputs['HD2_in_temp'] = HD2_in_temp

            HD2_mass_flow = HD2_in.GetMassFlow() * 3600.0
            HD2_inputs['HD2_mass_flow'] = HD2_mass_flow

            HD2_out_pres = HD2_out_ideal.GetPressure() / 1000.0 #KPa
            HD2_inputs['HD2_out_pres'] = HD2_out_pres

            HD2_out_temp = HD2_out_actual.GetTemperature() - 273.15
            HD2_inputs['HD2_out_temp'] = HD2_out_temp

            # print(HD2_inputs)

            HD2_in_specific_enthalpy = HD2_in.GetMassEnthalpy()
            HD2_outputs['HD2_in_specific_enthalpy'] = HD2_in_specific_enthalpy

            HD2_pressure_ratio = HD2_out_pres/HD2_in_pres
            HD2_outputs['HD2_pressure_ratio'] = HD2_pressure_ratio

            # HD2_out_adiabatic_temp = HD2_out_ideal.GetTemperature() - 273.15
            # HD2_outputs['HD2_out_adiabatic_temp'] = HD2_out_adiabatic_temp

            HD2_polytropic_power = abs(HD2.GetPowerGeneratedOrConsumed())
            HD2_outputs['HD2_polytropic_power'] = HD2_polytropic_power

            HD2_polytropic_head = HD2.get_PolytropicHead() # m
            HD2_outputs['HD2_polytropic_head'] = HD2_polytropic_head

            # HD2_polytropic_coeff = HD2.get_PolytropicCoefficient() # m
            # HD2_outputs['HD2_polytropic_coeff'] = HD2_polytropic_coeff

            # HD2_in_energy_flow = HD2_in.GetEnergyFlow()
            # HD2_outputs['HD2_in_energy_flow'] = HD2_in_energy_flow

            # HD2_out_energy_flow = HD2_out_actual.GetEnergyFlow()
            # HD2_outputs['HD2_out_energy_flow'] = HD2_out_energy_flow

            HD2_out_ideal_specific_enthalpy = HD2_out_ideal.GetMassEnthalpy()
            HD2_outputs['HD2_out_ideal_specific_enthalpy'] = HD2_out_ideal_specific_enthalpy


            HD2_out_actual_specific_enthalpy = HD2_out_actual.GetMassEnthalpy()
            HD2_outputs['HD2_out_actual_specific_enthalpy'] = HD2_out_actual_specific_enthalpy

            HD2_ideal_ethalpy_change = HD2_out_ideal_specific_enthalpy - HD2_in_specific_enthalpy
            # HD2_outputs['HD2_ideal_ethalpy_change'] = HD2_ideal_ethalpy_change

            HD2_actual_ethalpy_change = HD2_out_actual_specific_enthalpy - HD2_in_specific_enthalpy
            # HD2_outputs['HD2_actual_ethalpy_change'] = HD2_actual_ethalpy_change

            if HD2_actual_ethalpy_change == 0:
                HD2_actual_ethalpy_change = 1
            HD2_polytropic_efficiency = (HD2_ideal_ethalpy_change / HD2_actual_ethalpy_change) * 100
            HD2_outputs['HD2_polytropic_efficiency'] = HD2_polytropic_efficiency

            for key in HD2_outputs.keys():
                HD2_outputs[key] = float("{0:.2f}".format(HD2_outputs[key]))
            # print(HD2_outputs)
        
        ME_cylinder_bore = 0.72 #diameter in m
        ME_cylinder_stroke = 3.086 #stroke length in m
        ME_no_of_cylinders = 5
        cal_value_FG = 50000.0 #kJ/kg
        cal_value_FO = 45000.0
        cal_value_PF = 45000.0
        # ME_clearance_ratio = 0.1 #assumption => clearance volume is 10%
        # ME1_friction_power = 2500.0 #willian's line method. using historical data

        GE_cylinder_bore = 0.35 #diameter in m
        GE_cylinder_stroke = 0.4 #stroke length in m
        GE1_no_of_cylinders = 8
        GE2_no_of_cylinders = 6
        GE3_no_of_cylinders = 6
        GE4_no_of_cylinders = 8

        if running_status['ME1'] == 1:
            print("starting dwsim ME1")

            ME1_Air_in = self.ME1_sim.GetFlowsheetSimulationObject('ME1_Air_in').GetAsObject()
            ME1_Heat_added = self.ME1_sim.GetFlowsheetSimulationObject('ME1_Heat_added').GetAsObject()
            ME1_compression = self.ME1_sim.GetFlowsheetSimulationObject('ME1_compression').GetAsObject()
            ME1_compression_power = self.ME1_sim.GetFlowsheetSimulationObject('ME1_compression_power').GetAsObject()
            ME1_compressed = self.ME1_sim.GetFlowsheetSimulationObject('ME1_compressed').GetAsObject()
            ME1_heat_addition = self.ME1_sim.GetFlowsheetSimulationObject('ME1_heat_addition').GetAsObject()
            ME1_heated = self.ME1_sim.GetFlowsheetSimulationObject('ME1_heated').GetAsObject()
            ME1_expansion = self.ME1_sim.GetFlowsheetSimulationObject('ME1_expansion').GetAsObject()
            ME1_brake_power = self.ME1_sim.GetFlowsheetSimulationObject('ME1_brake_power').GetAsObject()
            ME1_Exhaust_gases = self.ME1_sim.GetFlowsheetSimulationObject('ME1_Exhaust_gases').GetAsObject()
            ME1_TC_exp = self.ME1_sim.GetFlowsheetSimulationObject('ME1_TC_exp').GetAsObject()
            ME1_TC_comp = self.ME1_sim.GetFlowsheetSimulationObject('ME1_TC_comp').GetAsObject()
            ME1_compressed_fresh_air = self.ME1_sim.GetFlowsheetSimulationObject('ME1_compressed_fresh_air').GetAsObject()
            ME1_fresh_air_in = self.ME1_sim.GetFlowsheetSimulationObject('ME1_fresh_air_in').GetAsObject()
            ME1_scav_air_cooler = self.ME1_sim.GetFlowsheetSimulationObject('ME1_scav_air_cooler').GetAsObject()
            ME1_cw_in = self.ME1_sim.GetFlowsheetSimulationObject('ME1_cw_in').GetAsObject()
            ME1_scav_air = self.ME1_sim.GetFlowsheetSimulationObject('ME1_scav_air').GetAsObject()
            ME1_CL = self.ME1_sim.GetFlowsheetSimulationObject('ME1_CL').GetAsObject()
            ME1_HT = self.ME1_sim.GetFlowsheetSimulationObject('ME1_HT').GetAsObject()
            # ME1 additional inputs using main inputs
            tags['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] = (tags['ME1_EG_Cyl1_ScavAirPistonUnderTemp'] + tags['ME1_EG_Cyl2_ScavAirPistonUnderTemp'] + tags['ME1_EG_Cyl3_ScavAirPistonUnderTemp'] + 
                                                tags['ME1_EG_Cyl4_ScavAirPistonUnderTemp'] + tags['ME1_EG_Cyl5_ScavAirPistonUnderTemp'])/5

            tags['ME1_PF_Flow'] = (tags['ME1_FG_Flow_InstMass'] * 0.01) + (tags['ME1_FO_Flow_InstMass'] * 0.005)
            if tags['ME1_Misc_Spd'] == 0.0: #it might happen when Engine run signal  is 1, but speed is 0.
                tags['ME1_Misc_Spd'] = 1.0 #just to avoid infinity answer afterwards, which could result in error during logging into float columns.
            tags['ME1_Suction_volumetric_flow'] = 3.14*(1/4)*(ME_cylinder_bore**2)*ME_cylinder_stroke*ME_no_of_cylinders*tags['ME1_Misc_Spd']*60
            # print(tags['ME1_Misc_Spd'])
            # print(tags['ME1_Suction_volumetric_flow'])
            tags['ME1_Total_fuel_flow'] = tags['ME1_FG_Flow_InstMass'] + tags['ME1_FO_Flow_InstMass'] + tags['ME1_PF_Flow']
            if tags['ME1_Total_fuel_flow'] == 0.0:
                tags['ME1_Total_fuel_flow'] = 1.0
            tags['ME1_Heat_added'] = (tags['ME1_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            # print(tags['ME1_Total_fuel_flow'])
            # print(tags['ME1_Heat_added'])
            # print(tags['ME1_EG_ScavAirMeanPrs'])
            # print(tags['ME1_EG_CylAvg_ScavAirPistonUnderTemp'])

            if 'ME1_EG_ScavAirMeanPrs' in out_of_range_keys: #if it is out of range
                ME1_sa_pres = out_of_range_keys['ME1_EG_ScavAirMeanPrs'] #temporary value
            else:
                ME1_sa_pres = tags['ME1_EG_ScavAirMeanPrs'] #original value
            #ME1
            ME1_Air_in.SetTemperature(tags['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15) #write in K
            # ME1_Air_in.SetPressure(tags['ME1_EG_ScavAirMeanPrs'] * 1000000) #tag in MPa, write in Pa #used the line below
            ME1_Air_in.SetPressure(ME1_sa_pres * 1000000) #tag in MPa, write in Pa
            ME1_Air_in.SetVolumetricFlow(tags['ME1_Suction_volumetric_flow']/3600.0) #write in m3/s
            ME1_compression.set_POut(tags['ME1_Cyl_AvgFiringPrs'] * 1000000) #tag in MPa, write in Pa
            ME1_Heat_added.set_EnergyFlow(tags['ME1_Heat_added']) #writing unit idk yet, to test it
            ME1_expansion.set_POut(ME1_sa_pres * 1000000) #tag in MPa, write in Pa
            ME1_CL.set_OutletTemperature(tags['ME1_EG_TC1_InTemp']+273.15)
            # ME1_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            ME1_fresh_air_in.SetTemperature(tags['ME1_EG_TC_AirInTempA']+273.15)
            ME1_TC_comp.set_POut(ME1_sa_pres * 1000000) #tag in MPa, write in Pa
            ME1_scav_air_cooler.set_OutletTemperature(tags['ME1_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            ME1_cw_in.SetPressure(tags['ME1_EG_ScavAir_CWInPrs'] * 1000000) #tag in MPa, write in Pa)
            ME1_cw_in.SetTemperature(tags['ME1_EG_ScavAir_CWInTemp']+273.15)
            ME1_HT.set_OutletTemperature(tags['ME1_EG_ScavAir_CWOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.ME1_sim)

            ME1_outputs['ME1_Suction_volumetric_flow'] = tags['ME1_Suction_volumetric_flow']
            ME1_outputs['ME1_Combustion_air_flow'] = ME1_Air_in.GetMassFlow() * 3600
            # ME1_outputs['ME1_Combustion_air_SpecificEnthalpy'] = ME1_Air_in.GetMassEnthalpy()
            ME1_outputs['ME1_Total_fuel_flow'] = tags['ME1_Total_fuel_flow']
            ME1_outputs['ME1_AirFuel_ratio'] = ME1_outputs['ME1_Combustion_air_flow'] / ME1_outputs['ME1_Total_fuel_flow']
            ME1_outputs['ME1_Heat_added'] = tags['ME1_Heat_added']
            ME1_outputs['ME1_Isentropic_compression_power'] = abs(ME1_compression.GetPowerGeneratedOrConsumed())
            ME1_outputs['ME1_Maximum_pressure'] = tags['ME1_Cyl_AvgFiringPrs'] * 10 #tag in MPa, converted to bar
            ME1_outputs['ME1_CylTemperature_after_isentropic_compression'] = ME1_compressed.GetTemperature() - 273.15
            ME1_outputs['ME1_CylTemperature_after_combustion'] = ME1_heated.GetTemperature() - 273.15
            # ME1_outputs['ME1_Friction_power'] = ME1_friction_power #willian's line method. using historical data
            ME1_outputs['ME1_Total_ideal_brake_power'] = abs(ME1_expansion.GetPowerGeneratedOrConsumed())
            ME1_outputs['ME1_Net_ideal_brake_power'] = ME1_outputs['ME1_Total_ideal_brake_power'] - ME1_outputs['ME1_Isentropic_compression_power']
            # print(ME1_outputs['ME1_Total_ideal_brake_power'])
            # print(ME1_outputs['ME1_Isentropic_compression_power'])
            ME1_outputs['ME1_Net_actual_brake_power'] = tags['Sft1_Misc_Pwr']
            if ME1_outputs['ME1_Net_actual_brake_power'] == 0.0:
                ME1_outputs['ME1_Net_actual_brake_power'] = 1.0
            # ME1_outputs['ME1_Actual_indicated_power'] = ME1_outputs['ME1_Net_actual_brake_power'] + ME1_friction_power
            ME1_outputs['ME1_Ideal_brake_thermal_efficiency'] = (ME1_outputs['ME1_Net_ideal_brake_power'] / ME1_outputs['ME1_Heat_added']) * 100 #Otto efficiency
            ME1_outputs['ME1_Actual_brake_thermal_efficiency'] = (ME1_outputs['ME1_Net_actual_brake_power'] / ME1_outputs['ME1_Heat_added']) * 100
            ME1_outputs['ME1_Relative_efficiency'] = (ME1_outputs['ME1_Actual_brake_thermal_efficiency'] / ME1_outputs['ME1_Ideal_brake_thermal_efficiency']) * 100
            ME1_outputs['ME1_Ideal_brake_specific_fuel_consumption'] = ME1_outputs['ME1_Total_fuel_flow'] / ME1_outputs['ME1_Net_ideal_brake_power']
            ME1_outputs['ME1_Actual_brake_specific_fuel_consumption'] = ME1_outputs['ME1_Total_fuel_flow'] / ME1_outputs['ME1_Net_actual_brake_power']
            ME1_outputs['ME1_Actual_brake_mean_effective_pressure'] = (ME1_outputs['ME1_Net_actual_brake_power'] / tags['ME1_Suction_volumetric_flow']) * 36 #output in bar
            ME1_outputs['ME1_Ideal_brake_mean_effective_pressure'] = (ME1_outputs['ME1_Net_ideal_brake_power'] / tags['ME1_Suction_volumetric_flow']) * 36 #output in bar
            ME1_outputs['ME1_Compression_pressure_ratio'] = ME1_outputs['ME1_Maximum_pressure'] / (ME1_sa_pres * 10)
            ME1_outputs['ME1_TC_compression_power'] = abs(ME1_TC_comp.GetPowerGeneratedOrConsumed())

            ME1_SAC_outputs['ME1_SAC_air_in_temperature'] = ME1_compressed_fresh_air.GetTemperature() - 273.15
            ME1_SAC_outputs['ME1_SAC_scav_air_in_SpecificEnthalpy'] = ME1_compressed_fresh_air.GetMassEnthalpy()
            ME1_SAC_outputs['ME1_SAC_scav_air_out_SpecificEnthalpy'] = ME1_scav_air.GetMassEnthalpy()
            ME1_SAC_outputs['ME1_SAC_cw_duty'] = ME1_scav_air_cooler.GetPowerGeneratedOrConsumed()
            ME1_SAC_outputs['ME1_SAC_cw_flow_required'] = ME1_cw_in.GetMassFlow() * 3600

            ME1_outputs = ME1_outputs | ME1_SAC_outputs
            for key in ME1_outputs.keys():
                ME1_outputs[key] = float("{0:.3f}".format(ME1_outputs[key]))

        if running_status['ME2'] == 1:
            print("starting dwsim ME2")

            ME2_Air_in = self.ME2_sim.GetFlowsheetSimulationObject('ME2_Air_in').GetAsObject()
            ME2_Heat_added = self.ME2_sim.GetFlowsheetSimulationObject('ME2_Heat_added').GetAsObject()
            ME2_compression = self.ME2_sim.GetFlowsheetSimulationObject('ME2_compression').GetAsObject()
            ME2_compression_power = self.ME2_sim.GetFlowsheetSimulationObject('ME2_compression_power').GetAsObject()
            ME2_compressed = self.ME2_sim.GetFlowsheetSimulationObject('ME2_compressed').GetAsObject()
            ME2_heat_addition = self.ME2_sim.GetFlowsheetSimulationObject('ME2_heat_addition').GetAsObject()
            ME2_heated = self.ME2_sim.GetFlowsheetSimulationObject('ME2_heated').GetAsObject()
            ME2_expansion = self.ME2_sim.GetFlowsheetSimulationObject('ME2_expansion').GetAsObject()
            ME2_brake_power = self.ME2_sim.GetFlowsheetSimulationObject('ME2_brake_power').GetAsObject()
            ME2_Exhaust_gases = self.ME2_sim.GetFlowsheetSimulationObject('ME2_Exhaust_gases').GetAsObject()
            ME2_TC_exp = self.ME2_sim.GetFlowsheetSimulationObject('ME2_TC_exp').GetAsObject()
            ME2_TC_comp = self.ME2_sim.GetFlowsheetSimulationObject('ME2_TC_comp').GetAsObject()
            ME2_compressed_fresh_air = self.ME2_sim.GetFlowsheetSimulationObject('ME2_compressed_fresh_air').GetAsObject()
            ME2_fresh_air_in = self.ME2_sim.GetFlowsheetSimulationObject('ME2_fresh_air_in').GetAsObject()
            ME2_scav_air_cooler = self.ME2_sim.GetFlowsheetSimulationObject('ME2_scav_air_cooler').GetAsObject()
            ME2_cw_in = self.ME2_sim.GetFlowsheetSimulationObject('ME2_cw_in').GetAsObject()
            ME2_scav_air = self.ME2_sim.GetFlowsheetSimulationObject('ME2_scav_air').GetAsObject()
            ME2_CL = self.ME2_sim.GetFlowsheetSimulationObject('ME2_CL').GetAsObject()
            ME2_HT = self.ME2_sim.GetFlowsheetSimulationObject('ME2_HT').GetAsObject()
            # ME2 additional inputs using main inputs
            tags['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] = (tags['ME2_EG_Cyl1_ScavAirPistonUnderTemp'] + tags['ME2_EG_Cyl2_ScavAirPistonUnderTemp'] + tags['ME2_EG_Cyl3_ScavAirPistonUnderTemp'] + 
                                                tags['ME2_EG_Cyl4_ScavAirPistonUnderTemp'] + tags['ME2_EG_Cyl5_ScavAirPistonUnderTemp'])/5

            tags['ME2_PF_Flow'] = (tags['ME2_FG_Flow_InstMass'] * 0.01) + (tags['ME2_FO_Flow_InstMass'] * 0.005)
            if tags['ME2_Misc_Spd'] == 0.0: #it might happen when Engine run signal  is 1, but speed is 0.
                tags['ME2_Misc_Spd'] = 1.0 #just to avoid infinity answer afterwards, which could result in error during logging into float columns.
            tags['ME2_Suction_volumetric_flow'] = 3.14*(1/4)*(ME_cylinder_bore**2)*ME_cylinder_stroke*ME_no_of_cylinders*tags['ME2_Misc_Spd']*60
            tags['ME2_Total_fuel_flow'] = tags['ME2_FG_Flow_InstMass'] + tags['ME2_FO_Flow_InstMass'] + tags['ME2_PF_Flow']
            if tags['ME2_Total_fuel_flow'] == 0.0:
                tags['ME2_Total_fuel_flow'] = 1.0
            tags['ME2_Heat_added'] = (tags['ME2_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            if 'ME2_EG_ScavAirMeanPrs' in out_of_range_keys: #if it is out of range
                ME2_sa_pres = out_of_range_keys['ME2_EG_ScavAirMeanPrs'] #temporary value
            else:
                ME2_sa_pres = tags['ME2_EG_ScavAirMeanPrs'] #original value

            # ME2
            ME2_Air_in.SetTemperature(tags['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15) #write in K
            ME2_Air_in.SetPressure(ME2_sa_pres * 1000000) #tag in MPa, write in Pa
            ME2_Air_in.SetVolumetricFlow(tags['ME2_Suction_volumetric_flow']/3600.0) #write in m3/s
            ME2_compression.set_POut(tags['ME2_Cyl_AvgFiringPrs'] * 1000000) #tag in MPa, write in Pa
            ME2_Heat_added.set_EnergyFlow(tags['ME2_Heat_added']) #writing unit idk yet, to test it
            ME2_expansion.set_POut(ME2_sa_pres * 1000000) #tag in MPa, write in Pa
            ME2_CL.set_OutletTemperature(tags['ME2_EG_TC1_InTemp']+273.15)
            # ME2_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            ME2_fresh_air_in.SetTemperature(tags['ME2_EG_TC_AirInTempA']+273.15)
            ME2_TC_comp.set_POut(ME2_sa_pres * 1000000) #tag in MPa, write in Pa
            ME2_scav_air_cooler.set_OutletTemperature(tags['ME2_EG_CylAvg_ScavAirPistonUnderTemp'] + 273.15)
            ME2_cw_in.SetPressure(tags['ME2_EG_ScavAir_CWInPrs'] * 1000000) #tag in MPa, write in Pa)
            ME2_cw_in.SetTemperature(tags['ME2_EG_ScavAir_CWInTemp']+273.15)
            ME2_HT.set_OutletTemperature(tags['ME2_EG_ScavAir_CWOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.ME2_sim)

            ME2_outputs['ME2_Suction_volumetric_flow'] = tags['ME2_Suction_volumetric_flow']
            ME2_outputs['ME2_Combustion_air_flow'] = ME2_Air_in.GetMassFlow() * 3600
            # ME2_outputs['ME2_Combustion_air_SpecificEnthalpy'] = ME2_Air_in.GetMassEnthalpy()
            ME2_outputs['ME2_Total_fuel_flow'] = tags['ME2_Total_fuel_flow']
            ME2_outputs['ME2_AirFuel_ratio'] = ME2_outputs['ME2_Combustion_air_flow'] / ME2_outputs['ME2_Total_fuel_flow']
            ME2_outputs['ME2_Heat_added'] = tags['ME2_Heat_added']
            ME2_outputs['ME2_Isentropic_compression_power'] = abs(ME2_compression.GetPowerGeneratedOrConsumed())
            ME2_outputs['ME2_Maximum_pressure'] = tags['ME2_Cyl_AvgFiringPrs'] * 10 #tag in MPa, converted to bar
            ME2_outputs['ME2_CylTemperature_after_isentropic_compression'] = ME2_compressed.GetTemperature() - 273.15
            ME2_outputs['ME2_CylTemperature_after_combustion'] = ME2_heated.GetTemperature() - 273.15
            # ME2_outputs['ME2_Friction_power'] = ME2_friction_power #willian's line method. using historical data
            ME2_outputs['ME2_Total_ideal_brake_power'] = abs(ME2_expansion.GetPowerGeneratedOrConsumed())
            ME2_outputs['ME2_Net_ideal_brake_power'] = ME2_outputs['ME2_Total_ideal_brake_power'] - ME2_outputs['ME2_Isentropic_compression_power']
            ME2_outputs['ME2_Net_actual_brake_power'] = tags['Sft1_Misc_Pwr']
            if ME2_outputs['ME2_Net_actual_brake_power'] == 0.0:
                ME2_outputs['ME2_Net_actual_brake_power'] = 1.0
            # ME2_outputs['ME2_Actual_indicated_power'] = ME2_outputs['ME2_Net_actual_brake_power'] + ME2_friction_power
            ME2_outputs['ME2_Ideal_brake_thermal_efficiency'] = (ME2_outputs['ME2_Net_ideal_brake_power'] / ME2_outputs['ME2_Heat_added']) * 100 #Otto efficiency
            ME2_outputs['ME2_Actual_brake_thermal_efficiency'] = (ME2_outputs['ME2_Net_actual_brake_power'] / ME2_outputs['ME2_Heat_added']) * 100
            ME2_outputs['ME2_Relative_efficiency'] = (ME2_outputs['ME2_Actual_brake_thermal_efficiency'] / ME2_outputs['ME2_Ideal_brake_thermal_efficiency']) * 100
            ME2_outputs['ME2_Ideal_brake_specific_fuel_consumption'] = ME2_outputs['ME2_Total_fuel_flow'] / ME2_outputs['ME2_Net_ideal_brake_power']
            ME2_outputs['ME2_Actual_brake_specific_fuel_consumption'] = ME2_outputs['ME2_Total_fuel_flow'] / ME2_outputs['ME2_Net_actual_brake_power']
            ME2_outputs['ME2_Actual_brake_mean_effective_pressure'] = (ME2_outputs['ME2_Net_actual_brake_power'] / tags['ME2_Suction_volumetric_flow']) * 36 #output in bar
            ME2_outputs['ME2_Ideal_brake_mean_effective_pressure'] = (ME2_outputs['ME2_Net_ideal_brake_power'] / tags['ME2_Suction_volumetric_flow']) * 36 #output in bar
            ME2_outputs['ME2_Compression_pressure_ratio'] = ME2_outputs['ME2_Maximum_pressure'] / (ME2_sa_pres * 10)
            ME2_outputs['ME2_TC_compression_power'] = abs(ME2_TC_comp.GetPowerGeneratedOrConsumed())

            ME2_SAC_outputs['ME2_SAC_air_in_temperature'] = ME2_compressed_fresh_air.GetTemperature() - 273.15
            ME2_SAC_outputs['ME2_SAC_scav_air_in_SpecificEnthalpy'] = ME2_compressed_fresh_air.GetMassEnthalpy()
            ME2_SAC_outputs['ME2_SAC_scav_air_out_SpecificEnthalpy'] = ME2_scav_air.GetMassEnthalpy()
            ME2_SAC_outputs['ME2_SAC_cw_duty'] = ME2_scav_air_cooler.GetPowerGeneratedOrConsumed()
            ME2_SAC_outputs['ME2_SAC_cw_flow_required'] = ME2_cw_in.GetMassFlow() * 3600

            ME2_outputs = ME2_outputs | ME2_SAC_outputs
            for key in ME2_outputs.keys():
                ME2_outputs[key] = float("{0:.3f}".format(ME2_outputs[key]))

        if running_status['GE1'] == 1:
            print("starting dwsim GE1")
            
            GE1_Air_in = self.GE1_sim.GetFlowsheetSimulationObject('GE1_Air_in').GetAsObject()
            GE1_Heat_added = self.GE1_sim.GetFlowsheetSimulationObject('GE1_Heat_added').GetAsObject()
            GE1_compression = self.GE1_sim.GetFlowsheetSimulationObject('GE1_compression').GetAsObject()
            GE1_compression_power = self.GE1_sim.GetFlowsheetSimulationObject('GE1_compression_power').GetAsObject()
            GE1_compressed = self.GE1_sim.GetFlowsheetSimulationObject('GE1_compressed').GetAsObject()
            GE1_heat_addition = self.GE1_sim.GetFlowsheetSimulationObject('GE1_heat_addition').GetAsObject()
            GE1_heated = self.GE1_sim.GetFlowsheetSimulationObject('GE1_heated').GetAsObject()
            GE1_expansion = self.GE1_sim.GetFlowsheetSimulationObject('GE1_expansion').GetAsObject()
            GE1_brake_power = self.GE1_sim.GetFlowsheetSimulationObject('GE1_brake_power').GetAsObject()
            GE1_Exhaust_gases = self.GE1_sim.GetFlowsheetSimulationObject('GE1_Exhaust_gases').GetAsObject()
            GE1_TC_exp = self.GE1_sim.GetFlowsheetSimulationObject('GE1_TC_exp').GetAsObject()
            GE1_TC_comp = self.GE1_sim.GetFlowsheetSimulationObject('GE1_TC_comp').GetAsObject()
            GE1_compressed_fresh_air = self.GE1_sim.GetFlowsheetSimulationObject('GE1_compressed_fresh_air').GetAsObject()
            GE1_fresh_air_in = self.GE1_sim.GetFlowsheetSimulationObject('GE1_fresh_air_in').GetAsObject()
            GE1_scav_air_cooler = self.GE1_sim.GetFlowsheetSimulationObject('GE1_scav_air_cooler').GetAsObject()
            GE1_cw_in = self.GE1_sim.GetFlowsheetSimulationObject('GE1_cw_in').GetAsObject()
            GE1_scav_air = self.GE1_sim.GetFlowsheetSimulationObject('GE1_scav_air').GetAsObject()
            GE1_CL = self.GE1_sim.GetFlowsheetSimulationObject('GE1_CL').GetAsObject()
            GE1_HT = self.GE1_sim.GetFlowsheetSimulationObject('GE1_HT').GetAsObject()
            # GE1 additional inputs using main inputs
            tags['GE1_CylAvg_CompressionPrs'] = (tags['GE1_Cyl1_CompressionPrs'] + tags['GE1_Cyl2_CompressionPrs'] + tags['GE1_Cyl3_CompressionPrs'] + 
                                        tags['GE1_Cyl4_CompressionPrs'] + tags['GE1_Cyl5_CompressionPrs'] + tags['GE1_Cyl6_CompressionPrs'] +
                                        tags['GE1_Cyl7_CompressionPrs'] + tags['GE1_Cyl8_CompressionPrs'])/8

            if running_status['GE1'] == 1 and running_status['GE2'] == 1:
                tags['GE1_FO_flow'] = tags['GE_FO_GE1GE2_Flow_InstMass']/2
            else:
                tags['GE1_FO_flow'] = tags['GE_FO_GE1GE2_Flow_InstMass']
            
            tags['GE1_PF_Flow'] = (tags['GE1_FG_Flow_InstMass'] * 0.01) + (tags['GE1_FO_flow'] * 0.005)
            if tags['GE1_Misc_Spd'] == 0.0:
                tags['GE1_Misc_Spd'] = 1.0
            tags['GE1_Suction_volumetric_flow'] = (3.14*(1/4)*(GE_cylinder_bore**2)*GE_cylinder_stroke*GE1_no_of_cylinders*tags['GE1_Misc_Spd']*60)/2
            tags['GE1_Total_fuel_flow'] = tags['GE1_FG_Flow_InstMass'] + tags['GE1_FO_flow'] + tags['GE1_PF_Flow']
            if tags['GE1_Total_fuel_flow'] == 0.0:
                tags['GE1_Total_fuel_flow'] = 1.0
            tags['GE1_Heat_added'] = (tags['GE1_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            # GE1
            GE1_Air_in.SetTemperature(tags['GE1_CS_AirClr_ChAirOutTemp'] + 273.15) #write in K
            GE1_Air_in.SetPressure(tags['GE1_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE1_Air_in.SetVolumetricFlow(tags['GE1_Suction_volumetric_flow']/3600.0) #write in m3/s
            GE1_compression.set_POut(tags['GE1_CylAvg_CompressionPrs'] * 1000000) #tag in MPa, write in Pa
            GE1_Heat_added.set_EnergyFlow(tags['GE1_Heat_added']) #writing unit idk yet, to test it
            GE1_expansion.set_POut(tags['GE1_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE1_CL.set_OutletTemperature(tags['GE1_EG_TC1_InTemp']+273.15)
            # GE1_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            GE1_fresh_air_in.SetTemperature(tags['GE1_EG_TC1_AirIntakeTemp']+273.15)
            GE1_TC_comp.set_POut(tags['GE1_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE1_scav_air_cooler.set_OutletTemperature(tags['GE1_CS_AirClr_ChAirOutTemp'] + 273.15)
            GE1_cw_in.SetPressure(tags['GE1_CS_LTCFW_AirClrInPrs'] * 1000000) #tag in MPa, write in Pa)
            GE1_cw_in.SetTemperature(tags['GE1_CS_LTCFW_AirClrInTemp']+273.15)
            GE1_HT.set_OutletTemperature(tags['GE1_CS_LTCFW_AirClrOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.GE1_sim)

            GE1_outputs['GE1_Suction_volumetric_flow'] = tags['GE1_Suction_volumetric_flow']
            GE1_outputs['GE1_Combustion_air_flow'] = GE1_Air_in.GetMassFlow() * 3600
            # GE1_outputs['GE1_Combustion_air_SpecificEnthalpy'] = GE1_Air_in.GetMassEnthalpy()
            GE1_outputs['GE1_Total_fuel_flow'] = tags['GE1_Total_fuel_flow']
            GE1_outputs['GE1_AirFuel_ratio'] = GE1_outputs['GE1_Combustion_air_flow'] / GE1_outputs['GE1_Total_fuel_flow']
            GE1_outputs['GE1_Heat_added'] = tags['GE1_Heat_added']
            GE1_outputs['GE1_Isentropic_compression_power'] = abs(GE1_compression.GetPowerGeneratedOrConsumed())
            GE1_outputs['GE1_Maximum_pressure'] = tags['GE1_CylAvg_CompressionPrs'] * 10 #tag in MPa, converted to bar
            GE1_outputs['GE1_CylTemperature_after_isentropic_compression'] = GE1_compressed.GetTemperature() - 273.15
            GE1_outputs['GE1_CylTemperature_after_combustion'] = GE1_heated.GetTemperature() - 273.15
            # GE1_outputs['GE1_Friction_power'] = GE1_friction_power #willian's line method. using historical data
            GE1_outputs['GE1_Total_ideal_brake_power'] = abs(GE1_expansion.GetPowerGeneratedOrConsumed())
            GE1_outputs['GE1_Net_ideal_brake_power'] = GE1_outputs['GE1_Total_ideal_brake_power'] - GE1_outputs['GE1_Isentropic_compression_power']
            GE1_outputs['GE1_Net_actual_brake_power'] = tags['GE1_Misc_Pwr']
            if GE1_outputs['GE1_Net_actual_brake_power'] == 0.0:
                GE1_outputs['GE1_Net_actual_brake_power'] = 1.0
            # GE1_outputs['GE1_Actual_indicated_power'] = GE1_outputs['GE1_Net_actual_brake_power'] + GE1_friction_power
            GE1_outputs['GE1_Ideal_brake_thermal_efficiency'] = (GE1_outputs['GE1_Net_ideal_brake_power'] / GE1_outputs['GE1_Heat_added']) * 100 #Otto efficiency
            GE1_outputs['GE1_Actual_brake_thermal_efficiency'] = (GE1_outputs['GE1_Net_actual_brake_power'] / GE1_outputs['GE1_Heat_added']) * 100
            GE1_outputs['GE1_Relative_efficiency'] = (GE1_outputs['GE1_Actual_brake_thermal_efficiency'] / GE1_outputs['GE1_Ideal_brake_thermal_efficiency']) * 100
            GE1_outputs['GE1_Ideal_brake_specific_fuel_consumption'] = GE1_outputs['GE1_Total_fuel_flow'] / GE1_outputs['GE1_Net_ideal_brake_power']
            GE1_outputs['GE1_Actual_brake_specific_fuel_consumption'] = GE1_outputs['GE1_Total_fuel_flow'] / GE1_outputs['GE1_Net_actual_brake_power']
            GE1_outputs['GE1_Actual_brake_mean_effective_pressure'] = (GE1_outputs['GE1_Net_actual_brake_power'] / tags['GE1_Suction_volumetric_flow']) * 36 #output in bar
            GE1_outputs['GE1_Ideal_brake_mean_effective_pressure'] = (GE1_outputs['GE1_Net_ideal_brake_power'] / tags['GE1_Suction_volumetric_flow']) * 36 #output in bar
            GE1_outputs['GE1_Compression_pressure_ratio'] = GE1_outputs['GE1_Maximum_pressure'] / (tags['GE1_CS_AirClr_ChAirOutPrs'] * 10)
            GE1_outputs['GE1_TC_compression_power'] = abs(GE1_TC_comp.GetPowerGeneratedOrConsumed())

            GE1_SAC_outputs['GE1_SAC_air_in_temperature'] = GE1_compressed_fresh_air.GetTemperature() - 273.15
            GE1_SAC_outputs['GE1_SAC_scav_air_in_SpecificEnthalpy'] = GE1_compressed_fresh_air.GetMassEnthalpy()
            GE1_SAC_outputs['GE1_SAC_scav_air_out_SpecificEnthalpy'] = GE1_scav_air.GetMassEnthalpy()
            GE1_SAC_outputs['GE1_SAC_cw_duty'] = GE1_scav_air_cooler.GetPowerGeneratedOrConsumed()
            GE1_SAC_outputs['GE1_SAC_cw_flow_required'] = GE1_cw_in.GetMassFlow() * 3600

            GE1_outputs = GE1_outputs | GE1_SAC_outputs
            for key in GE1_outputs.keys():
                GE1_outputs[key] = float("{0:.3f}".format(GE1_outputs[key]))

        if running_status['GE2'] == 1:
            print("starting dwsim GE2")

            GE2_Air_in = self.GE2_sim.GetFlowsheetSimulationObject('GE2_Air_in').GetAsObject()
            GE2_Heat_added = self.GE2_sim.GetFlowsheetSimulationObject('GE2_Heat_added').GetAsObject()
            GE2_compression = self.GE2_sim.GetFlowsheetSimulationObject('GE2_compression').GetAsObject()
            GE2_compression_power = self.GE2_sim.GetFlowsheetSimulationObject('GE2_compression_power').GetAsObject()
            GE2_compressed = self.GE2_sim.GetFlowsheetSimulationObject('GE2_compressed').GetAsObject()
            GE2_heat_addition = self.GE2_sim.GetFlowsheetSimulationObject('GE2_heat_addition').GetAsObject()
            GE2_heated = self.GE2_sim.GetFlowsheetSimulationObject('GE2_heated').GetAsObject()
            GE2_expansion = self.GE2_sim.GetFlowsheetSimulationObject('GE2_expansion').GetAsObject()
            GE2_brake_power = self.GE2_sim.GetFlowsheetSimulationObject('GE2_brake_power').GetAsObject()
            GE2_Exhaust_gases = self.GE2_sim.GetFlowsheetSimulationObject('GE2_Exhaust_gases').GetAsObject()
            GE2_TC_exp = self.GE2_sim.GetFlowsheetSimulationObject('GE2_TC_exp').GetAsObject()
            GE2_TC_comp = self.GE2_sim.GetFlowsheetSimulationObject('GE2_TC_comp').GetAsObject()
            GE2_compressed_fresh_air = self.GE2_sim.GetFlowsheetSimulationObject('GE2_compressed_fresh_air').GetAsObject()
            GE2_fresh_air_in = self.GE2_sim.GetFlowsheetSimulationObject('GE2_fresh_air_in').GetAsObject()
            GE2_scav_air_cooler = self.GE2_sim.GetFlowsheetSimulationObject('GE2_scav_air_cooler').GetAsObject()
            GE2_cw_in = self.GE2_sim.GetFlowsheetSimulationObject('GE2_cw_in').GetAsObject()
            GE2_scav_air = self.GE2_sim.GetFlowsheetSimulationObject('GE2_scav_air').GetAsObject()
            GE2_CL = self.GE2_sim.GetFlowsheetSimulationObject('GE2_CL').GetAsObject()
            GE2_HT = self.GE2_sim.GetFlowsheetSimulationObject('GE2_HT').GetAsObject()
            #GE2 additional inputs using main inputs
            tags['GE2_CylAvg_CompressionPrs'] = (tags['GE2_Cyl1_CompressionPrs'] + tags['GE2_Cyl2_CompressionPrs'] + tags['GE2_Cyl3_CompressionPrs'] + 
                                        tags['GE2_Cyl4_CompressionPrs'] + tags['GE2_Cyl5_CompressionPrs'] + tags['GE2_Cyl6_CompressionPrs'])/8

            if running_status['GE1'] == 1 and running_status['GE2'] == 1:
                tags['GE2_FO_flow'] = tags['GE_FO_GE1GE2_Flow_InstMass']/2
            else:
                tags['GE2_FO_flow'] = tags['GE_FO_GE1GE2_Flow_InstMass']

            tags['GE2_PF_Flow'] = (tags['GE2_FG_Flow_InstMass'] * 0.01) + (tags['GE2_FO_flow'] * 0.005)
            if tags['GE2_Misc_Spd'] == 0.0:
                tags['GE2_Misc_Spd'] = 1.0
            tags['GE2_Suction_volumetric_flow'] = (3.14*(1/4)*(GE_cylinder_bore**2)*GE_cylinder_stroke*GE2_no_of_cylinders*tags['GE2_Misc_Spd']*60)/2
            tags['GE2_Total_fuel_flow'] = tags['GE2_FG_Flow_InstMass'] + tags['GE2_FO_flow'] + tags['GE2_PF_Flow']
            if tags['GE2_Total_fuel_flow'] == 0.0:
                tags['GE2_Total_fuel_flow'] = 1.0
            tags['GE2_Heat_added'] = (tags['GE2_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            # GE2
            GE2_Air_in.SetTemperature(tags['GE2_CS_AirClr_ChAirOutTemp'] + 273.15) #write in K
            GE2_Air_in.SetPressure(tags['GE2_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE2_Air_in.SetVolumetricFlow(tags['GE2_Suction_volumetric_flow']/3600.0) #write in m3/s
            GE2_compression.set_POut(tags['GE2_CylAvg_CompressionPrs'] * 1000000) #tag in MPa, write in Pa
            GE2_Heat_added.set_EnergyFlow(tags['GE2_Heat_added']) #writing unit idk yet, to test it
            GE2_expansion.set_POut(tags['GE2_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE2_CL.set_OutletTemperature(tags['GE2_EG_TC1_InTemp']+273.15)
            # GE2_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            GE2_fresh_air_in.SetTemperature(tags['GE2_EG_TC1_AirIntakeTemp']+273.15)
            GE2_TC_comp.set_POut(tags['GE2_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE2_scav_air_cooler.set_OutletTemperature(tags['GE2_CS_AirClr_ChAirOutTemp'] + 273.15)
            GE2_cw_in.SetPressure(tags['GE2_CS_LTCFW_AirClrInPrs'] * 1000000) #tag in MPa, write in Pa)
            GE2_cw_in.SetTemperature(tags['GE2_CS_LTCFW_AirClrInTemp']+273.15)
            GE2_HT.set_OutletTemperature(tags['GE2_CS_LTCFW_AirClrOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.GE2_sim)

            GE2_outputs['GE2_Suction_volumetric_flow'] = tags['GE2_Suction_volumetric_flow']
            GE2_outputs['GE2_Combustion_air_flow'] = GE2_Air_in.GetMassFlow() * 3600
            # GE2_outputs['GE2_Combustion_air_SpecificEnthalpy'] = GE2_Air_in.GetMassEnthalpy()
            GE2_outputs['GE2_Total_fuel_flow'] = tags['GE2_Total_fuel_flow']
            GE2_outputs['GE2_AirFuel_ratio'] = GE2_outputs['GE2_Combustion_air_flow'] / GE2_outputs['GE2_Total_fuel_flow']
            GE2_outputs['GE2_Heat_added'] = tags['GE2_Heat_added']
            GE2_outputs['GE2_Isentropic_compression_power'] = abs(GE2_compression.GetPowerGeneratedOrConsumed())
            GE2_outputs['GE2_Maximum_pressure'] = tags['GE2_CylAvg_CompressionPrs'] * 10 #tag in MPa, converted to bar
            GE2_outputs['GE2_CylTemperature_after_isentropic_compression'] = GE2_compressed.GetTemperature() - 273.15
            GE2_outputs['GE2_CylTemperature_after_combustion'] = GE2_heated.GetTemperature() - 273.15
            # GE2_outputs['GE2_Friction_power'] = GE2_friction_power #willian's line method. using historical data
            GE2_outputs['GE2_Total_ideal_brake_power'] = abs(GE2_expansion.GetPowerGeneratedOrConsumed())
            GE2_outputs['GE2_Net_ideal_brake_power'] = GE2_outputs['GE2_Total_ideal_brake_power'] - GE2_outputs['GE2_Isentropic_compression_power']
            GE2_outputs['GE2_Net_actual_brake_power'] = tags['GE2_Misc_Pwr']
            if GE2_outputs['GE2_Net_actual_brake_power'] == 0.0:
                GE2_outputs['GE2_Net_actual_brake_power'] = 1.0
            # GE2_outputs['GE2_Actual_indicated_power'] = GE2_outputs['GE2_Net_actual_brake_power'] + GE2_friction_power
            GE2_outputs['GE2_Ideal_brake_thermal_efficiency'] = (GE2_outputs['GE2_Net_ideal_brake_power'] / GE2_outputs['GE2_Heat_added']) * 100 #Otto efficiency
            GE2_outputs['GE2_Actual_brake_thermal_efficiency'] = (GE2_outputs['GE2_Net_actual_brake_power'] / GE2_outputs['GE2_Heat_added']) * 100
            GE2_outputs['GE2_Relative_efficiency'] = (GE2_outputs['GE2_Actual_brake_thermal_efficiency'] / GE2_outputs['GE2_Ideal_brake_thermal_efficiency']) * 100
            GE2_outputs['GE2_Ideal_brake_specific_fuel_consumption'] = GE2_outputs['GE2_Total_fuel_flow'] / GE2_outputs['GE2_Net_ideal_brake_power']
            GE2_outputs['GE2_Actual_brake_specific_fuel_consumption'] = GE2_outputs['GE2_Total_fuel_flow'] / GE2_outputs['GE2_Net_actual_brake_power']
            GE2_outputs['GE2_Actual_brake_mean_effective_pressure'] = (GE2_outputs['GE2_Net_actual_brake_power'] / tags['GE2_Suction_volumetric_flow']) * 36 #output in bar
            GE2_outputs['GE2_Ideal_brake_mean_effective_pressure'] = (GE2_outputs['GE2_Net_ideal_brake_power'] / tags['GE2_Suction_volumetric_flow']) * 36 #output in bar
            GE2_outputs['GE2_Compression_pressure_ratio'] = GE2_outputs['GE2_Maximum_pressure'] / (tags['GE2_CS_AirClr_ChAirOutPrs'] * 10)
            GE2_outputs['GE2_TC_compression_power'] = abs(GE2_TC_comp.GetPowerGeneratedOrConsumed())

            GE2_SAC_outputs['GE2_SAC_air_in_temperature'] = GE2_compressed_fresh_air.GetTemperature() - 273.15
            GE2_SAC_outputs['GE2_SAC_scav_air_in_SpecificEnthalpy'] = GE2_compressed_fresh_air.GetMassEnthalpy()
            GE2_SAC_outputs['GE2_SAC_scav_air_out_SpecificEnthalpy'] = GE2_scav_air.GetMassEnthalpy()
            GE2_SAC_outputs['GE2_SAC_cw_duty'] = GE2_scav_air_cooler.GetPowerGeneratedOrConsumed()
            GE2_SAC_outputs['GE2_SAC_cw_flow_required'] = GE2_cw_in.GetMassFlow() * 3600

            GE2_outputs = GE2_outputs | GE2_SAC_outputs
            for key in GE2_outputs.keys():
                GE2_outputs[key] = float("{0:.3f}".format(GE2_outputs[key]))

        if running_status['GE3'] == 1:
            print("starting dwsim GE3")
            
            GE3_Air_in = self.GE3_sim.GetFlowsheetSimulationObject('GE3_Air_in').GetAsObject()
            GE3_Heat_added = self.GE3_sim.GetFlowsheetSimulationObject('GE3_Heat_added').GetAsObject()
            GE3_compression = self.GE3_sim.GetFlowsheetSimulationObject('GE3_compression').GetAsObject()
            GE3_compression_power = self.GE3_sim.GetFlowsheetSimulationObject('GE3_compression_power').GetAsObject()
            GE3_compressed = self.GE3_sim.GetFlowsheetSimulationObject('GE3_compressed').GetAsObject()
            GE3_heat_addition = self.GE3_sim.GetFlowsheetSimulationObject('GE3_heat_addition').GetAsObject()
            GE3_heated = self.GE3_sim.GetFlowsheetSimulationObject('GE3_heated').GetAsObject()
            GE3_expansion = self.GE3_sim.GetFlowsheetSimulationObject('GE3_expansion').GetAsObject()
            GE3_brake_power = self.GE3_sim.GetFlowsheetSimulationObject('GE3_brake_power').GetAsObject()
            GE3_Exhaust_gases = self.GE3_sim.GetFlowsheetSimulationObject('GE3_Exhaust_gases').GetAsObject()
            GE3_TC_exp = self.GE3_sim.GetFlowsheetSimulationObject('GE3_TC_exp').GetAsObject()
            GE3_TC_comp = self.GE3_sim.GetFlowsheetSimulationObject('GE3_TC_comp').GetAsObject()
            GE3_compressed_fresh_air = self.GE3_sim.GetFlowsheetSimulationObject('GE3_compressed_fresh_air').GetAsObject()
            GE3_fresh_air_in = self.GE3_sim.GetFlowsheetSimulationObject('GE3_fresh_air_in').GetAsObject()
            GE3_scav_air_cooler = self.GE3_sim.GetFlowsheetSimulationObject('GE3_scav_air_cooler').GetAsObject()
            GE3_cw_in = self.GE3_sim.GetFlowsheetSimulationObject('GE3_cw_in').GetAsObject()
            GE3_scav_air = self.GE3_sim.GetFlowsheetSimulationObject('GE3_scav_air').GetAsObject()
            GE3_CL = self.GE3_sim.GetFlowsheetSimulationObject('GE3_CL').GetAsObject()
            GE3_HT = self.GE3_sim.GetFlowsheetSimulationObject('GE3_HT').GetAsObject()
            #GE3 additional inputs using main inputs
            tags['GE3_CylAvg_CompressionPrs'] = (tags['GE3_Cyl1_CompressionPrs'] + tags['GE3_Cyl2_CompressionPrs'] + tags['GE3_Cyl3_CompressionPrs'] + 
                                        tags['GE3_Cyl4_CompressionPrs'] + tags['GE3_Cyl5_CompressionPrs'] + tags['GE3_Cyl6_CompressionPrs'])/8
            if running_status['GE3'] == 1 and running_status['GE4'] == 1:
                tags['GE3_FO_flow'] = tags['GE_FO_GE3GE4_Flow_InstMass']/2
            else:
                tags['GE3_FO_flow'] = tags['GE_FO_GE3GE4_Flow_InstMass']
            tags['GE3_PF_Flow'] = (tags['GE3_FG_Flow_InstMass'] * 0.01) + (tags['GE3_FO_flow'] * 0.005)
            if tags['GE3_Misc_Spd'] == 0.0:
                tags['GE3_Misc_Spd'] = 1.0
            tags['GE3_Suction_volumetric_flow'] = (3.14*(1/4)*(GE_cylinder_bore**2)*GE_cylinder_stroke*GE3_no_of_cylinders*tags['GE3_Misc_Spd']*60)/2
            tags['GE3_Total_fuel_flow'] = tags['GE3_FG_Flow_InstMass'] + tags['GE3_FO_flow'] + tags['GE3_PF_Flow']
            if tags['GE3_Total_fuel_flow'] == 0.0:
                tags['GE3_Total_fuel_flow'] = 1.0
            tags['GE3_Heat_added'] = (tags['GE3_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            # GE3
            GE3_Air_in.SetTemperature(tags['GE3_CS_AirClr_ChAirOutTemp'] + 273.15) #write in K
            GE3_Air_in.SetPressure(tags['GE3_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE3_Air_in.SetVolumetricFlow(tags['GE3_Suction_volumetric_flow']/3600.0) #write in m3/s
            GE3_compression.set_POut(tags['GE3_CylAvg_CompressionPrs'] * 1000000) #tag in MPa, write in Pa
            GE3_Heat_added.set_EnergyFlow(tags['GE3_Heat_added']) #writing unit idk yet, to test it
            GE3_expansion.set_POut(tags['GE3_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE3_CL.set_OutletTemperature(tags['GE3_EG_TC1_InTemp']+273.15)
            # GE3_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            GE3_fresh_air_in.SetTemperature(tags['GE3_EG_TC1_AirIntakeTemp']+273.15)
            GE3_TC_comp.set_POut(tags['GE3_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE3_scav_air_cooler.set_OutletTemperature(tags['GE3_CS_AirClr_ChAirOutTemp'] + 273.15)
            GE3_cw_in.SetPressure(tags['GE3_CS_LTCFW_AirClrInPrs'] * 1000000) #tag in MPa, write in Pa)
            GE3_cw_in.SetTemperature(tags['GE3_CS_LTCFW_AirClrInTemp']+273.15)
            GE3_HT.set_OutletTemperature(tags['GE3_CS_LTCFW_AirClrOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.GE3_sim)

            GE3_outputs['GE3_Suction_volumetric_flow'] = tags['GE3_Suction_volumetric_flow']
            GE3_outputs['GE3_Combustion_air_flow'] = GE3_Air_in.GetMassFlow() * 3600
            # GE3_outputs['GE3_Combustion_air_SpecificEnthalpy'] = GE3_Air_in.GetMassEnthalpy()
            GE3_outputs['GE3_Total_fuel_flow'] = tags['GE3_Total_fuel_flow']
            GE3_outputs['GE3_AirFuel_ratio'] = GE3_outputs['GE3_Combustion_air_flow'] / GE3_outputs['GE3_Total_fuel_flow']
            GE3_outputs['GE3_Heat_added'] = tags['GE3_Heat_added']
            GE3_outputs['GE3_Isentropic_compression_power'] = abs(GE3_compression.GetPowerGeneratedOrConsumed())
            GE3_outputs['GE3_Maximum_pressure'] = tags['GE3_CylAvg_CompressionPrs'] * 10 #tag in MPa, converted to bar
            GE3_outputs['GE3_CylTemperature_after_isentropic_compression'] = GE3_compressed.GetTemperature() - 273.15
            GE3_outputs['GE3_CylTemperature_after_combustion'] = GE3_heated.GetTemperature() - 273.15
            # GE3_outputs['GE3_Friction_power'] = GE3_friction_power #willian's line method. using historical data
            GE3_outputs['GE3_Total_ideal_brake_power'] = abs(GE3_expansion.GetPowerGeneratedOrConsumed())
            GE3_outputs['GE3_Net_ideal_brake_power'] = GE3_outputs['GE3_Total_ideal_brake_power'] - GE3_outputs['GE3_Isentropic_compression_power']
            GE3_outputs['GE3_Net_actual_brake_power'] = tags['GE3_Misc_Pwr']
            if GE3_outputs['GE3_Net_actual_brake_power'] == 0.0:
                GE3_outputs['GE3_Net_actual_brake_power'] = 1.0
            # GE3_outputs['GE3_Actual_indicated_power'] = GE3_outputs['GE3_Net_actual_brake_power'] + GE3_friction_power
            GE3_outputs['GE3_Ideal_brake_thermal_efficiency'] = (GE3_outputs['GE3_Net_ideal_brake_power'] / GE3_outputs['GE3_Heat_added']) * 100 #Otto efficiency
            GE3_outputs['GE3_Actual_brake_thermal_efficiency'] = (GE3_outputs['GE3_Net_actual_brake_power'] / GE3_outputs['GE3_Heat_added']) * 100
            GE3_outputs['GE3_Relative_efficiency'] = (GE3_outputs['GE3_Actual_brake_thermal_efficiency'] / GE3_outputs['GE3_Ideal_brake_thermal_efficiency']) * 100
            GE3_outputs['GE3_Ideal_brake_specific_fuel_consumption'] = GE3_outputs['GE3_Total_fuel_flow'] / GE3_outputs['GE3_Net_ideal_brake_power']
            GE3_outputs['GE3_Actual_brake_specific_fuel_consumption'] = GE3_outputs['GE3_Total_fuel_flow'] / GE3_outputs['GE3_Net_actual_brake_power']
            GE3_outputs['GE3_Actual_brake_mean_effective_pressure'] = (GE3_outputs['GE3_Net_actual_brake_power'] / tags['GE3_Suction_volumetric_flow']) * 36 #output in bar
            GE3_outputs['GE3_Ideal_brake_mean_effective_pressure'] = (GE3_outputs['GE3_Net_ideal_brake_power'] / tags['GE3_Suction_volumetric_flow']) * 36 #output in bar
            GE3_outputs['GE3_Compression_pressure_ratio'] = GE3_outputs['GE3_Maximum_pressure'] / (tags['GE3_CS_AirClr_ChAirOutPrs'] * 10)
            GE3_outputs['GE3_TC_compression_power'] = abs(GE3_TC_comp.GetPowerGeneratedOrConsumed())

            GE3_SAC_outputs['GE3_SAC_air_in_temperature'] = GE3_compressed_fresh_air.GetTemperature() - 273.15
            GE3_SAC_outputs['GE3_SAC_scav_air_in_SpecificEnthalpy'] = GE3_compressed_fresh_air.GetMassEnthalpy()
            GE3_SAC_outputs['GE3_SAC_scav_air_out_SpecificEnthalpy'] = GE3_scav_air.GetMassEnthalpy()
            GE3_SAC_outputs['GE3_SAC_cw_duty'] = GE3_scav_air_cooler.GetPowerGeneratedOrConsumed()
            GE3_SAC_outputs['GE3_SAC_cw_flow_required'] = GE3_cw_in.GetMassFlow() * 3600

            GE3_outputs = GE3_outputs | GE3_SAC_outputs
            for key in GE3_outputs.keys():
                GE3_outputs[key] = float("{0:.3f}".format(GE3_outputs[key]))

        if running_status['GE4'] == 1:
            print("starting dwsim GE4")

            GE4_Air_in = self.GE4_sim.GetFlowsheetSimulationObject('GE4_Air_in').GetAsObject()
            GE4_Heat_added = self.GE4_sim.GetFlowsheetSimulationObject('GE4_Heat_added').GetAsObject()
            GE4_compression = self.GE4_sim.GetFlowsheetSimulationObject('GE4_compression').GetAsObject()
            GE4_compression_power = self.GE4_sim.GetFlowsheetSimulationObject('GE4_compression_power').GetAsObject()
            GE4_compressed = self.GE4_sim.GetFlowsheetSimulationObject('GE4_compressed').GetAsObject()
            GE4_heat_addition = self.GE4_sim.GetFlowsheetSimulationObject('GE4_heat_addition').GetAsObject()
            GE4_heated = self.GE4_sim.GetFlowsheetSimulationObject('GE4_heated').GetAsObject()
            GE4_expansion = self.GE4_sim.GetFlowsheetSimulationObject('GE4_expansion').GetAsObject()
            GE4_brake_power = self.GE4_sim.GetFlowsheetSimulationObject('GE4_brake_power').GetAsObject()
            GE4_Exhaust_gases = self.GE4_sim.GetFlowsheetSimulationObject('GE4_Exhaust_gases').GetAsObject()
            GE4_TC_exp = self.GE4_sim.GetFlowsheetSimulationObject('GE4_TC_exp').GetAsObject()
            GE4_TC_comp = self.GE4_sim.GetFlowsheetSimulationObject('GE4_TC_comp').GetAsObject()
            GE4_compressed_fresh_air = self.GE4_sim.GetFlowsheetSimulationObject('GE4_compressed_fresh_air').GetAsObject()
            GE4_fresh_air_in = self.GE4_sim.GetFlowsheetSimulationObject('GE4_fresh_air_in').GetAsObject()
            GE4_scav_air_cooler = self.GE4_sim.GetFlowsheetSimulationObject('GE4_scav_air_cooler').GetAsObject()
            GE4_cw_in = self.GE4_sim.GetFlowsheetSimulationObject('GE4_cw_in').GetAsObject()
            GE4_scav_air = self.GE4_sim.GetFlowsheetSimulationObject('GE4_scav_air').GetAsObject()
            GE4_CL = self.GE4_sim.GetFlowsheetSimulationObject('GE4_CL').GetAsObject()
            GE4_HT = self.GE4_sim.GetFlowsheetSimulationObject('GE4_HT').GetAsObject()
            #GE4 additional inputs using main inputs
            tags['GE4_CylAvg_CompressionPrs'] = (tags['GE4_Cyl1_CompressionPrs'] + tags['GE4_Cyl2_CompressionPrs'] + tags['GE4_Cyl3_CompressionPrs'] + 
                                        tags['GE4_Cyl4_CompressionPrs'] + tags['GE4_Cyl5_CompressionPrs'] + tags['GE4_Cyl6_CompressionPrs'])/8
            if running_status['GE3'] == 1 and running_status['GE4'] == 1:
                tags['GE4_FO_flow'] = tags['GE_FO_GE3GE4_Flow_InstMass']/2
            else:
                tags['GE4_FO_flow'] = tags['GE_FO_GE3GE4_Flow_InstMass']
            tags['GE4_PF_Flow'] = (tags['GE4_FG_Flow_InstMass'] * 0.01) + (tags['GE4_FO_flow'] * 0.005)
            if tags['GE4_Misc_Spd'] == 0.0:
                tags['GE4_Misc_Spd'] = 1.0
            tags['GE4_Suction_volumetric_flow'] = (3.14*(1/4)*(GE_cylinder_bore**2)*GE_cylinder_stroke*GE4_no_of_cylinders*tags['GE4_Misc_Spd']*60)/2
            tags['GE4_Total_fuel_flow'] = tags['GE4_FG_Flow_InstMass'] + tags['GE4_FO_flow'] + tags['GE4_PF_Flow']
            if tags['GE4_Total_fuel_flow'] == 0.0:
                tags['GE4_Total_fuel_flow'] = 1.0
            tags['GE4_Heat_added'] = (tags['GE4_Total_fuel_flow'] * cal_value_FG)/3600 #kW

            # GE4
            GE4_Air_in.SetTemperature(tags['GE4_CS_AirClr_ChAirOutTemp'] + 273.15) #write in K
            GE4_Air_in.SetPressure(tags['GE4_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE4_Air_in.SetVolumetricFlow(tags['GE4_Suction_volumetric_flow']/3600.0) #write in m3/s
            GE4_compression.set_POut(tags['GE4_CylAvg_CompressionPrs'] * 1000000) #tag in MPa, write in Pa
            GE4_Heat_added.set_EnergyFlow(tags['GE4_Heat_added']) #writing unit idk yet, to test it
            GE4_expansion.set_POut(tags['GE4_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE4_CL.set_OutletTemperature(tags['GE4_EG_TC1_InTemp']+273.15)
            # GE4_fresh_air_in.SetPressure(100.0 * 1000) #ambient pressure in Pa
            GE4_fresh_air_in.SetTemperature(tags['GE4_EG_TC1_AirIntakeTemp']+273.15)
            GE4_TC_comp.set_POut(tags['GE4_CS_AirClr_ChAirOutPrs'] * 1000000) #tag in MPa, write in Pa
            GE4_scav_air_cooler.set_OutletTemperature(tags['GE4_CS_AirClr_ChAirOutTemp'] + 273.15)
            GE4_cw_in.SetPressure(tags['GE4_CS_LTCFW_AirClrInPrs'] * 1000000) #tag in MPa, write in Pa)
            GE4_cw_in.SetTemperature(tags['GE4_CS_LTCFW_AirClrInTemp']+273.15)
            GE4_HT.set_OutletTemperature(tags['GE4_CS_LTCFW_AirClrOutTemp']+273.15)

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.GE4_sim)

            GE4_outputs['GE4_Suction_volumetric_flow'] = tags['GE4_Suction_volumetric_flow']
            GE4_outputs['GE4_Combustion_air_flow'] = GE4_Air_in.GetMassFlow() * 3600
            # GE4_outputs['GE4_Combustion_air_SpecificEnthalpy'] = GE4_Air_in.GetMassEnthalpy()
            GE4_outputs['GE4_Total_fuel_flow'] = tags['GE4_Total_fuel_flow']
            GE4_outputs['GE4_AirFuel_ratio'] = GE4_outputs['GE4_Combustion_air_flow'] / GE4_outputs['GE4_Total_fuel_flow']
            GE4_outputs['GE4_Heat_added'] = tags['GE4_Heat_added']
            GE4_outputs['GE4_Isentropic_compression_power'] = abs(GE4_compression.GetPowerGeneratedOrConsumed())
            GE4_outputs['GE4_Maximum_pressure'] = tags['GE4_CylAvg_CompressionPrs'] * 10 #tag in MPa, converted to bar
            GE4_outputs['GE4_CylTemperature_after_isentropic_compression'] = GE4_compressed.GetTemperature() - 273.15
            GE4_outputs['GE4_CylTemperature_after_combustion'] = GE4_heated.GetTemperature() - 273.15
            # GE4_outputs['GE4_Friction_power'] = GE4_friction_power #willian's line method. using historical data
            GE4_outputs['GE4_Total_ideal_brake_power'] = abs(GE4_expansion.GetPowerGeneratedOrConsumed())
            GE4_outputs['GE4_Net_ideal_brake_power'] = GE4_outputs['GE4_Total_ideal_brake_power'] - GE4_outputs['GE4_Isentropic_compression_power']
            GE4_outputs['GE4_Net_actual_brake_power'] = tags['GE4_Misc_Pwr']
            if GE4_outputs['GE4_Net_actual_brake_power'] == 0.0:
                GE4_outputs['GE4_Net_actual_brake_power'] = 1.0
            # GE4_outputs['GE4_Actual_indicated_power'] = GE4_outputs['GE4_Net_actual_brake_power'] + GE4_friction_power
            GE4_outputs['GE4_Ideal_brake_thermal_efficiency'] = (GE4_outputs['GE4_Net_ideal_brake_power'] / GE4_outputs['GE4_Heat_added']) * 100 #Otto efficiency
            GE4_outputs['GE4_Actual_brake_thermal_efficiency'] = (GE4_outputs['GE4_Net_actual_brake_power'] / GE4_outputs['GE4_Heat_added']) * 100
            GE4_outputs['GE4_Relative_efficiency'] = (GE4_outputs['GE4_Actual_brake_thermal_efficiency'] / GE4_outputs['GE4_Ideal_brake_thermal_efficiency']) * 100
            GE4_outputs['GE4_Ideal_brake_specific_fuel_consumption'] = GE4_outputs['GE4_Total_fuel_flow'] / GE4_outputs['GE4_Net_ideal_brake_power']
            GE4_outputs['GE4_Actual_brake_specific_fuel_consumption'] = GE4_outputs['GE4_Total_fuel_flow'] / GE4_outputs['GE4_Net_actual_brake_power']
            GE4_outputs['GE4_Actual_brake_mean_effective_pressure'] = (GE4_outputs['GE4_Net_actual_brake_power'] / tags['GE4_Suction_volumetric_flow']) * 36 #output in bar
            GE4_outputs['GE4_Ideal_brake_mean_effective_pressure'] = (GE4_outputs['GE4_Net_ideal_brake_power'] / tags['GE4_Suction_volumetric_flow']) * 36 #output in bar
            GE4_outputs['GE4_Compression_pressure_ratio'] = GE4_outputs['GE4_Maximum_pressure'] / (tags['GE4_CS_AirClr_ChAirOutPrs'] * 10)
            GE4_outputs['GE4_TC_compression_power'] = abs(GE4_TC_comp.GetPowerGeneratedOrConsumed())

            GE4_SAC_outputs['GE4_SAC_air_in_temperature'] = GE4_compressed_fresh_air.GetTemperature() - 273.15
            GE4_SAC_outputs['GE4_SAC_scav_air_in_SpecificEnthalpy'] = GE4_compressed_fresh_air.GetMassEnthalpy()
            GE4_SAC_outputs['GE4_SAC_scav_air_out_SpecificEnthalpy'] = GE4_scav_air.GetMassEnthalpy()
            GE4_SAC_outputs['GE4_SAC_cw_duty'] = GE4_scav_air_cooler.GetPowerGeneratedOrConsumed()
            GE4_SAC_outputs['GE4_SAC_cw_flow_required'] = GE4_cw_in.GetMassFlow() * 3600

            GE4_outputs = GE4_outputs | GE4_SAC_outputs
            for key in GE4_outputs.keys():
                GE4_outputs[key] = float("{0:.3f}".format(GE4_outputs[key]))

        if running_status['NG1'] == 1:
            print("starting dwsim NG1")
            # NG1
            if tags_av_check['NS_NG1-40101_PV'] == 1 and tags_av_check['NS_NG1-40102_PV'] == 1 and  tags_av_check['NS_NG1-40103_PV'] == 1:
                NG1_air_comp = self.NG1_sim.GetFlowsheetSimulationObject('NG1_air_comp').GetAsObject()
                NG1_Air = self.NG1_sim.GetFlowsheetSimulationObject('NG1_Air').GetAsObject()
                NG1_comp_out = self.NG1_sim.GetFlowsheetSimulationObject('NG1_comp_out').GetAsObject()
                NG1_clr = self.NG1_sim.GetFlowsheetSimulationObject('NG1_clr').GetAsObject()
                NG1_htr_in = self.NG1_sim.GetFlowsheetSimulationObject('NG1_htr_in').GetAsObject()
                NG1_htr = self.NG1_sim.GetFlowsheetSimulationObject('NG1_htr').GetAsObject()
                NG1_sep_in = self.NG1_sim.GetFlowsheetSimulationObject('NG1_sep_in').GetAsObject()
            
                NG1_Air.SetTemperature(tags['Nav_Atm_AmbTemp'] + 273.15)
                # NG1_Air.SetPressure(tags['Nav_Atm_AmbPrs'] * 100) #tag in Mbar, write in Pa
                NG1_Air.SetVolumetricFlow((tags['Elec_NGen1_Flow']/0.78)/3600) #write in m3/s
                NG1_air_comp.set_POut(tags['NS_NG1-40101_PV'] * 1000000) #tag in MPa, write in Pa
                NG1_clr.set_OutletTemperature(tags['NS_NG1-40102_PV']+273.15)
                NG1_htr.set_OutletTemperature(tags['NS_NG1-40103_PV']+273.15)

                from DWSIM.GlobalSettings import Settings
                Settings.SolverMode = 0
                errors = self.interf.CalculateFlowsheet2(self.NG1_sim)

                NG1_outputs['NG1_Air_flow_estimated'] = NG1_Air.GetMassFlow() * 3600
                NG1_outputs['NG1_Air_comp_in_SpecificEnthalpy'] = NG1_Air.GetMassEnthalpy()
                NG1_outputs['NG1_Air_comp_out_SpecificEnthalpy'] = NG1_comp_out.GetMassEnthalpy()
                NG1_outputs['NG1_air_comp_polytropic_power'] = abs(NG1_air_comp.GetPowerGeneratedOrConsumed())
                NG1_outputs['NG1_air_comp_out_temperature'] = NG1_comp_out.GetTemperature() - 273.15
                NG1_outputs['NG1_cooling_duty'] = NG1_clr.GetPowerGeneratedOrConsumed()
                NG1_outputs['NG1_heating_duty'] = abs(NG1_htr.GetPowerGeneratedOrConsumed())
                NG1_outputs['NG1_htr_in_SpecificEnthalpy'] = NG1_htr_in.GetMassEnthalpy()
                NG1_outputs['NG1_htr_out_SpecificEnthalpy'] = NG1_sep_in.GetMassEnthalpy()

                for key in NG1_outputs.keys():
                    NG1_outputs[key] = float("{0:.3f}".format(NG1_outputs[key]))

        if running_status['NG2'] == 1:
            print("starting dwsim NG2")
            if tags_av_check['NS_NG2-40101_PV'] == 1 and tags_av_check['NS_NG2-40102_PV'] == 1 and  tags_av_check['NS_NG2-40103_PV'] == 1:
                # NG2
                NG2_air_comp = self.NG2_sim.GetFlowsheetSimulationObject('NG2_air_comp').GetAsObject()
                NG2_Air = self.NG2_sim.GetFlowsheetSimulationObject('NG2_Air').GetAsObject()
                NG2_comp_out = self.NG2_sim.GetFlowsheetSimulationObject('NG2_comp_out').GetAsObject()
                NG2_clr = self.NG2_sim.GetFlowsheetSimulationObject('NG2_clr').GetAsObject()
                NG2_htr_in = self.NG2_sim.GetFlowsheetSimulationObject('NG2_htr_in').GetAsObject()
                NG2_htr = self.NG2_sim.GetFlowsheetSimulationObject('NG2_htr').GetAsObject()
                NG2_sep_in = self.NG2_sim.GetFlowsheetSimulationObject('NG2_sep_in').GetAsObject()

                NG2_Air.SetTemperature(tags['Nav_Atm_AmbTemp'] + 273.15)
                # NG2_Air.SetPressure(tags['Nav_Atm_AmbPrs'] * 100) #tag in Mbar, write in Pa
                NG2_Air.SetVolumetricFlow((tags['Elec_NGen2_Flow']/0.78)/3600) #write in m3/s
                NG2_air_comp.set_POut(tags['NS_NG2-40101_PV'] * 1000000) #tag in MPa, write in Pa
                NG2_clr.set_OutletTemperature(tags['NS_NG2-40102_PV']+273.15)
                NG2_htr.set_OutletTemperature(tags['NS_NG2-40103_PV']+273.15)

                from DWSIM.GlobalSettings import Settings
                Settings.SolverMode = 0
                errors = self.interf.CalculateFlowsheet2(self.NG2_sim)

                NG2_outputs['NG2_Air_flow_estimated'] = NG2_Air.GetMassFlow() * 3600
                NG2_outputs['NG2_Air_comp_in_SpecificEnthalpy'] = NG2_Air.GetMassEnthalpy()
                NG2_outputs['NG2_Air_comp_out_SpecificEnthalpy'] = NG2_comp_out.GetMassEnthalpy()
                NG2_outputs['NG2_air_comp_polytropic_power'] = abs(NG2_air_comp.GetPowerGeneratedOrConsumed())
                NG2_outputs['NG2_air_comp_out_temperature'] = NG2_comp_out.GetTemperature() - 273.15
                NG2_outputs['NG2_cooling_duty'] = NG2_clr.GetPowerGeneratedOrConsumed()
                NG2_outputs['NG2_heating_duty'] = abs(NG2_htr.GetPowerGeneratedOrConsumed())
                NG2_outputs['NG2_htr_in_SpecificEnthalpy'] = NG2_htr_in.GetMassEnthalpy()
                NG2_outputs['NG2_htr_out_SpecificEnthalpy'] = NG2_sep_in.GetMassEnthalpy()

                for key in NG2_outputs.keys():
                    NG2_outputs[key] = float("{0:.3f}".format(NG2_outputs[key]))

        #@@@@@@@@@@@@@@@ below block updated for AB simulation from here   
        #Aux Boiler
        FO_cal_value = 50000 #kJ/kg
        if running_status['AB_AB1'] == 1 and running_status['AB_AB2'] == 1:
                AB1_heat_av = ((tags['Blr_AuxBlr_FO_Flow_InstMass'] * 50000)/3600)/2 #kW
                AB2_heat_av = ((tags['Blr_AuxBlr_FO_Flow_InstMass'] * 50000)/3600)/2
        elif running_status['AB_AB1'] == 1:
                AB1_heat_av = ((tags['Blr_AuxBlr_FO_Flow_InstMass'] * 50000)/3600)
                AB2_heat_av = 0
        elif running_status['AB_AB2'] == 1:
                AB2_heat_av = ((tags['Blr_AuxBlr_FO_Flow_InstMass'] * 50000)/3600)
                AB1_heat_av = 0
        if running_status['AB_AB1'] == 1:
            print("starting dwsim AB1")
            AB1_steam = self.AB1_sim.GetFlowsheetSimulationObject('AB1_steam').GetAsObject()
            AB1_steam.SetPressure(tags['Blr_AuxBlr1_StmPrs'] * 1000000) #tag in MPa, write in Pa

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.AB1_sim)
        
            AB_AB1_outputs['AB1_Heat_added'] = AB1_heat_av
            AB_AB1_outputs['AB1_Steam_temp'] = AB1_steam.GetTemperature() - 273.15
            AB_AB1_outputs['AB1_Steam_SpecificEnthalpy'] = AB1_steam.GetMassEnthalpy()
            AB_AB1_outputs['AB1_Steam_flow'] =  (AB_AB1_outputs['AB1_Heat_added']/AB_AB1_outputs['AB1_Steam_SpecificEnthalpy']) * 3600 * 0.8 #assuming 80% efficiency

        if running_status['AB_AB2'] == 1:
            print("starting dwsim AB2")
            AB2_steam = self.AB2_sim.GetFlowsheetSimulationObject('AB2_steam').GetAsObject()
            AB2_steam.SetPressure(tags['Blr_AuxBlr2_StmPrs'] * 1000000) #tag in MPa, write in Pa

            from DWSIM.GlobalSettings import Settings
            Settings.SolverMode = 0
            errors = self.interf.CalculateFlowsheet2(self.AB2_sim)
        
            AB_AB2_outputs['AB2_Heat_added'] = AB2_heat_av
            AB_AB2_outputs['AB2_Steam_temp'] = AB2_steam.GetTemperature() - 273.15
            AB_AB2_outputs['AB2_Steam_SpecificEnthalpy'] = AB2_steam.GetMassEnthalpy()
            AB_AB2_outputs['AB2_Steam_flow'] =  (AB_AB2_outputs['AB2_Heat_added']/AB_AB2_outputs['AB2_Steam_SpecificEnthalpy']) * 3600 * 0.8 #assuming 80% efficiency

        # above block updated for AB simulation till here
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Calculate additional key outputs using basic dwsim outputs
        # 'Cargo_vapor', 'HD', 'FBOG', 'NBOG' # for overall modes
    
        Cargo_vapor_outputs = {}
        HD_outputs = {} 
        FBOG_outputs = {} 
        NBOG_outputs = {}

        # key_outputs_FGSS = ['Cargo_vapor_total_duty', 'FBOG_total_duty', 'FBOG_total_steam', 'HD_polytropic_efficiency', 'NBOG_polytropic_efficiency', 'NBOG_polytropic_power']
        #'Cargo_vapor_total_duty' = LNGV_duty + WUH_duty
        if running_status['LNGV'] == 1:
            LNGV_duty = LNGV_outputs['LNGV_Qc']
        else:
            LNGV_duty = 0
        if running_status['WUH'] == 1:
            WUH_duty = WUH_outputs['WUH_Qc']
        else:
            WUH_duty = 0
        Cargo_vapor_outputs['Cargo_vapor_total_duty'] = LNGV_duty + WUH_duty
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #'FBOG_total_duty' = FV_duty + BOGH_duty
        if running_status['FV'] == 1:
            FV_duty = FV_outputs['FV_Qc']
        else:
            FV_duty = 0
        if running_status['BOGH'] == 1:
            BOGH_duty = BOGH_outputs['BOGH_Qc']
        else:
            BOGH_duty = 0
        FBOG_outputs['FBOG_total_duty'] = FV_duty + BOGH_duty

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # 'FBOG_total_steam' = FV_steam + BOGH_steam
        if running_status['FV'] == 1:
            FV_steam = FV_outputs['FV_steam_required']
        else:
            FV_steam = 0
        if running_status['BOGH'] == 1:
            BOGH_steam = BOGH_outputs['BOGH_steam_required']
        else:
            BOGH_steam = 0
        FBOG_outputs['FBOG_total_steam'] = FV_steam + BOGH_steam
        
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # 'HD_polytropic_efficiency' = HD1_polytropic_efficiency or HD2_polytropic_efficiency or avg(HD1_polytropic_efficiency,HD2_polytropic_efficiency)
        if running_status['HD1'] == 1 and running_status['HD2'] == 0:
            HD_outputs['HD_polytropic_efficiency'] = HD1_outputs['HD1_polytropic_efficiency']
        elif running_status['HD1'] == 0 and running_status['HD2'] == 1:
            HD_outputs['HD_polytropic_efficiency'] = HD2_outputs['HD2_polytropic_efficiency']
        elif running_status['HD1'] == 1 and running_status['HD2'] == 1:
            HD_outputs['HD_polytropic_efficiency'] = (HD1_outputs['HD1_polytropic_efficiency'] + HD2_outputs['HD2_polytropic_efficiency'])/2
        

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # 'NBOG_polytropic_efficiency' = avg(LD Stage1 and LD Stage2)
        # 'NBOG_polytropic_power' = avg(LD Stage1 and LD Stage2)

        if running_status['LD1'] == 1 and running_status['LD2'] == 0:
            NBOG_outputs['NBOG_polytropic_efficiency'] = (LD1_outputs['LD1_S1_polytropic_efficiency'] + LD1_outputs['LD1_S2_polytropic_efficiency'])/2
            NBOG_outputs['NBOG_polytropic_power'] = (LD1_outputs['LD1_S1_polytropic_power'] + LD1_outputs['LD1_S2_polytropic_power'])/2
        elif running_status['LD1'] == 0 and running_status['LD2'] == 1:
            NBOG_outputs['NBOG_polytropic_efficiency'] = (LD2_outputs['LD2_S1_polytropic_efficiency'] + LD2_outputs['LD2_S2_polytropic_efficiency'])/2
            NBOG_outputs['NBOG_polytropic_power'] = (LD2_outputs['LD2_S1_polytropic_power'] + LD2_outputs['LD2_S2_polytropic_power'])/2
        elif running_status['LD1'] == 1 and running_status['LD2'] == 1:
            NBOG_outputs['NBOG_polytropic_efficiency'] = (LD1_outputs['LD1_S1_polytropic_efficiency'] + LD1_outputs['LD1_S2_polytropic_efficiency'] + LD2_outputs['LD2_S1_polytropic_efficiency'] + LD2_outputs['LD2_S2_polytropic_efficiency'])/4
            NBOG_outputs['NBOG_polytropic_power'] = (LD1_outputs['LD1_S1_polytropic_power'] + LD1_outputs['LD1_S2_polytropic_power'] + LD2_outputs['LD2_S1_polytropic_power'] + LD2_outputs['LD2_S2_polytropic_power'])/4

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #calculate EMS outputs
        Fuel_Consumption_outputs = {}

        #FOC outputs
        Fuel_Consumption_outputs['FG_Consumption_ME'] = tags['ME1_FG_Flow_InstMass'] + tags['ME2_FG_Flow_InstMass']
        Fuel_Consumption_outputs['FG_Consumption_GE'] = tags['GE1_FG_Flow_InstMass'] + tags['GE2_FG_Flow_InstMass'] + tags['GE3_FG_Flow_InstMass'] + tags['GE4_FG_Flow_InstMass']
        Fuel_Consumption_outputs['FO_Consumption_Aux_Boiler'] = tags['Blr_AuxBlr_FO_Flow_InstMass']
        if tags_av_check['NS_GPS_019_PV'] == 1:
            Fuel_Consumption_outputs['Speed'] = tags['NS_GPS_019_PV']
        else:
            Fuel_Consumption_outputs['Speed'] = 9.9 #if speed tag above is not available in current simfile, write its value 0 to db. this tag is available after 07/09/2023.

        Fuel_Consumption_outputs['FG_Consumption_GCU'] = tags['FG_GCU1_Flow']
        Fuel_Consumption_outputs['FO_Consumption_ME'] = tags['ME1_FO_Flow_InstMass'] + tags['ME2_FO_Flow_InstMass']
        Fuel_Consumption_outputs['FO_Consumption_GE'] = tags['GE_FO_GE1GE2_Flow_InstMass'] + tags['GE_FO_GE3GE4_Flow_InstMass']
        Fuel_Consumption_outputs['Total_FG_Consumption'] = Fuel_Consumption_outputs['FG_Consumption_ME'] + Fuel_Consumption_outputs['FG_Consumption_GE'] + Fuel_Consumption_outputs['FG_Consumption_GCU']
        Fuel_Consumption_outputs['PF_Consumption_ME_FG'] = Fuel_Consumption_outputs['FG_Consumption_ME']*0.01
        Fuel_Consumption_outputs['PF_Consumption_ME_FO'] = Fuel_Consumption_outputs['FO_Consumption_ME']*0.005
        Fuel_Consumption_outputs['PF_Consumption_GE_FG'] = Fuel_Consumption_outputs['FG_Consumption_GE']*0.01
        Fuel_Consumption_outputs['PF_Consumption_GE_FO'] = Fuel_Consumption_outputs['FO_Consumption_GE']*0.005
        Fuel_Consumption_outputs['Total_FO_Consumption'] = Fuel_Consumption_outputs['FO_Consumption_ME'] + Fuel_Consumption_outputs['FO_Consumption_GE'] + Fuel_Consumption_outputs['FO_Consumption_Aux_Boiler'] + Fuel_Consumption_outputs['PF_Consumption_ME_FO'] + Fuel_Consumption_outputs['PF_Consumption_GE_FO']
        Fuel_Consumption_outputs['Total_Fuel_Consumption'] = Fuel_Consumption_outputs['Total_FG_Consumption'] + Fuel_Consumption_outputs['Total_FO_Consumption'] + Fuel_Consumption_outputs['PF_Consumption_ME_FG'] + Fuel_Consumption_outputs['PF_Consumption_GE_FG']        

        Fuel_Economy_outputs = {}
        if running_status['Fuel_Economy'] == 1: #calculate and log Fuel_Economy only if speed > 1 otherwise it comes as infinity. speed > 1 is already replicated in running status rule.
            if Fuel_Consumption_outputs['Speed'] == 0: #only in case of test run
                Fuel_Economy_outputs['Fuel_Economy'] = 0 
            else:
                Fuel_Economy_outputs['Fuel_Economy'] = Fuel_Consumption_outputs['Total_Fuel_Consumption']/Fuel_Consumption_outputs['Speed']
            # print(Fuel_Consumption_outputs['Total_Fuel_Consumption'])
            # print(Fuel_Consumption_outputs['Speed'])

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        dwsim_outputs = {}
        keys = ['FV_outputs', 'LNGV_outputs', 'BOGH_outputs', 'WUH_outputs', 'GWH_Stm_outputs', 'LD1_outputs', 'LD2_outputs', 'HD1_outputs', 'HD2_outputs', 'SC_outputs', 'Cargo_vapor_outputs', 
                'HD_outputs', 'NBOG_outputs', 'FBOG_outputs', 'Fuel_Consumption_outputs', 'Fuel_Economy_outputs',
                'ME1_outputs', 'ME2_outputs', 'GE1_outputs', 'GE2_outputs', 'GE3_outputs', 'GE4_outputs', 'NG1_outputs', 'NG2_outputs',
                'AB_AB1_outputs', 'AB_AB2_outputs'] # updated for AB simulation
        values = [FV_outputs, LNGV_outputs, BOGH_outputs, WUH_outputs, GWH_Stm_outputs, LD1_outputs, LD2_outputs, HD1_outputs, HD2_outputs, SC_outputs, Cargo_vapor_outputs, 
                  HD_outputs, NBOG_outputs, FBOG_outputs, Fuel_Consumption_outputs, Fuel_Economy_outputs,
                  ME1_outputs, ME2_outputs, GE1_outputs, GE2_outputs, GE3_outputs, GE4_outputs, NG1_outputs, NG2_outputs,
                  AB_AB1_outputs, AB_AB2_outputs] # updated for AB simulation
        for i in range(len(keys)):
            dwsim_outputs[keys[i]] = values[i] #nested dict format for convenient history logging of individual assets. example is below:
            # {'FV_outputs': {}, 'LNGV_outputs': {}, 'LD1_outputs': {'LD1_S1_in_specific_enthalpy': -50.06, 'LD1_S1_pressure_ratio': 3.86}}
        dwsim_outputs_to_append_to_tags =  FV_outputs|LNGV_outputs|BOGH_outputs|WUH_outputs|GWH_Stm_outputs|LD1_outputs|LD2_outputs|HD1_outputs|HD2_outputs|SC_outputs|Cargo_vapor_outputs|HD_outputs|NBOG_outputs|FBOG_outputs|Fuel_Consumption_outputs|Fuel_Economy_outputs|ME1_outputs|ME2_outputs|GE1_outputs|GE2_outputs|GE3_outputs|GE4_outputs|NG1_outputs|NG2_outputs|AB_AB1_outputs|AB_AB2_outputs # updated for AB simulation
        return dwsim_outputs, dwsim_outputs_to_append_to_tags

    def outputsLogging(self, dwsim_outputs, running_status, onboard_timestamp, tags_av_check):
        # key_outputs_FGSS = ['Cargo_vapor_total_duty', 'FBOG_total_duty', 'FBOG_total_steam', 'HD_polytropic_efficiency', 'NBOG_polytropic_efficiency', 'NBOG_polytropic_power']
        
        assets = ['FV', 'LNGV', 'BOGH', 'WUH', 'GWH_Stm', 'LD1', 'LD2', 'HD1', 'HD2', 'SC', 'Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy', 
                  'ME1', 'ME2', 'GE1', 'GE2', 'GE3', 'GE4', 'AB_AB1', 'AB_AB2'] # updated for AB simulation #mention those assets/items which have outputs to log. Because not all items have outputs to log
        if tags_av_check['NS_NG1-40101_PV'] == 1 and tags_av_check['NS_NG2-40101_PV'] == 1: #these will be available after 07/09/2023
            assets = assets + ['NG1', 'NG2']
        # print(running_status)
        # print(dwsim_outputs)
        # print("logging of outputs will start:")
        for asset in assets:
            # print(asset)
            if running_status[asset] == 1:
                table = asset + "_output_history"
                self.cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [table]) #updated for PostgreSQL
                row = self.cursor.fetchall()
                self.conn.commit()
                # print(row)
                # required_outputs = [item[0] for item in row][1:] #exclude timestamp_onboard #updated on 12042023 => in AB only, idk why it sorts the list, so timestamp_onboard becomes part of outputs to be logged
                required_outputs = [item[0] for item in row] #updated on 12042023
                required_outputs.remove('TimeStamp_onboard') #updated on 12042023
                #save realtime as well as the history for these outputs
                # print(required_outputs)
            #realtime
                asset = asset+"_outputs"
                for output_tag in required_outputs:
                    if 'Performance_health' not in output_tag: #excluding it for now, yet awaiting confirmation. later if needed it should be included
                        # print(asset)
                        # print(output_tag)
                        # print(dwsim_outputs)
                        if np.isnan(dwsim_outputs[asset][output_tag]): #while testing, LMTD may be float nan, so handling that error
                            # print(asset)
                            print(output_tag)
                            # print(dwsim_outputs[asset][output_tag])
                            # print(type(dwsim_outputs[asset][output_tag]))
                            print('this is nan, setting to temporary value 0')
                            dwsim_outputs[asset][output_tag] = 0.0
                            
                        self.cursor.execute('update public."Output_Tags" set "Value" = %s where "TagName" = %s', [float(dwsim_outputs[asset][output_tag]), output_tag]) #updated for PostgreSQL
                        self.conn.commit()
                # print("realtime logging of outputs done for", asset)
            #history
                # timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # query = f"'{timestamp_now}', '{onboard_timestamp}', " #replace second with timestamp_onboard here
                query = f"'{onboard_timestamp}', "
                for output_tag in required_outputs:
                    if 'Performance_health' not in output_tag: #excluding it for now, yet awaiting confirmation. later if needed it should be included
                        query = query + f"{dwsim_outputs[asset][output_tag]}, "
                if asset[:-8] in ['Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy', 'ME1', 'ME2', 'GE1', 'GE2', 'GE3', 'GE4', 'NG1', 'NG2', 'AB_AB1', 'AB_AB2']: # updated for AB simulation #health is not required for these, as these are just used for key outputs for dashbaord.
                    query = query[:-2]
                else:
                    query = query + f"{100}"
                query = f'insert into public."{table}" values({query})' #updated for PostgreSQL
                # print(query)
                self.cursor.execute(query)
                self.conn.commit()
                # print("history logging of outputs done for", asset)
            #in case required tags are needed from Output_Tags table
            # self.cursor.execute("select TagName from Output_Tags")
            # row = self.cursor.fetchall()
            # self.conn.commit()
            # required_outputs = [item[0] for item in row]
        


    def runningStatus(self, tags, tags_av_check):
        #FV
        running_status = {}
        if tags['FG_FV_DischFlow'] > 100:
            running_status['FV'] = 1
        else:
            running_status['FV'] = 0
        #LNGV
        # if tags['CM_LNGVapr_InTempInd'] < -30 and tags['CM_LNGVapr_InPrs'] > 40:
        if tags['CM_LNGVapr_Stop'] == 0 and tags['FG_Flow_VaprToAtm'] > 100:
            running_status['LNGV'] = 1
        else:
            running_status['LNGV'] = 0
        #BOGH
        if tags['FG_FV_DischFlow'] > 100:
            running_status['BOGH'] = 1
        else:
            running_status['BOGH'] = 0
        #WUH #may be we can use just HD run tag here
        if (tags['FG_FBOG_WuHtr_OutTempInd'] - tags['FG_FBOG_WuHtr_InTempInd'] > 10) and (tags['FG_FBOG_WuHtr_CondWtrTempInd'] - tags['FG_FBOG_WuHtr_OutTempInd'] > 0):
            running_status['WUH'] = 1
        else:
            running_status['WUH'] = 0
        #GWHS
        # if tags['CM_GwCircPp1_Run'] == 1 and tags['FG_GW_MainHtr_RtnTemp'] > 30:
        if (tags['FG_GW_MainHtr_OutTemp'] - tags['FG_GW_MainHtr_RtnTemp'] > 5) and tags['CM_GwCircPp1_Run'] == 1:
            running_status['GWH_Stm'] = 1
            # running_status['GWHS'] = 1
        else:
            running_status['GWH_Stm'] = 0
            # running_status['GWHS'] = 0
        #LD1
        # if tags['CM_LD1_Flow'] > 100 and tags['CM_LD1_Run'] == 1: #updated on 11292023
        if tags['CM_LD1_Flow'] > 100: #updated on 11292023
            running_status['LD1'] = 1
        else:
            running_status['LD1'] = 0
        #LD2
        # if tags['CM_LD2_Flow'] > 100 and tags['CM_LD2_Run'] == 1: #updated on 11292023
        if tags['CM_LD2_Flow'] > 100: #updated on 11292023
            running_status['LD2'] = 1
        else:
            running_status['LD2'] = 0
        #HD1
        if tags['CM_HD1_Run'] == 1 and (tags['CM_HD1_DischPrs']-tags['CM_HD1_InPrsAlrmCtrl'] > 30) and tags['CM_HD1_IGVPosCtrl'] > 5:
            running_status['HD1'] = 1
        else:
            running_status['HD1'] = 0
        #HD2
        if tags['CM_HD2_Run'] == 1 and (tags['CM_HD2_DischPrs']-tags['CM_HD2_InPrsAlrmCtrl'] > 30) and tags['CM_HD2_IGVPosCtrl'] > 5:
            running_status['HD2'] = 1
        else:
            running_status['HD2'] = 0
        #SC
        if tags['CM_LNGSubClr_CoolDownMode'] == 1 and tags['CM_LNGSubClr_Run'] == 1:
            running_status['SC'] = 1
        else:
            running_status['SC'] = 0

        #dont need the below
        #LPHD1
        # if tags['CM_HD1_AuxLoPpRun'] == 1:
        #     running_status['LPHD1'] = 1
        # else:
        #     running_status['LPHD1'] = 0
        # #LPHD2
        # if tags['CM_HD2_AuxLoPpRun'] == 1:
        #     running_status['LPHD2'] = 1
        # else:
        #     running_status['LPHD2'] = 0
        # #OHHD1
        # if tags['CM_HD1_OilHtrRun'] == 1:
        #     running_status['OHHD1'] = 1
        # else:
        #     running_status['OHHD1'] = 0
        # #OHHD2
        # if tags['CM_HD2_OilHtrRun'] == 1:
        #     running_status['OHHD2'] = 1
        # else:
        #     running_status['OHHD2'] = 0
        #GWHE
        if tags['CM_GwHtr1_Run'] == 1 or tags['CM_GwHtr2_Run'] == 1 or tags['CM_GwHtr3_Run'] == 1 or tags['CM_GwHtr4_Run'] == 1:
            running_status['GWH_Elec'] = 1
        else:
            running_status['GWH_Elec'] = 0
        #GP1
        if tags['CM_GwCircPp1_Run'] == 1:
            running_status['GWH_StmPP'] = 1
        else:
            running_status['GWH_StmPP'] = 0
        #GP2
        if tags['CM_GwCircPp2_Run'] == 1:
            running_status['GWH_ElecPP'] = 1
        else:
            running_status['GWH_ElecPP'] = 0

        # running status of below 4 is also required when logging key outputs
        # 'Cargo_vapor', 'HD', 'FBOG', 'NBOG'
        if running_status['LNGV'] == 1 or running_status['WUH'] == 1:
            running_status['Cargo_vapor'] = 1
        else:
            running_status['Cargo_vapor'] = 0
        
        if running_status['HD1'] == 1 or running_status['HD2'] == 1:
            running_status['HD'] = 1
        else:
            running_status['HD'] = 0
        
        if running_status['FV'] == 1 or running_status['BOGH'] == 1:
            running_status['FBOG'] = 1
        else:
            running_status['FBOG'] = 0
        
        if running_status['LD1'] == 1 or running_status['LD2'] == 1:
            running_status['NBOG'] = 1
        else:
            running_status['NBOG'] = 0

        running_status['Fuel_Consumption'] = 1 #fuel consumption related outputs are needed to be calculated and logged all the time, so its running status is 1 always.

        if tags_av_check['NS_GPS_019_PV'] == 1:
            if tags['NS_GPS_019_PV'] > 1:  #calculate and log fuel economy outputs only if speed is more than 1
                running_status['Fuel_Economy'] = 1
            else:
                running_status['Fuel_Economy'] = 0
        else:
            running_status['Fuel_Economy'] = 0
        
        if running_status['GWH_Stm'] == 1 or running_status['GWH_Elec'] == 1:
            running_status['GWH'] = 1
            running_status['GWH_ExpTank'] = 1
        else:
            running_status['GWH'] = 0
            running_status['GWH_ExpTank'] = 0

        #updated block on 12122023 from here
        if tags_av_check['NS_IG-00531_PV'] == 1:
            if tags['FG_IG_SystemRun'] == 1 and tags['NS_IG-00531_PV'] == 1:
                running_status['IG'] = 1
            else:
                running_status['IG'] = 0
        else:
            if tags['FG_IG_SystemRun'] == 1:
                running_status['IG'] = 1
            else:
                running_status['IG'] = 0

        #updated block on 12122023 till here

        if tags['Elec_NGen1_SystemRun'] == 1:
            running_status['NG1'] = 1
        else:
            running_status['NG1'] = 0
        if tags['Elec_NGen2_SystemRun'] == 1:
            running_status['NG2'] = 1
        else:
            running_status['NG2'] = 0
        # if tags['Elec_NGen1_SystemRun'] == 1 or tags['Elec_NGen2_SystemRun'] == 1: #updated on 11292023
        #     running_status['NG1_Tank'] = 1 #updated on 11292023
        # else:
        #     running_status['NG1_Tank'] = 0 #updated on 11292023
        # if tags['ME1_Misc_Run'] == 1 and tags['ME1_Misc_Load'] > 0: #updated on 11292023
        if tags['ME1_FG_Flow_InstMass'] > 100 or tags['ME1_FO_Flow_InstMass'] > 100: #updated on 11292023
            running_status['ME1'] = 1
        else:
            running_status['ME1'] = 0
        # if tags['ME2_Misc_Run'] == 1 and tags['ME2_Misc_Load'] > 0: #updated on 11292023
        if tags['ME2_FG_Flow_InstMass'] > 100 or tags['ME2_FO_Flow_InstMass'] > 100: #updated on 11292023
            running_status['ME2'] = 1
        else:
            running_status['ME2'] = 0
        if running_status['ME1'] == 1:
            running_status['MEEG_ECO1'] = 1
        else:
            running_status['MEEG_ECO1'] = 0
        if running_status['ME2'] == 1:
            running_status['MEEG_ECO2'] = 1
        else:
            running_status['MEEG_ECO2'] = 0
        if tags['GE1_Misc_Run'] == 1:
            running_status['GE1'] = 1
        else:
            running_status['GE1'] = 0
        if tags['GE2_Misc_Run'] == 1:
            running_status['GE2'] = 1
        else:
            running_status['GE2'] = 0
        if tags['GE3_Misc_Run'] == 1:
            running_status['GE3'] = 1
        else:
            running_status['GE3'] = 0
        if tags['GE4_Misc_Run'] == 1:
            running_status['GE4'] = 1
        else:
            running_status['GE4'] = 0
        if running_status['GE1'] == 1 or running_status['GE2'] == 1:
            running_status['GEEG_ECO1'] = 1
        else:
            running_status['GEEG_ECO1'] = 0
        if running_status['GE3'] == 1 or running_status['GE4'] == 1:
            running_status['GEEG_ECO4'] = 1
        else:
            running_status['GEEG_ECO4'] = 0
        if running_status['ME1'] == 1 or running_status['ME2'] == 1:
            running_status['MEEG'] = 1
        else:
            running_status['MEEG'] = 0
        if running_status['GE1'] == 1 or running_status['GE2'] == 1 or running_status['GE3'] == 1 or running_status['GE4'] == 1:
            running_status['GEEG'] = 1
        else:
            running_status['GEEG'] = 0
        
        #@@@@@@@@@@@@@
        # FW_Gen1 tags['NS_MM002-XI_PV'] == 1
        # FW_Gen2 tags['NS_MM602-XI_PV'] == 1
        # FW_VFD_hydro_unit tags['NS_MM933-XI_PV'] == 1
        # FW_Hot_water_pp tags['NS_MM908-03XI_PV'] == 1
        # FW_ME1bearings running_status['ME1'] == 1:
        # FW_ME2bearings running_status['ME2'] == 1
        # FW_Ref tags['NS_MM066-XI_PV'] == 1 or tags['NS_MM666-XI_PV'] == 1
        # FW_CFW_PP1 NS_CF013-03MC_PV
        # FW_CFW_PP2 NS_CF014-03MC_PV

        #@@@@@@@@@@@@@@@
        # print("test**************")
        # print(tags['Blr_AuxBlr1_StmPrs'])
        # print(tags_av_check['NS_MM048-XI_PV'])
        # print(tags['NS_MM048-XI_PV'])
        # print("test**************")

        if tags_av_check['NS_MM048-XI_PV'] == 1 and tags_av_check['NS_MM648-XI_PV'] == 1:
            if tags['NS_MM048-XI_PV'] == 1:
                running_status['AB_AB1'] = 1
            else:
                running_status['AB_AB1'] = 0
            if tags['NS_MM648-XI_PV'] == 1:
                running_status['AB_AB2'] = 1
            else:
                running_status['AB_AB2'] = 0
        else:
            # if tags['Blr_AuxBlr1_StmPrs'] > 0.3: #updated on 11292023
            if tags['Blr_AuxBlr1_Run'] == 1 and tags['Blr_AuxBlr_FO_Flow_InstMass'] > 5: #updated on 11292023
                running_status['AB_AB1'] = 1
            else:
                running_status['AB_AB1'] = 0
            # if tags['Blr_AuxBlr2_StmPrs'] > 0.3: #updated on 11292023
            if tags['Blr_AuxBlr2_Run'] == 1 and tags['Blr_AuxBlr_FO_Flow_InstMass'] > 5: #updated on 11292023
                running_status['AB_AB2'] = 1
            else:
                running_status['AB_AB2'] = 0

        if running_status['AB_AB1'] == 1 or running_status['AB_AB2'] == 1:
            running_status['AB'] = 1
            # running_status['AB_Main'] = 1 # updated on 11282023
        else:
            running_status['AB'] = 0
            # running_status['AB_Main'] = 0 # updated on 11282023
        
        if tags_av_check['NS_MM018-XI_PV'] == 1 and tags_av_check['NS_MM618-XI_PV'] == 1:
            if tags['NS_MM018-XI_PV'] == 1:
                running_status['LO_PuriME1'] = 1
            else:
                running_status['LO_PuriME1'] = 0
            if tags['NS_MM618-XI_PV'] == 1:
                running_status['LO_PuriME2'] = 1
            else:
                running_status['LO_PuriME2'] = 0
        else:
            if tags['ME1_LO_Puri1_InTemp'] > 78:
                running_status['LO_PuriME1'] = 1
            else:
                running_status['LO_PuriME1'] = 0
            if tags['ME2_LO_Puri1_InTemp'] > 78:
                running_status['LO_PuriME2'] = 1
            else:
                running_status['LO_PuriME2'] = 0
        
        if tags_av_check['NS_MM023-XI_PV'] == 1 and tags_av_check['NS_MM021-XI_PV'] == 1 and tags_av_check['NS_MM623-XI_PV'] == 1 and tags_av_check['NS_MM621-XI_PV'] == 1:
            if tags['NS_MM021-XI_PV'] == 1: #puriGE1/2/3/4 rules updated on 12062023
                running_status['LO_PuriGE1'] = 1
            else:
                running_status['LO_PuriGE1'] = 0
            if tags['NS_MM023-XI_PV'] == 1:
                running_status['LO_PuriGE2'] = 1
            else:
                running_status['LO_PuriGE2'] = 0
            if tags['NS_MM621-XI_PV'] == 1:
                running_status['LO_PuriGE3'] = 1
            else:
                running_status['LO_PuriGE3'] = 0
            if tags['NS_MM623-XI_PV'] == 1:
                running_status['LO_PuriGE4'] = 1
            else:
                running_status['LO_PuriGE4'] = 0
        else:
            if tags['GE_LO_GE1GE2_Puri_InTemp'] > 83 or tags['GE_LO_GE1GE2_Puri2_InTemp'] > 83:
                running_status['LO_PuriGE1'] = 1
                running_status['LO_PuriGE2'] = 1
            else:
                running_status['LO_PuriGE1'] = 0
                running_status['LO_PuriGE2'] = 0
            if tags['GE_LO_GE3GE4_Puri_InTemp'] > 83 or tags['GE_LO_GE3GE4_Puri2_InTemp'] > 83:
                running_status['LO_PuriGE3'] = 1
                running_status['LO_PuriGE4'] = 1
            else:
                running_status['LO_PuriGE3'] = 0
                running_status['LO_PuriGE4'] = 0
        # print("tags av check test=>", tags_av_check['NS_PP004-03MI_PV'])
        if tags_av_check['NS_PP004-03MI_PV'] == 1 and tags_av_check['NS_PP043-03MI_PV'] == 1 and tags_av_check['NS_PP009-03MI_PV'] == 1 and tags_av_check['NS_PP044-03MI_PV'] == 1:
            if tags['NS_PP004-03MI_PV'] == 1 or tags['NS_PP043-03MI_PV'] == 1:
                running_status['LO_StrnTube1'] = 1
            else:
                running_status['LO_StrnTube1'] = 0
            if tags['NS_PP009-03MI_PV'] == 1 or tags['NS_PP044-03MI_PV'] == 1:
                running_status['LO_StrnTube2'] = 1
            else:
                running_status['LO_StrnTube2'] = 0
        else:
            if running_status['ME1'] == 1 or running_status['ME2'] == 1:
                running_status['LO_StrnTube1'] = 1
                running_status['LO_StrnTube2'] = 1
            else:
                running_status['LO_StrnTube1'] = 0
                running_status['LO_StrnTube2'] = 0

        running_status['VA'] = 1

        if tags_av_check['NS_PP036-03XI_PV'] == 1 and tags_av_check['NS_PP037-03AXI_PV'] == 1 and tags_av_check['NS_PP038-03AXI_PV'] == 1 and tags_av_check['NS_PP038-03XC_PV'] == 1:
            if tags['NS_PP036-03XI_PV'] == 1:
                running_status['BLST_PP1'] = 1
            else:
                running_status['BLST_PP1'] = 0
            if tags['NS_PP037-03AXI_PV'] == 1:
                running_status['BLST_PP2'] = 1
            else:
                running_status['BLST_PP2'] = 0
            if tags['NS_PP038-03AXI_PV'] == 1 or tags['NS_PP038-03XC_PV'] == 1:
                running_status['BLST_PP3'] = 1
            else:
                running_status['BLST_PP3'] = 0

        else:
            running_status['BLST_PP1'] = 1
            running_status['BLST_PP2'] = 1
            running_status['BLST_PP3'] = 1

        running_status['BLST'] = 1
        running_status['BLG'] = 1
        running_status['CT1'] = 1
        running_status['CT2'] = 1
        running_status['CT3'] = 1
        running_status['CT4'] = 1

        if running_status['ME1'] == 1:
            running_status['FW_ME1SAC'] = 1
        else:
            running_status['FW_ME1SAC'] = 0
        if running_status['ME2'] == 1:
            running_status['FW_ME2SAC'] = 1
        else:
            running_status['FW_ME2SAC'] = 0
        if running_status['GE1'] == 1:
            running_status['FW_GE1SAC'] = 1
        else:
            running_status['FW_GE1SAC'] = 0
        if running_status['GE2'] == 1:
            running_status['FW_GE2SAC'] = 1
        else:
            running_status['FW_GE2SAC'] = 0
        if running_status['GE3'] == 1:
            running_status['FW_GE3SAC'] = 1
        else:
            running_status['FW_GE3SAC'] = 0
        if running_status['GE4'] == 1:
            running_status['FW_GE4SAC'] = 1
        else:
            running_status['FW_GE4SAC'] = 0

        if tags_av_check['NS_PP040-03MI_PV'] == 1 and tags_av_check['NS_PP045-03MI_PV'] == 1 and tags_av_check['NS_PP046-03MI_PV'] == 1:
            if tags['NS_PP040-03MI_PV'] == 1:
                running_status['FW_GEwtrCircPP1'] = 1
            else:
                running_status['FW_GEwtrCircPP1'] = 0
            if tags['NS_PP045-03MI_PV'] == 1:
                running_status['FW_GEwtrCircPP2'] = 1
            else:
                running_status['FW_GEwtrCircPP2'] = 0
            if tags['NS_PP046-03MI_PV'] == 1:
                running_status['FW_GEwtrCircPP3'] = 1
            else:
                running_status['FW_GEwtrCircPP3'] = 0
        else:
            if running_status['GE1'] == 1 or running_status['GE2'] == 1 or running_status['GE3'] == 1 or running_status['GE4'] == 1:
                running_status['FW_GEwtrCircPP1'] = 1
                running_status['FW_GEwtrCircPP2'] = 1
                running_status['FW_GEwtrCircPP3'] = 1
            else:
                running_status['FW_GEwtrCircPP1'] = 0
                running_status['FW_GEwtrCircPP2'] = 0
                running_status['FW_GEwtrCircPP3'] = 0

        if tags['Mach_CfwPp1_Run'] == 1:
            running_status['FW_CentralPP1'] = 1
        else:
            running_status['FW_CentralPP1'] = 0
        if tags['Mach_CfwPp2_Run'] == 1:
            running_status['FW_CentralPP2'] = 1
        else:
            running_status['FW_CentralPP2'] = 0
        if tags['Mach_CfwPp3_Run'] == 1:
            running_status['FW_CentralPP3'] = 1
        else:
            running_status['FW_CentralPP3'] = 0
        # if tags['NS_PP061-03MI_PV'] == 1:
        #     running_status['FW_BoosterPP'] = 1
        # else:
        #     running_status['FW_BoosterPP'] = 0
        # if tags['NS_PP030-03MI_PV'] == 1:
        #     running_status['FW_ME1CFWPP1'] = 1
        # else:
        #     running_status['FW_ME1CFWPP1'] = 0
        # if tags['NS_PP058-03MI_PV'] == 1:
        #     running_status['FW_ME1CFWPP2'] = 1
        # else:
        #     running_status['FW_ME1CFWPP2'] = 0
        # if tags['NS_PP033-03MI_PV'] == 1:
        #     running_status['FW_ME2CFWPP1'] = 1
        # else:
        #     running_status['FW_ME2CFWPP1'] = 0
        # if tags['NS_PP059-03MI_PV'] == 1:
        #     running_status['FW_ME2CFWPP2'] = 1
        # else:
        #     running_status['FW_ME2CFWPP2'] = 0

        running_status['FW_BoosterPP'] = 1

        if running_status['ME1'] == 1:
            running_status['FW_ME1CFWPP1'] = 1
            running_status['FW_ME1CFWPP2'] = 1
        else:
            running_status['FW_ME1CFWPP1'] = 0
            running_status['FW_ME1CFWPP2'] = 0

        if running_status['ME2'] == 1:
            running_status['FW_ME2CFWPP1'] = 1
            running_status['FW_ME2CFWPP2'] = 1
        else:
            running_status['FW_ME2CFWPP1'] = 0
            running_status['FW_ME2CFWPP2'] = 0

        if tags['Mach_CswPp1_Run'] == 1:
            running_status['FW_CSWPP1'] = 1
        else:
            running_status['FW_CSWPP1'] = 0
        if tags['Mach_CswPp2_Run'] == 1:
            running_status['FW_CSWPP2'] = 1
        else:
            running_status['FW_CSWPP2'] = 0
        if tags['Mach_CswPp3_Run'] == 1:
            running_status['FW_CSWPP3'] = 1
        else:
            running_status['FW_CSWPP3'] = 0
        #FO and FG
        #@@@@@@@@@@@@@@@@@@@@@@@@ #updated on 11292023 from here
        # if running_status['LD1'] == 1 or running_status['LD2'] == 1: #updated on 11292023
        #     running_status['FG'] = 1 #updated on 11292023
        # else: 
        #     running_status['FG'] = 0 #updated on 11292023
        
        if tags['ME1_FO_Flow_InstMass'] > 30 or tags['ME2_FO_Flow_InstMass'] > 30 or tags['GE_FO_GE1GE2_Flow_InstMass'] > 30 or tags['GE_FO_GE3GE4_Flow_InstMass'] > 30 or tags['Blr_AuxBlr_FO_Flow_InstMass'] > 10:
            running_status['FO'] = 1
        else:
            running_status['FO'] = 0

        if (tags['Mach_HFOPuri1_Run'] == 1 and tags['Mach_HFOPuri1_InTemp'] > 50) or (tags['Mach_HFOPuri2_Run'] == 1 and tags['Mach_HFOPuri2_InTemp'] > 50):
            running_status['FO_Puri'] = 1
        else:
            running_status['FO_Puri'] = 0
        
        if tags_av_check['NS_MM944-XI_PV'] == 1:
            if tags['NS_MM944-XI_PV'] == 1:
                running_status['INCIN'] = 1
            else:
                running_status['INCIN'] = 0
        else:
            running_status['INCIN'] = 0

        #MEFG_ME1
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['ME1'] == 1:
            running_status['MEFG_ME1'] = 1
        else:
            running_status['MEFG_ME1'] = 0

        #MEFG_ME2
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['ME2'] == 1:
            running_status['MEFG_ME2'] = 1
        else:
            running_status['MEFG_ME2'] = 0

        if running_status['MEFG_ME1'] == 1 or running_status['MEFG_ME2'] == 1:
            running_status['MEFG'] = 1
        else:
            running_status['MEFG'] = 0
        
        #MEFG_GE1
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['GE1'] == 1:
            running_status['GEFG_GE1'] = 1
        else:
            running_status['GEFG_GE1'] = 0
        
        #MEFG_GE2
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['GE2'] == 1:
            running_status['GEFG_GE2'] = 1
        else:
            running_status['GEFG_GE2'] = 0

        #MEFG_GE3
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['GE3'] == 1:
            running_status['GEFG_GE3'] = 1
        else:
            running_status['GEFG_GE3'] = 0

        #MEFG_GE4
        if (running_status['LD1'] == 1 or running_status['LD2'] == 1) and running_status['GE4'] == 1:
            running_status['GEFG_GE4'] = 1
        else:
            running_status['GEFG_GE4'] = 0
        
        if tags_av_check['NS_MF001-03MI_PV'] == 1:
            if tags['NS_MF001-03MI_PV'] == 1:
                running_status['GEFG_Fan1'] = 1
            else:
                running_status['GEFG_Fan1'] = 0
        else:
            running_status['GEFG_Fan1'] = 0

        if tags_av_check['NS_MF010-03MI_PV'] == 1:
            if tags['NS_MF010-03MI_PV'] == 1:
                running_status['GEFG_Fan2'] = 1
            else:
                running_status['GEFG_Fan2'] = 0
        else:
            running_status['GEFG_Fan2'] = 0
        
        if running_status['GEFG_GE1'] == 1 or running_status['GEFG_GE2'] or running_status['GEFG_GE3'] or running_status['GEFG_GE4']:
            running_status['GEFG'] = 1
        else:
            running_status['GEFG'] = 0
        
        if tags['FG_GCU1_Run'] == 1:
            running_status['GCU'] = 1
        else:
            running_status['GCU'] = 0
        
        #@@@@@@@@@@@@@@@@@@@@@@@@@ #updated on 11292023 till here
        #to check later. it seems in mimic the running tags are available.
        if running_status['GE1'] == 1:
            running_status['GEEG_SCR1'] = 1
        else:
            running_status['GEEG_SCR1'] = 0

        if running_status['GE2'] == 1:
            running_status['GEEG_SCR2'] = 1
        else:
            running_status['GEEG_SCR2'] = 0

        if running_status['GE3'] == 1:
            running_status['GEEG_SCR3'] = 1
        else:
            running_status['GEEG_SCR3'] = 0

        if running_status['GE4'] == 1:
            running_status['GEEG_SCR4'] = 1
        else:
            running_status['GEEG_SCR4'] = 0
        
        # running_status['CT1_Main'] = 1 # updated on 11282023
        # running_status['CT2_Main'] = 1 # updated on 11282023
        # running_status['CT3_Main'] = 1 # updated on 11282023
        # running_status['CT4_Main'] = 1 # updated on 11282023

        # kpi_assets = ['FV', 'LNGV', 'BOGH', 'WUH', 'GWH_Stm', 'LD1', 'LD2', 'HD1', 'HD2', 'SC', 'Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy', 
        #           'ME1', 'ME2', 'GE1', 'GE2', 'GE3', 'GE4', 'NG1', 'NG2']
        # kpi_assets = ['Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy']
        # for key in running_status.keys():
        #     # if key not in kpi_assets:
        #     running_status[key] = 1  #just for testing, but keeping kpi assets as they are originally to avoid simulation errors


        #updated on 12192023 from here
        if tags_av_check['NS_MM002-XI_PV'] == 1:
            if tags['NS_MM002-XI_PV'] == 1:
                running_status['FW_Gen1'] = 1
            else:
                running_status['FW_Gen1'] = 0
        else:
            running_status['FW_Gen1'] = 1

        if tags_av_check['NS_MM602-XI_PV'] == 1:
            if tags['NS_MM602-XI_PV'] == 1:
                running_status['FW_Gen2'] = 1
            else:
                running_status['FW_Gen2'] = 0
        else:
            running_status['FW_Gen2'] = 1

        if tags_av_check['NS_MM933-XI_PV'] == 1:
            if tags['NS_MM933-XI_PV'] == 1:
                running_status['FW_VFD_hydro_unit'] = 1
            else:
                running_status['FW_VFD_hydro_unit'] = 0
        else:
            running_status['FW_VFD_hydro_unit'] = 1

        if tags_av_check['NS_MM908-03XI_PV'] == 1:
            if tags['NS_MM908-03XI_PV'] == 1:
                running_status['FW_Hot_water_pp'] = 1
            else:
                running_status['FW_Hot_water_pp'] = 0
        else:
            running_status['FW_Hot_water_pp'] = 1

        if tags_av_check['NS_MM066-XI_PV'] == 1 and tags_av_check['NS_MM666-XI_PV'] == 1:
            if tags['NS_MM066-XI_PV'] == 1 and tags['NS_MM666-XI_PV'] == 1:
                running_status['FW_Ref'] = 1
            else:
                running_status['FW_Ref'] = 0
        else:
            running_status['FW_Ref'] = 1
        #*****

        if tags_av_check['NS_CF013-03MC_PV'] == 1:
            if tags['NS_CF013-03MC_PV'] == 1:
                running_status['FW_CFW_PP1'] = 1
            else:
                running_status['FW_CFW_PP1'] = 0
        else:
            running_status['FW_CFW_PP1'] = 1

        if tags_av_check['NS_CF014-03MC_PV'] == 1:
            if tags['NS_CF014-03MC_PV'] == 1:
                running_status['FW_CFW_PP2'] = 1
            else:
                running_status['FW_CFW_PP2'] = 0
        else:
            running_status['FW_CFW_PP2'] = 1
        #updated on 12192023 till here
        if running_status['ME1'] == 1:
            running_status['FW_ME1bearings'] = 1
        else:
            running_status['FW_ME1bearings'] = 0

        if running_status['ME2'] == 1:
            running_status['FW_ME2bearings'] = 1
        else:
            running_status['FW_ME2bearings'] = 0

        if running_status['LO_PuriME1'] == 1 or running_status['LO_PuriME2'] == 1 or running_status['LO_PuriGE1'] == 1 or running_status['LO_PuriGE2'] == 1 or running_status['LO_PuriGE3'] == 1 or running_status['LO_PuriGE4'] == 1 or running_status['LO_StrnTube1'] == 1 or running_status['LO_StrnTube2'] == 1:
            running_status['LO'] = 1
        else:
            running_status['LO'] = 0

        running_status['FW'] = 0
        
        fw_components = []
        for key in running_status.keys():
            if key[:3] == 'FW_':
                fw_components.append(key)
        
        for item in fw_components:
            if running_status[item] == 1:
                running_status['FW'] = 1
                break

        # print(fw_components)
        # print(running_status['FW'])
        if self.test_run == 1: #updated on 12062023
            for key in running_status.keys():
                running_status[key] = 1  #testing
        return running_status


##-------------------------------------------------------------------------------------------------------
    def cloudDataLogging(self):
        
        self.cursor.execute('''select "Value" from public."Application_status" where "Item" = 'Input_file';''') #updated for PostgreSQL
        row = self.cursor.fetchall()
        self.conn.commit()
        flag = row[0][0]
        # print(flag)
        folder = flag[-19:-11]
        # print(folder)
        # base = 'C:\\Users\\okfar\\OneDrive\\Miscellaneous work\\SHI LNG\\fleet\\study for updates about sim file timestamp\\S-Project1 py\\latest\\9929106'
        # base = 'C:\\Users\\SHI\\Documents\\S-Project\\S-Project1 py\\latest\\9929106' #for FAT sample sim files
        # base = 'D:\\SimData\\9929106'
        # base = 'C:\\Users\\iu\\Documents\\Optics Analytics Projects\\S-Project1 py\\latest\\9929106'
        # base = 'C:\\Users\\iu\\Documents\\simfiles'
        # base = 'C:\\Users\\iu\\Downloads\\9929106\\9929106\\' #my notebook 02/01/2014 ~ 02/14/2014

        # path = base + '\\' +folder
        path = self.simfiles_path + '/' +folder
        sim_files = natsorted(os.listdir(path))
        
        # print(len(sim_files))

        for i in range(len(sim_files)):

            if sim_files[i] == flag:
                print("previously flagged file is:", flag)
                if i == (len(sim_files) - 1): #it means its last file

                    print('no more file available')

                #above line means the flag is the last item
                #it means no file is available up next
                #now we need to find if next day folder is available or not
                #first find next day folder name
                    
                    folders = natsorted(os.listdir(self.simfiles_path))
                    for j in range(len(folders)):
                        if folders[j] == folder:
                            if j == (len(folders) - 1):
                                print("no more folder is available")
                                application_status = 'Holding'
                                print("switch to:", application_status)
                            else:
                                folder = folders[j+1]
                                print('next day folder is:', folder)
                                path = self.simfiles_path + '/' +folder
                                sim_files = natsorted(os.listdir(path))
                                if len(sim_files) == 0:
                                    print("new folder is empty")
                                    application_status = 'Holding'
                                    print("switch to:", application_status)
                                else:
                                    flag = sim_files[0]
                                    print("sim file in next day folder:", flag)
                                    print("next file to read is:", flag)
                                    # location = len(sim_files) - i
                                    #if location is more than 2, it means more than 1 files are available next --
                                    #it means we are behind, so we need to speed up in playback mode
                                    if len(sim_files) > 1:
                                        application_status = 'Playback'
                                    # print(location)
                                        print("switch to :", application_status)
                                    else:
                                        application_status = 'Normal'
                                        print("switch to:", application_status)

                                    break
                                #replace the flag now with first file in new folder

                else:
                    flag = sim_files[i+1] #replace the flag now with next file in same folder
                    print("next file to read is:", flag)
                    location = len(sim_files) - i
                    #if location is more than 2, it means more than 1 files are available next --
                    #it means we are behing, so we need to speed up in playback mode
                    if location > 2:
                        application_status = 'Playback'
                    # print(location)
                        print("switch to :", application_status)
                    else:
                        application_status = 'Normal'
                    break
        
        if application_status == 'Normal':
            frequency = 60
        elif application_status == 'Playback':
            frequency = 0.01
        elif application_status == 'Holding':
            frequency = 5
        else:
            frequency = 5


        self.cursor.execute(f'''update public."Application_status" set "Value" = %s where "Item" = 'Input_file';''', [flag]) #updated for PostgreSQL
        self.conn.commit()
        self.cursor.execute('''update public."Application_status" set "Value" = %s where "Item" = 'Status';''', [application_status]) #updated for PostgreSQL
        self.conn.commit()    
        self.cursor.execute('''update public."Application_status" set "Value" = %s where "Item" = 'Frequency';''', [str(frequency)]) #updated for PostgreSQL
        self.conn.commit()


        if application_status == 'Normal' or application_status == 'Playback':
            print('proceeding with status:', application_status)
            sim_file = self.simfiles_path+ '/' +folder+ '/' +flag
            with open(sim_file) as f:
                lines = f.readlines()
            print("len of lines:", len(lines))

            if len(lines) == 2:
                names_str = lines[0]
                sample1_str = lines[1]


                names = names_str.split(',')
                sample1 = sample1_str.split(',')


                list_str = ['names', 'sample1']
                list = [names, sample1]
                # r i in range(len(list)):
                # print("len of ", list_str[i], "is: ", len(list[i]))
                if len(names) == len(sample1):
                    dict = {}
                    for i in range(len(names)):
                        dict[names[i]] = [sample1[i]]
                else:
                    print("tags and samples size not same")

            elif len(lines) == 3:
                names_str = lines[0]
                sample1_str = lines[1]
                sample2_str = lines[2]
                
                names = names_str.split(',')
                sample1 = sample1_str.split(',')
                sample2 = sample2_str.split(',')
                
                list_str = ['names', 'sample1', 'sample2']
                list = [names, sample1, sample2]    
                    # r i in range(len(list)):
                # print("len of ", list_str[i], "is: ", len(list[i]))
                if len(names) == len(sample1) == len(sample2):
                    dict = {}
                    for i in range(len(names)):
                        dict[names[i]] = [sample1[i], sample2[i]]
                else:
                    print("tags and samples size not same")

            elif len(lines) == 4:
                names_str = lines[0]
                sample1_str = lines[1]
                sample2_str = lines[2]
                sample3_str = lines[3]
              
                names = names_str.split(',')
                sample1 = sample1_str.split(',')
                sample2 = sample2_str.split(',')
                sample3 = sample3_str.split(',')
                
                list_str = ['names', 'sample1', 'sample2', 'sample3']
                list = [names, sample1, sample2, sample3]    
                    # r i in range(len(list)):
                # print("len of ", list_str[i], "is: ", len(list[i]))
                if len(names) == len(sample1) == len(sample2) == len(sample3):
                    dict = {}
                    for i in range(len(names)):
                        dict[names[i]] = [sample1[i], sample2[i], sample3[i]]
                else:
                    print("tags and samples size not same")

            elif len(lines) == 5:
                names_str = lines[0]
                sample1_str = lines[1]
                sample2_str = lines[2]
                sample3_str = lines[3]
                sample4_str = lines[4]
                
                names = names_str.split(',')
                sample1 = sample1_str.split(',')
                sample2 = sample2_str.split(',')
                sample3 = sample3_str.split(',')
                sample4 = sample4_str.split(',')
                
                list_str = ['names', 'sample1', 'sample2', 'sample3', 'sample4']
                list = [names, sample1, sample2, sample3, sample4]    
                    # r i in range(len(list)):
                # print("len of ", list_str[i], "is: ", len(list[i]))
                if len(names) == len(sample1) == len(sample2) == len(sample3) == len(sample4):
                    dict = {}
                    for i in range(len(names)):
                        dict[names[i]] = [sample1[i], sample2[i], sample3[i], sample4[i]]
                else:
                    print("tags and samples size not same")

            elif len(lines) == 6:
                names_str = lines[0]
                sample1_str = lines[1]
                sample2_str = lines[2]
                sample3_str = lines[3]
                sample4_str = lines[4]
                sample5_str = lines[5]
                names = names_str.split(',')
                sample1 = sample1_str.split(',')
                sample2 = sample2_str.split(',')
                sample3 = sample3_str.split(',')
                sample4 = sample4_str.split(',')
                sample5 = sample5_str.split(',')
                list_str = ['names', 'sample1', 'sample2', 'sample3', 'sample4', 'sample5']
                list = [names, sample1, sample2, sample3, sample4, sample5]    
                    # r i in range(len(list)):
                # print("len of ", list_str[i], "is: ", len(list[i]))
                if len(names) == len(sample1) == len(sample2) == len(sample3) == len(sample4) == len(sample5):
                    dict = {}
                    for i in range(len(names)):
                        dict[names[i]] = [sample1[i], sample2[i], sample3[i], sample4[i], sample5[i]]

                else:
                    print("tags and samples size not same") #if tags and sample size is not same, what are the items to return? and what would be the mode? double check it once
            

            no_of_samples = len(lines)-1
            
            return dict, no_of_samples, application_status, frequency
        
        else:
            dict = {}
            no_of_samples = 0
            return dict, no_of_samples, application_status, frequency

            #until now, we have got samples in a dict, no. of samples (len(lines)), execution mode and frequency
            #now its time to exit this function by returning all 4 items mentioned above
#///////////////////////////////////////////////////////////////////////////////////////////
    
    def inputsLogging(self, i, required_tags, tags, tags_presence):
        #@@@@@@@@@@@@ updated on 11292023 from here.
        onboard_timestamp = tags['Nav_GPS1_UTC'] #events duration should be counted using this onboard timestamp to nullify the effect of irregular inputs
        self.cursor.execute('''update public."Application_status" set "Value" = %s where "Item" = 'TimeStamp_onboard';''', [onboard_timestamp]) #updated for PostgreSQL
        self.conn.commit()
        current_timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.log_inputs_realtime == 1: #no need to updated on every loop if Bistelligence doesn't need it
            for tag in required_tags:
                if tag == 'Nav_GPS1_UTC':  
                    self.cursor.execute('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s', [onboard_timestamp, tag]) #updated for PostgreSQL
                    self.conn.commit()
                else:
                    if tags_presence[tag] == 1:
                        value = str(tags[tag])
                        realtime_logging = True
                        if len(value) == 0:
                            value = 999
                            realtime_logging = False
                        # print(dict[tag])
                        # print(tag, " => ", value)
                        # now = datetime.now()
                        # current_timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
                        # if realtime_logging:
                        # self.cursor.execute("update input_tags_test set Value = (?) where TagName = (?)", float(value), tag)
                        self.cursor.execute('update public."Input_Tags" set "Value" = %s where "Standard_Key" = %s', [float(value), tag]) #updated for PostgreSQL
                        self.conn.commit()
                        self.cursor.execute('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s', [current_timestamp_str, tag]) #updated for PostgreSQL
                        self.conn.commit()
         #@@@@@@@@@@@@ updated on 11292023 till here.
        print("value no. ", i, " is done. TimeStamp is :", tags['Nav_GPS1_UTC'])
        #logging input history
        if self.log_inputs_history == 1:
            tables = ['Input_history1', 'Input_history2','Input_history3','Input_history4','Input_history5','Input_history6']
            tags_without_hyphen = {}
            for key in tags.keys():
                value = tags[key]
                # if len(value) == 0:
                #     value = 99
                key = key.replace("-", "_")
                tags_without_hyphen[key] = value
            # print(tags_without_hyphen)
            for table in tables:
                self.cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [table]) #updated for PostgreSQL
                row = self.cursor.fetchall()
                self.conn.commit()
                # required_columns = [item[0] for item in row][2:] #updated on 12042023
                required_columns = [item[0] for item in row] #updated on 12042023
                required_columns.remove('Nav_GPS1_UTC') #updated on 12042023
                required_columns.remove('TimeStamp') #updated on 12042023
                # print(required_columns)
                # len(required_columns)
                query = f'''insert into public."{table}" values('{current_timestamp_str}', '{onboard_timestamp}',''' #updated for PostgreSQL
                for col in required_columns:
                    query = query + f"{tags_without_hyphen[col]}, "
                query = query[:-2] + ")"
                # print(query)
                self.cursor.execute(query)
                self.conn.commit() 
        return onboard_timestamp
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#functions for condition/rules templates
    def findConditionsStatus(self, condition_list, scenario_problem):
        sdev_only = False
        mavg_only = False
        delta_only = False
        mavg_and_delta = False #trend counter
        subtract_only = False
        sum_only = False
        sample_size = 0 
        delta_sample_size = 0
        condition_exists = True
        if len(condition_list) == 2:
            if 'standard deviation' in condition_list[0]:
                sdev_only = True #need only the points sample
                sample_size = int(condition_list[1])
            elif 'moving average' in condition_list[0]:
                mavg_only = True #need only the points sample
                sample_size = int(condition_list[1])
            elif 'delta' in condition_list[0]:
                delta_only = True #need only the points sample
                sample_size = int(condition_list[1])
            elif 'subtract' in condition_list[0]:
                subtract_only = True
            elif 'sum' in condition_list[0]:
                sum_only = True
            else:
                condition_exists = False
        elif len(condition_list) > 2 and ('subtract' in condition_list[0] or 'sum' in condition_list[0]):
            if 'subtract' in condition_list[0]:
                subtract_only = True
            elif 'sum' in condition_list[0]:
                sum_only = True
            else:
                condition_exists = False 
        elif len(condition_list) == 4:
            if 'moving average' in condition_list[0] and 'delta' in condition_list[2]: 
                mavg_and_delta = True #need the points sample to calculate mavg and then mavg sample to find delta
                #standard deviation also dealt similar to mavg
                sample_size = int(condition_list[1]) #for mavg
                delta_sample_size = int(condition_list[3]) #for collecting samples in mavg_samples equal to delta_sample_size
            else:
                condition_exists = False
        else:
            # print('no condition or something not pre-defined')
            condition_exists = False
        if scenario_problem == self.for_test:
            # print("---conditions status---")
            # print("index=>", i)
            print("condition exists=>", condition_exists)
            print("condition list=>", condition_list)
            # print("sample size=>", sample_size)
            # print("delta sample size=>", delta_sample_size)
            # print('------------------------')
        return sdev_only, mavg_only, delta_only, subtract_only, sum_only, mavg_and_delta, sample_size, delta_sample_size, condition_exists

    def calcAggregate(self, sdev_only, mavg_only, tag, scenario_problem):
        tag_to_read = scenario_problem+"__"+tag
        if mavg_only:
            tag_agg = sum(self.agg[tag_to_read])/len(self.agg[tag_to_read])
        elif sdev_only:
            tag_agg = np.std(self.agg[tag_to_read])
        return tag_agg

    def tagNotExists_inSampleList(self, tag, tags, tag_to_sample, scenario_problem):
        self.agg[tag_to_sample] = [tags[tag]]
        samples_ok = False
        if scenario_problem == self.for_test:
            print("fell into function: tagNotExists_inSampleList(). latest samples are: ", self.agg[tag_to_sample])
        return samples_ok

    def tagExists_butSampleSizeTooShort(self, tag, tags, tag_to_sample, scenario_problem):
        self.agg[tag_to_sample].append(tags[tag])
        samples_ok = False
        if scenario_problem == self.for_test:
            print("fell into function: tagExists_butSampleSizeTooShort(). latest samples are: ", self.agg[tag_to_sample])
        return samples_ok

    def SampleSizeOneShort(self, tag, tags, tag_to_sample, scenario_problem):
        self.agg[tag_to_sample].append(tags[tag])
        samples_ok = True
        if scenario_problem == self.for_test:
            print("fell into function: SampleSizeOneShort(). 1 is added now and latest samples are okay for calculation: ", self.agg[tag_to_sample])
        return samples_ok

    def SampleSizeOK(self, tag, tags, tag_to_sample, scenario_problem):
        self.agg[tag_to_sample].pop(0)
        self.agg[tag_to_sample].append(tags[tag])
        samples_ok = True
        if scenario_problem == self.for_test:
            print("fell into function: SampleSizeOK(). latest is appended now and oldest is popped, and latest samples are okay for calculation: ", self.agg[tag_to_sample])
        return samples_ok

    def tagNotExists_inMAvgList(self, tag, tag_to_sample, scenario_problem):
        avg = sum(self.agg[tag_to_sample])/len(self.agg[tag_to_sample])
        self.mavg_samples[tag_to_sample] = [avg]
        samples_ok = False
        if scenario_problem == self.for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', tag_to_sample, ' are ', self.mavg_samples, 'it ended up in tagNotExists_inMAvgList()')
        return samples_ok

    def MAvgSampleSizeTooShort(self, tag, tag_to_sample, scenario_problem):
        avg = sum(self.agg[tag_to_sample])/len(self.agg[tag_to_sample])
        self.mavg_samples[tag_to_sample].append(avg)
        samples_ok = False
        if scenario_problem == self.for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', tag_to_sample, ' are ', self.mavg_samples, 'it ended up in MAvgSampleSizeTooShort()')
        return samples_ok

    def MAvgSampleSizeOneShort(self, tag, tag_to_sample, scenario_problem):
        avg = sum(self.agg[tag_to_sample])/len(self.agg[tag_to_sample])
        self.mavg_samples[tag_to_sample].append(avg)
        samples_ok = True
        if scenario_problem == self.for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', tag_to_sample, ' are ', self.mavg_samples, 'it ended up in MAvgSampleSizeOneShort()')
        return samples_ok

    def MAvgSampleSizeOK(self, tag, tag_to_sample, scenario_problem):
        self.mavg_samples[tag_to_sample].pop(0)
        avg = sum(self.agg[tag_to_sample])/len(self.agg[tag_to_sample])
        self.mavg_samples[tag_to_sample].append(avg)
        samples_ok = True
        if scenario_problem == self.for_test:
            print('at point ', 'point+1(point NA now)', ' mavg samples for', tag_to_sample, ' are ', self.mavg_samples, 'it ended up in MAvgSampleSizeOK()')
        return samples_ok

    def checkSamplesStatus(self, tag, tags, sample_size, samples_ok, mavg_and_delta, delta_sample_size, condition_list, scenario_problem):
        # if scenario_problem == self.for_test:
            # print('here', tag)
        # print('starting of check Samples Status')
        # print(samples_ok)
        tag_to_sample = scenario_problem+"__"+tag
        if tag_to_sample not in self.agg.keys():
            samples_ok = self.tagNotExists_inSampleList(tag, tags, tag_to_sample, scenario_problem) #create tag in sample list
        elif tag_to_sample in self.agg.keys():
            if len(self.agg[tag_to_sample])+1 < sample_size:
                samples_ok = self.tagExists_butSampleSizeTooShort(tag, tags, tag_to_sample, scenario_problem)
                # print(tag, '1st')
            elif len(self.agg[tag_to_sample])+1 == sample_size:
                samples_ok = self.SampleSizeOneShort(tag, tags, tag_to_sample, scenario_problem)
                # print(tag, '2rd')
            elif len(self.agg[tag_to_sample])+1 > sample_size:
                samples_ok = self.SampleSizeOK(tag, tags, tag_to_sample, scenario_problem)
                # print(tag, '3rd')
        # print('ending first step in check Samples Status')
        if scenario_problem == self.for_test:
            print("samples_ok: ", samples_ok)
        if mavg_and_delta:
             #proceed if combination of mavg and delta is defined
            if samples_ok: #sample is collected well, now go to combined condition
                if scenario_problem == self.for_test:
                    print("raw samples are collected well at point", 'point+1(point NA now)')
                #now calc avg and append to mavg_samples until sample size of mavg_samples is equal to delta_sample_size
                if tag_to_sample not in self.mavg_samples.keys():
                    # print(point)
                    # print(samples_ok)
                    # print(mavg_samples)
                    # print(agg)
                    # print(condition_list)
                    samples_ok = self.tagNotExists_inMAvgList(tag, tag_to_sample, scenario_problem) #create tag in mavg_samples list
                elif tag_to_sample in self.mavg_samples.keys():
                    if len(self.mavg_samples[tag_to_sample])+1 < delta_sample_size:
                        samples_ok = self.MAvgSampleSizeTooShort(tag, tag_to_sample, scenario_problem)
                    elif len(self.mavg_samples[tag_to_sample])+1 == delta_sample_size:
                        samples_ok = self.MAvgSampleSizeOneShort(tag, tag_to_sample, scenario_problem)
                    elif len(self.mavg_samples[tag_to_sample])+1 > delta_sample_size:
                        samples_ok = self.MAvgSampleSizeOK(tag, tag_to_sample, scenario_problem)
        #now we have got samples status, whether samples are valid for all conditions
            if scenario_problem == self.for_test:
                if samples_ok:
                    print("mavg samples are collected well at point", 'point+1(point NA now)')
        return samples_ok

    def moreThan(self, additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem):
        threshold = float(threshold)
        # print(condition_list)
        sdev_only, mavg_only, delta_only, subtract_only, sum_only, mavg_and_delta, sample_size, delta_sample_size, condition_exists = self.findConditionsStatus(condition_list, scenario_problem)
        update_size = 1
        #now we have 4 cases defined. now we need to build samples for each case
        #create samples and return their status
        if condition_exists: #first think we need is samples
            if sum_only == True or subtract_only == True:
                samples_ok = True
            else:
                samples_ok = False
                samples_ok = self.checkSamplesStatus(tag, tags, sample_size, samples_ok, mavg_and_delta, delta_sample_size, condition_list, scenario_problem)

            if samples_ok == False:
                event = 'Unknown'
                # continued == False #no need to check other row conditions in a single scenario
            elif samples_ok:
                tag_to_read = scenario_problem+"__"+tag
                if sdev_only == True or mavg_only == True:
                    #now lets go to event detection. We need event status now
                    tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                    if scenario_problem == self.for_test:
                        print("collected raw samples are: ", self.agg[scenario_problem+"__"+tag], "threshold is: ", threshold, 'calculated agg value:', tag_agg)

                    if tag_agg > threshold:
                        event = True
                    else:
                        event = False
                elif delta_only:

                    if scenario_problem == self.for_test:
                        print("collected raw samples are: ", self.agg[tag_to_read], "threshold is: ", threshold)
                    # point_to_compare = 0 #compare with the point at index 0
                    # it means it needs to compare to previous value, which is currenlty at index 0 in list e.g. [10, 11].
                    if 'absolute' in condition_list[0]:
                        if abs(tags[tag] - self.agg[tag_to_read][0]) > threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if tags[tag] - self.agg[tag_to_read][0] > threshold:
                            if scenario_problem == self.for_test:
                                print("current point", tags[tag])
                                print("point in sample", self.agg[tag_to_read][0])
                            event = True
                        else:
                            event = False

                    # agg = SampleSizeOneShort(tag, agg, tags, tag_to_read) #idk why i wrote this line at first place
                elif mavg_and_delta:
                    if scenario_problem == self.for_test:
                        print("collected mavg samples are: ", self.mavg_samples[tag_to_read], "threshold is: ", threshold)
                    # point_to_compare = 0
                    if 'absolute' in condition_list[2]:
                        if abs(self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0]) > threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0] > threshold:
                            event = True
                        else:
                            event = False

                elif subtract_only: 
                    value = tags[tag]
                    if scenario_problem == self.for_test:
                        print(value)
                    for i in range(1, len(condition_list)):
                        value = value - tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after subtracting given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) > threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value > threshold:
                            event = True
                        else:
                            event = False
                elif sum_only:
                    value = tags[tag]
                    for i in range(1, len(condition_list)):
                        value = value + tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after adding given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) > threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value > threshold:
                            event = True
                        else:
                            event = False

        else: #no condition defined
            # print(scenario_problem) #testing
            # print(threshold)
            # print(tag)
            # print(threshold)
            if tags[tag] > threshold:
                event = True
            else:
                event = False   

        return event, continued

    def lessThan(self, additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem):
        threshold = float(threshold)
        # print(condition_list)
        sdev_only, mavg_only, delta_only, subtract_only, sum_only, mavg_and_delta, sample_size, delta_sample_size, condition_exists = self.findConditionsStatus(condition_list, scenario_problem)
        update_size = 1
        #now we have 4 cases defined. now we need to build samples for each case
        #create samples and return their status
        if condition_exists: #first think we need is samples
            if sum_only == True or subtract_only == True:
                samples_ok = True
            else:
                samples_ok = False
                samples_ok = self.checkSamplesStatus(tag, tags, sample_size, samples_ok, mavg_and_delta, delta_sample_size, condition_list, scenario_problem)

            if samples_ok == False:
                event = 'Unknown'
                # continued == False #no need to check other row conditions in a single scenario
            elif samples_ok:
                tag_to_read = scenario_problem+"__"+tag
                if sdev_only == True or mavg_only == True:
                    #now lets go to event detection. We need event status now
                    tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                    if scenario_problem == self.for_test:
                        print('points', self.agg[tag_to_read])
                        print('agg value:', tag_agg)
                    if tag_agg < threshold:
                        event = True
                    else:
                        event = False
                elif delta_only:
                    # point_to_compare = 0 #compare with the point at index 0
                    # it means it needs to compare to previous value, which is currenlty at index 0 in list e.g. [10, 11].
                    if 'absolute' in condition_list[0]:
                        if abs(tags[tag] - self.agg[tag_to_read][0]) < threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if tags[tag] - self.agg[tag_to_read][0] < threshold:
                            if scenario_problem == self.for_test:
                                print("current point", tags[tag])
                                print("point in sample", self.agg[tag_to_read][0])
                            event = True
                        else:
                            event = False

                elif mavg_and_delta:
                    # point_to_compare = 0
                    if 'absolute' in condition_list[2]:
                        if abs(self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0]) < threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0] < threshold:
                            event = True
                        else:
                            event = False

                elif subtract_only: 
                    value = tags[tag]
                    for i in range(1, len(condition_list)):
                        value = value - tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after subtracting given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) < threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value < threshold:
                            event = True
                        else:
                            event = False
                elif sum_only:
                    value = tags[tag]
                    for i in range(1, len(condition_list)):
                        value = value + tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after adding given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) < threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value < threshold:
                            event = True
                        else:
                            event = False

        else: #no condition defined
            # print(tag)
            # print(threshold)
            # print(type(threshold))
            # print(tags[tag])
            # print(type(tags[tag]))
            if tags[tag] < threshold:
                event = True
            else:
                event = False   

        return event, continued

    def equalTo(self, additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem):
        threshold = float(threshold)
        # print(condition_list)
        sdev_only, mavg_only, delta_only, subtract_only, sum_only, mavg_and_delta, sample_size, delta_sample_size, condition_exists = self.findConditionsStatus(condition_list, scenario_problem)
        update_size = 1
        #now we have 4 cases defined. now we need to build samples for each case
        #create samples and return their status
        if condition_exists: #first think we need is samples
            if sum_only == True or subtract_only == True:
                samples_ok = True
            else:
                samples_ok = False
                samples_ok = self.checkSamplesStatus(tag, tags, sample_size, samples_ok, mavg_and_delta, delta_sample_size, condition_list, scenario_problem)

            if samples_ok == False:
                event = 'Unknown'
                # continued == False #no need to check other row conditions in a single scenario
            elif samples_ok:
                tag_to_read = scenario_problem+"__"+tag
                if sdev_only == True or mavg_only == True:
                    #now lets go to event detection. We need event status now
                    tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                    if scenario_problem == self.for_test:
                        print('points', self.agg[tag_to_read])
                        print('agg value:', tag_agg)
                    if tag_agg == threshold:
                        event = True
                    else:
                        event = False
                elif delta_only:
                    # point_to_compare = 0 #compare with the point at index 0
                    # it means it needs to compare to previous value, which is currenlty at index 0 in list e.g. [10, 11].
                    if 'absolute' in condition_list[0]:
                        if abs(tags[tag] - self.agg[tag_to_read][0]) == threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if tags[tag] - self.agg[tag_to_read][0] == threshold:
                            if scenario_problem == self.for_test:
                                print("current point", tags[tag])
                                print("point in sample", self.agg[tag_to_read][0])
                            event = True
                        else:
                            event = False

                elif mavg_and_delta:
                    # point_to_compare = 0
                    if 'absolute' in condition_list[2]:
                        if abs(self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0]) == threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if self.mavg_samples[tag_to_read][-1] - self.mavg_samples[tag_to_read][0] == threshold:
                            event = True
                        else:
                            event = False

                elif subtract_only: 
                    value = tags[tag]
                    for i in range(1, len(condition_list)):
                        value = value - tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after subtracting given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) == threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value == threshold:
                            event = True
                        else:
                            event = False
                elif sum_only:
                    value = tags[tag]
                    for i in range(1, len(condition_list)):
                        value = value + tags[condition_list[i]]
                        if scenario_problem == self.for_test:
                            print("after loop value: ", value)
                    if scenario_problem == self.for_test:
                        print("value after adding given keys: ", value)
                    if 'absolute' in additional_cond:
                        if abs(value) == threshold:
                            event = True
                        else:
                            event = False
                    else:
                        if value == threshold:
                            event = True
                        else:
                            event = False

        # else: #no condition defined
        #     if tags[tag] > threshold:
        #         event = True
        #     else:
        #         event = False   

        # return event, continued
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        else:
            if 'Intermediate' in tag:
                # print(tags[tag])
                if tags[tag] == 0:
                    event = False
                elif tags[tag] == 1:
                    event = True
                elif tags[tag] == 2:
                    event = 'Unknown'
            else:
                if tags[tag] == threshold:
                    event = True
                else:
                    event = False
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        return event, continued

    def outOfRange(self, additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem):

        threshold = threshold.replace("]", "")
        threshold = threshold.replace("[", "")
        threshold = threshold.replace("'", "")
        threshold = threshold.split(",")
        low_val = float(threshold[0])
        high_val = float(threshold[1])


        if 'standard deviation' in additional_cond or 'moving average' in additional_cond:
            condition = condition_list[0]
            if 'standard deviation' in additional_cond:
                sdev_only = True
            else:
                sdev_only = False
            if 'moving average' in additional_cond:
                mavg_only = True
            else:
                mavg_only = False

            sample_size = int(condition_list[1])
            update_size = 1
            tag_to_sample = scenario_problem+"__"+tag
            if tag_to_sample not in self.agg.keys():
                self.agg[tag_to_sample] = [tags[tag]]
                event = 'Unknown'
                if scenario_problem == self.for_test:
                    print("samples exist, but too short, appending one for now")
                    print('points', self.agg[tag_to_sample])
                # continued == False #no need to check other row conditions in a single scenario
            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 < sample_size:
                event = 'Unknown'
                # agg[tag].append(tags[tag])
                self.agg[tag_to_sample].append(tags[tag])
                if scenario_problem == self.for_test:
                    print("samples exist, but too short, appending one for now")
                    print('points', self.agg[tag_to_sample])
                continued == False #no need to check other row conditions in a single scenario
            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 == sample_size:
                # agg[tag].append(tags[tag])
                self.agg[tag_to_sample].append(tags[tag])
                tag_agg = self.calcAggregate(sdev_only, mavg_only, self.agg, tag, scenario_problem)
                if scenario_problem == self.for_test:
                    print("samples exist, but one short, appended one now and samples are OK for calculation")
                    print('points', self.agg[tag_to_sample])
                    print('agg value:', tag_agg)
                    print("low val:", low_val)
                    print("high val:", high_val)

                if tag_agg < low_val or tag_agg > high_val:
                    event = True
                else:
                    event = False

            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 > sample_size:
                self.agg[tag_to_sample].pop(0)
                self.agg[tag_to_sample].append(tags[tag])
                tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                if scenario_problem == self.for_test:
                    print("samples more than sample size, appended latest and popped oldest and samples are OK for calculation")
                    print('points', self.agg[tag_to_sample])
                    print('agg value:', tag_agg)
                    print("low val:", low_val)
                    print("high val:", high_val)

                if tag_agg < low_val or tag_agg > high_val:
                    event = True
                else:
                    event = False

        elif 'subtract' in additional_cond or 'sum' in additional_cond:
            if 'subtract' in additional_cond:
                value = tags[tag]
                for i in range(1, len(condition_list)):
                    value = value - tags[condition_list[i]]
                    if scenario_problem == self.for_test:
                        print("after loop value: ", value)
                if scenario_problem == self.for_test:
                    print("value after subtracting given keys: ", value)
                if 'absolute' in additional_cond:
                    if abs(value) < low_val or abs(value) > high_val:
                        event = True
                    else:
                        event = False
                else:
                    if value < low_val or value > high_val:
                        event = True
                    else:
                        event = False
            elif 'sum' in additional_cond:
                value = tags[tag]
                for i in range(1, len(condition_list)):
                    value = value + tags[condition_list[i]]
                    if scenario_problem == self.for_test:
                        print("after loop value: ", value)
                if scenario_problem == self.for_test:
                    print("value after adding given keys: ", value)
                if 'absolute' in additional_cond:
                    if abs(value) < low_val or abs(value) > high_val:
                        event = True
                    else:
                        event = False
                else:
                    if value < low_val or value > high_val:
                        event = True
                    else:
                        event = False

        else:
            if tags[tag] < low_val or tags[tag] > high_val:
                event = True
            else:
                event = False

        return event, continued


    def inRange(self, additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem):

        threshold = threshold.replace("]", "")
        threshold = threshold.replace("[", "")
        threshold = threshold.replace("'", "")
        threshold = threshold.split(",")
        # print(threshold)
        low_val = float(threshold[0])
        high_val = float(threshold[1])

        if 'standard deviation' in additional_cond or 'moving average' in additional_cond:
            condition = condition_list[0] 
            if 'standard deviation' in additional_cond:
                sdev_only = True
            else:
                sdev_only = False
            if 'moving average' in additional_cond:
                mavg_only = True
            else:
                mavg_only = False
            sample_size = int(condition_list[1])
            update_size = 1
            tag_to_sample = scenario_problem+"__"+tag
            if tag_to_sample not in self.agg.keys():
                self.agg[tag_to_sample] = [tags[tag]]
                event = 'Unknown'
                if scenario_problem == self.for_test:
                    print("samples exist, but too short, appending one for now")
                    print('points', self.agg[tag_to_sample])
                # continued == False #no need to check other row conditions in a single scenario
            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 < sample_size:
                event = 'Unknown'
                self.agg[tag_to_sample].append(tags[tag])
                if scenario_problem == self.for_test:
                    print("samples exist, but too short, appending one for now")
                    print('points', self.agg[tag_to_sample])

                continued == False #no need to check other row conditions in a single scenario
            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 == sample_size:
                    self.agg[tag_to_sample].append(tags[tag])
                    tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                    if scenario_problem == self.for_test:
                        print("samples exist, but one short, appended one now and samples are OK for calculation")
                        print('points', self.agg[tag_to_sample])
                        print('agg value:', tag_agg)
                        print("low val:", low_val)
                        print("high val:", high_val)
                    if (tag_agg > low_val or tag_agg == low_val) and (tag_agg < high_val or tag_agg == high_val):
                        event = True
                    else:
                        event = False
            elif tag_to_sample in self.agg.keys() and len(self.agg[tag_to_sample])+1 > sample_size:
                    self.agg[tag_to_sample].pop(0)
                    self.agg[tag_to_sample].append(tags[tag])
                    tag_agg = self.calcAggregate(sdev_only, mavg_only, tag, scenario_problem)
                    if scenario_problem == self.for_test:
                        print("samples more than sample size, appended latest and popped oldest and samples are OK for calculation")
                        print('points', self.agg[tag_to_sample])
                        print('agg value:', tag_agg)
                        print("low val:", low_val)
                        print("high val:", high_val)

                    if (tag_agg > low_val or tag_agg == low_val) and (tag_agg < high_val or tag_agg == high_val):
                        event = True
                    else:
                        event = False

        elif 'subtract' in additional_cond or 'sum' in additional_cond:
            if 'subtract' in additional_cond:
                value = tags[tag]
                for i in range(1, len(condition_list)):
                    value = value - tags[condition_list[i]]
                    if scenario_problem == self.for_test:
                        print("after loop value: ", value)
                if scenario_problem == self.for_test:
                    print("value after subtracting given keys: ", value)
                if 'absolute' in additional_cond:
                    if (abs(value) > low_val or abs(value) == low_val) and (abs(value) < high_val or abs(value) == high_val):
                        event = True
                    else:
                        event = False
                else:
                    if (value > low_val or value == low_val) and (value < high_val or value == high_val):
                        event = True
                    else:
                        event = False
            elif 'sum' in additional_cond:
                value = tags[tag]
                for i in range(1, len(condition_list)):
                    value = value + tags[condition_list[i]]
                    if scenario_problem == self.for_test:
                        print("after loop value: ", value)
                if scenario_problem == self.for_test:
                    print("value after adding given keys: ", value)
                if 'absolute' in additional_cond:
                    if (abs(value) > low_val or abs(value) == low_val) and (abs(value) < high_val or abs(value) == high_val):
                        event = True
                    else:
                        event = False
                else:
                    if (value > low_val or value == low_val) and (value < high_val or value == high_val):
                        event = True
                    else:
                        event = False

        else:
            if (tags[tag] > low_val or tags[tag] == low_val) and (tags[tag] < high_val or tags[tag] == high_val):
                event = True
            else:
                event = False

        return event, continued        

    def eventSoFar(self, event, logic, event_so_far, scenario_problem): #event is status of current line, event_so_far is what comes from above lines
        if event == True and logic == 'OR' and event_so_far == True: #for first line
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 1 of eventsofar func')
        elif event == True and logic == 'AND' and event_so_far == True:
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 2 of eventsofar func')
        elif event == False and logic == 'AND' and event_so_far == True:
            event_so_far = False
            if scenario_problem == self.for_test:
                print('fell into condition 3 of eventsofar func')
        elif event == True and logic == 'AND' and event_so_far == 'Unknown': 
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into condition 4 of eventsofar func')
        elif event == 'Unknown' and logic == 'OR' and event_so_far == True:
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 5 of eventsofar func')
        elif event == True and logic == 'OR' and event_so_far == 'Unknown':
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 6 of eventsofar func')
        elif event == 'Unknown' and logic == 'AND' and event_so_far == True: #may be this should be unknown as well, as it is similar to 4th condition above
            # event_so_far = False
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into condition 7 of eventsofar func')
        elif event == True and logic == 'OR' and event_so_far == True: #may be this should be unknown as well, as it is similar to 4th condition above
            # event_so_far = False
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 8 of eventsofar func')
        elif event == False and logic == 'OR' and event_so_far == True:
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 9 of eventsofar func')
        elif event == True and logic == 'OR' and event_so_far == False:
            event_so_far = True
            if scenario_problem == self.for_test:
                print('fell into condition 10 of eventsofar func')
        elif event == True and logic == 'AND' and event_so_far == False:
            event_so_far = False
            if scenario_problem == self.for_test:
                print('fell into condition 11 of eventsofar func')
        elif (event == 'Unknown' and event_so_far == False) and (logic == 'AND'):
            event_so_far = False
            if scenario_problem == self.for_test:
                print('fell into condition 12 of eventsofar func')
        elif (event == 'Unknown' and event_so_far == False) and (logic == 'OR'):
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into condition 13 of eventsofar func')
        elif (event == False and event_so_far == 'Unknown') and (logic == 'OR'):
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into condition 14 of eventsofar func')
        elif (event == False and event_so_far == 'Unknown') and (logic == 'AND'):
            event_so_far = False
            if scenario_problem == self.for_test:
                print('fell into condition 15 of eventsofar func')
        elif (event == 'Unknown' and event_so_far == 'Unknown') and (logic == 'OR' or logic == 'AND'):
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into condition 16 of eventsofar func')
        elif (event == False and event_so_far == False) and (logic == 'OR' or logic == 'AND'):
            event_so_far = False
            if scenario_problem == self.for_test:
                print('fell into condition 17 of eventsofar func')
        else:
            event_so_far = 'Unknown'
            if scenario_problem == self.for_test:
                print('fell into last else condition of eventsofar func')

        return event_so_far

    def lineStatus(self, continued, event, event_so_far, tags, problem, tag, additional_cond, 
                   condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem):

        # if continued == True and problem == 'nan': #now 'blank' is being used instead of 'nan'
        if continued == True:
            # continued = True
            if str(implement) == '0.0':
                print('implement is 0, so event of this line is Unknown')
                event = 'Unknown' #no need to apply persistence, even though persistence exists for this line
                continued = True
                if scenario_problem == self.for_test:
                    print("this line is not implemented, event is: ", event)
                    print("-------------")
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)
            elif operator == '>':

                event, continued = self.moreThan(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                #here we need to add persistence check for current line. persistence check is to be done after event is available. 
                # if event is available, do persistence check and then proceed to find event_so_far
                if 'True' in persistence_list:
                    event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if scenario_problem == self.for_test:
                    # print("> of linestatus")
                    print("this line's status:", event, "logic:", logic, "status comes from above:", event_so_far)
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)

            elif operator == '<':

                event, continued = self.lessThan(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                if 'True' in persistence_list:
                    event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if scenario_problem == self.for_test:
                    # print("> of linestatus")
                    print("this line's status:", event, "logic:", logic, "status comes from above:", event_so_far)
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)

            elif operator == '=':

                event, continued = self.equalTo(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                if 'True' in persistence_list:
                    event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if scenario_problem == self.for_test:
                    # print("> of linestatus")
                    print("this line's status:", event, "logic:", logic, "status comes from above:", event_so_far)
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)

            elif operator == '][':

                event, continued = self.outOfRange(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                if 'True' in persistence_list:
                    event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if scenario_problem == self.for_test:
                    # print("> of linestatus")
                    print("this line's status:", event, "logic:", logic, "status comes from above:", event_so_far)
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)

            elif operator == '[]' or operator == 'NOT ][':

                event, continued = self.inRange(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                if 'True' in persistence_list:
                    event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if scenario_problem == self.for_test:
                    # print("> of linestatus")
                    print("this line's status:", event, "logic:", logic, "status comes from above:", event_so_far)
                event_so_far = self.eventSoFar(event, logic, event_so_far, scenario_problem)
        else:
            continued = False

        return event_so_far, continued

    def createVariables(self, row_num_in_scenario, df):

        problem = df.loc[row_num_in_scenario]['Problem_Name']
        # tag = df.loc[row_num_in_scenario]['Standard_Key'].replace('-', '_')
        tag = df.loc[row_num_in_scenario]['Standard_Key']
        additional_cond = df.loc[row_num_in_scenario]['Additional condition']
        condition_list = df.loc[row_num_in_scenario]['Additional condition'].split(",")
        operator = df.loc[row_num_in_scenario]['Condition']
        threshold = df.loc[row_num_in_scenario]['Threshold']
        logic = df.loc[row_num_in_scenario-1]['Logic']
        implement = df.loc[row_num_in_scenario]['Implement']
        if self.test_run == 1: #updated on 12062023
            if tag == 'NS_IG010-XA_PV' or tag == 'NS_AN_NG2-00273_PV':
                implement = 0
            else:
                implement = 1
        persistence_list = df.loc[row_num_in_scenario]['Persistence'].split(",")
        persistence_duration = 1 #by default, just to send argument to function. it will be over-written below if persistence is True.
        if 'True' in persistence_list:
            persistence_duration = int(persistence_list[1])
        # if scenario_problem == self.for_test:
            # print("implement is => ", implement)
            # print(type(implement))

        return problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration

    def persistenceCheck(self, event, persistence_list, persistence_duration, scenario_problem, tag):
        #first thing is to make persistence_tag to collect samples for each key, to make key unique to this row only, lets combine problem name with key:
        persistence_tag = scenario_problem+"__"+tag
        if event == True and ('True' in persistence_list): #its needed only if status is active
            if scenario_problem == self.for_test:
                print("persistence to apply")
            if event == True and persistence_tag not in self.persistence.keys(): #make status list in persistence dict
                self.persistence[persistence_tag] = [event]
                event = 'Unknown'
                if scenario_problem == self.for_test:
                    print("fell into 1st condition of persistence (no samples present). event is: ", event)
            elif (persistence_tag in self.persistence.keys()) and len(self.persistence[persistence_tag])+1 < persistence_duration: #if less points than required, status is still Unknown
                self.persistence[persistence_tag].append(event)
                event = 'Unknown'
                if scenario_problem == self.for_test:
                    print("fell into 2nd condition of persistence (sample exist but short). event is: ", event)
            elif (persistence_tag in self.persistence.keys()) and len(self.persistence[persistence_tag])+1 == persistence_duration: #Event is persisted as long as user defind time, now its final status is True
                self.persistence[persistence_tag].append(event)
                event = True
                if scenario_problem == self.for_test:
                    print("fell into 3rd condition of persistence (samples are one short, but appended one now and now equal to persistence duration). event is: ", event)
            elif (persistence_tag in self.persistence.keys()) and len(self.persistence[persistence_tag])+1 > persistence_duration: #if more than the required inputs, then remove oldest and append latest
                self.persistence[persistence_tag].pop(0)
                self.persistence[persistence_tag].append(event)
                event = True
                if scenario_problem == self.for_test:
                    print("fell into 4th condition of persistence (samples more than persistence duration, latest is appended and oldest is popped). event is: ", event)
        elif ('True' in persistence_list) and event != True: #if event is false, remove status list from persistence dict, 
            if persistence_tag in self.persistence.keys():
                self.persistence[persistence_tag] = []
                if scenario_problem == self.for_test:
                    print("fell into 5th condition of persistence (persistence is reset as event is not active). event is: ", event)
                # and event_so_far will go forward unchanged
        if scenario_problem == self.for_test:
            if persistence_tag in self.persistence.keys():
                print("persistence stored for ", persistence_tag, " are: ", self.persistence[persistence_tag])
            else:
                print("persistence check => ", persistence_tag, " is yet not available in persistence dict because it has not been triggered yet, probably due to additional condition." )
        return event
        
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    def rcaTemplatesReader(self, rca_dfs, tags, running_status, problems_to_detect):

        status = {}
        parent_node = {}
        # assets = ['FV', 'LNGV', 'BOGH', 'WUH', 'GWHS', 'LD1', 'LD2', 'HD1', 'HD2', 'SC']
        assets = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
                  'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 
                  'GCU', 'INCIN'] #updated on 11292023
        # for point in range(points):
        # print("starting iteration ", point)
        # print(running_status)
        for itr in range(len(rca_dfs)):
            if running_status[assets[itr]] == 1:
                print(f"starting rca template: {assets[itr]}")
                df = rca_dfs[itr]
                # print(f"df {assets[itr]} started")
                # print(df, "started")
                # ------------------------------------------
                df = df.loc[:, :'Implement']
                df.fillna('blank', inplace=True) #updated on 12032023 #changed from nan to blank

                implemented = df['Implement'] == 1.0
                # df = df[implemented] #updated on 12032023
                df = df[implemented].reset_index()
                df = df.drop(columns=['index'], axis=1)
                # print(df)
                # -------------------------------------------

                previous_problem = 'start_of_sheet'
                #^^^^^^^^^^^^^^^^^^^^^^^^^^
                component_running = True #by default it is true, but later if some component is not running, the rows below that component will be skipped until next running component is found.
                last = 'none' #just to update parent node and status if component is not running
                #^^^^^^^^^^^^^^^^^^^^^^^^^^
                # print("*************************")
                # print('this is point number:', point + 1)
                # # print(tags['CM_LD1_OilFilterAlrmCtrlTemp'])
                # print("*************************")

                # while True:
                for i in range(len(df.index)):  # go row by row
                    scenario_problem = df.loc[i]['Problem_Name']
                    # tag = df.loc[i]['Standard_Key'].replace('-', '_')
                    tag = df.loc[i]['Standard_Key']
                    additional_cond = df.loc[i]['Additional condition']
                    condition_list = df.loc[i]['Additional condition'].split(",")
                    operator = df.loc[i]['Condition']
                    threshold = df.loc[i]['Threshold']
                    persistence_list = df.loc[i]['Persistence'].split(",")
                    persistence_duration = 1 #by default, just to send argument to function. it will be over-written below if persistence is True.
                    if 'True' in persistence_list:
                        persistence_duration = int(persistence_list[1])
                    implement = df.loc[i]['Implement']
                    if self.test_run == 1: #updated on 12062023
                        if tag == 'NS_IG010-XA_PV' or tag == 'NS_AN_NG2-00273_PV':
                            implement = 0
                        else:
                            implement = 1
                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ newly added lines
                    level = df.loc[i]['Level']
                    run_check = str(df.loc[i]['Run Check'])
                    #updated on 12192023 from here
                    if level == 'COMPONENT':
                        if run_check == '1.0':
                            if running_status[scenario_problem] == 1:
                                component_running = True
                            else:
                                component_running = False
                        else:
                            component_running = True
                    #updated on 12192023 till here
                    if component_running:
                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    # if scenario_problem != 'nan': #now 'blank' is being used
                        if scenario_problem != previous_problem and problems_to_detect[scenario_problem] == 1:
                            previous_problem = scenario_problem
                            parent_node[scenario_problem] = df.loc[i]['Parent_Node']

                            continued = True
                            if scenario_problem == self.for_test:
                                    print(scenario_problem, "started")
                            # print(i)
                            if df.loc[i]['Standard_Key'] == 'blank': #updated on 12032023 #changed from nan to blank
                                event = 'Unknown'
                                continued = False
                                #need to break here
                            else:
                                event = False

                            if str(implement) == '0.0':
                                event = 'Unknown'
                                continued = True
                                if scenario_problem == self.for_test:
                                    print("this line is not implemented, event is: ", event)

                            elif operator == '>':
                                # if scenario_problem == self.for_test:
                                #     print("value of CM_LD1_OilFilterAlrmCtrlTemp is", tags['CM_LD1_OilFilterAlrmCtrlTemp'])
                                event, continued = self.moreThan(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                                if scenario_problem == self.for_test:
                                    print("data of 1st line: ", tag, " ", operator, " ", threshold, " ", condition_list)
                                    print("event of 1st line: ", event)

                            elif operator == '<':
                            
                                event, continued = self.lessThan(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                                if scenario_problem == self.for_test:
                                    print("data of 1st line: ", tag, " ", operator, " ", threshold, " ", condition_list)
                                    print("event of 1st line: ", event)

                            elif operator == '=':
                            
                                event, continued = self.equalTo(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                                if scenario_problem == self.for_test:
                                    print("data of 1st line: ", tag, " ", operator, " ", threshold, " ", condition_list)
                                    print("event of 1st line: ", event)

                            elif operator == '][':
                                # print(problem)
                                event, continued = self.outOfRange(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                                if scenario_problem == self.for_test:
                                    print("data of 1st line: ", tag, " ", operator, " ", threshold, " ", condition_list)
                                    print("event of 1st line: ", event)

                            elif operator == '[]' or operator == 'NOT ][':
                            
                                event, continued = self.inRange(additional_cond, condition_list, tag, tags, threshold, continued, scenario_problem)
                                if scenario_problem == self.for_test:
                                    print("data of 1st line: ", tag, " ", operator, " ", threshold, " ", condition_list)
                                    print("event of 1st line: ", event)

                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                            #here we need to add persistence check for current line. persistence check is to be done after event is available. 
                            # if event is available, do persistence check and then proceed to find event_so_far
                            if 'True' in persistence_list:
                                event = self.persistenceCheck(event, persistence_list, persistence_duration, scenario_problem, tag)
                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                            event_so_far = event
                            if scenario_problem == self.for_test:
                                print(scenario_problem, "=> after line 1 event so far =>", event_so_far, ", and it will go to the lines below")
                                print("-------------")

                            if i+1 < len(df.index) and continued == True:
                            
                                row_num_in_scenario = i+1
                                problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration = self.createVariables(row_num_in_scenario, df)
                                if scenario_problem == self.for_test:
                                    print("line 2 data =>", problem, tag, condition_list, operator, threshold, logic)
                                # if problem != 'nan':
                                if problem != previous_problem: #it means another problem started
                                    continued = False
                                    if scenario_problem == self.for_test:
                                        print("********* end of rule *********")
                                        print("this line has another scenario started, so this line will not be processed")
                                if continued == True:
                                    event_so_far, continued = self.lineStatus(continued, event, event_so_far, tags, problem, tag, additional_cond, 
                                                                         condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem)
                                    if scenario_problem == self.for_test:
                                        print(scenario_problem, "after line 2 =>", event_so_far)
                                        print("-------------")

                            if i+2 < len(df.index) and continued == True:
                            
                                row_num_in_scenario = i+2
                                problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration = self.createVariables(row_num_in_scenario, df)
                                if scenario_problem == self.for_test:
                                    print("line 3 data =>", problem, tag, condition_list, operator, threshold, logic)
                                # if problem != 'nan':
                                if problem != previous_problem:
                                    continued = False
                                    if scenario_problem == self.for_test:
                                        print("********* end of rule *********")
                                        print("this line has another scenario started, this line will not be processed")
                                if continued == True:
                                    event_so_far, continued = self.lineStatus(continued, event, event_so_far, tags, problem, tag, additional_cond, 
                                                                         condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem)
                                    if scenario_problem == self.for_test:
                                        print(scenario_problem, "after line 3 =>", event_so_far)
                                        print("-------------")

                            if i+3 < len(df.index) and continued == True:
                            
                                row_num_in_scenario = i+3
                                problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration = self.createVariables(row_num_in_scenario, df)
                                if scenario_problem == self.for_test:
                                    print("line 4 data =>", problem, tag, condition_list, operator, threshold, logic)
                                # if problem != 'nan':
                                if problem != previous_problem:
                                    continued = False
                                    if scenario_problem == self.for_test:
                                        print("********* end of rule *********")
                                        print("this line has another scenario started, this line will not be processed")
                                if continued == True:
                                    event_so_far, continued = self.lineStatus(continued, event, event_so_far, tags, problem, tag, additional_cond, 
                                                                         condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem)
                                    if scenario_problem == self.for_test:
                                        print(scenario_problem, "after line 4 =>", event_so_far)
                                        print("-------------")

                            if i+4 < len(df.index) and continued == True:
                            
                                row_num_in_scenario = i+4
                                problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration = self.createVariables(row_num_in_scenario, df)
                                if scenario_problem == self.for_test:
                                    print("line 5 data =>", problem, tag, condition_list, operator, threshold, logic)
                                # if problem != 'nan':
                                if problem != previous_problem:
                                    continued = False
                                    if scenario_problem == self.for_test:
                                        print("********* end of rule *********")
                                        print("this line has another scenario started, this line will not be processed")
                                if continued == True:
                                    event_so_far, continued = self.lineStatus(continued, event, event_so_far, tags, problem, tag, additional_cond, 
                                                                         condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem)
                                    if scenario_problem == self.for_test:
                                        print(scenario_problem, "after line 5 =>", event_so_far)
                                        print("-------------")

                            if i+5 < len(df.index) and continued == True:
                            
                                row_num_in_scenario = i+5
                                problem, tag, additional_cond, condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration = self.createVariables(row_num_in_scenario, df)
                                if scenario_problem == self.for_test:
                                    print("line 6 data =>", problem, tag, condition_list, operator, threshold, logic)
                                # if problem != 'nan':
                                if problem != previous_problem:
                                    continued = False
                                    if scenario_problem == self.for_test:
                                        print("********* end of rule *********")
                                        print("this line has another scenario started, this line will not be processed")
                                if continued == True:
                                    event_so_far, continued = self.lineStatus(continued, event, event_so_far, tags, problem, tag, additional_cond, 
                                                                         condition_list, operator, threshold, logic, implement, persistence_list, persistence_duration, scenario_problem)
                                    if scenario_problem == self.for_test:
                                        print(scenario_problem, "after line 6 =>", event_so_far)
                                        print("-------------")                   

                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            if 'Intermediate' in scenario_problem:
                                if event_so_far == True:
                                    intermediate_ev = 1
                                elif event_so_far == False:
                                    intermediate_ev = 0
                                elif event_so_far == 'Unknown':
                                    intermediate_ev = 2
                                # print('status of intermediate event is:', intermediate_ev)
                                tags[scenario_problem] = intermediate_ev
                                status[scenario_problem] = intermediate_ev

                            else:
                                status[scenario_problem] = event_so_far
                            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

                            if scenario_problem == self.for_test:
                                if self.agg_test in self.agg:
                                    print(self.agg[self.agg_test])
                                print("final result of ", self.for_test, "is =>", status[scenario_problem])
                                print("----------------------------------")
                        elif problems_to_detect[scenario_problem] == 0:
                            status[scenario_problem] = 'Unknown_TagNA'
                            parent_node[scenario_problem] = df.loc[i]['Parent_Node']
                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    else:
                        if ('Intermediate' not in scenario_problem) and (scenario_problem != last):
                            parent_node[scenario_problem] = df.loc[i]['Parent_Node']
                            status[scenario_problem] = 'Unknown_ComponentNotRunning'
                        last = scenario_problem
                    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # print("sheet ", df, "done")
            elif running_status[assets[itr]] == 0: #if asset is not running, then just read scenario and their parent node, so that levels could be created for all scenarios
                # print(f"{assets[itr]} is not running, so its rca is skipped")
                df = rca_dfs[itr]
                last = 'none'
                for i in range(len(df.index)):  # go row by row
                    scenario_problem = df.loc[i]['Problem_Name']
                    if ('Intermediate' not in scenario_problem) and (scenario_problem != last): #so that nan could be avoided in case of same parent nodes for multiple lines. Actually in excel its not filled for all rows
                        #and we dont need to put status of intermediate to status dict, and we dont need parent node of intermediate problem.
                        # Intermediate's only purpose is to detect rule with local logic
                        status[scenario_problem] = 'Unknown_AssetNotRunning'
                        parent_node[scenario_problem] = df.loc[i]['Parent_Node']
                    last = scenario_problem
        
        #change boolean status to string
        for key in status.keys():
            status[key] = str(status[key])
        # print(status)
        
        return status, parent_node

    def logStatusandParentNode(self, status, parent_node):
        # print(parent_node)
        self.cursor.execute('truncate table public."RCA_update"') #updated for PostgreSQL
        self.conn.commit()
        rca_update = {}
        # print('creating rca update history dict')
        for key in status.keys():
            rca_update[key] = [str(status[key]), parent_node[key]] #status is in boolean, so converting to string
        # rca_update_history #status and parent node dictionaries are combined in this dict
        # print('logging rca update')
        
        # print(rca_update)
        for key in rca_update.keys():
            # print(key, "=>", rca_update[key][0], "=> ", rca_update[key][1], "=>", type(rca_update[key][1]))
            self.cursor.execute('insert into public."RCA_update" values(%s, %s, %s, %s)', [datetime.now(), key, rca_update[key][0], rca_update[key][1]]) #updated for PostgreSQL
            self.conn.commit()
        # print(rca_update)
        return rca_update #updated on 12122023
    
    def RCAlevels(self, HOS_dict): #updated for DailyHOS
        self.cursor.execute('truncate table public."RCA_levels"') #updated for PostgreSQL
        self.conn.commit()

        # cursor.execute("truncate table RCA_Status")
        # conn.commit()

        self.cursor.execute('''select "scenarioName" from public."RCA_update" where "ParentNode" = 'None';''') #updated for PostgreSQL
        row = self.cursor.fetchall()
        self.conn.commit()
        Level1_Equipment = []
        for item in row:
            Level1_Equipment.append(item[0])
        # print(Level1_Equipment)
        # print('equipment done')

        asset_hierarchy = {} #updated for dailyHOS
        problem_hierarchy = {} #updated on 11292023. this is done to avoid querying sql for rca levels in every loop. this dict will serve the purpose efficiently

        for Equipment in Level1_Equipment:
            if Equipment in HOS_dict.keys(): #updated for dailyHOS
                asset_hierarchy[Equipment] = [] #updated for dailyHOS
            Equipment_string = Equipment
            Level2_Component = []
            self.cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Equipment]) #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()

            for item in row:
                Level2_Component.append(item[0])
                # print(Level2_Component)
                # print('component done')
                if item[0] in HOS_dict.keys(): #updated for dailyHOS
                    asset_hierarchy[Equipment].append(item[0]) #updated for dailyHOS

            for Component in Level2_Component:
                Component_string = Component
                Level3_Scenario = []

                self.cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Component]) #updated for PostgreSQL
                row = self.cursor.fetchall()
                self.conn.commit()

                for item in row:
                    Level3_Scenario.append(item[0])
                    # print(Level3_Scenario)
                    # print('scenarios done')

                for Scenario in Level3_Scenario:
                    Scenario_string = Scenario

                    Level4_RootCauses = []
                    self.cursor.execute('select "scenarioName" from public."RCA_update" where "ParentNode" = %s', [Scenario]) #updated for PostgreSQL
                    row = self.cursor.fetchall()
                    self.conn.commit()

                    for item in row:
                        Level4_RootCauses.append(item[0])
                    if len(Level4_RootCauses)>0:
                        RootCauses_string = Level4_RootCauses[0]
                        for i in range(1, len(Level4_RootCauses)):
                            RootCauses_string = RootCauses_string + "," + Level4_RootCauses[i]
                    else:
                        RootCauses_string = ""

                    abbreviations = ['LDC1', 'LDC2', 'HDC1', 'HDC2', 'FVAP', 'LNGVAP', 'BOGHTR', 'WUHTR', 'GWHSTM', 'SCLR']
                    to_replace = ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'BOGH', 'WUH', 'GWHS', 'SC']
                    for i in range(len(abbreviations)):
                        Equipment_string = Equipment_string.replace(abbreviations[i]+"_", to_replace[i]+"_")
                        Component_string = Component_string.replace(abbreviations[i]+"_", to_replace[i]+"_")
                    # print("start logging rca levels")
                    self.cursor.execute('insert into public."RCA_levels" values(%s, %s, %s, %s)', [Equipment_string, Component_string, Scenario_string, RootCauses_string]) #updated for PostgreSQL
                    self.conn.commit()
                    problem_hierarchy[Scenario_string] = RootCauses_string # updated on 11292023
        # print(asset_hierarchy)
        return asset_hierarchy, problem_hierarchy #updated for dailyHOS # updated on 11292023

    def applyInferredStatus(self, status):
        self.cursor.execute('select "Level3_Scenario", "Level4_RootCauses" from public."RCA_levels"') #updated for PostgreSQL
        row = self.cursor.fetchall()
        self.conn.commit()
        # print(row)
        scenarios_and_rootcauses = {}
        for item in row:
            scenarios_and_rootcauses[item[0]] = item[1].split(",")
        # print(scenarios_and_rootcauses)
        for key in scenarios_and_rootcauses.keys():
            if len(scenarios_and_rootcauses[key]) > 1:
                for rootcause in scenarios_and_rootcauses[key]:
                    if rootcause in status.keys():
                        if str(status[rootcause]) == 'True' and (str(status[key]) == 'False' or str(status[key]) == 'Unknown'):
                            # print('scenario=> ', key, 'scenario_status=> ', status[key], 'rootcause=> ', rootcause, 'rootcause_status=> ', status[rootcause])
                            self.cursor.execute('''update public."RCA_update" set "Status" = 'InferredTrue' where "scenarioName" = %s''', [key]) #updated for PostgreSQL
                            self.conn.commit()
                            status[key] = 'InferredTrue'
        return status
    
    def updateRCAstatus(self, Prestatus, running_status, status, onboard_timestamp, available_scenarios, rules, problem_hierarchy): #updated on 12122023
        # assets = ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'BOGH', 'WUH', 'GWHS', 'GWHE', 'SC']
        assets = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
                  'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 
                  'GCU', 'INCIN'] #updated on 11292023
        # print("Prestatus dict=>", Prestatus)
        # print("status dict=>", status)
        #below is the case when some problem has been modified in template, but previously it was present in Prestatus
        #@@@@@@@@@@ updated on 11292023 from here. only first line is updated in this block, rest has only indentation
        if self.compare_pre_and_curr_status == 1: #in production, we dont need to compare prestatus and status all the time, because no update will happen in templates there
            for scenario in Prestatus.keys():
                if scenario not in status.keys(): 
                    status[scenario] = 'NAnow_Modified'
            #below is the case when a new problem is added in template, and it was absent previously in Prestatus
            # for scenario in status.keys(): #not all problems need to be checked, only scenarios should be compared between old(prestatus) and new(available_scenarios) list
            for scenario in available_scenarios:
                if scenario not in Prestatus.keys():
                    if scenario in status: 
                        Prestatus[scenario] = [onboard_timestamp, status[scenario]] #if not in Prestatus, add it to Prestatus
                        #but this is added here in dict, its still not available in db, so insert in db too, so that could be updated ---
                        # in the end of this function
                    else: #scenario not in status => there are chances that some scenario was available in RCA_ID, but later it was deactivated from master sheet (implement = 0).
                        Prestatus[scenario] = [onboard_timestamp, 'NAnow_Modified']
                    self.cursor.execute('insert into public."Prestatus" values(%s,%s,%s)', [scenario, Prestatus[scenario][0], Prestatus[scenario][1]]) #updated for PostgreSQL
        #@@@@@@@@@@ updated on 11292023 till here
        # for scenario in Prestatus.keys():
        
        for scenario in available_scenarios:
            # if scenario == 'SC_Outlet_customer_temp_too_low':
            #     print('here=>', status['SC_Outlet_customer_temp_too_low'])
            #@@@@@@@@@@@@@@@@ updated on 11292023 from here. no need to run a loop, just use split operation to find asset
            # for i in range(len(assets)):
            #     if assets[i]+"_" in scenario:
            #         asset = assets[i]
            #         break
            asset = scenario.split("_")[0]
            
            #deactivated the block on 12122023 from here
            # if running_status[asset] == 0: #if asset is not running
            #     Scenario_status = 'Unknown_AssetNotRunning'
            # elif running_status[asset] == 1:#running
            #     if scenario in status.keys():
            #         Scenario_status = str(status[scenario])
            #     else:
            #         Scenario_status = 'Unknown'
            #deactivated the block on 12122023 till here

            Scenario_status = status[scenario] #updated on 12122023

            if self.test_run == 1:
                Scenario_status = 'True' #forced True just for testing
            if Scenario_status == 'True' or Scenario_status == 'InferredTrue':
                #@@@@@@@@@@@@@updated on 11292023 from here to avoid querying rca levels in every loop
                # self.cursor.execute("select Level4_RootCauses from RCA_levels where Level3_Scenario = (?)", scenario)
                # row = self.cursor.fetchall()
                # self.conn.commit()
                # # print(scenario)
                # # print(row)
                # # print(len(row))
                # # print(scenario)
                # RootCauses = row[0][0]
                # print(RootCauses)
                RootCauses = problem_hierarchy[scenario]
                active = {}
                non_active = {}
                # print(len(RootCauses))
                if len(RootCauses) == 0:
                    active_string = 'None'
                    non_active_string = 'None'
                else:
                    RootCauses = RootCauses.split(",")           
                    active = {}
                    non_active = {}
                    for rootcause in RootCauses:
                        if rootcause in status.keys():
                            RootCause_status = str(status[rootcause])
                        else:
                            RootCause_status = 'Unknown'

                        # print(RootCause_status)
                        rootcause = rootcause.split("_") #updated on 12122023
                        rootcause = "_".join(rootcause[1:]) #updated on 12122023
                        if RootCause_status == 'True':
                            active[rootcause] = RootCause_status
                        # elif RootCause_status == 'InferredTrue':
                        #     RootCause_status = 'False'
                        #     active[rootcause] = RootCause_status
                        elif RootCause_status == 'Unknown':
                            non_active[rootcause] = RootCause_status
                        else:
                            # if RootCause_status == 'Suspected' or RootCause_status == 'InferredTrue':
                            RootCause_status = 'False'
                            non_active[rootcause] = RootCause_status
                    if len(active) == 0:
                        active_string = 'None'
                    else:
                        active_string = json.dumps(active)
                    if len(non_active) == 0:
                        non_active_string = 'None'
                    else:
                        non_active_string = json.dumps(non_active)
                    to_remove = '{}"'
                    for item in to_remove:
                        active_string = active_string.replace(item, "")
                        active_string = active_string.replace(",", "   ---   ")
                        non_active_string = non_active_string.replace(item, "")
                        non_active_string = non_active_string.replace(",", "   ---   ")
                # abbreviations = ['LDC1', 'LDC2', 'HDC1', 'HDC2', 'FVAP', 'LNGVAP', 'BOGHTR', 'WUHTR', 'GWHSTM', 'GWHE', 'SCLR']
                # for abb in abbreviations:
                #@@@@@@@@@@@@@ updated on 11292023 from here. dont need to search for asset. asset is already found above.
                # for asset in assets:
                #     if asset+"_" in scenario:

                # Scenario_friendly_name = scenario.replace(asset+"_", "") #updated on 12122023
                Scenario_friendly_name = scenario.split("_") #updated on 12122023
                Scenario_friendly_name = "_".join(Scenario_friendly_name[1:]) #updated on 12122023
    
                # active_string = active_string.replace(asset+"_", "") #updated on 12122023
                # non_active_string = non_active_string.replace(asset+"_", "") #updated on 12122023
                #@@@@@@@@@@@@@ updated on 11292023 till here.
                self.cursor.execute('select "Level3_Scenario", "ScenarioStatus", "Level4_ActiveRootCauses", "Level4_OtherRootCauses" from public."RCA_Active" where "ScenarioID" = %s', [scenario]) #updated for PostgreSQL
                row = self.cursor.fetchall()
                self.conn.commit()
                # print(row)
                date_format = "%d/%m/%Y %H:%M:%S"
                now = pd.to_datetime(datetime.now(), format = date_format)
                # print(now)
                #rule for scenario, and rootcauses too if there are active rootcauses available
                rule = scenario +" => "+ rules[scenario] + " --- "
                if len(active.keys()) > 0:
                    for key in active.keys():
                        key = asset+"_"+key #updated on 12122023
                        rule = rule + key + " => " + rules[key] + " --- "
                rule = rule[:-5]
                if self.hide_rules == 1:
                    rule = 'NA'
                if len(row) == 0:
                        
                        self.cursor.execute('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)', [str(now), Scenario_friendly_name, Scenario_status, active_string, non_active_string, scenario, onboard_timestamp, rule]) #updated for PostgreSQL
                        self.conn.commit()
                        # ActivePeriod = 0
                        pre_scenario_status = Prestatus[scenario][1]
                        StartTime_onboard = Prestatus[scenario][0]
                        # StartTime = pd.to_datetime(StartTime)
                        StartTime_onboard = pd.to_datetime(StartTime_onboard)
                        # EndTime = datetime.datetime.now()
                        EndTime_onboard = pd.to_datetime(onboard_timestamp)
                        
                        ActivePeriod = (EndTime_onboard - StartTime_onboard).total_seconds()/60
                        
                        ActivePeriod = float("{0:.2f}".format(ActivePeriod))
                        # pre_scenario_status = 'Unknown'
                        self.cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(StartTime_onboard), str(EndTime_onboard), int(ActivePeriod), Scenario_friendly_name, pre_scenario_status, Scenario_status, active_string, non_active_string, scenario, str(now), rule, "Open", "None"]) #updated for PostgreSQL
                        self.conn.commit()
                        # Prestatus[scenario] = [str(EndTime), pre_scenario_status]
                        # Prestatus[scenario] = [str(EndTime_onboard), pre_scenario_status] #deact on 03012023
                        Prestatus[scenario] = [str(EndTime_onboard), Scenario_status]

                else:
                    data = row[0]
                    pre_scenario = data[0]
                    pre_scenario_status = data[1]
                    pre_active_string = data[2]
                    pre_non_active_string = data[3]
                    # StartTime = Prestatus[scenario][0]
                    StartTime_onboard = Prestatus[scenario][0]
                    # EndTime = datetime.datetime.now()
                    # StartTime = pd.to_datetime(StartTime)
                    # EndTime = pd.to_datetime(EndTime)
                    StartTime_onboard = pd.to_datetime(StartTime_onboard)
                    EndTime_onboard = pd.to_datetime(onboard_timestamp)

                    Prestatus[scenario] = [str(StartTime_onboard), Scenario_status] #if everything is same, nothing is going to change in Prestatus
                    #i think even deleting above line won't change anything. purpose is to keep prestatus same as before if there is no change in any of items below
                    # print(data)
                    if Scenario_friendly_name != pre_scenario or Scenario_status != pre_scenario_status or active_string != pre_active_string or non_active_string != pre_non_active_string:
                        self.cursor.execute('delete from public."RCA_Active" where "ScenarioID" = %s', [scenario]) #updated for PostgreSQL
                        self.conn.commit()
                        self.cursor.execute('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)', [str(now), Scenario_friendly_name, Scenario_status, active_string, non_active_string, scenario, onboard_timestamp, rule]) #updated for PostgreSQL
                        self.conn.commit()
                        #find the pre-status and start-time
                        ActivePeriod = (EndTime_onboard - StartTime_onboard).total_seconds()/60
                        ActivePeriod = float("{0:.2f}".format(ActivePeriod))
                        # print(ActivePeriod)
                        self.cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(StartTime_onboard), str(EndTime_onboard), int(ActivePeriod), Scenario_friendly_name, pre_scenario_status, Scenario_status, active_string, non_active_string, scenario, str(now), rule, "Open", "None"]) #updated for PostgreSQL
                        self.conn.commit()
                        Prestatus[scenario] = [str(EndTime_onboard), Scenario_status] #if something updated, Prestatus should be updated with current time and current status
                    # EndTime = datetime.datetime.now()
                    # Prestatus[scenario] = [str(EndTime), Scenario_status]
            elif Scenario_status == 'False' or Scenario_status == 'Unknown' or Scenario_status == 'Unknown_AssetNotRunning' or Scenario_status == 'NAnow_Modified' or Scenario_status == 'Unknown_ComponentNotRunning': #updated on 12122023
                self.cursor.execute('delete from public."RCA_Active" where "ScenarioID" = %s', [scenario]) #updated for PostgreSQL
                self.conn.commit()
                pre_scenario_status = Prestatus[scenario][1]
                # if scenario == 'LDC1_Overtemperature_of_bearings':
                #     print(scenario, "---->", Scenario_status, pre_scenario_status)
                date_format = "%d/%m/%Y %H:%M:%S"
                now = pd.to_datetime(datetime.now(), format = date_format)
                StartTime_onboard = Prestatus[scenario][0]
                # EndTime = datetime.datetime.now()
                StartTime_onboard = pd.to_datetime(StartTime_onboard)
                # EndTime = pd.to_datetime(EndTime)
                EndTime_onboard = pd.to_datetime(onboard_timestamp)

                # ---------------
                # abbreviations = ['LDC1', 'LDC2', 'HDC1', 'HDC2', 'FVAP', 'LNGVAP', 'BOGHTR', 'WUHTR', 'GWHSTM', 'GWHE', 'SCLR']
                # for abb in abbreviations:
                #@@@@@@@@@@@@@ updated on 11292023 from here. dont need to search for asset. asset is already found above.
                # for asset in assets:
                #     if asset in scenario:
                Scenario_friendly_name = scenario.replace(asset+"_", "")
                #@@@@@@@@@@@@@ updated on 11292023 till here
                # ---------------
                # if pre_scenario_status == 'True' or pre_scenario_status == 'InferredTrue' or pre_scenario_status == 'False' or pre_scenario_status == 'Unknown' and ((Scenario_status == 'False' or Scenario_status == 'Unknown') and Scenario_status != pre_scenario_status):
                if pre_scenario_status != Scenario_status:
                        ActivePeriod = (EndTime_onboard - StartTime_onboard).total_seconds()/60
                        ActivePeriod = float("{0:.2f}".format(ActivePeriod))
                        # print(ActivePeriod)
                        active_string = 'None' #Scenario has turned to false or unknown in this case, so no need to explore into active or non-active string
                        non_active_string = 'None'
                        
                        # print("here", scenario, "---->", Scenario_friendly_name)
                        self.cursor.execute('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [str(StartTime_onboard), str(EndTime_onboard), int(ActivePeriod), Scenario_friendly_name, pre_scenario_status, Scenario_status, active_string, non_active_string, scenario, str(now), 'NA', "Open", "None"]) #updated for PostgreSQL
                        self.conn.commit()
                        Prestatus[scenario] = [str(EndTime_onboard), Scenario_status] #if status is updated, Prestatus should be updated with current time and current status

        for scenario in Prestatus.keys(): #update Prestatus table for up-to-date status and its timestamp
            
            self.cursor.execute('update public."Prestatus" set "TimeStamp" = %s where "Scenario" = %s', [Prestatus[scenario][0], scenario]) #updated for PostgreSQL
            self.conn.commit()
            self.cursor.execute('update public."Prestatus" set "Status" = %s where "Scenario" = %s', [Prestatus[scenario][1], scenario]) #updated for PostgreSQL
            self.conn.commit()

        return Prestatus


    def saveHOS(self, previous_timestamp, previous_status, HOS_dict, onboard_timestamp, running_status, asset_hierarchy, HOS_TodaySoFar): #updated for DailyHOS):
        # previous_timestamp = pd.to_datetime(previous_timestamp, format = "%Y/%m/%d %H:%M:%S")
        # onboard_timestamp = pd.to_datetime(onboard_timestamp, format = "%Y/%m/%d %H:%M:%S")
        #above two lines did not work on linux so hyphen is used below in time format.
        previous_timestamp = pd.to_datetime(previous_timestamp, format = "%Y-%m-%d %H:%M:%S")
        onboard_timestamp = pd.to_datetime(onboard_timestamp, format = "%Y-%m-%d %H:%M:%S")
        # print(previous_timestamp)
        # print(HOS_dict)
        # print(onboard_timestamp)
        #DailyHOS
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #below whole block updated for DailyHOS from here

        # print(asset_hierarchy)
        # print(HOS_dict)
        # print(len(HOS_dict.keys()))
        # print(len(running_status.keys()))
        # print(HOS_TodaySoFar)
        asset_hierarchy_assets = []
        for key in asset_hierarchy.keys():
            asset_hierarchy_assets.append(key)
            asset_hierarchy_assets = asset_hierarchy_assets + asset_hierarchy[key]
        # print(len(asset_hierarchy_assets))
        for item in HOS_dict.keys():
            if item not in asset_hierarchy_assets:
                print(item, "=> not present in hierarchy")

        # print(running_status)
        new_day = False
        # print(previous_timestamp.date())
        # print(onboard_timestamp.date())
        elapsedsofar = {}
        for key in asset_hierarchy.keys():
            if previous_status[key] == 1 and running_status[key] == 1:
                elapsed = onboard_timestamp - previous_timestamp
                elapsed = elapsed.total_seconds()
                if elapsed > 180.0: #if many simfiles are missing, it should not be replicated in HOS
                    elapsed = 60.0
                elapsed = elapsed/3600
                elapsedsofar[key] = HOS_TodaySoFar[key] + elapsed
            else:
                elapsedsofar[key] = HOS_TodaySoFar[key] #if stopped, elapsed so far remains same as previous

            if len(asset_hierarchy[key]) > 0:
                for value in asset_hierarchy[key]:
                    if previous_status[value] == 1 and running_status[value] == 1:
                        elapsed = onboard_timestamp - previous_timestamp
                        elapsed = elapsed.total_seconds()
                        if elapsed > 180.0: #if many simfiles are missing, it should not be replicated in HOS
                            elapsed = 60.0
                        elapsed = elapsed/3600
                        elapsedsofar[value] = HOS_TodaySoFar[value] + elapsed
                    else:
                        elapsedsofar[value] = HOS_TodaySoFar[value]

        if previous_timestamp.date() != onboard_timestamp.date():
            new_day = True
            print('new day started, so dailyHOS to write')
        if new_day:
            for key in asset_hierarchy.keys():
                hvalue = elapsedsofar[key]
                if hvalue > 24.0 and hvalue < 24.3: # updated on 12062023
                    hvalue = 24.0
                hvalue = "{0:.3f}".format(hvalue) #hours value # updated on 12032023
                self.cursor.execute('insert into public."DailyHOS" values(%s,%s,%s,%s)', [str(previous_timestamp.date()), key, "-", hvalue]) #updated for PostgreSQL
                self.conn.commit()
                self.cursor.execute('update public."HOS" set "DailyHOS" = %s where "Asset" = %s', [hvalue, key]) #updated for PostgreSQL
                self.conn.commit()
                HOS_TodaySoFar[key] = 0 #reset it as new day started and dailyHOS is already written for previous day
                if len(asset_hierarchy[key]) > 0:
                    for value in asset_hierarchy[key]:
                        hvalue = elapsedsofar[value]
                        if hvalue > 24.0 and hvalue < 24.3: # updated on 12062023
                            hvalue = 24.0
                        hvalue = "{0:.3f}".format(hvalue) # updated on 12032023
                        self.cursor.execute('insert into public."DailyHOS" values(%s,%s,%s,%s)', [str(previous_timestamp.date()), key, value, hvalue]) #updated for PostgreSQL
                        self.conn.commit()
                        self.cursor.execute('update public."HOS" set "DailyHOS" = %s where "Asset" = %s', [hvalue, value]) #updated for PostgreSQL
                        self.conn.commit()
                        HOS_TodaySoFar[value] = 0
            self.cursor.execute('update public."HOS" set "TodaySoFar" = 0') #updated for PostgreSQL #reset todaysofar as new day started
            self.conn.commit()

        else:
            for key in asset_hierarchy.keys():
                hvalue = "{0:.3f}".format(elapsedsofar[key]) # updated on 12032023
                # print("type=>", type(hvalue))
                self.cursor.execute('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s', [hvalue, key]) #updated for PostgreSQL
                self.conn.commit()
                HOS_TodaySoFar[key] = float(hvalue) # updated on 12032023
                if len(asset_hierarchy[key]) > 0:
                    for value in asset_hierarchy[key]:
                        hvalue = "{0:.3f}".format(elapsedsofar[value]) # updated on 12032023
                        self.cursor.execute('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s', [hvalue, value]) #updated for PostgreSQL
                        self.conn.commit()
                        HOS_TodaySoFar[value] = float(hvalue)  # updated on 12032023

    
        #above whole block updated for DailyHOS till here
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #below is for current HOS calc
        for asset in HOS_dict.keys():
            previous_service_time = HOS_dict[asset]
            current_status = running_status[asset]
            # print(current_status)
            
            if previous_status[asset] == 1 and current_status == 1:
                elapsed_running_time = onboard_timestamp - previous_timestamp
                elapsed_running_time = elapsed_running_time.total_seconds() # updated for DailyHOS
                if elapsed_running_time > 180.0: # updated for DailyHOS
                    elapsed_running_time = 60.0 # updated for DailyHOS
                elapsed_running_time = elapsed_running_time/3600 #in hours # updated for DailyHOS
                # print("in hours:", HOS)
                HOS =  previous_service_time + elapsed_running_time
                if HOS < 0:
                    HOS = 0
            else:
                HOS = previous_service_time

            HOS_dict[asset] = HOS
            previous_status[asset] = current_status
        for asset in HOS_dict.keys():
            self.cursor.execute('update public."HOS" set "HOS" = %s where "Asset" = %s', ["{0:.3f}".format(HOS_dict[asset]), asset]) #updated for PostgreSQL
            self.conn.commit()
            self.cursor.execute('update public."HOS" set "TimeStamp" = %s where "Asset" = %s', [str(onboard_timestamp), asset]) #updated for PostgreSQL
            self.conn.commit()
            
        previous_timestamp = onboard_timestamp
        
        # self.cursor.execute("update Application_status set Value = (?) where Item = 'AssetRunStatusUntil'", str(previous_timestamp))
        # self.conn.commit()
        return previous_timestamp, previous_status, HOS_dict, HOS_TodaySoFar #updated for DailyHOS
        # return previous_status, previous_timestamp

    def maintenanceAlarm(self, SOR_time, HOS_dict):
        reset_period = 24*7 #adding 7 days to reset by program itself after 7 days
        month_hours = np.array([720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200, 7920, 8640, 9360,
                                10080, 10800, 11520, 12240, 12960, 13680, 14400, 15120, 15840, 16560, 17280,
                                18000, 18720, 19440, 20160, 20880, 21600, 22320, 23040, 23760, 24480, 25200,
                                25920, 26640, 27360, 28080, 28800, 29520, 30240, 30960, 31680, 32400, 33120,
                                33840, 34560, 35280, 36000, 36720, 37440, 38160, 38880, 39600, 40320, 41040, 
                                41760, 42480, 43200])
        three_months_hours = np.array([2160, 4320, 6480, 8640, 10800, 12960, 15120, 17280, 19440, 21600, 23760,
                                     25920, 28080, 30240, 32400, 34560, 36720, 38880, 41040, 43200])
        six_months_hours = np.array([4320, 8640, 12960, 17280, 21600, 25920, 30240, 34560, 38880, 43200])
        year_hours = np.array([8640, 17280, 25920, 34560, 43200])
        ten_k_hours = np.array([10000, 20000, 30000, 40000, 50000])
        thirty_months = np.array([21600, 43200])
        five_year_hours = np.array([43200])
        ten_year_hours = np.array([86400])
        month_hours_reset = month_hours + reset_period
        three_months_hours_reset = three_months_hours + reset_period
        six_months_hours_reset = six_months_hours + reset_period
        year_hours_reset = year_hours + reset_period
        ten_k_hours_reset = ten_k_hours + reset_period
        five_year_hours_reset = five_year_hours + reset_period
        ten_year_hours_reset = ten_year_hours + reset_period
        thirty_months_reset = thirty_months + reset_period
        current_time = datetime.now()
        current_time = pd.to_datetime(current_time, format = "%d/%m/%Y %H:%M:%S")
        SOR_time = pd.to_datetime(SOR_time)
        calender_time_elapsed = current_time - SOR_time
        calender_hours_elapsed = calender_time_elapsed.total_seconds()/3600 #in hours
        # calender_hours_elapsed = 4321 #to test for 6month alarm
        # HOS = 4321
        # calender_hours_elapsed = 8641 #to test for 1year alarm
        # HOS = 8641
        # calender_hours_elapsed = 43201 #to test for 5years alarm
        # HOS = 43201
        self.cursor.execute('''update public."Calender_time" set "TimeStamp" = %s where "Kind" = 'Elapsed_time';''', [str(current_time)]) #updated for PostgreSQL
        self.conn.commit()
        self.cursor.execute('''update public."Calender_time" set "Value" = %s where "Kind" = 'Elapsed_time';''', [calender_hours_elapsed]) #updated for PostgreSQL
        self.conn.commit()
        maintenance_alarm_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        maintenance_alarms_list = ['LD1_half_year_HOS', 'LD1_year_HOS', 'LD1_5years_HOS', 'LD2_half_year_HOS', 'LD2_year_HOS', 'LD2_5years_HOS',
                                   'HD1_3months_HOS', 'HD1_half_year_HOS', 'HD1_year_HOS', 'HD1_5years_HOS', 'HD1_10years_HOS', 'HD2_3months_HOS',
                                    'HD2_half_year_HOS', 'HD2_year_HOS', 'HD2_5years_HOS', 'HD2_10years_HOS', 'SC_10000hrs_HOS', 'SC_3months_HOS',
                                    'SC_year_HOS', 'SC_5years_HOS', 'FV_half_year_HOS', 'FV_year_HOS', 'FV_30months_HOS', 'FV_5years_HOS', 'LNGV_half_year_HOS',
                                    'LNGV_year_HOS', 'LNGV_30months_HOS', 'LNGV_5years_HOS', 'GWHS_month_HOS', 'GWHS_year_HOS', 'GWHS_5years_HOS']
        
        for asset in HOS_dict.keys():
            if asset in ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'GWHS', 'SC']:

                # categories = ['month_hours', 'three_months_hours', 'six_months_hours', 'year_hours', 'ten_k_hours', 'thirty_months', 'five_year_hours', 'ten_year_hours']

                list_HOS = [asset+'_month_HOS', asset+'_3months_HOS', asset+'_half_year_HOS', asset+'_year_HOS', asset+'_10000hrs_HOS',
                            asset+'_30months_HOS', asset+'_5years_HOS', asset+'_10years_HOS']
                # dict_HOS = {asset+'_half_year_HOS': six_months_hours, asset+'_year_HOS': year_hours, asset+'_5years_HOS': five_year_hours}
                dict_HOS = {asset+'_month_HOS': month_hours, asset+'_3months_HOS': three_months_hours, asset+'_half_year_HOS': six_months_hours, 
                            asset+'_year_HOS': year_hours, asset+'_10000hrs_HOS': ten_k_hours, asset+'_30months_HOS': thirty_months, 
                            asset+'_5years_HOS': five_year_hours, asset+'_10years_HOS': ten_year_hours}

                # dict_reset_HOS = {asset+'_half_year_HOS': six_months_hours_reset, asset+'_year_HOS': year_hours_reset, asset+'_5years_HOS': five_year_hours_reset}

                dict_reset_HOS = {asset+'_month_HOS': month_hours_reset, asset+'_3months_HOS': three_months_hours_reset, asset+'_half_year_HOS': six_months_hours_reset, 
                            asset+'_year_HOS': year_hours_reset, asset+'_10000hrs_HOS': ten_k_hours_reset, asset+'_30months_HOS': thirty_months_reset, 
                            asset+'_5years_HOS': five_year_hours_reset, asset+'_10years_HOS': ten_year_hours_reset}

                list_calender = ['half_year_calender', 'year_calender', '5years_calender']
                dict_calender = {'half_year_calender': six_months_hours, 'year_calender': year_hours, '5years_calender': five_year_hours}
                dict_reset_calender = {'half_year_calender': six_months_hours_reset, 'year_calender': year_hours_reset, '5years_calender': five_year_hours_reset}

                for item in list_HOS:
                    if item in maintenance_alarms_list:
                        for i in range(len(dict_HOS[item])):
                            if int(HOS_dict[asset]) >= dict_HOS[item][i] and int(HOS_dict[asset]) <= dict_reset_HOS[item][i]:
                                self.cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [1, item]) #updated for PostgreSQL
                                self.conn.commit()
                                self.cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [maintenance_alarm_time, item]) #updated for PostgreSQL
                                self.conn.commit()
                                # print("activated")
                                break
                            
                            else:
                                self.cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [0, item]) #updated for PostgreSQL
                                self.conn.commit()
                                self.cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [maintenance_alarm_time, item]) #updated for PostgreSQL
                                self.conn.commit()
                                # print("deactivated")
                for item in list_calender:
                    for i in range(len(dict_calender[item])):
                        if int(calender_hours_elapsed) >= dict_calender[item][i] and int(calender_hours_elapsed) <= dict_reset_calender[item][i]:
                            self.cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [1, item]) #updated for PostgreSQL
                            self.conn.commit()
                            self.cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [maintenance_alarm_time, item]) #updated for PostgreSQL
                            self.conn.commit()
                            break
                        
                        else:
                            self.cursor.execute('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s', [0, item]) #updated for PostgreSQL
                            self.conn.commit()
                            self.cursor.execute('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s', [maintenance_alarm_time, item]) #updated for PostgreSQL
                            self.conn.commit()

    def saveAlertCount(self):
        total_alerts = {}
        # searchables = ['LD1', 'LD2', 'HD1', 'HD2', 'FV', 'LNGV', 'WUH', 'BOGH', 'GWH', 'SC'] #GWH is used to include both GWHS and GWHE
        searchables = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
                  'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 
                  'GCU', 'INCIN'] #updated list on 12192023
        for asset in searchables:
            self.cursor.execute(f'''select "ScenarioID" from public."RCA_Active" where "ScenarioID" like '{asset}%';''') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()

            total_alerts[asset] = len(row)
        
        # print(total_alerts)
        for key in total_alerts.keys():    
            asset = key
            count = total_alerts[key]
            #updated on 12192023 till here
            self.cursor.execute('update public."Active_count" set "Alert_count" = %s where "Asset" = %s', [count, asset]) #updated for PostgreSQL
            self.conn.commit()
            self.cursor.execute('update public."Active_count" set "TimeStamp" = %s where "Asset" = %s', [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), asset]) #updated for PostgreSQL
            self.conn.commit()

    def totalAvailableScenarios(self):

        total_scenarios = {}
        searchables = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
                  'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 
                  'GCU', 'INCIN'] #updated list on 12192023
        
        for asset in searchables:
            self.cursor.execute(f'''select "Level3_ScenarioName" from public."RCA_ID" where "Level3_ScenarioName" like '{asset}%';''') #updated for PostgreSQL
            row = self.cursor.fetchall()
            self.conn.commit()

            total_scenarios[asset] = len(row)
        # print(total_scenarios)

        for key in total_scenarios.keys():
            asset = key
            count = total_scenarios[key]
            self.cursor.execute('update public."Active_count" set "Total_count" = %s where "Asset" = %s', [count, asset]) #updated for PostgreSQL
            self.conn.commit()

    def runningStatusLogging(self, running_status, onboard_timestamp):
        #update
        not_to_log = ['Cargo_vapor', 'HD', 'FBOG', 'NBOG', 'Fuel_Consumption', 'Fuel_Economy'] #no need to log these, as these are only creating in running status for key outputs on dashboard.
        # assets = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
        #           'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO1', 'FG']
        for asset in running_status.keys():
            query = f'''update public."Running_status_update" set "Status" = {running_status[asset]} where "Asset" = '{asset}';''' #updated for PostgreSQL
            self.cursor.execute(query)
            self.conn.commit()
        #history
        # timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table = "Running_status_history"
        self.cursor.execute('select "column_name" from information_schema.columns where "table_name" = %s', [table]) #updated for PostgreSQL
        row = self.cursor.fetchall()
        self.conn.commit()
        required_columns = [item[0].replace("_running_status", "") for item in row][1:]
        # print(required_columns)
        # len(required_columns)
        query = f"'{onboard_timestamp}', "
        for col in required_columns:
            query = query + f"{running_status[col]}, "
        query = query[:-2] + ")"
        query = f'insert into public."Running_status_history" values({query}' #updated for PostgreSQL
        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

    def importRCAtemplates(self):
        # sheets = ['FV', 'LNGV', 'BOGH', 'WUH', 'GWHS', 'LD1', 'LD2', 'HD1', 'HD2', 'SC']
        sheets = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
                  'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO', 'MEFG', 'GEFG', 
                  'GCU', 'INCIN'] #updated on 11292023
        # master_sheet_path = 'C:\\Users\\iu\\Documents\\SLM clone\\assets\\SHI Rules Master sheet_062223_rev2.4.3.xlsx'
        master_sheet_path = self.RCA_mastersheet_path
        decrypted_workbook = io.BytesIO()
        with open(master_sheet_path, 'rb') as file:
            master_sheet = msoffcrypto.OfficeFile(file)
            master_sheet.load_key(self.ent)
            master_sheet.decrypt(decrypted_workbook)
        # for sheet in sheets:
        #     vars()[sheet] = pd.read_excel(master_sheet_path, sheet_name=sheet) #this works fine, but to check running status it gets confused with this method ---
                                                                                #   because method for changing df name to string is not well known
        # rca_dfs.append(vars()[sheet]) #this creates a list of dfs, each df will be a variable having name like FV, LNGV etc. as given in above 'sheets' list.
        
        # LD1_df = pd.read_excel(master_sheet_path, sheet_name='LD1')
        # LD2_df = pd.read_excel(master_sheet_path, sheet_name='LD2')
        # HD1_df = pd.read_excel(master_sheet_path, sheet_name='HD1')
        # HD2_df = pd.read_excel(master_sheet_path, sheet_name='HD2')
        # LNGV_df = pd.read_excel(master_sheet_path, sheet_name='LNGV')
        # FV_df = pd.read_excel(master_sheet_path, sheet_name='FV')
        # BOGH_df = pd.read_excel(master_sheet_path, sheet_name='BOGH')
        # WUH_df = pd.read_excel(master_sheet_path, sheet_name='WUH')
        # GWH_df = pd.read_excel(master_sheet_path, sheet_name='GWH')
        # SC_df = pd.read_excel(master_sheet_path, sheet_name='SC')
        # IG_df = pd.read_excel(master_sheet_path, sheet_name='IG')
        # NG1_df = pd.read_excel(master_sheet_path, sheet_name='NG1')
        # NG2_df = pd.read_excel(master_sheet_path, sheet_name='NG2')
        # ME1_df = pd.read_excel(master_sheet_path, sheet_name='ME1')
        # ME2_df = pd.read_excel(master_sheet_path, sheet_name='ME2')
        # MEEG_df = pd.read_excel(master_sheet_path, sheet_name='MEEG')
        # GEEG_df = pd.read_excel(master_sheet_path, sheet_name='GEEG')
        # AB_df = pd.read_excel(master_sheet_path, sheet_name='AB')
        # VA_df = pd.read_excel(master_sheet_path, sheet_name='VA')
        # LO_df = pd.read_excel(master_sheet_path, sheet_name='LO')
        # BLST_df = pd.read_excel(master_sheet_path, sheet_name='BLST')
        # BLG_df = pd.read_excel(master_sheet_path, sheet_name='BLG')
        # GE1_df = pd.read_excel(master_sheet_path, sheet_name='GE1')
        # GE2_df = pd.read_excel(master_sheet_path, sheet_name='GE2')
        # GE3_df = pd.read_excel(master_sheet_path, sheet_name='GE3')
        # GE4_df = pd.read_excel(master_sheet_path, sheet_name='GE4')
        # CT1_df = pd.read_excel(master_sheet_path, sheet_name='CT1')
        # CT2_df = pd.read_excel(master_sheet_path, sheet_name='CT2')
        # CT3_df = pd.read_excel(master_sheet_path, sheet_name='CT3')
        # CT4_df = pd.read_excel(master_sheet_path, sheet_name='CT4')
        # FW_df = pd.read_excel(master_sheet_path, sheet_name='FW')
        # FO1_df = pd.read_excel(master_sheet_path, sheet_name='FO1')
        # FG_df = pd.read_excel(master_sheet_path, sheet_name='FG')


        # rca_dfs = [LD1_df, LD2_df, HD1_df, HD2_df, LNGV_df, FV_df, BOGH_df, WUH_df, GWH_df, SC_df, IG_df, NG1_df, NG2_df, ME1_df, ME2_df, MEEG_df, GEEG_df, 
        #           AB_df, VA_df, LO_df, BLST_df, BLG_df, GE1_df, GE2_df, GE3_df, GE4_df, CT1_df, CT2_df, CT3_df, CT4_df, FW_df, FO1_df, FG_df]
        
        rca_dfs=[]
        for sheet in sheets:
            rca_dfs.append(pd.read_excel(decrypted_workbook,sheet_name=sheet))
        
        for df in rca_dfs: #below line is added just for linux, setting first item to string 'None' to avoid its confusion with nan in linux. won't harm on windows btw
            df.at[0, 'Parent_Node'] = 'None'
        # print(rca_dfs)
        return rca_dfs

    def rcaID(self, rca_dfs):
        rca_id = {}
        for i in range(len(rca_dfs)):
            df = rca_dfs[i]
            # print(df, "started")
            df = df.loc[:, ['Problem_Name', 'Level', 'Implement', 'Priority', 'AdviceMessage']] #updated on 11292023
            df.rename(columns = {'Problem_Name':'Level3_ScenarioName'}, inplace = True)
            mask = df['Level']=='SCENARIO'
            df = df[mask]
            mask = df['Implement'] == 1.0 #updated on 11292023
            df = df[mask] #updated on 11292023
            if i == 0:
                final_df = df.copy()
            else:
                final_df = pd.concat([final_df, df], axis=0)
        final_df = final_df.drop_duplicates('Level3_ScenarioName', keep='first').reset_index() #updated for PostgreSQL
        # final_df.to_sql('RCA_ID', self.engine, index=False, if_exists='replace') #updated for PostgreSQL #replace(drop) table does not work with pgsql because view depends on this table
        # print(final_df)
        # print(final_df.columns)
        self.cursor.execute('truncate table public."RCA_ID"') #updated for PostgreSQL
        self.conn.commit() #updated for PostgreSQL
        for i in range(len(final_df.index)): #updated for PostgreSQL
            Level3_ScenarioName = final_df.loc[i]['Level3_ScenarioName'] #updated for PostgreSQL
            Level = final_df.loc[i]['Level'] #updated for PostgreSQL
            Implement = final_df.loc[i]['Implement'] #updated for PostgreSQL
            Priority = final_df.loc[i]['Priority'] #updated for PostgreSQL
            AdviceMessage = final_df.loc[i]['AdviceMessage'] #updated for PostgreSQL
            self.cursor.execute('insert into public."RCA_ID" values (%s, %s, %s, %s, %s)', [Level3_ScenarioName, Level, int(Implement), float(Priority), AdviceMessage]) #updated for PostgreSQL
            self.conn.commit() #updated for PostgreSQL

        available_scenarios = final_df['Level3_ScenarioName'].values.tolist()
        return available_scenarios

    def updateSignal(self):
        self.cursor.execute('select * from public."Templates_update"') #updated for PostgreSQL
        row = self.cursor.fetchall()
        self.conn.commit()
        # print(row)
        templates_updated = row[0][1] #string
        # print(updated)
        return templates_updated

    def findRules(self, rca_dfs):
        self.cursor.execute('truncate public."RCA_rules"') #updated for PostgreSQL
        self.conn.commit()
        rules = {}
        keys = {}
        for df in rca_dfs:
            df.fillna('blank', inplace = True) #updated on 12032023 #changed from nan to blank
            previous = 'none' #something to kick-start with
            for i in range(len(df.index)): #go row by row
                scenario = df.loc[i]['Problem_Name']
                if scenario != previous: #if its a new problem started, add only one line to rule for now
                    # tag = df.loc[i]['Standard_Key'].replace('-', '_')
                    tag = df.loc[i]['Standard_Key']
                    additional_cond = df.loc[i]['Additional condition']
                    operator = df.loc[i]['Condition']
                    threshold = str(df.loc[i]['Threshold'])
                    logic = df.loc[i]['Logic']
                    if tag != 'blank': #updated on 12032023 #changed from nan to blank
                        if 'Intermediate' in tag:
                            rule = f" ({rules[tag]}) {logic} "
                            rule = rule.replace("blank", "")
                            rule = rule.strip()
                            rules[scenario] = rule

                            key = keys[tag]
                            keys[scenario] = key

                        else:
                            rule = f" {tag} {operator} {threshold} {additional_cond} {logic} "
                            rule = rule.replace("blank", "")
                            rule = rule.strip()
                            rules[scenario] = rule

                            key = tag
                            keys[scenario] = key
                    elif tag == 'blank': #updated on 12032023 #changed from nan to blank
                        rules[scenario] = 'None'
                        keys[scenario] = 'None'
                    previous = scenario
                elif scenario == previous: # if it continues add each line to previous rule
                    # tag = df.loc[i]['Standard_Key'].replace('-', '_')
                    # updated 11212023 at 6pm from here
                    tag = df.loc[i]['Standard_Key']
                    # updated 11212023 at 6pm till here
                    additional_cond = df.loc[i]['Additional condition']
                    operator = df.loc[i]['Condition']
                    threshold = str(df.loc[i]['Threshold'])
                    logic = df.loc[i]['Logic']
                    if tag != 'blank': #updated on 12032023 #changed from nan to blank
                        if 'Intermediate' in tag:
                            rule = rule + f" ({rules[tag]}) {logic} "
                            rule = rule.replace("blank", "")
                            rule = rule.replace("  ", " ")
                            rule = rule.strip()
                            rules[scenario] = rule

                            key = key + ", " + keys[tag]
                            keys[scenario] = key

                        else:
                            rule = rule + f" {tag} {operator} {threshold} {additional_cond} {logic} "
                            rule = rule.replace("blank", "")
                            rule = rule.replace("  ", " ")
                            rule = rule.strip()
                            rules[scenario] = rule

                            key = key + ", " + tag
                            keys[scenario] = key
                    previous = scenario
            #insert rules and standard keys
        for problem in rules.keys():
            if self.hide_rules == 1: #to not to write rules to db
                rules[problem] = 'NA'
            self.cursor.execute('insert into public."RCA_rules" values(%s,%s,%s)', [problem, rules[problem], keys[problem]]) #updated for PostgreSQL
            self.conn.commit()
            
        return rules, keys

    def alarmLoggingforNoKPIassets(self, alarm_tags, tags):
        for tag in alarm_tags:
            self.cursor.execute('update public."Output_Tags" set "Value" = %s where "TagName" = %s', [float(tags[tag]), tag]) #updated for PostgreSQL
            self.conn.commit()

    def findtargetScenarios(self, keys, tags_presence): #updated on 12052023
        problems_to_detect = {}
        # if 'LD2_Overtemp_of_bearings' in keys.keys():
        #     print('################')
        #     print('present')
        #     print('################')
        for problem in keys.keys():
            detect = True #updated on 12052023
            if keys[problem] == 'None':
                detect = True #updated on 12052023
            else:
                needed_tags = keys[problem].split(", ")
                for tag in needed_tags:
                    # if tag not in tags.keys(): #updated on 12052023
                    if tag in tags_presence.keys():
                        if tags_presence[tag] == 0: #updated on 12052023
                            detect = False #updated on 12052023
                            break
                    # else: #updated on 12052023
            if detect: #updated on 12052023
                problems_to_detect[problem] = 1 #updated on 12052023
            else: #updated on 12052023
                problems_to_detect[problem] = 0 #updated on 12052023
                    
        # print(problems_to_detect['ME1_Cylinder_exh_gas_out_temp_High'])
        # print(problems_to_detect['ME1_Starting_air_in_pres_low'])
        # print(problems_to_detect['ME1_Control_air_pres_low'])
        # print(problems_to_detect)
        return problems_to_detect

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enter arguments")
    # Add command-line options
    parser.add_argument("-H", "--host", required=True, help="Hostname or IP address")
    parser.add_argument("-U", "--user", required=True, help="Username")
    parser.add_argument("-P", "--password", required=True, help="Password")
    parser.add_argument("-p", "--port", required=True, help="port")
    parser.add_argument("-D", "--database", required=True, help="PostgreSQL database")
    parser.add_argument("-X", "--excelpwd", required=True, help="Excel sheet password")
    parser.add_argument("-d", "--dwsimpath", required=False, help="DWSIM Path")
    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the options
    host = args.host
    user = args.user
    password = args.password
    pg_database = args.database
    pg_port = args.port
    excel_password=args.excelpwd
    dwsim_path = args.dwsimpath

    if dwsim_path==None:
        dwsim_path=''

    # Your script logic here
    print(f"Host: {host}")
    print(f"Database: {pg_database}")
    print(f"User: {user}")

    object = slmApplication(user,password,excel_password,host,pg_database,pg_port,dwsim_path)      
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230106_000000.sim' where Item = 'Input_file'") #only for temporary test. need to deactivate later

    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230201_113000.sim' where Item = 'Input_file'") #for FV #only for temporary test. need to deactivate later
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230201_123500.sim' where Item = 'Input_file'")  # for LNGV - not run so far
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230201_000000.sim' where Item = 'Input_file'") #to begin with 02/01/2023
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230714_034500.sim' where Item = 'Input_file'")
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230212_182000.sim' where Item = 'Input_file'") #for LD2, flow decreases from around 1000 to around 500. need to test power deviation here
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230213_170500.sim' where Item = 'Input_file'") #WUH starts at 17:18
    # object.cursor.execute("update Application_status set Value = '9929106_1m_20230709_000000.sim' where Item = 'Input_file'") #start from July2023 for full scale
    # object.conn.commit()

    #importing rca templates
    rca_dfs = object.importRCAtemplates()
    
    #collect RCA_ID and save it
    available_scenarios = object.rcaID(rca_dfs)

    #read SOR from db
    object.cursor.execute('''select "TimeStamp" from public."Calender_time" where "Kind" = 'Start_of_run';''') #updated for PostgreSQL
    row = object.cursor.fetchall()
    object.conn.commit()
    SOR_time = row[0][0]
    #read Prestatus from db
    Prestatus = {}
    object.cursor.execute('select * from public."Prestatus"') #updated for PostgreSQL
    row = object.cursor.fetchall()
    object.conn.commit()
    # print(row)
    Prestatus = {}
    for item in row:
        Prestatus[item[0]] = [item[1], item[2]]
    # print("prestatus are recovered from DB")
    # print(Prestatus)

    HOS_dict = {}
    HOS_TodaySoFar = {} #updated for DailyHOS
    object.cursor.execute('select "Asset", "HOS", "TodaySoFar" from public."HOS"') #updated for PostgreSQL #updated for DailyHOS
    asset_HOS = object.cursor.fetchall()
    object.conn.commit()
    for item in asset_HOS:
        HOS_dict[item[0]] = item[1]
        HOS_TodaySoFar[item[0]] = item[2] #updated for DailyHOS
    #previous HOS are recovered from db
    # previous_status = {'LD1': 1, 'LD2': 1, 'HD1': 1, 'HD2': 1, 'FV': 1, 'LNGV': 1, 'GWHS': 1, 'WUH': 1, 'SC': 1, 'BOGH': 1,
    #                          'LPHD1': 1, 'OHHD1': 1, 'LPHD2': 1, 'OHHD2': 1, 'GWHE': 1, 'GP1': 1, 'GP2': 1} #this is initial status for HOS function
    # sheets = ['LD1', 'LD2', 'HD1', 'HD2', 'LNGV', 'FV', 'BOGH', 'WUH', 'GWH', 'SC', 'IG', 'NG1', 'NG2', 'ME1', 'ME2', 'MEEG', 'GEEG', 
    #               'AB', 'VA', 'LO', 'BLST', 'BLG', 'GE1', 'GE2', 'GE3', 'GE4', 'CT1', 'CT2', 'CT3', 'CT4', 'FW', 'FO1', 'FG']

    previous_status = {}
    for item in HOS_dict.keys():
        previous_status[item] = 1
    #lets suppose all were running previously, 
    #if current status is running, only then HOS will get increment

    read_cloud_data = True
    # previous_time_FV = 'none'
    # previous_time_LD2 = 'none'
    object.cursor.execute('select "Standard_Key" from public."Input_Tags"') #updated for PostgreSQL 
    row = object.cursor.fetchall()
    object.conn.commit()
    # print(row)
    required_tags = []
    for item in row:
        required_tags.append(item[0])
    # print(len(required_tags))
    # print("required tags list prepared, len is: ", len(required_tags))
    
    object.cursor.execute('''select "TagName" from public."Output_Tags" where "Description" = 'To display instead of KPI';''') #updated for PostgreSQL 
    row = object.cursor.fetchall()
    object.conn.commit()
    alarm_tags = []
    for item in row:
        alarm_tags.append(item[0])
    # len(alarm_tags)
    # print(alarm_tags)

    start_of_program = 1 #only for those items which are supposed to run only once at start of program

    while read_cloud_data:
        # read_cloud_data, tags = object.cloudDataLogging()
        dict, no_of_samples, application_status, frequency = object.cloudDataLogging()
        print("no. of total tags in simfile: ", len(dict.keys()))
        if application_status == 'Playback' or application_status == 'Normal':
            for i in range(no_of_samples):
                tags = {} #will contain only 1 value of current iteration for required tags only
                tags_presence = {}
                for tag in required_tags:
                    if tag == 'Nav_GPS1_UTC': #mention here the tags which are needed to be put in string format
                        tags[tag] = dict[tag][i]
                    else:
                        if tag in dict.keys():
                            tags_presence[tag] = 1
                            # print(dict[tag])
                            value = dict[tag][i]
                            if len(value) == 0:
                                value = 99
                            tags[tag] = float(value) #now our main tags dict has been prepared with all required inputs and having 1 sample for each tag.
                        else:
                            tags_presence[tag] = 0
                            tags[tag] = 99 #just to write tags data to history tables

                #@@@@@@@@@@@@@@@@ check wheter required tags are available in current simfile
                # tags_presence = {}
                # for tag in required_tags:
                #     if tag in tags:
                #         tags_presence[tag] = 1
                #     else:
                #         tags_presence[tag] = 0
                #@@@@@@@@@@@@@@@@
                onboard_timestamp = object.inputsLogging(i, required_tags, tags, tags_presence)
                #updated block on 12122023 from here
                if start_of_program == 1 or start_of_program == 0:
                    tags_av_check = {}
                    tags_av_check_list = ['NS_GPS_019_PV', 'NS_PP004-03MI_PV', 'NS_PP043-03MI_PV', 'NS_PP009-03MI_PV', 'NS_PP044-03MI_PV', 'NS_PP036-03XI_PV', 
                                        'NS_PP037-03AXI_PV', 'NS_PP038-03AXI_PV', 'NS_PP038-03XC_PV', 'NS_PP040-03MI_PV', 'NS_PP045-03MI_PV', 'NS_PP046-03MI_PV',
                                        'NS_PP061-03MI_PV', 'NS_PP030-03MI_PV', 'NS_PP058-03MI_PV', 'NS_PP033-03MI_PV', 'NS_PP059-03MI_PV', 'NS_MM048-XI_PV',
                                        'NS_MM648-XI_PV', 'NS_MM018-XI_PV', 'NS_MM618-XI_PV', 'NS_MM023-XI_PV', 'NS_MM021-XI_PV', 'NS_MM623-XI_PV',
                                        'NS_MM621-XI_PV', 'NS_NG1-40101_PV', 'NS_NG1-40102_PV', 'NS_NG1-40103_PV', 'NS_NG2-40101_PV', 'NS_NG2-40102_PV', 'NS_NG2-40103_PV',
                                        'NS_MM944-XI_PV', 'NS_MF001-03MI_PV', 'NS_MF010-03MI_PV', 'NS_IG-00531_PV', 'NS_CF013-03MC_PV', 'NS_CF014-03MC_PV',
                                        'NS_MM002-XI_PV', 'NS_MM602-XI_PV', 'NS_MM908-03XI_PV', 'NS_MM066-XI_PV', 'NS_MM666-XI_PV', 'NS_MM933-XI_PV'] #updated list on 12192023
                    for item in tags_av_check_list:
                        
                        if item in tags.keys():
                            pres = True
                        else:
                            pres = False
                        if pres == True and tags[item] == 99:
                            tags_av_check[item] = 0
                        elif pres == True:
                            tags_av_check[item] = 1
                        else:
                            tags_av_check[item] = 0
                #updated block on 12122023 till here
                running_status = object.runningStatus(tags, tags_av_check)
                # print(running_status)
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                #manipulate running status for test purpose
                # running_status = {'FV': 0, 'LNGV': 0, 'BOGH': 0, 'WUH': 0, 'GWHS': 0, 'LD1': 0, 'LD2': 1, 'HD1': 0, 'HD2': 0, 'SC': 0, 'LPHD1': 0, 'LPHD2': 0, 'OHHD1': 0, 'OHHD2': 0, 'GWHE': 0, 'GP1': 0, 'GP2': 0}
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                
                object.runningStatusLogging(running_status, onboard_timestamp)
                print('running status logged')
                print("---------")
                dwsim_outputs, dwsim_outputs_to_append_to_tags = object.dwsimSimulation(tags, running_status, onboard_timestamp, tags_av_check)
                # print(len(dwsim_outputs))
                print("dwsim outputs are calculated")
                print("---------")
                object.outputsLogging(dwsim_outputs, running_status, onboard_timestamp, tags_av_check)
                # print(tags)
                if 'NS_IG004-XA_PV' in tags.keys(): #so it will work only after 07/09 when these alarms are available.
                    object.alarmLoggingforNoKPIassets(alarm_tags, tags)

                tags = tags | dwsim_outputs_to_append_to_tags #now this contains inputs and outputs combined. this is good to send forward to other programs
                # print(tags)
                # print(dwsim_outputs)
                # print("total tags including required inputs and outputs are: ", len(tags))

                #need to update templates if there is an update signal
                templates_updated = object.updateSignal()
                if templates_updated == '1': #re-read templates
                    #importing rca templates
                    rca_dfs = object.importRCAtemplates()
                    #collect RCA_ID and save it
                    available_scenarios = object.rcaID(rca_dfs)
                    print("rca templates and rca id were re-read after templates were updated by user")
                    
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                #change value of any key for test purpose
                # tags['CM_LNGSubClr_Flow'] = 8
                #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                if start_of_program == 1:
                    rules, keys = object.findRules(rca_dfs) #save rules too. It reads rules from templates and converts into one-liner string. It saves standard keys too
                    # for dwsim_output in dwsim_outputs: #updated on 12052023
                    #     tags_presence[dwsim_output] = 1 #updated on 12052023 #so that dwsim outputs should be considered as available tags
                                                          # above did not work because dwsim outputs contains outputs only for running assets 
                
                if start_of_program == 1 or '2023-07-09 00:0' in onboard_timestamp: #tags are updated after 0709 in simfile, so need to find target scenarios again
                    print("finding target scenarios at start of program in case of simfiles updated after 0709")
                    # print("test ****************")
                    # print(tags_presence['NS_MM831-XA_PV']) 
                    problems_to_detect = object.findtargetScenarios(keys, tags_presence) #updated on 12052023
                    # print("test ****************")
                    # print(problems_to_detect['AB_Main_Power_panel_fail'])
                
                status, parent_node = object.rcaTemplatesReader(rca_dfs, tags, running_status, problems_to_detect)
                print("status and parent node are read")
                print("---------")
                # print(parent_node['AB_AB2_Steam_pres_low'])
                rca_update = object.logStatusandParentNode(status, parent_node) #updated on 12122023
                                                                    #parent node needs to be written to sql on start of program only, not on every iteration
                                                                    #need to review it and update if possible - reviewed. keep as it is
                                                                    #i think its better to just insert all data on every iteration, --- 
                                                                    # as updating status only (without parent node) using where clause could take even longer as compared to inserting all data
                print("rca update history is logged")

                if start_of_program == 1: #here include those functions which need to be run once at restart/SOR
                    asset_hierarchy, problem_hierarchy = object.RCAlevels(HOS_dict) #updated for DailyHOS #updated on 11292023 #RCA levels too need to be run once on start of program.
                    print("rca levels done")
                    object.totalAvailableScenarios() #to find total available scenarios in master sheet for each asset. I think it needs to be run if templates are updated, so deactivated here
                    previous_timestamp = onboard_timestamp
                    #to be used in HOS function as previous timestamp to calculate time after comparing current running status with past
                    #its to be set only in first iteration
                    start_of_program = 0

                if templates_updated == '1': #update RCA levels and scenarios for each asset, and save rules too, if there is an update signal
                    asset_hierarchy, problem_hierarchy = object.RCAlevels(HOS_dict) #updated for DailyHOS #updated on 11292023 
                    print("rca levels done")
                    object.totalAvailableScenarios()
                    #reset update signal back to 0
                    object.cursor.execute('''update public."Templates_update" set "Status" = '0' where "Activity" = 'RCA_templates_updated';''') #updated for PostgreSQL
                    object.conn.commit()
                    print("rca levels and no. of scenarios updated after templates were updated by user")
                    #save rules too
                    rules = object.findRules(rca_dfs)
                
                # print(rca_update)
                status = object.applyInferredStatus(status)
                print("inferred status applied")
                # print("now good to go for rca active and rca history log")
                Prestatus = object.updateRCAstatus(Prestatus, running_status, status, onboard_timestamp, available_scenarios, rules, problem_hierarchy) #updated on 12122023
                print("rca status is done")
                previous_timestamp, previous_status, HOS_dict, HOS_TodaySoFar = object.saveHOS(previous_timestamp, previous_status, HOS_dict, onboard_timestamp, running_status, asset_hierarchy, HOS_TodaySoFar) #updated for DailyHOS)
                print("HOS are saved")
                object.maintenanceAlarm(SOR_time, HOS_dict)
                print("maintenance alarms checked")
                object.saveAlertCount()
                print("Alert count updated")
                # object.perfhealth() #decision pending yet
                # print("perfHealth is updated")
                print("All done! Time_onboard: ", onboard_timestamp, "--- Time_now:", datetime.now())
                print("================================================")


                time.sleep(frequency)
                if i == no_of_samples-1: #last iteration
                    print("reading new cloud inputs. TimeStamp is :", datetime.now())
                    read_cloud_data = True

        
        else:
            print("Holding mode")
            time.sleep(frequency)
            read_cloud_data = True


if __name__ == '__main__':
    main()



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
##for refreshing prestatus table for SOR
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# import pyodbc
# try:
#     conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-DS34DTB\SQLEXPRESS;DATABASE=SLM-Project;UID=user1;PWD=1234'
#     # conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LPPLVAI\SQLEXPRESS2019;DATABASE=S-Project;UID=sa;PWD=Welcome1'
#     # conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMERSON\SQLEXPRESS01;DATABASE=SLM-Project;UID=user1;PWD=1234'
#     # self.conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O74IH9F\SPARTA;DATABASE=S-Project;UID=sa;PWD=1234'
#     conn = pyodbc.connect(conn_string)
#     cursor = conn.cursor()
#     print("SQL connected!")
# except:
#     print("SQL not connected!")
# cursor.execute("select Level3_ScenarioName from RCA_ID")
# row = cursor.fetchall()
# conn.commit()
# scenarios = [item[0] for item in row]
# cursor.execute("truncate table Prestatus")
# conn.commit()
# for item in scenarios:
#     cursor.execute("insert into Prestatus values((?),(?),(?))", item, '2023-02-01 00:00:00', 'Unknown')
#     conn.commit()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#refresh db for SOR
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# update public."HOS" set "HOS" = 0;
# update public."HOS" set "DailyHOS" = 0;
# update public."HOS" set "TodaySoFar" = 0;
# truncate table public."DailyHOS";

# truncate table public."Running_status_history";
# update public."Running_status_update" set "Status" = 0;
# truncate table public."RCA_Active";
# truncate table public."RCA_history";

# truncate table public."LD1_output_history";
# truncate table public."LD2_output_history";
# truncate table public."HD1_output_history";
# truncate table public."HD2_output_history";
# truncate table public."FV_output_history";
# truncate table public."LNGV_output_history";
# truncate table public."BOGH_output_history";
# truncate table public."WUH_output_history";
# truncate table public."GWH_Stm_output_history";
# truncate table public."SC_output_history";
# truncate table public."ME1_output_history";
# truncate table public."ME2_output_history";
# truncate table public."GE1_output_history";
# truncate table public."GE2_output_history";
# truncate table public."GE3_output_history";
# truncate table public."GE4_output_history";
# truncate table public."NG1_output_history";
# truncate table public."NG2_output_history";
# truncate table public."AB_AB1_output_history";
# truncate table public."AB_AB2_output_history";

# truncate table public."FBOG_output_history";
# truncate table public."NBOG_output_history";
# truncate table public."Cargo_vapor_output_history";
# truncate table public."HD_output_history";
# truncate table public."Fuel_Consumption_output_history";
# truncate table public."Fuel_Economy_output_history";

# truncate table public."Input_history1";
# truncate table public."Input_history2";
# truncate table public."Input_history3";
# truncate table public."Input_history4";
# truncate table public."Input_history5";
# truncate table public."Input_history6";

# truncate table public."RCA_update";
# update public."Prestatus" set "TimeStamp" = '2023-02-01 00:05:14';
# update public."Prestatus" set "Status" = 'Unknown';

# update public."Application_status" set "Value" = '9929106_1m_20230201_000000.sim' where "Item" = 'Input_file';

# update public."Output_Tags" set "Value" = 100 where "TagName" like '%fouling_factor%';

# truncate table public."Log_messages";

# update public."RCA_rules" set "Rules" = 'NA';
# update public."RCA_Active" set "Rules" = 'NA';
# update public."RCA_history" set "Rules" = 'NA';


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#ran following while sharing db to SHI only for db related settings. it removed all important things which should be hidden.

# update RCA_rules set Rules = 'NA'
# update RCA_Active set Rules = 'NA'
# update RCA_history set Rules = 'NA'
# truncate table Input_history
# update Prestatus set Status = 'NA'
# update Prestatus set Scenario = 'NA'
# update Prestatus set TimeStamp = 'NA'
# update Application_status set Value = 'NA'
# update Calender_time set Value = 0
# update Calender_time set Kind = 'NA'
# update Log_messages set Message = 'NA'
# update RCA_ID set Level = 'NA'
# update RCA_ID set Priority = 1
# update RCA_levels set Level4_RootCauses = 'NA'
# update RCA_update set Status = 'NA'
# update RCA_update set ParentNode = 'NA'
# update RCA_update set scenarioName = 'NA'
# drop table RCA_rules 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#but for final deployment to site, only rules need to be hidden and input history is not needed.
#so for the final deployment, only below actions are needed before delivering db to IT team for docker image.
#in short, run following to convert db from dev to prod version.

# truncate table public."Input_history1";
# truncate table public."Input_history2";
# truncate table public."Input_history3";
# truncate table public."Input_history4";
# truncate table public."Input_history5";
# truncate table public."Input_history6";

# update public."RCA_rules" set "Rules" = 'NA';
# update public."RCA_Active" set "Rules" = 'NA';
# update public."RCA_history" set "Rules" = 'NA';



