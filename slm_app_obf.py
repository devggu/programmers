import pyodbc #line:1
from zipfile import ZipFile #line:2
import glob #line:3
import os #line:4
import os .path #line:5
import time #line:6
import getpass #line:7
from datetime import datetime #line:8
import pandas as pd #line:9
from numpy import NaN #line:10
import openpyxl #line:11
import msoffcrypto #line:12
import io #line:13
import json #line:14
from natsort import natsorted #line:15
from sqlalchemy import create_engine ,text #line:16
import urllib #line:17
import sqlite3 as db #line:18
import numpy as np #line:19
import clr #line:20
from System .IO import Directory ,Path ,File #line:21
from System import String ,Environment #line:22
import psycopg2 #line:23
class slmApplication ():#line:25
    def __init__ (O00O00O0000OOO00O ,O000O0O0O00OOOOO0 ,O0OO0O000OOO0OOO0 ,O0O0OOO00O0OOOOO0 ,OO000O0OOO0O00OOO ,O00O0O000O00O00OO ,O00000OOO0OO00OOO ,O0OO0O00O0O00O0O0 ):#line:26
        try :#line:27
            O00O00O0000OOO00O .excel_pwd =O0O0OOO00O0OOOOO0 #line:28
            if O0OO0O00O0O00O0O0 =='':#line:29
                O0OO0O00O0O00O0O0 ='/usr/local/lib/dwsim/'#line:30
            O00O00O0000OOO00O .conn_string =f'dbname ={O00O0O000O00O00OO} user={O000O0O0O00OOOOO0} password={O0OO0O000OOO0OOO0} host={OO000O0OOO0O00OOO} port={O00000OOO0OO00OOO}'#line:33
            O00O00O0000OOO00O .conn =psycopg2 .connect (O00O00O0000OOO00O .conn_string )#line:37
            O00O00O0000OOO00O .cursor =O00O00O0000OOO00O .conn .cursor ()#line:38
            O0OO0OO0OOO0O00O0 =urllib .parse .quote_plus (O00O00O0000OOO00O .conn_string )#line:40
            print ("SQL connected!")#line:43
        except :#line:46
            print ("SQL not connected!")#line:47
        OOO0O00O00O0O000O =O0OO0O00O0O00O0O0 #line:48
        O00O00O0000OOO00O .test_run =0 #line:52
        OO0O00O0O00OOO000 =True #line:53
        if OO0O00O0O00OOO000 :#line:54
            O00O00O0000OOO00O .log_inputs_realtime =0 #line:55
            O00O00O0000OOO00O .log_inputs_history =0 #line:56
            O00O00O0000OOO00O .hide_rules =1 #line:57
        else :#line:58
            O00O00O0000OOO00O .log_inputs_realtime =1 #line:59
            O00O00O0000OOO00O .log_inputs_history =1 #line:60
            O00O00O0000OOO00O .hide_rules =0 #line:61
        O00O00O0000OOO00O .compare_pre_and_curr_status =1 #line:63
        O00O00O0000OOO00O .log_less_priority_items =0 #line:64
        clr .AddReference (OOO0O00O00O0O000O +"CapeOpen.dll")#line:67
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.Automation.dll")#line:68
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.Interfaces.dll")#line:69
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.GlobalSettings.dll")#line:70
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.SharedClasses.dll")#line:71
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.Thermodynamics.dll")#line:72
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.UnitOperations.dll")#line:73
        clr .AddReference (OOO0O00O00O0O000O +"DWSIM.Inspector.dll")#line:74
        clr .AddReference (OOO0O00O00O0O000O +"System.Buffers.dll")#line:75
        from DWSIM .Interfaces .Enums .GraphicObjects import ObjectType #line:77
        from DWSIM .Thermodynamics import Streams ,PropertyPackages #line:78
        from DWSIM .UnitOperations import UnitOperations #line:79
        from DWSIM .Automation import Automation3 #line:80
        from DWSIM .GlobalSettings import Settings #line:81
        O00O00O0000OOO00O .interf =Automation3 ()#line:85
        OO00OO0O00OOOO00O ='assets/'#line:88
        OO00OO0OOO0OOO000 ='assets/py_conn/'#line:90
        O000O0O000O000O00 =os .path .abspath (os .path .dirname (__file__ ))#line:91
        O00O00O0000OOO00O .RCA_mastersheet_path =os .path .join (O000O0O000O000O00 ,OO00OO0O00OOOO00O +'SLM Rules Master sheet_12202023_rev3.7')#line:92
        OOO00OOO00O0O000O =OO00OO0O00OOOO00O +'simfiles'#line:98
        O00O00O0000OOO00O .simfiles_path =os .path .join (O000O0O000O000O00 ,OOO00OOO00O0O000O )#line:99
        OOO00OO0O0O0O0000 =os .path .join (O000O0O000O000O00 ,OO00OO0OOO0OOO000 )#line:105
        O00O00O0000OOO00O .ent ='@@@LD2_S2_out_actual_specific_enthalpy@@@'#line:106
        O00O00O0000OOO00O .sim1 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"sclr_py_conn.dwxmz")#line:111
        print ("sim1-SC interface ready")#line:112
        O00O00O0000OOO00O .sim2 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"fv_py_conn.dwxmz")#line:113
        print ("sim2-FV interface ready")#line:114
        O00O00O0000OOO00O .sim3 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"lngv_py_conn.dwxmz")#line:115
        print ("sim3-LNGV interface ready")#line:116
        O00O00O0000OOO00O .sim4 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"bogh_py_conn.dwxmz")#line:117
        print ("sim4-BOGH interface ready")#line:118
        O00O00O0000OOO00O .sim5 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"wuh_py_conn.dwxmz")#line:119
        print ("sim5-WUH interface ready")#line:120
        O00O00O0000OOO00O .sim6 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"gwhs_py_conn.dwxmz")#line:121
        print ("sim6-GWHStm interface ready")#line:122
        O00O00O0000OOO00O .sim7 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"LD1_py_conn.dwxmz")#line:123
        print ("sim7-LD1 interface ready")#line:124
        O00O00O0000OOO00O .sim8 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"LD2_py_conn.dwxmz")#line:125
        print ("sim8-LD2 interface ready")#line:126
        O00O00O0000OOO00O .sim9 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"HD1_py_conn.dwxmz")#line:127
        print ("sim9-HD1 interface ready")#line:128
        O00O00O0000OOO00O .sim10 =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"HD2_py_conn.dwxmz")#line:129
        print ("sim10-HD2 interface ready")#line:130
        O00O00O0000OOO00O .ME1_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"ME1_py_conn.dwxmz")#line:131
        O00O00O0000OOO00O .ME2_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"ME2_py_conn.dwxmz")#line:132
        O00O00O0000OOO00O .GE1_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"GE1_py_conn.dwxmz")#line:133
        O00O00O0000OOO00O .GE2_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"GE2_py_conn.dwxmz")#line:134
        O00O00O0000OOO00O .GE3_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"GE3_py_conn.dwxmz")#line:135
        O00O00O0000OOO00O .GE4_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"GE4_py_conn.dwxmz")#line:136
        print ("ME1/2 and GE1/2/3/4 interface ready")#line:137
        O00O00O0000OOO00O .NG1_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"NG1_py_conn.dwxmz")#line:138
        O00O00O0000OOO00O .NG2_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"NG2_py_conn.dwxmz")#line:139
        print ("NG1/2 interface ready")#line:140
        O00O00O0000OOO00O .AB1_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"AB1_py_conn.dwxmz")#line:141
        O00O00O0000OOO00O .AB2_sim =O00O00O0000OOO00O .interf .LoadFlowsheet (OOO00OO0O0O0O0000 +"AB2_py_conn.dwxmz")#line:142
        print ("AB1/2 interface ready")#line:143
        O00O00O0000OOO00O .agg ={}#line:145
        O00O00O0000OOO00O .persistence ={}#line:146
        O00O00O0000OOO00O .mavg_samples ={}#line:147
        O00O00O0000OOO00O .for_test ='none_for_test'#line:150
        O00O00O0000OOO00O .agg_test ='none'#line:157
    def validateInputs (OO0OO0OOOOO000OO0 ,OO000000OO00OO0OO ,O0OOO0OOOO0000000 ,OO0OOOOOO0O0OO000 ):#line:159
        OO0OO0000O00O0O00 ={}#line:161
        for O0OOO0O00O0O0OOOO in O0OOO0OOOO0000000 .keys ():#line:162
            OO0O0OO00OOO000OO =OO000000OO00OO0OO [O0OOO0O00O0O0OOOO ]#line:163
            OO0OOO000O0OO0OO0 =O0OOO0OOOO0000000 [O0OOO0O00O0O0OOOO ][0 ]#line:164
            OOO0O00O00000OOO0 =O0OOO0OOOO0000000 [O0OOO0O00O0O0OOOO ][1 ]#line:165
            OO00O0OO00O000OO0 =OO0OOO000O0OO0OO0 [0 ]#line:166
            O00OO00O00O0O0O00 =OO0OOO000O0OO0OO0 [1 ]#line:167
            O00O0OO0O00OO0OOO ='normal range of '+O0OOO0O00O0O0OOOO +': ['+str (OO00O0OO00O000OO0 )+","+str (O00OO00O00O0O0O00 )+"]. Current value of "+O0OOO0O00O0O0OOOO +": "+str (OO0O0OO00OOO000OO )+". Temporary value of "+str (OOO0O00O00000OOO0 )+" will be used in dwsim to avoid non-convergence of flowsheet."#line:168
            OO0OO0OOOOO000OO0 .cursor .execute ('select "Tag" from public."Log_messages"')#line:170
            O0O000OO0O0O0000O =OO0OO0OOOOO000OO0 .cursor .fetchall ()#line:171
            OO0OO0OOOOO000OO0 .conn .commit ()#line:172
            OO0O0O000O0OOOO00 =[OO0000O0OOOO0OOO0 [0 ]for OO0000O0OOOO0OOO0 in O0O000OO0O0O0000O ]#line:173
            if OO0O0OO00OOO000OO <OO00O0OO00O000OO0 or OO0O0OO00OOO000OO >O00OO00O00O0O0O00 :#line:175
                print (O0OOO0O00O0O0OOOO ,'is out of range, so using temporary value which is: ',OOO0O00O00000OOO0 )#line:176
                OO0OO0000O00O0O00 [O0OOO0O00O0O0OOOO ]=OOO0O00O00000OOO0 #line:177
                if O0OOO0O00O0O0OOOO not in OO0O0O000O0OOOO00 :#line:178
                    OO0OO0OOOOO000OO0 .cursor .execute ('insert into public."Log_messages" values(%s, %s, %s, %s)',[OO0OOOOOO0O0OO000 ,O0OOO0O00O0O0OOOO ,'dwsimSimulation',O00O0OO0O00OO0OOO ])#line:179
                    OO0OO0OOOOO000OO0 .conn .commit ()#line:180
            else :#line:181
                pass #line:183
        return OO0OO0000O00O0O00 #line:185
    def dwsimSimulation (OO0O0O0O0O0O00O00 ,OO0000000OOOOOO00 ,O0O0O00000O000O00 ,OOO00O000OOO00OO0 ,O00O0O0OO0OO0O0O0 ):#line:187
        OO0OO000OO0OO0O00 ={}#line:188
        OO0OO000O0000OO0O ={}#line:189
        OO0OOO0O00O0O0O0O ={}#line:190
        O000OO000OO00O0OO ={}#line:191
        OOOO000O0O0O0000O ={}#line:192
        OOO0OOO00OOOO0000 ={}#line:193
        O00O0OOOO0000O00O ={}#line:194
        O0OO0OO000OO0O0OO ={}#line:195
        O0OO0O000OOO000OO ={}#line:196
        OO00O00000O0OO0O0 ={}#line:197
        OOOOO000O000OOOO0 ={}#line:198
        OOO0OOO000OO0O0OO ={}#line:199
        O0OOOOOOO0OOO0000 ={}#line:200
        O00OOOO0O00OOOOOO ={}#line:201
        OOOO00O0O000000OO ={}#line:202
        O0O0OO00O0OOO0O00 ={}#line:203
        O0OO00OO000000OOO ={}#line:204
        O0OO0OO0O0O0O000O ={}#line:205
        O00OO0O00OO0OO0O0 ={}#line:206
        O0OO00O0OO0OO0OO0 ={}#line:207
        O00OOOOO00OO0O0O0 ={}#line:208
        O0OOO000O0O000O0O ={}#line:209
        O0OO00O0O0O0O0OO0 ={}#line:210
        O0OOOO0OOO000OO0O ={}#line:211
        O0000O00O0OOO0O00 ={}#line:212
        OO00O0O0O00O00O00 ={}#line:213
        O00O0000OO00000OO ={'CM_LNGSubClr_Flow':[[3 ,10 ],5 ],'ME1_EG_ScavAirMeanPrs':[[0.1 ,0.5 ],0.26 ],'ME2_EG_ScavAirMeanPrs':[[0.1 ,0.5 ],0.26 ]}#line:217
        O0OOO0OOO00000OO0 =OO0O0O0O0O0O00O00 .validateInputs (OO0000000OOOOOO00 ,O00O0000OO00000OO ,OOO00O000OOO00OO0 )#line:219
        if O0O0O00000O000O00 ['SC']==1 :#line:223
            print ("starting dwsim SC")#line:225
            O0O0OOO00OO00O0O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('LNG_in').GetAsObject ()#line:229
            O00O0000OO0000O00 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('LNG_out').GetAsObject ()#line:230
            OOOOOO0O00O0O0OO0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX2_LNG_cooling').GetAsObject ()#line:231
            OO0OO0000OO0OOOO0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_comp_in').GetAsObject ()#line:234
            O0OOO00O0000OO00O =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_comp').GetAsObject ()#line:235
            OO0O00O00O0OOO0O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_comp_out_ideal').GetAsObject ()#line:236
            OO00OOO0O000000OO =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_comp_out_actual').GetAsObject ()#line:237
            OO0O00OO0000O0000 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX300').GetAsObject ()#line:238
            OO0OOO000OO00OOOO =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_exp').GetAsObject ()#line:241
            OOO0000OOOO0O0OO0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_exp_in').GetAsObject ()#line:242
            O00OOO00O0OOO00O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_exp_out_ideal').GetAsObject ()#line:243
            O0O0O0O0OOO0000O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MTC_exp_out_actual').GetAsObject ()#line:244
            OO0OO000OOOOOO0O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MC_comp_in').GetAsObject ()#line:247
            O00O00OO0O00O0O00 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MC_comp').GetAsObject ()#line:248
            O00O00OOOO00OOO0O =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MC_comp_out_ideal').GetAsObject ()#line:249
            O0000O0O00000OOOO =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('MC_comp_out_actual').GetAsObject ()#line:250
            O0OO000000OO00OO0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX200').GetAsObject ()#line:251
            O00O0O00O000O00OO =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX200_out').GetAsObject ()#line:252
            O0OOOO0OO0O0OO00O =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX1_ref_cooling').GetAsObject ()#line:255
            OO000O00OOO0000O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX1-2_ref_heating').GetAsObject ()#line:256
            OO0OO00OOOOO00OO0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX1-2_out').GetAsObject ()#line:257
            O000OOO0OOOOO00O0 =OO0O0O0O0O0O00O00 .sim1 .GetFlowsheetSimulationObject ('HX1-2_ideal').GetAsObject ()#line:258
            OOO00000OOO00OOO0 =100000.0 #line:264
            O000OO0O0OOO0O0O0 =OO0000000OOOOOO00 ['CM_LNGSubClr_DropPrs']/1000.0 #line:268
            OOOOO0OO0OO0OO000 =(OO0000000OOOOOO00 ['CM_LNGSubClr_OutPrs'])#line:269
            OO00O00OOO00OO0O0 =OOOOO0OO0OO0OO000 +O000OO0O0OOO0O0O0 #line:270
            O0O0OOO00OO00O0O0 .SetPressure (OO00O00OOO00OO0O0 *OOO00000OOO00OOO0 )#line:271
            OOOOOO0O00O0O0OO0 .set_DeltaP (O000OO0O0OOO0O0O0 *OOO00000OOO00OOO0 )#line:272
            O0O0OOO00OO00O0O0 .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_InTemp']+273.15 )#line:273
            if 'CM_LNGSubClr_Flow'in O0OOO0OOO00000OO0 :#line:275
                O00000O0000O00O0O =O0OOO0OOO00000OO0 ['CM_LNGSubClr_Flow']#line:276
            else :#line:277
                O00000O0000O00O0O =OO0000000OOOOOO00 ['CM_LNGSubClr_Flow']#line:278
            O0O0OOO00OO00O0O0 .SetMassFlow (O00000O0000O00O0O /3600.0 )#line:281
            OOOOOO0O00O0O0OO0 .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_OutTemp']+273.15 )#line:283
            OO0OO0000OO0OOOO0 .SetPressure (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompInPrs']*OOO00000OOO00OOO0 )#line:286
            OO0OO0000OO0OOOO0 .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompInTemp']+273.15 )#line:287
            O0OOO00O0000OO00O .set_POut (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompOutPrs']*OOO00000OOO00OOO0 )#line:289
            OO00OOO0O000000OO .SetPressure (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompOutPrs']*OOO00000OOO00OOO0 )#line:290
            OO00OOO0O000000OO .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompOutTemp']+273.15 )#line:291
            OO0O00OO0000O0000 .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_Hx300_OutTemp']+273.15 )#line:292
            O0O00OO0OOOOOO0O0 =OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_CompOutPrs']-OO0000000OOOOOO00 ['CM_LNGSubClr_Hx300_OutPrs']#line:293
            OO0O00OO0000O0000 .set_DeltaP (O0O00OO0OOOOOO0O0 *OOO00000OOO00OOO0 )#line:294
            O00O00OO0O00O0O00 .set_POut (OO0000000OOOOOO00 ['CM_LNGSubClr_MC_CompOutPrs']*OOO00000OOO00OOO0 )#line:297
            O0000O0O00000OOOO .SetPressure (OO0000000OOOOOO00 ['CM_LNGSubClr_MC_CompOutPrs']*OOO00000OOO00OOO0 )#line:298
            O0000O0O00000OOOO .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_MC_CompOutTemp']+273.15 )#line:299
            O0OO000000OO00OO0 .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_Hx1_InTemp']+273.15 )#line:300
            O0OOOO0OO0O0OO00O .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineInTemp']+273.15 )#line:303
            OO00O00O0OOO0O000 =OO0000000OOOOOO00 ['CM_LNGSubClr_MC_CompOutPrs']-OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineInPrs']#line:304
            O0OOOO0OO0O0OO00O .set_DeltaP (OO00O00O0OOO0O000 *OOO00000OOO00OOO0 )#line:305
            OO0OOO000OO00OOOO .set_POut (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineOutPrs']*OOO00000OOO00OOO0 )#line:308
            O0O0O0O0OOO0000O0 .SetPressure (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineOutPrs']*OOO00000OOO00OOO0 )#line:309
            O0O0O0O0OOO0000O0 .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineOutTemp']+273.15 )#line:310
            O000OOO0OOOOO00O0 .SetPressure (OO0000000OOOOOO00 ['CM_LNGSubClr_MTC_TurbineOutPrs']*OOO00000OOO00OOO0 )#line:313
            O000OOO0OOOOO00O0 .SetTemperature (OO0000000OOOOOO00 ['CM_LNGSubClr_Hx1_InTemp']+273.15 )#line:314
            from DWSIM .GlobalSettings import Settings #line:317
            Settings .SolverMode =0 #line:318
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim1 )#line:319
            O00000OO00O00O000 ={}#line:322
            O00O0O0000OOO0OO0 =O0O0OOO00OO00O0O0 .GetTemperature ()-273.15 #line:325
            OOOOO0OO0OO0OO000 =O00O0000OO0000O00 .GetPressure ()/OOO00000OOO00OOO0 #line:326
            OO000O0OOO0O0OOO0 =O00O0000OO0000O00 .GetMassFlow ()*3600 #line:327
            O00000000O0OOO0O0 =OO0OO0000OO0OOOO0 .GetPressure ()/OOO00000OOO00OOO0 #line:329
            O0000000OO0OO0O0O =OO0OO0000OO0OOOO0 .GetTemperature ()-273.15 #line:330
            OOOO000OOOOOOO0O0 =OO00OOO0O000000OO .GetPressure ()/OOO00000OOO00OOO0 #line:331
            O0OO0O000O000000O =OO00OOO0O000000OO .GetTemperature ()-273.15 #line:332
            O00OO00OO0OOOOO0O =OO0OO000OOOOOO0O0 .GetPressure ()/OOO00000OOO00OOO0 #line:334
            O00O0O0O00O00O0O0 =OO0OO000OOOOOO0O0 .GetTemperature ()-273.15 #line:335
            OO0OOOO000O0OOOO0 =O0000O0O00000OOOO .GetPressure ()/OOO00000OOO00OOO0 #line:336
            OO0O00000O0O00OOO =O0000O0O00000OOOO .GetTemperature ()-273.15 #line:337
            OOOO0OO00O0OO00OO =O00O0O00O000O00OO .GetTemperature ()-273.15 #line:338
            OO0000O0OOO00O00O =OOO0000OOOO0O0OO0 .GetPressure ()/OOO00000OOO00OOO0 #line:340
            O00O00O0OO000O00O =OOO0000OOOO0O0OO0 .GetTemperature ()-273.15 #line:341
            O0OO000OO0OOOO0OO =O0O0O0O0OOO0000O0 .GetPressure ()/OOO00000OOO00OOO0 #line:342
            OOOOOO0O0OO0O000O =O0O0O0O0OOO0000O0 .GetTemperature ()-273.15 #line:343
            O00O0OOOO0OOO0000 =OO0OO00OOOOO00OO0 .GetTemperature ()-273.15 #line:345
            O00000OO00O00O000 ['LNG_in_temp']=O00O0O0000OOO0OO0 #line:347
            O00000OO00O00O000 ['LNG_out_pres']=OOOOO0OO0OO0OO000 #line:348
            O00000OO00O00O000 ['LNG_out_flow']=OO000O0OOO0O0OOO0 #line:349
            O00000OO00O00O000 ['MTC_comp_in_pres']=O00000000O0OOO0O0 #line:350
            O00000OO00O00O000 ['MTC_comp_in_temp']=O0000000OO0OO0O0O #line:351
            O00000OO00O00O000 ['MTC_comp_out_pres']=OOOO000OOOOOOO0O0 #line:352
            O00000OO00O00O000 ['MTC_comp_out_temp']=O0OO0O000O000000O #line:353
            O00000OO00O00O000 ['MC_comp_in_pres']=O00OO00OO0OOOOO0O #line:354
            O00000OO00O00O000 ['MC_comp_in_temp']=O00O0O0O00O00O0O0 #line:355
            O00000OO00O00O000 ['MC_comp_out_pres']=OO0OOOO000O0OOOO0 #line:356
            O00000OO00O00O000 ['MC_comp_out_temp']=OO0O00000O0O00OOO #line:357
            O00000OO00O00O000 ['HX200_out_temp']=OOOO0OO00O0OO00OO #line:358
            O00000OO00O00O000 ['MTC_exp_in_pres']=OO0000O0OOO00O00O #line:359
            O00000OO00O00O000 ['MTC_exp_in_temp']=O00O00O0OO000O00O #line:360
            O00000OO00O00O000 ['MTC_exp_out_pres']=O0OO000OO0OOOO0OO #line:361
            O00000OO00O00O000 ['MTC_exp_out_temp']=OOOOOO0O0OO0O000O #line:362
            O00000OO00O00O000 ['HX12_out_temp']=O00O0OOOO0OOO0000 #line:363
            O0O000OOOOO0OO00O =OO0OO0000OO0OOOO0 .GetMassEnthalpy ()#line:367
            O0OO0O0O00O0O0O0O =OOOO000OOOOOOO0O0 /O00000000O0OOO0O0 #line:368
            OO0OO00OOO0O0OOO0 =abs (O0OOO00O0000OO00O .GetPowerGeneratedOrConsumed ())#line:369
            OOOO0O0O000OOO0OO =O0OOO00O0000OO00O .get_PolytropicHead ()#line:370
            O00O00000OOOO0OOO =OO0O00O00O0OOO0O0 .GetTemperature ()-273.15 #line:371
            O0O000OOOOO0OO00O =OO0OO0000OO0OOOO0 .GetMassEnthalpy ()#line:372
            OOO000O00OOO0OOOO =OO0O00O00O0OOO0O0 .GetMassEnthalpy ()#line:373
            OO00O000OO0OOO0O0 =OO00OOO0O000000OO .GetMassEnthalpy ()#line:374
            O0000O0OO0000O0O0 =OOO000O00OOO0OOOO -O0O000OOOOO0OO00O #line:375
            O0OO00OOOO0OO0OOO =OO00O000OO0OOO0O0 -O0O000OOOOO0OO00O #line:376
            O00OOOOO000O0O00O =(O0000O0OO0000O0O0 /O0OO00OOOO0OO0OOO )*100 #line:377
            O0OO0O000000OOO00 =OO0O00OO0000O0000 .get_DeltaT ()#line:378
            OOOOOOOOOOOOO0000 =OO0O00OO0000O0000 .GetPowerGeneratedOrConsumed ()#line:379
            OO0OO000OO0OO0O00 ['SC_MTC_comp_in_specific_enthalpy']=O0O000OOOOO0OO00O #line:381
            OO0OO000OO0OO0O00 ['SC_MTC_comp_pressure_ratio']=O0OO0O0O00O0O0O0O #line:382
            OO0OO000OO0OO0O00 ['SC_MTC_comp_polytropic_power']=OO0OO00OOO0O0OOO0 #line:383
            OO0OO000OO0OO0O00 ['SC_MTC_comp_polytropic_head']=OOOO0O0O000OOO0OO #line:384
            OO0OO000OO0OO0O00 ['SC_MTC_comp_in_specific_enthalpy']=O0O000OOOOO0OO00O #line:385
            OO0OO000OO0OO0O00 ['SC_MTC_comp_out_actual_specific_enthalpy']=OO00O000OO0OOO0O0 #line:386
            OO0OO000OO0OO0O00 ['SC_MTC_comp_polytropic_efficiency']=O00OOOOO000O0O00O #line:387
            OO0OO000OO0OO0O00 ['SC_HX300_deltaT']=O0OO0O000000OOO00 #line:388
            OO0OO000OO0OO0O00 ['SC_HX300_duty']=OOOOOOOOOOOOO0000 #line:389
            O00OOOOOO0000O000 =OO0OO000OOOOOO0O0 .GetMassEnthalpy ()#line:392
            OO0O0O00OO0OO0OO0 =OO0OOOO000O0OOOO0 /O00OO00OO0OOOOO0O #line:393
            OO000OOO00000O0O0 =abs (O00O00OO0O00O0O00 .GetPowerGeneratedOrConsumed ())#line:394
            OOO0OOO0O00OO00OO =O00O00OO0O00O0O00 .get_PolytropicHead ()#line:395
            OO0OOOOOO000OO0OO =O00O00OOOO00OOO0O .GetTemperature ()-273.15 #line:396
            O00OOOOOO0000O000 =OO0OO000OOOOOO0O0 .GetMassEnthalpy ()#line:397
            O0OO000O0O0O00000 =O00O00OOOO00OOO0O .GetMassEnthalpy ()#line:398
            O0OOOOOO0OOO00000 =O0000O0O00000OOOO .GetMassEnthalpy ()#line:399
            OOO000O00000O0OO0 =O0OO000O0O0O00000 -O00OOOOOO0000O000 #line:400
            OO0O0OOOOOOO0000O =O0OOOOOO0OOO00000 -O00OOOOOO0000O000 #line:401
            O0OOOO000OOOO00O0 =(OOO000O00000O0OO0 /OO0O0OOOOOOO0000O )*100 #line:402
            OOO0O0O0O0O000OO0 =O0OO000000OO00OO0 .get_DeltaT ()#line:403
            O0000O0OOO000OO00 =O0OO000000OO00OO0 .GetPowerGeneratedOrConsumed ()#line:404
            OO0OO000OO0OO0O00 ['SC_MC_comp_in_specific_enthalpy']=O00OOOOOO0000O000 #line:406
            OO0OO000OO0OO0O00 ['SC_MC_comp_pressure_ratio']=OO0O0O00OO0OO0OO0 #line:407
            OO0OO000OO0OO0O00 ['SC_MC_comp_polytropic_power']=OO000OOO00000O0O0 #line:408
            OO0OO000OO0OO0O00 ['SC_MC_comp_polytropic_head']=OOO0OOO0O00OO00OO #line:409
            OO0OO000OO0OO0O00 ['SC_MC_comp_in_specific_enthalpy']=O00OOOOOO0000O000 #line:410
            OO0OO000OO0OO0O00 ['SC_MC_comp_out_actual_specific_enthalpy']=O0OOOOOO0OOO00000 #line:411
            OO0OO000OO0OO0O00 ['SC_MC_comp_polytropic_efficiency']=O0OOOO000OOOO00O0 #line:412
            OO0OO000OO0OO0O00 ['SC_HX200_deltaT']=OOO0O0O0O0O000OO0 #line:413
            OO0OO000OO0OO0O00 ['SC_HX200_duty']=O0000O0OOO000OO00 #line:414
            O000OOO00OOO00OOO =OOO0000OOOO0O0OO0 .GetMassEnthalpy ()#line:417
            O0O000OOO00OOOO0O =OO0000O0OOO00O00O /O0OO000OO0OOOO0OO #line:418
            O0OOOO0OO000000OO =abs (OO0OOO000OO00OOOO .GetPowerGeneratedOrConsumed ())#line:419
            O0000O000O0O00000 =OO0OOO000OO00OOOO .get_PolytropicHead ()#line:420
            O00OOOOO0O00OO000 =O00OOO00O0OOO00O0 .GetTemperature ()-273.15 #line:421
            O000OOO00OOO00OOO =OOO0000OOOO0O0OO0 .GetMassEnthalpy ()#line:422
            OOO0O0O0000O00OO0 =O00OOO00O0OOO00O0 .GetMassEnthalpy ()#line:423
            O0OO0O0OOOO00O0O0 =O0O0O0O0OOO0000O0 .GetMassEnthalpy ()#line:424
            OOO00O00O0OOO00O0 =OOO0O0O0000O00OO0 -O000OOO00OOO00OOO #line:425
            OOO00O0O0O0000O00 =O0OO0O0OOOO00O0O0 -O000OOO00OOO00OOO #line:426
            O0000O000OOO0OO0O =(OOO00O0O0O0000O00 /OOO00O00O0OOO00O0 )*100 #line:427
            OO0OO000OO0OO0O00 ['SC_MTC_exp_in_specific_enthalpy']=O000OOO00OOO00OOO #line:429
            OO0OO000OO0OO0O00 ['SC_MTC_exp_pressure_ratio']=O0O000OOO00OOOO0O #line:430
            OO0OO000OO0OO0O00 ['SC_MTC_exp_polytropic_power']=O0OOOO0OO000000OO #line:431
            OO0OO000OO0OO0O00 ['SC_MTC_exp_polytropic_head']=O0000O000O0O00000 #line:432
            OO0OO000OO0OO0O00 ['SC_MTC_exp_in_specific_enthalpy']=O000OOO00OOO00OOO #line:433
            OO0OO000OO0OO0O00 ['SC_MTC_exp_out_actual_specific_enthalpy']=O0OO0O0OOOO00O0O0 #line:434
            OO0OO000OO0OO0O00 ['SC_MTC_exp_polytropic_efficiency']=O0000O000OOO0OO0O #line:435
            O0O000OOOO0O0OO00 =OOOOOO0O00O0O0OO0 .get_DeltaT ()#line:438
            OOOO0O0OO0000OO00 =OOOOOO0O00O0O0OO0 .GetPowerGeneratedOrConsumed ()#line:439
            O000000OO0O0O0000 =O0OOOO0OO0O0OO00O .get_DeltaT ()#line:440
            O0O0OOOO000O0O0OO =O0OOOO0OO0O0OO00O .GetPowerGeneratedOrConsumed ()#line:441
            O0000OO00O000OOO0 =OO000O00OOO0000O0 .get_DeltaT ()#line:442
            O00000O0000O000O0 =OO000O00OOO0000O0 .GetPowerGeneratedOrConsumed ()#line:443
            OO0OO000OO0OO0O00 ['SC_HX2_deltaT']=O0O000OOOO0O0OO00 #line:445
            OO0OO000OO0OO0O00 ['SC_HX2_LNG_cold_power']=OOOO0O0OO0000OO00 #line:446
            OO0OO000OO0OO0O00 ['SC_HX1_deltaT']=O000000OO0O0O0000 #line:447
            OO0OO000OO0OO0O00 ['SC_HX1_duty']=O0O0OOOO000O0O0OO #line:448
            OO0OO000OO0OO0O00 ['SC_HX12_regenerator_deltaT']=O0000OO00O000OOO0 #line:449
            OO0OO000OO0OO0O00 ['SC_HX12_regenerator_duty']=O00000O0000O000O0 #line:450
            O0O0O0OO0O00O0O00 =OOOOOO0O0OO0O000O #line:453
            O0OO0000000O0OOO0 =OO0O00000O0O00OOO #line:454
            O0OOO00O0OO0OOO00 =OO0000000OOOOOO00 ['CM_LNGSubClr_MTC1_Pwr']+OO0000000OOOOOO00 ['CM_LNGSubClr_MTC2_Pwr']+OO0000000OOOOOO00 ['CM_LNGSubClr_MTC3_Pwr']#line:456
            OO0OO0O00OO0OOO0O =OO0000000OOOOOO00 ['CM_LNGSubClr_MC1_Pwr']+OO0000000OOOOOO00 ['CM_LNGSubClr_MC2_Pwr']+OO0000000OOOOOO00 ['CM_LNGSubClr_MC3_Pwr']+OO0000000OOOOOO00 ['CM_LNGSubClr_MC4_Pwr']#line:457
            O000O0OO00000O0OO =OOOO0O0OO0000OO00 /(O0OOO00O0OO0OOO00 +OO0OO0O00OO0OOO0O )#line:459
            OO0OO000OO0OO0O00 ['SC_SC_min_temp']=O0O0O0OO0O00O0O00 #line:462
            OO0OO000OO0OO0O00 ['SC_SC_max_temp']=O0OO0000000O0OOO0 #line:463
            OO0OO000OO0OO0O00 ['SC_MTC_actual_power']=O0OOO00O0OO0OOO00 #line:464
            OO0OO000OO0OO0O00 ['SC_MC_actual_power']=OO0OO0O00OO0OOO0O #line:465
            OO0OO000OO0OO0O00 ['SC_COP']=O000O0OO00000O0OO #line:467
            for O00000O00O0O00O00 in OO0OO000OO0OO0O00 .keys ():#line:468
                OO0OO000OO0OO0O00 [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OO0OO000OO0OO0O00 [O00000O00O0O00O00 ]))#line:469
        if O0O0O00000O000O00 ['FV']==1 :#line:473
            print ("starting dwsim FV")#line:475
            O0OOOO0O0O0000O0O =OO0O0O0O0O0O00O00 .sim2 .GetFlowsheetSimulationObject ('FV_cold_in').GetAsObject ()#line:478
            O0OO0OO0O0O0O00O0 =OO0O0O0O0O0O00O00 .sim2 .GetFlowsheetSimulationObject ('FV_cold_out').GetAsObject ()#line:479
            OOOO00OO0O00O0000 =OO0O0O0O0O0O00O00 .sim2 .GetFlowsheetSimulationObject ('FV_HT_1').GetAsObject ()#line:480
            O000O00O00OO000O0 =OO0O0O0O0O0O00O00 .sim2 .GetFlowsheetSimulationObject ('FV_stm_in').GetAsObject ()#line:481
            OO0OO0O0O0OOOO00O =OO0O0O0O0O0O00O00 .sim2 .GetFlowsheetSimulationObject ('FV_stm_out').GetAsObject ()#line:482
            O0OOOO0O0O0000O0O .SetTemperature (OO0000000OOOOOO00 ['FG_FV_InTempInd']+273.15 )#line:488
            O0OOOO0O0O0000O0O .SetPressure (OO0000000OOOOOO00 ['FG_FV_InPrs']*1000.0 )#line:489
            O0OOOO0O0O0000O0O .SetMassFlow (OO0000000OOOOOO00 ['FG_FV_DischFlow']/3600.0 )#line:490
            OOOO00OO0O00O0000 .set_OutletTemperature (OO0000000OOOOOO00 ['FG_FV_OutTemp2Ind']+273.15 )#line:491
            OO00OOOO0000OOO0O =OO0000000OOOOOO00 ['FG_FV_InPrs']-OO0000000OOOOOO00 ['FG_FV_OutPrs']#line:492
            OOOO00OO0O00O0000 .set_DeltaP (OO00OOOO0000OOO0O *1000.0 )#line:493
            O000O00O00OO000O0 .SetTemperature (OO0000000OOOOOO00 ['FG_FV_CondWtrTempInd']+273.15 )#line:494
            from DWSIM .GlobalSettings import Settings #line:496
            Settings .SolverMode =0 #line:497
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim2 )#line:498
            O0O0OOOOOO00000OO ={}#line:500
            OO0OO000OO0O0O000 =O0OOOO0O0O0000O0O .GetTemperature ()-273.15 #line:502
            OO000OOOOO000OO00 =O0OOOO0O0O0000O0O .GetPressure ()/1000.0 #line:504
            O0O0OOOOOO00000OO ['FV_cold_in_temp']=OO0OO000OO0O0O000 #line:506
            O0O0OOOOOO00000OO ['FV_cold_in_pres']=OO000OOOOO000OO00 #line:507
            O0000O00O00OOO000 =O0OOOO0O0O0000O0O .GetMassFlow ()*3600.0 #line:509
            O0O0OOOOOO00000OO ['FV_mass_flow']=O0000O00O00OOO000 #line:510
            O0O0OOOOOOO0O00OO =O0OO0OO0O0O0O00O0 .GetTemperature ()-273.15 #line:512
            OO0O0OOO0OO000O0O =O0OO0OO0O0O0O00O0 .GetPressure ()/1000.0 #line:514
            O0O0OOOOOO00000OO ['FV_cold_out_temp']=O0O0OOOOOOO0O00OO #line:516
            O0O0OOOOOO00000OO ['FV_cold_out_pres']=OO0O0OOO0OO000O0O #line:517
            O0000OO0000OO0OO0 =O000O00O00OO000O0 .GetTemperature ()-273.15 #line:519
            OO0OOOO00O00OOOOO =O0000OO0000OO0OO0 #line:522
            O0O0OOOOOO00000OO ['FV_stm_in_temp']=O0000OO0000OO0OO0 #line:525
            O0O0OOOOOO00000OO ['FV_stm_out_temp']=OO0OOOO00O00OOOOO #line:526
            O0O00OO0O0OO00OOO =abs (OOOO00OO0O00O0000 .GetPowerGeneratedOrConsumed ())#line:530
            OO0OO000O0000OO0O ['FV_Qc']=O0O00OO0O0OO00OOO #line:531
            O00O0O0O00OOOOO0O =((O0000OO0000OO0OO0 -O0O0OOOOOOO0O00OO )-(OO0OOOO00O00OOOOO -OO0OO000OO0O0O000 ))/np .log ((O0000OO0000OO0OO0 -O0O0OOOOOOO0O00OO )/(OO0OOOO00O00OOOOO -OO0OO000OO0O0O000 ))#line:534
            OO0OO000O0000OO0O ['FV_LMTD']=O00O0O0O00OOOOO0O #line:535
            O0OOOOOO0O000O000 =6.1 #line:538
            OOO0O0OOOO0000O0O =O0O00OO0O0OO00OOO /(O0OOOOOO0O000O000 *O00O0O0O00OOOOO0O )*1000 #line:539
            OO0OO000O0000OO0O ['FV_U']=OOO0O0OOOO0000O0O #line:540
            OOOO00O00O00000OO =424.0 #line:543
            OO0O0O0O0O0O00O00 .cursor .execute ('''select "Value" from public."Output_Tags" where "TagName" = 'FV_fouling_factor';''')#line:546
            O00O00O000000O0OO =OO0O0O0O0O0O00O00 .cursor .fetchall ()#line:547
            OO0O0O0O0O0O00O00 .conn .commit ()#line:548
            OOOO0O000000O0OOO =O00O00O000000O0OO [0 ][0 ]#line:549
            if OO0000000OOOOOO00 ['FG_FV_DischFlow']>2500 :#line:551
                OO000OO0OO0OO00O0 =(1 /OOO0O0OOOO0000O0O )-(1 /OOOO00O00O00000OO )#line:552
                OO000OO0OO0OO00O0 =(1 -OO000OO0OO0OO00O0 )*100 #line:553
            elif OOOO0O000000O0OOO <100.0 :#line:554
                OO000OO0OO0OO00O0 =OOOO0O000000O0OOO #line:555
            else :#line:556
                OO000OO0OO0OO00O0 =100 #line:557
            OO0OO000O0000OO0O ['FV_fouling_factor']=OO000OO0OO0OO00O0 #line:559
            OO0O0OOOOOOOOOOO0 =O0OOOO0O0O0000O0O .GetMassEnthalpy ()#line:562
            OO0OO000O0000OO0O ['FV_cold_in_specific_enthalpy']=OO0O0OOOOOOOOOOO0 #line:563
            O0O0OOO00OO00OO00 =O0OO0OO0O0O0O00O0 .GetMassEnthalpy ()#line:566
            OO0OO000O0000OO0O ['FV_cold_out_specific_enthalpy']=O0O0OOO00OO00OO00 #line:567
            O0O0O0OO0000O000O =O0O0OOOOOOO0O00OO -OO0OO000OO0O0O000 #line:570
            OO0OO000O0000OO0O ['FV_cold_temp_rise']=O0O0O0OO0000O000O #line:571
            O0OOO0000O00OOOO0 =O0000OO0000OO0OO0 -O0O0OOOOOOO0O00OO #line:574
            OO0OO000O0000OO0O ['FV_minimum_approach']=O0OOO0000O00OOOO0 #line:575
            O000OOO000OO0000O =O000O00O00OO000O0 .GetMassFlow ()*3600 #line:578
            OO0OO000O0000OO0O ['FV_steam_required']=O000OOO000OO0000O #line:579
            O0OOO000000O00O0O =O0OOOO0O0O0000O0O .GetEnergyFlow ()#line:585
            OO0OO000O0000OO0O ['FV_cold_in_energy_flow']=O0OOO000000O00O0O #line:586
            OO00OO000OO0O0O0O =O0OO0OO0O0O0O00O0 .GetEnergyFlow ()#line:588
            OO0OO000O0000OO0O ['FV_cold_out_energy_flow']=OO00OO000OO0O0O0O #line:589
            for O00000O00O0O00O00 in OO0OO000O0000OO0O .keys ():#line:591
                OO0OO000O0000OO0O [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OO0OO000O0000OO0O [O00000O00O0O00O00 ]))#line:592
        if O0O0O00000O000O00 ['LNGV']==1 :#line:595
            print ("starting dwsim LNGV")#line:597
            OO0O00O0O0O0O0OO0 =OO0O0O0O0O0O00O00 .sim3 .GetFlowsheetSimulationObject ('LNGV_cold_in').GetAsObject ()#line:600
            OO0O0OO00OO0OO000 =OO0O0O0O0O0O00O00 .sim3 .GetFlowsheetSimulationObject ('LNGV_cold_out').GetAsObject ()#line:601
            OOO0O000O0O0OO000 =OO0O0O0O0O0O00O00 .sim3 .GetFlowsheetSimulationObject ('LNGV_HT_1').GetAsObject ()#line:602
            O0O0O0000O0OO0OOO =OO0O0O0O0O0O00O00 .sim3 .GetFlowsheetSimulationObject ('LNGV_stm_in').GetAsObject ()#line:603
            O0O0OOO0O00O0O0OO =OO0O0O0O0O0O00O00 .sim3 .GetFlowsheetSimulationObject ('LNGV_stm_out').GetAsObject ()#line:604
            OO0O00O0O0O0O0OO0 .SetTemperature (OO0000000OOOOOO00 ['CM_LNGVapr_InTempInd']+273.15 )#line:611
            OO0O00O0O0O0O0OO0 .SetPressure (OO0000000OOOOOO00 ['CM_LNGVapr_InPrs']*1000.0 )#line:612
            OO0O00O0O0O0O0OO0 .SetMassFlow (OO0000000OOOOOO00 ['FG_Flow_VaprToAtm']/3600.0 )#line:613
            OOO0O000O0O0OO000 .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LNGVapr_OutTempInd']+273.15 )#line:614
            O00O00OOOOOOOOO00 =OO0000000OOOOOO00 ['CM_LNGVapr_InPrs']-OO0000000OOOOOO00 ['CM_LNGVapr_OutPrs']#line:615
            OOO0O000O0O0OO000 .set_DeltaP (O00O00OOOOOOOOO00 *1000.0 )#line:616
            O0O0O0000O0OO0OOO .SetTemperature (OO0000000OOOOOO00 ['CM_LNGVapr_CondWtrTempInd']+273.15 )#line:617
            from DWSIM .GlobalSettings import Settings #line:619
            Settings .SolverMode =0 #line:620
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim3 )#line:621
            O0OOO0000OO0O0O0O ={}#line:623
            O0O0O00OOO0OOO00O =OO0O00O0O0O0O0OO0 .GetTemperature ()-273.15 #line:625
            OOO00O000O0O0000O =OO0O00O0O0O0O0OO0 .GetPressure ()/1000.0 #line:627
            O0OOO0000OO0O0O0O ['LNGV_cold_in_temp']=O0O0O00OOO0OOO00O #line:629
            O0OOO0000OO0O0O0O ['LNGV_cold_in_pres']=OOO00O000O0O0000O #line:630
            O0OOO0O0OOOO0O0OO =OO0O00O0O0O0O0OO0 .GetMassFlow ()*3600.0 #line:632
            O0OOO0000OO0O0O0O ['LNGV_mass_flow']=O0OOO0O0OOOO0O0OO #line:633
            O0O0000O0O0OOO000 =OO0O0OO00OO0OO000 .GetTemperature ()-273.15 #line:635
            OO000O0000OOO0OOO =OO0O0OO00OO0OO000 .GetPressure ()/1000.0 #line:637
            O0OOO0000OO0O0O0O ['LNGV_cold_out_temp']=O0O0000O0O0OOO000 #line:639
            O0OOO0000OO0O0O0O ['LNGV_cold_out_pres']=OO000O0000OOO0OOO #line:640
            OOO00OOO0OO0000OO =O0O0O0000O0OO0OOO .GetTemperature ()-273.15 #line:642
            OO00O0O000O000000 =OOO00OOO0OO0000OO #line:645
            O0OOO0000OO0O0O0O ['LNGV_stm_in_temp']=OOO00OOO0OO0000OO #line:648
            O0OOO0000OO0O0O0O ['LNGV_stm_out_temp']=OO00O0O000O000000 #line:649
            O0OOO0OO000000O00 =abs (OOO0O000O0O0OO000 .GetPowerGeneratedOrConsumed ())#line:653
            OO0OOO0O00O0O0O0O ['LNGV_Qc']=O0OOO0OO000000O00 #line:654
            OO0OOOOOOOOO0OO00 =((OOO00OOO0OO0000OO -O0O0000O0O0OOO000 )-(OO00O0O000O000000 -O0O0O00OOO0OOO00O ))/np .log ((OOO00OOO0OO0000OO -O0O0000O0O0OOO000 )/(OO00O0O000O000000 -O0O0O00OOO0OOO00O ))#line:657
            OO0OOO0O00O0O0O0O ['LNGV_LMTD']=OO0OOOOOOOOO0OO00 #line:658
            O00O0O0000OOOO00O =71.0 #line:661
            OO0OOOO0O00OOOOOO =O0OOO0OO000000O00 /(O00O0O0000OOOO00O *OO0OOOOOOOOO0OO00 )*1000 #line:662
            OO0OOO0O00O0O0O0O ['LNGV_U']=OO0OOOO0O00OOOOOO #line:663
            OOO0OOO000OOOO0OO =183.8 #line:666
            OO0O0O0O0O0O00O00 .cursor .execute ('''select "Value" from public."Output_Tags" where "TagName" = 'LNGV_fouling_factor';''')#line:669
            O00O00O000000O0OO =OO0O0O0O0O0O00O00 .cursor .fetchall ()#line:670
            OO0O0O0O0O0O00O00 .conn .commit ()#line:671
            OOOO0O000000O0OOO =O00O00O000000O0OO [0 ][0 ]#line:672
            if OO0000000OOOOOO00 ['FG_Flow_VaprToAtm']>20000 :#line:674
                OOO0O00000OO00OOO =(1 /OO0OOOO0O00OOOOOO )-(1 /OOO0OOO000OOOO0OO )#line:675
                OOO0O00000OO00OOO =(1 -OOO0O00000OO00OOO )*100 #line:676
            elif OOOO0O000000O0OOO <100.0 :#line:677
                OOO0O00000OO00OOO =OOOO0O000000O0OOO #line:678
            else :#line:679
                OOO0O00000OO00OOO =100 #line:680
            OO0OOO0O00O0O0O0O ['LNGV_fouling_factor']=OOO0O00000OO00OOO #line:682
            OOO0O000O0000OO0O =OO0O00O0O0O0O0OO0 .GetMassEnthalpy ()#line:685
            OO0OOO0O00O0O0O0O ['LNGV_cold_in_specific_enthalpy']=OOO0O000O0000OO0O #line:686
            OOO0OOOOO0OOO0000 =OO0O0OO00OO0OO000 .GetMassEnthalpy ()#line:689
            OO0OOO0O00O0O0O0O ['LNGV_cold_out_specific_enthalpy']=OOO0OOOOO0OOO0000 #line:690
            O00OO00OOOO0O00O0 =O0O0000O0O0OOO000 -O0O0O00OOO0OOO00O #line:693
            OO0OOO0O00O0O0O0O ['LNGV_cold_temp_rise']=O00OO00OOOO0O00O0 #line:694
            O000OO0O00O0O00OO =OOO00OOO0OO0000OO -O0O0000O0O0OOO000 #line:697
            OO0OOO0O00O0O0O0O ['LNGV_minimum_approach']=O000OO0O00O0O00OO #line:698
            OO000O0O0OOOOOO00 =O0O0O0000O0OO0OOO .GetMassFlow ()*3600 #line:701
            OO0OOO0O00O0O0O0O ['LNGV_steam_required']=OO000O0O0OOOOOO00 #line:702
            OO00000O00O0000O0 =OO0O00O0O0O0O0OO0 .GetEnergyFlow ()#line:708
            OO0OOO0O00O0O0O0O ['LNGV_cold_in_energy_flow']=OO00000O00O0000O0 #line:709
            O000O0000OOOOOO0O =OO0O0OO00OO0OO000 .GetEnergyFlow ()#line:711
            OO0OOO0O00O0O0O0O ['LNGV_cold_out_energy_flow']=O000O0000OOOOOO0O #line:712
            for O00000O00O0O00O00 in OO0OOO0O00O0O0O0O .keys ():#line:714
                OO0OOO0O00O0O0O0O [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OO0OOO0O00O0O0O0O [O00000O00O0O00O00 ]))#line:715
        if O0O0O00000O000O00 ['BOGH']==1 :#line:718
            print ("starting dwsim BOGH")#line:721
            OOO0OO000OO000O00 =OO0O0O0O0O0O00O00 .sim4 .GetFlowsheetSimulationObject ('BOGH_cold_in').GetAsObject ()#line:725
            O0OOOO00OO0000OO0 =OO0O0O0O0O0O00O00 .sim4 .GetFlowsheetSimulationObject ('BOGH_cold_out').GetAsObject ()#line:726
            OOO00OO00OOO0OO00 =OO0O0O0O0O0O00O00 .sim4 .GetFlowsheetSimulationObject ('BOGH_HT_1').GetAsObject ()#line:727
            OOOO0OOO000000O00 =OO0O0O0O0O0O00O00 .sim4 .GetFlowsheetSimulationObject ('BOGH_stm_in').GetAsObject ()#line:728
            OO00OOO00O000OOO0 =OO0O0O0O0O0O00O00 .sim4 .GetFlowsheetSimulationObject ('BOGH_stm_out').GetAsObject ()#line:729
            OOO0OO000OO000O00 .SetTemperature (OO0000000OOOOOO00 ['FG_FV_OutTempInd']+273.15 )#line:735
            OOO0OO000OO000O00 .SetPressure (OO0000000OOOOOO00 ['FG_FV_OutPrs']*1000.0 )#line:736
            OOO0OO000OO000O00 .SetMassFlow (OO0000000OOOOOO00 ['FG_FV_DischFlow']/3600.0 )#line:737
            OOO00OO00OOO0OO00 .set_OutletTemperature (OO0000000OOOOOO00 ['FG_FBOG_BogHtr_OutTempInd']+273.15 )#line:738
            O0000000OOOOOOO0O =OO0000000OOOOOO00 ['FG_FV_OutPrs']-OO0000000OOOOOO00 ['FG_FBOG_BogHtr_OutPrs']#line:739
            OOO00OO00OOO0OO00 .set_DeltaP (O0000000OOOOOOO0O *1000.0 )#line:740
            OOOO0OOO000000O00 .SetTemperature (OO0000000OOOOOO00 ['FG_FBOG_BogHtr_CondWtrTempInd']+273.15 )#line:741
            from DWSIM .GlobalSettings import Settings #line:743
            Settings .SolverMode =0 #line:744
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim4 )#line:745
            O00O00OO0OOO00OOO ={}#line:748
            O0OOOO0O000000O00 =OOO0OO000OO000O00 .GetTemperature ()-273.15 #line:750
            O00O00O0O0O0OOOO0 =OOO0OO000OO000O00 .GetPressure ()/1000.0 #line:752
            O00O00OO0OOO00OOO ['BOGH_cold_in_temp']=O0OOOO0O000000O00 #line:754
            O00O00OO0OOO00OOO ['BOGH_cold_in_pres']=O00O00O0O0O0OOOO0 #line:755
            O000O0OO0OOO0O0O0 =OOO0OO000OO000O00 .GetMassFlow ()*3600.0 #line:757
            O00O00OO0OOO00OOO ['BOGH_mass_flow']=O000O0OO0OOO0O0O0 #line:758
            OO000OOOOO0OO0OO0 =O0OOOO00OO0000OO0 .GetTemperature ()-273.15 #line:760
            OO0000000O0OOO0OO =O0OOOO00OO0000OO0 .GetPressure ()/1000.0 #line:762
            O00O00OO0OOO00OOO ['BOGH_cold_out_temp']=OO000OOOOO0OO0OO0 #line:764
            O00O00OO0OOO00OOO ['BOGH_cold_out_pres']=OO0000000O0OOO0OO #line:765
            O000OOO00O0O000O0 =OOOO0OOO000000O00 .GetTemperature ()-273.15 #line:767
            OOOOO0O00O00OOOO0 =O000OOO00O0O000O0 #line:770
            O00O00OO0OOO00OOO ['BOGH_stm_in_temp']=O000OOO00O0O000O0 #line:773
            O00O00OO0OOO00OOO ['BOGH_stm_out_temp']=OOOOO0O00O00OOOO0 #line:774
            OOO00O00O0O0O00OO =abs (OOO00OO00OOO0OO00 .GetPowerGeneratedOrConsumed ())#line:778
            O000OO000OO00O0OO ['BOGH_Qc']=OOO00O00O0O0O00OO #line:779
            O00O0OOO0OO0O00O0 =((O000OOO00O0O000O0 -OO000OOOOO0OO0OO0 )-(OOOOO0O00O00OOOO0 -O0OOOO0O000000O00 ))/np .log ((O000OOO00O0O000O0 -OO000OOOOO0OO0OO0 )/(OOOOO0O00O00OOOO0 -O0OOOO0O000000O00 ))#line:782
            O000OO000OO00O0OO ['BOGH_LMTD']=O00O0OOO0OO0O00O0 #line:783
            O0OO00O000OO0OO0O =15.5 #line:786
            OOO00OOOO00OOOO0O =OOO00O00O0O0O00OO /(O0OO00O000OO0OO0O *O00O0OOO0OO0O00O0 )*1000 #line:787
            O000OO000OO00O0OO ['BOGH_U']=OOO00OOOO00OOOO0O #line:788
            O00O000OOOO00OOO0 =145.0 #line:791
            OO0O0O0O0O0O00O00 .cursor .execute ('''select "Value" from public."Output_Tags" where "TagName" = 'BOGH_fouling_factor';''')#line:794
            O00O00O000000O0OO =OO0O0O0O0O0O00O00 .cursor .fetchall ()#line:795
            OO0O0O0O0O0O00O00 .conn .commit ()#line:796
            OOOO0O000000O0OOO =O00O00O000000O0OO [0 ][0 ]#line:797
            if OO0000000OOOOOO00 ['FG_FV_DischFlow']>2500 :#line:799
                O0OO0O0OO0O0O000O =(1 /OOO00OOOO00OOOO0O )-(1 /O00O000OOOO00OOO0 )#line:800
                O0OO0O0OO0O0O000O =(1 -O0OO0O0OO0O0O000O )*100 #line:801
            elif OOOO0O000000O0OOO <100.0 :#line:802
                O0OO0O0OO0O0O000O =OOOO0O000000O0OOO #line:803
            else :#line:804
                O0OO0O0OO0O0O000O =100 #line:805
            O000OO000OO00O0OO ['BOGH_fouling_factor']=O0OO0O0OO0O0O000O #line:807
            OO0OOO0O0000000OO =OOO0OO000OO000O00 .GetMassEnthalpy ()#line:810
            O000OO000OO00O0OO ['BOGH_cold_in_specific_enthalpy']=OO0OOO0O0000000OO #line:811
            OOO000OO0O00O00OO =O0OOOO00OO0000OO0 .GetMassEnthalpy ()#line:814
            O000OO000OO00O0OO ['BOGH_cold_out_specific_enthalpy']=OOO000OO0O00O00OO #line:815
            OOO000O00OOOO0000 =OO000OOOOO0OO0OO0 -O0OOOO0O000000O00 #line:818
            O000OO000OO00O0OO ['BOGH_cold_temp_rise']=OOO000O00OOOO0000 #line:819
            OOO0O000000O0O00O =O000OOO00O0O000O0 -OO000OOOOO0OO0OO0 #line:822
            O000OO000OO00O0OO ['BOGH_minimum_approach']=OOO0O000000O0O00O #line:823
            O000O0000OO000O00 =OOOO0OOO000000O00 .GetMassFlow ()*3600 #line:826
            O000OO000OO00O0OO ['BOGH_steam_required']=O000O0000OO000O00 #line:827
            O000OO000OO0O0O0O =OOO0OO000OO000O00 .GetEnergyFlow ()#line:833
            O000OO000OO00O0OO ['BOGH_cold_in_energy_flow']=O000OO000OO0O0O0O #line:834
            O0O00O0OO0OOOO000 =O0OOOO00OO0000OO0 .GetEnergyFlow ()#line:836
            O000OO000OO00O0OO ['BOGH_cold_out_energy_flow']=O0O00O0OO0OOOO000 #line:837
            for O00000O00O0O00O00 in O000OO000OO00O0OO .keys ():#line:839
                O000OO000OO00O0OO [O00000O00O0O00O00 ]=float ("{0:.2f}".format (O000OO000OO00O0OO [O00000O00O0O00O00 ]))#line:840
        if O0O0O00000O000O00 ['WUH']==1 :#line:843
            print ("starting dwsim WUH")#line:845
            OO000OO0000000000 =OO0O0O0O0O0O00O00 .sim5 .GetFlowsheetSimulationObject ('WUH_cold_in').GetAsObject ()#line:848
            OO0000000000O0OO0 =OO0O0O0O0O0O00O00 .sim5 .GetFlowsheetSimulationObject ('WUH_cold_out').GetAsObject ()#line:849
            O0000000O0O0OO000 =OO0O0O0O0O0O00O00 .sim5 .GetFlowsheetSimulationObject ('WUH_HT_1').GetAsObject ()#line:850
            OOOOOO000000000OO =OO0O0O0O0O0O00O00 .sim5 .GetFlowsheetSimulationObject ('WUH_stm_in').GetAsObject ()#line:851
            OO00O0OOO0O0000OO =OO0O0O0O0O0O00O00 .sim5 .GetFlowsheetSimulationObject ('WUH_stm_out').GetAsObject ()#line:852
            OO000OO0000000000 .SetTemperature (OO0000000OOOOOO00 ['FG_FBOG_WuHtr_InTempInd']+273.15 )#line:858
            OO000OO0000000000 .SetPressure (OO0000000OOOOOO00 ['FG_FBOG_WuHtr_InPrs']*1000.0 )#line:859
            O0000000O0O0OO000 .set_OutletTemperature (OO0000000OOOOOO00 ['FG_FBOG_WuHtr_OutTempInd']+273.15 )#line:861
            OOOOO000O0OOOOOOO =OO0000000OOOOOO00 ['FG_FBOG_WuHtr_InPrs']-OO0000000OOOOOO00 ['FG_FBOG_WuHtr_OutPrs']#line:862
            O0000000O0O0OO000 .set_DeltaP (OOOOO000O0OOOOOOO *1000.0 )#line:863
            OOOOOO000000000OO .SetTemperature (OO0000000OOOOOO00 ['FG_FBOG_WuHtr_CondWtrTempInd']+273.15 )#line:864
            from DWSIM .GlobalSettings import Settings #line:866
            Settings .SolverMode =0 #line:867
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim5 )#line:868
            O0O0000O0O0000000 ={}#line:870
            OO0OO0O0OOOO00000 =OO000OO0000000000 .GetTemperature ()-273.15 #line:872
            O000O0O00O0OO0O00 =OO000OO0000000000 .GetPressure ()/1000.0 #line:874
            O0O0000O0O0000000 ['WUH_cold_in_temp']=OO0OO0O0OOOO00000 #line:876
            O0O0000O0O0000000 ['WUH_cold_in_pres']=O000O0O00O0OO0O00 #line:877
            O00O0000OOOOOOO00 =OO000OO0000000000 .GetMassFlow ()*3600.0 #line:879
            O0O0000O0O0000000 ['WUH_mass_flow']=O00O0000OOOOOOO00 #line:880
            OOOO000O00O000OO0 =OO0000000000O0OO0 .GetTemperature ()-273.15 #line:882
            O0O00O00OOOOOOOO0 =OO0000000000O0OO0 .GetPressure ()/1000.0 #line:884
            O0O0000O0O0000000 ['WUH_cold_out_temp']=OOOO000O00O000OO0 #line:886
            O0O0000O0O0000000 ['WUH_cold_out_pres']=O0O00O00OOOOOOOO0 #line:887
            OO0000OOOOO0OO0O0 =OOOOOO000000000OO .GetTemperature ()-273.15 #line:889
            O0O0000OO00O00OOO =OO0000OOOOO0OO0O0 #line:892
            O0O0000O0O0000000 ['WUH_stm_in_temp']=OO0000OOOOO0OO0O0 #line:895
            O0O0000O0O0000000 ['WUH_stm_out_temp']=O0O0000OO00O00OOO #line:896
            O0OO0OOOOO0OOOOOO =abs (O0000000O0O0OO000 .GetPowerGeneratedOrConsumed ())#line:900
            OOOO000O0O0O0000O ['WUH_Qc']=O0OO0OOOOO0OOOOOO #line:901
            OO0OOOOOO0O000O0O =((OO0000OOOOO0OO0O0 -OOOO000O00O000OO0 )-(O0O0000OO00O00OOO -OO0OO0O0OOOO00000 ))/np .log ((OO0000OOOOO0OO0O0 -OOOO000O00O000OO0 )/(O0O0000OO00O00OOO -OO0OO0O0OOOO00000 ))#line:904
            OOOO000O0O0O0000O ['WUH_LMTD']=OO0OOOOOO0O000O0O #line:905
            O0OOO00OOO000OO00 =38.2 #line:908
            O00OOO0O0O0000OOO =O0OO0OOOOO0OOOOOO /(O0OOO00OOO000OO00 *OO0OOOOOO0O000O0O )*1000 #line:909
            OOOO000O0O0O0000O ['WUH_U']=O00OOO0O0O0000OOO #line:910
            O00O000OO000OO000 =394.6 #line:913
            O0000OOOO0O0O00O0 =100 #line:917
            OOOO000O0O0O0000O ['WUH_fouling_factor']=O0000OOOO0O0O00O0 #line:918
            OOO0O0000OOO0O000 =OO000OO0000000000 .GetMassEnthalpy ()#line:921
            OOOO000O0O0O0000O ['WUH_cold_in_specific_enthalpy']=OOO0O0000OOO0O000 #line:922
            O0OOOO0OOO000OOOO =OO0000000000O0OO0 .GetMassEnthalpy ()#line:925
            OOOO000O0O0O0000O ['WUH_cold_out_specific_enthalpy']=O0OOOO0OOO000OOOO #line:926
            O00000O0O0O0O0O00 =OOOO000O00O000OO0 -OO0OO0O0OOOO00000 #line:929
            OOOO000O0O0O0000O ['WUH_cold_temp_rise']=O00000O0O0O0O0O00 #line:930
            O0OO0OO00O00O0O0O =OO0000OOOOO0OO0O0 -OOOO000O00O000OO0 #line:933
            OOOO000O0O0O0000O ['WUH_minimum_approach']=O0OO0OO00O00O0O0O #line:934
            OO0000OO000000OOO =OOOOOO000000000OO .GetMassFlow ()*3600 #line:937
            OOOO000O0O0O0000O ['WUH_steam_required']=OO0000OO000000OOO #line:938
            O0OOO0O0O00000O0O =OO000OO0000000000 .GetEnergyFlow ()#line:944
            OOOO000O0O0O0000O ['WUH_cold_in_energy_flow']=O0OOO0O0O00000O0O #line:945
            O00OO0O0O0O00O000 =OO0000000000O0OO0 .GetEnergyFlow ()#line:947
            OOOO000O0O0O0000O ['WUH_cold_out_energy_flow']=O00OO0O0O0O00O000 #line:948
            for O00000O00O0O00O00 in OOOO000O0O0O0000O .keys ():#line:950
                OOOO000O0O0O0000O [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OOOO000O0O0O0000O [O00000O00O0O00O00 ]))#line:951
        if O0O0O00000O000O00 ['GWH_Stm']==1 :#line:954
            print ("starting dwsim GWH_Stm")#line:956
            OO0OOO00OOOOO0O0O =OO0O0O0O0O0O00O00 .sim6 .GetFlowsheetSimulationObject ('GWHS_cold_in').GetAsObject ()#line:959
            O00000O0OO0OOOOO0 =OO0O0O0O0O0O00O00 .sim6 .GetFlowsheetSimulationObject ('GWHS_cold_out').GetAsObject ()#line:960
            OOO00OO0O0000O0OO =OO0O0O0O0O0O00O00 .sim6 .GetFlowsheetSimulationObject ('GWHS_HT_1').GetAsObject ()#line:961
            OO000O00OOOOO00O0 =OO0O0O0O0O0O00O00 .sim6 .GetFlowsheetSimulationObject ('GWHS_stm_in').GetAsObject ()#line:962
            OO00000O0OOO0O0OO =OO0O0O0O0O0O00O00 .sim6 .GetFlowsheetSimulationObject ('GWHS_stm_out').GetAsObject ()#line:963
            OO0OOO00OOOOO0O0O .SetTemperature (OO0000000OOOOOO00 ['FG_GW_MainHtr_RtnTemp']+273.15 )#line:971
            OO0OOO00OOOOO0O0O .SetPressure (OO0000000OOOOOO00 ['FG_GW_MainHtr_InPrs']*1000.0 )#line:972
            OOO00OO0O0000O0OO .set_OutletTemperature (OO0000000OOOOOO00 ['FG_GW_MainHtr_OutTempCtrl']+273.15 )#line:974
            from DWSIM .GlobalSettings import Settings #line:977
            Settings .SolverMode =0 #line:978
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim6 )#line:979
            O0OO0O000O0OOOO00 ={}#line:981
            O0OO00OO0000O00O0 =OO0OOO00OOOOO0O0O .GetTemperature ()-273.15 #line:983
            O0O00O00OOO0O0OOO =OO0OOO00OOOOO0O0O .GetPressure ()/1000.0 #line:985
            O0OO0O000O0OOOO00 ['GWHS_cold_in_temp']=O0OO00OO0000O00O0 #line:987
            O0OO0O000O0OOOO00 ['GWHS_cold_in_pres']=O0O00O00OOO0O0OOO #line:988
            O0O0OOOO0OO0O0OO0 =OO0OOO00OOOOO0O0O .GetMassFlow ()*3600.0 #line:990
            O0OO0O000O0OOOO00 ['GWHS_mass_flow']=O0O0OOOO0OO0O0OO0 #line:991
            O0OO000O0000O0OO0 =O00000O0OO0OOOOO0 .GetTemperature ()-273.15 #line:993
            O00OOOO00OO000O00 =O00000O0OO0OOOOO0 .GetPressure ()/1000.0 #line:995
            O0OO0O000O0OOOO00 ['GWHS_cold_out_temp']=O0OO000O0000O0OO0 #line:997
            O0OO0O000O0OOOO00 ['GWHS_cold_out_pres']=O00OOOO00OO000O00 #line:998
            OOOO0O000000OO0OO =OO000O00OOOOO00O0 .GetTemperature ()-273.15 #line:1000
            OOO0O0O00O00O0O00 =OO00000O0OOO0O0OO .GetTemperature ()-273.15 #line:1001
            OOO0O0O00O00O0O00 =OOOO0O000000OO0OO #line:1003
            O0OO0O000O0OOOO00 ['GWHS_stm_in_temp']=OOOO0O000000OO0OO #line:1006
            O0OO0O000O0OOOO00 ['GWHS_stm_out_temp']=OOO0O0O00O00O0O00 #line:1007
            OO000O0O0OO0OOOO0 =abs (OOO00OO0O0000O0OO .GetPowerGeneratedOrConsumed ())#line:1011
            OOO0OOO00OOOO0000 ['GWHS_Qc']=OO000O0O0OO0OOOO0 #line:1012
            O00O00OOO00OOOOO0 =((OOOO0O000000OO0OO -O0OO000O0000O0OO0 )-(OOO0O0O00O00O0O00 -O0OO00OO0000O00O0 ))/np .log ((OOOO0O000000OO0OO -O0OO000O0000O0OO0 )/(OOO0O0O00O00O0O00 -O0OO00OO0000O00O0 ))#line:1015
            OOO0OOO00OOOO0000 ['GWHS_LMTD']=O00O00OOO00OOOOO0 #line:1016
            O00O0O0O0OO0OO00O =4.59 #line:1019
            O00O00O000OOOOOO0 =OO000O0O0OO0OOOO0 /(O00O0O0O0OO0OO00O *O00O00OOO00OOOOO0 )*1000 #line:1020
            OOO0OOO00OOOO0000 ['GWHS_U']=O00O00O000OOOOOO0 #line:1021
            O00OO0O000OOOOOOO =3375.8 #line:1024
            O0OOOO0O00O000O0O =100 #line:1030
            OOO0OOO00OOOO0000 ['GWHS_fouling_factor']=O0OOOO0O00O000O0O #line:1031
            O00OOO00O00000OOO =OO0OOO00OOOOO0O0O .GetMassEnthalpy ()#line:1034
            OOO0OOO00OOOO0000 ['GWHS_cold_in_specific_enthalpy']=O00OOO00O00000OOO #line:1035
            OO00O0000OO00OOOO =O00000O0OO0OOOOO0 .GetMassEnthalpy ()#line:1038
            OOO0OOO00OOOO0000 ['GWHS_cold_out_specific_enthalpy']=OO00O0000OO00OOOO #line:1039
            OO0OO0OOO0OOOO0OO =O0OO000O0000O0OO0 -O0OO00OO0000O00O0 #line:1042
            OOO0OOO00OOOO0000 ['GWHS_cold_temp_rise']=OO0OO0OOO0OOOO0OO #line:1043
            OOO00000OOOO00O0O =OOOO0O000000OO0OO -O0OO000O0000O0OO0 #line:1046
            OOO0OOO00OOOO0000 ['GWHS_minimum_approach']=OOO00000OOOO00O0O #line:1047
            OOOOOO00OOO000O0O =OO000O00OOOOO00O0 .GetMassFlow ()*3600 #line:1050
            OOO0OOO00OOOO0000 ['GWHS_steam_required']=OOOOOO00OOO000O0O #line:1051
            O000OO0000OO0OO0O =OO0OOO00OOOOO0O0O .GetEnergyFlow ()#line:1057
            OOO0OOO00OOOO0000 ['GWHS_cold_in_energy_flow']=O000OO0000OO0OO0O #line:1058
            OO00OOOOOOO00O0O0 =O00000O0OO0OOOOO0 .GetEnergyFlow ()#line:1060
            OOO0OOO00OOOO0000 ['GWHS_cold_out_energy_flow']=OO00OOOOOOO00O0O0 #line:1061
            for O00000O00O0O00O00 in OOO0OOO00OOOO0000 .keys ():#line:1063
                OOO0OOO00OOOO0000 [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OOO0OOO00OOOO0000 [O00000O00O0O00O00 ]))#line:1064
        if O0O0O00000O000O00 ['LD1']==1 :#line:1068
            print ("starting dwsim LD1")#line:1070
            OOOO0OO0OO00O0OOO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S1_in').GetAsObject ()#line:1073
            O0000OOOO0000O0OO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S1').GetAsObject ()#line:1074
            O00OO00OOOOO0OO0O =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S1_out_ideal').GetAsObject ()#line:1075
            O00000000OOO0OO00 =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S1_out_actual').GetAsObject ()#line:1076
            OO0OO0O000O0O0O0O =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_interclr').GetAsObject ()#line:1078
            O000OOO00OOOOO0OO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S2_in').GetAsObject ()#line:1080
            OO0O0O0OO00000OOO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S2').GetAsObject ()#line:1081
            O00O0OO0O0O00O0O0 =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S2_out_ideal').GetAsObject ()#line:1082
            O0OO0OO0OOOO0O0O0 =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_S2_out_actual').GetAsObject ()#line:1083
            OOOOO0000OOOO00OO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_afterclr').GetAsObject ()#line:1085
            O0OO0OO0O0O0000OO =OO0O0O0O0O0O00O00 .sim7 .GetFlowsheetSimulationObject ('LD1_out').GetAsObject ()#line:1086
            OOOO0OO0OO00O0OOO .SetPressure (OO0000000OOOOOO00 ['CM_LD1_CtrlPrs']*1000.0 )#line:1093
            OOOO0OO0OO00O0OOO .SetTemperature (OO0000000OOOOOO00 ['CM_LD1_CtrlTemp']+273.15 )#line:1094
            OOOO0OO0OO00O0OOO .SetMassFlow (OO0000000OOOOOO00 ['CM_LD1_Flow']/3600.0 )#line:1095
            O00000000OOO0OO00 .SetPressure (OO0000000OOOOOO00 ['CM_LD1_Stage2InPrs']*1000.0 )#line:1096
            O00000000OOO0OO00 .SetTemperature (OO0000000OOOOOO00 ['CM_LD1_Stage1DischAlrmTemp']+273.15 )#line:1097
            O00000000OOO0OO00 .SetMassFlow (OO0000000OOOOOO00 ['CM_LD1_Flow']/3600.0 )#line:1098
            O0000OOOO0000O0OO .set_POut (OO0000000OOOOOO00 ['CM_LD1_Stage2InPrs']*1000.0 )#line:1099
            OO0OO0O000O0O0O0O .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LD1_Stage2InTemp']+273.15 )#line:1100
            OO0O0O0OO00000OOO .set_POut (OO0000000OOOOOO00 ['CM_LD1_Stage2DischAlrmCtrlPrs']*1000.0 )#line:1104
            O0OO0OO0OOOO0O0O0 .SetPressure (OO0000000OOOOOO00 ['CM_LD1_Stage2DischAlrmCtrlPrs']*1000.0 )#line:1105
            O0OO0OO0OOOO0O0O0 .SetTemperature (OO0000000OOOOOO00 ['CM_LD1_Stage2DischAlrmTemp']+273.15 )#line:1106
            O0OO0OO0OOOO0O0O0 .SetMassFlow (OO0000000OOOOOO00 ['CM_LD1_Flow']/3600.0 )#line:1107
            OOOOO0000OOOO00OO .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LD1_DischTemp']+273.15 )#line:1108
            from DWSIM .GlobalSettings import Settings #line:1111
            Settings .SolverMode =0 #line:1112
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim7 )#line:1113
            O0OO0O00O0OOO0OOO ={}#line:1115
            O0000O0OOOO0OOOO0 =OOOO0OO0OO00O0OOO .GetPressure ()/1000.0 #line:1118
            O0OO0O00O0OOO0OOO ['LD1_S1_in_pres']=O0000O0OOOO0OOOO0 #line:1119
            O000OO000OOOO0OO0 =OOOO0OO0OO00O0OOO .GetTemperature ()-273.15 #line:1121
            O0OO0O00O0OOO0OOO ['LD1_S1_in_temp']=O000OO000OOOO0OO0 #line:1122
            OOOOO000000OOOOOO =OOOO0OO0OO00O0OOO .GetMassFlow ()*3600.0 #line:1124
            O0OO0O00O0OOO0OOO ['LD1_mass_flow']=OOOOO000000OOOOOO #line:1125
            OOO000OO0O0O0OOOO =O00OO00OOOOO0OO0O .GetPressure ()/1000.0 #line:1127
            O0OO0O00O0OOO0OOO ['LD1_S1_out_pres']=OOO000OO0O0O0OOOO #line:1128
            O0O0OOO000O0O0000 =O00000000OOO0OO00 .GetTemperature ()-273.15 #line:1130
            O0OO0O00O0OOO0OOO ['LD1_S1_out_temp']=O0O0OOO000O0O0000 #line:1131
            O00O00O0OO00OO000 =O000OOO00OOOOO0OO .GetPressure ()/1000.0 #line:1135
            O0OO0O00O0OOO0OOO ['LD1_S2_in_pres']=O00O00O0OO00OO000 #line:1136
            OOO0OOO0O00O00OOO =O000OOO00OOOOO0OO .GetTemperature ()-273.15 #line:1138
            O0OO0O00O0OOO0OOO ['LD1_S2_in_temp']=OOO0OOO0O00O00OOO #line:1139
            O0O0O00O0OOOO00OO =O00O0OO0O0O00O0O0 .GetPressure ()/1000.0 #line:1141
            O0OO0O00O0OOO0OOO ['LD1_S2_out_pres']=O0O0O00O0OOOO00OO #line:1142
            O0O00OOO0OO00O0OO =O0OO0OO0OOOO0O0O0 .GetTemperature ()-273.15 #line:1144
            O0OO0O00O0OOO0OOO ['LD1_S2_out_temp']=O0O00OOO0OO00O0OO #line:1145
            O0OOO0O000000000O =O0OO0OO0O0O0000OO .GetTemperature ()-273.15 #line:1147
            O0OO0O00O0OOO0OOO ['LD1_out_temp']=O0OOO0O000000000O #line:1148
            O0OOO0OO0O0O0OO0O =OOOO0OO0OO00O0OOO .GetMassEnthalpy ()#line:1153
            O00O0OOOO0000O00O ['LD1_S1_in_specific_enthalpy']=O0OOO0OO0O0O0OO0O #line:1154
            OO00OO000OO0O00O0 =OOO000OO0O0O0OOOO /O0000O0OOOO0OOOO0 #line:1156
            O00O0OOOO0000O00O ['LD1_S1_pressure_ratio']=OO00OO000OO0O00O0 #line:1157
            OO00O0OO0000000O0 =abs (O0000OOOO0000O0OO .GetPowerGeneratedOrConsumed ())#line:1162
            O00O0OOOO0000O00O ['LD1_S1_polytropic_power']=OO00O0OO0000000O0 #line:1163
            OOO0O00OO000OOOOO =O0000OOOO0000O0OO .get_PolytropicHead ()#line:1165
            O00O0OOOO0000O00O ['LD1_S1_polytropic_head']=OOO0O00OO000OOOOO #line:1166
            OOO0OO0OO0OO0O0OO =O00OO00OOOOO0OO0O .GetMassEnthalpy ()#line:1178
            OOO0000O0O0OOOO00 =O00000000OOO0OO00 .GetMassEnthalpy ()#line:1182
            O00O0OOOO0000O00O ['LD1_S1_out_actual_specific_enthalpy']=OOO0000O0O0OOOO00 #line:1183
            O00O0000OOO0OO0OO =OOO0OO0OO0OO0O0OO -O0OOO0OO0O0O0OO0O #line:1185
            O0OOOO00000OOO0O0 =OOO0000O0O0OOOO00 -O0OOO0OO0O0O0OO0O #line:1188
            O00O0OOOO0000O00O ['LD1_S1_actual_ethalpy_change']=O0OOOO00000OOO0O0 #line:1189
            if O0OOOO00000OOO0O0 ==0 :#line:1190
                O0OOOO00000OOO0O0 =1 #line:1191
            OO0O00OO00OO0O00O =(O00O0000OOO0OO0OO /O0OOOO00000OOO0O0 )*100 #line:1192
            O00O0OOOO0000O00O ['LD1_S1_polytropic_efficiency']=OO0O00OO00OO0O00O #line:1193
            OOOOOOO0OO00O0O0O =OO0OO0O000O0O0O0O .get_DeltaT ()#line:1195
            O00O0OOOO0000O00O ['LD1_interclr_deltaT']=OOOOOOO0OO00O0O0O #line:1196
            O0OO0O000O000O0OO =OO0OO0O000O0O0O0O .GetPowerGeneratedOrConsumed ()#line:1198
            O00O0OOOO0000O00O ['LD1_interclr_duty']=O0OO0O000O000O0OO #line:1199
            O0O0OO00OOOOOOO00 =O000OOO00OOOOO0OO .GetMassEnthalpy ()#line:1203
            O00O0OOOO0000O00O ['LD1_S2_in_specific_enthalpy']=O0O0OO00OOOOOOO00 #line:1204
            O0OO0OOO0OOOO0O00 =O0O0O00O0OOOO00OO /O00O00O0OO00OO000 #line:1206
            O00O0OOOO0000O00O ['LD1_S2_pressure_ratio']=O0OO0OOO0OOOO0O00 #line:1207
            O00OO00O00O0O0OO0 =abs (OO0O0O0OO00000OOO .GetPowerGeneratedOrConsumed ())#line:1212
            O00O0OOOO0000O00O ['LD1_S2_polytropic_power']=O00OO00O00O0O0OO0 #line:1213
            O0O0000OO00OOOO0O =OO0O0O0OO00000OOO .get_PolytropicHead ()#line:1215
            O00O0OOOO0000O00O ['LD1_S2_polytropic_head']=O0O0000OO00OOOO0O #line:1216
            O0OO00OOO0000O00O =O00O0OO0O0O00O0O0 .GetMassEnthalpy ()#line:1228
            OO0OO0OO0O0OO0O0O =O0OO0OO0OOOO0O0O0 .GetMassEnthalpy ()#line:1232
            O00O0OOOO0000O00O ['LD1_S2_out_actual_specific_enthalpy']=OO0OO0OO0O0OO0O0O #line:1233
            OO0OOOOOO0OOOOOOO =O0OO00OOO0000O00O -O0O0OO00OOOOOOO00 #line:1235
            O0O0O0O00O000O000 =OO0OO0OO0O0OO0O0O -O0O0OO00OOOOOOO00 #line:1238
            O00O0OOOO0000O00O ['LD1_S2_actual_ethalpy_change']=O0O0O0O00O000O000 #line:1239
            if O0O0O0O00O000O000 ==0 :#line:1241
                O0O0O0O00O000O000 =1 #line:1242
            O0OOO000O000O0000 =(OO0OOOOOO0OOOOOOO /O0O0O0O00O000O000 )*100 #line:1244
            O00O0OOOO0000O00O ['LD1_S2_polytropic_efficiency']=O0OOO000O000O0000 #line:1245
            OOO00O0OOO0000O00 =OOOOO0000OOOO00OO .get_DeltaT ()#line:1247
            O00O0OOOO0000O00O ['LD1_afterclr_deltaT']=OOO00O0OOO0000O00 #line:1248
            OOO0OOO0OOO0O00O0 =OOOOO0000OOOO00OO .GetPowerGeneratedOrConsumed ()#line:1250
            O00O0OOOO0000O00O ['LD1_afterclr_duty']=OOO0OOO0OOO0O00O0 #line:1251
            O000O000O000O000O =O0OO0OO0O0O0000OO .GetMassEnthalpy ()#line:1255
            O00O0OOOO0000O00O ['LD1_out_specific_enthalpy']=O000O000O000O000O #line:1256
            O00O0OOOO0000O00O ['LD1_polytropic_efficiency']=(OO0O00OO00OO0O00O +O0OOO000O000O0000 )/2 #line:1261
            for O00000O00O0O00O00 in O00O0OOOO0000O00O .keys ():#line:1263
                O00O0OOOO0000O00O [O00000O00O0O00O00 ]=float ("{0:.2f}".format (O00O0OOOO0000O00O [O00000O00O0O00O00 ]))#line:1264
        if O0O0O00000O000O00 ['LD2']==1 :#line:1267
            print ("starting dwsim LD2")#line:1269
            OOOOO00O0000OO0O0 =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S1_in').GetAsObject ()#line:1273
            O00O0OO0OOO0OOOO0 =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S1').GetAsObject ()#line:1274
            O00OO000O0O0OO0OO =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S1_out_ideal').GetAsObject ()#line:1275
            OOO0O0OO000O0O0OO =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S1_out_actual').GetAsObject ()#line:1276
            O0OO00OO0O0O00000 =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_interclr').GetAsObject ()#line:1278
            OOO000OOOO000O0OO =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S2_in').GetAsObject ()#line:1280
            O0O0O0O0O0O0OO000 =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S2').GetAsObject ()#line:1281
            OOO0O0O0O00O0OOOO =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S2_out_ideal').GetAsObject ()#line:1282
            O0O0000O000OO0OOO =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_S2_out_actual').GetAsObject ()#line:1283
            O00OO0000O0O0000O =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_afterclr').GetAsObject ()#line:1285
            O0O0O0O0O0000O00O =OO0O0O0O0O0O00O00 .sim8 .GetFlowsheetSimulationObject ('LD2_out').GetAsObject ()#line:1286
            OOOOO00O0000OO0O0 .SetPressure (OO0000000OOOOOO00 ['CM_LD2_CtrlPrs']*1000.0 )#line:1293
            OOOOO00O0000OO0O0 .SetTemperature (OO0000000OOOOOO00 ['CM_LD2_CtrlTemp']+273.15 )#line:1294
            OOOOO00O0000OO0O0 .SetMassFlow (OO0000000OOOOOO00 ['CM_LD2_Flow']/3600.0 )#line:1295
            OOO0O0OO000O0O0OO .SetPressure (OO0000000OOOOOO00 ['CM_LD2_Stage2InPrs']*1000.0 )#line:1296
            OOO0O0OO000O0O0OO .SetTemperature (OO0000000OOOOOO00 ['CM_LD2_Stage1DischAlrmTemp']+273.15 )#line:1297
            OOO0O0OO000O0O0OO .SetMassFlow (OO0000000OOOOOO00 ['CM_LD2_Flow']/3600.0 )#line:1298
            O00O0OO0OOO0OOOO0 .set_POut (OO0000000OOOOOO00 ['CM_LD2_Stage2InPrs']*1000.0 )#line:1299
            O0OO00OO0O0O00000 .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LD2_Stage2InTemp']+273.15 )#line:1300
            O0O0O0O0O0O0OO000 .set_POut (OO0000000OOOOOO00 ['CM_LD2_Stage2DischAlrmCtrlPrs']*1000.0 )#line:1304
            O0O0000O000OO0OOO .SetPressure (OO0000000OOOOOO00 ['CM_LD2_Stage2DischAlrmCtrlPrs']*1000.0 )#line:1305
            O0O0000O000OO0OOO .SetTemperature (OO0000000OOOOOO00 ['CM_LD2_Stage2DischAlrmTemp']+273.15 )#line:1306
            O0O0000O000OO0OOO .SetMassFlow (OO0000000OOOOOO00 ['CM_LD2_Flow']/3600.0 )#line:1307
            O00OO0000O0O0000O .set_OutletTemperature (OO0000000OOOOOO00 ['CM_LD2_DischTemp']+273.15 )#line:1308
            from DWSIM .GlobalSettings import Settings #line:1311
            Settings .SolverMode =0 #line:1312
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim8 )#line:1313
            O000OOO000OO00O00 ={}#line:1315
            OO0OOOO0O00OOO0O0 =OOOOO00O0000OO0O0 .GetPressure ()/1000.0 #line:1318
            O000OOO000OO00O00 ['LD2_S1_in_pres']=OO0OOOO0O00OOO0O0 #line:1319
            O00OOOOOOO0O0OOOO =OOOOO00O0000OO0O0 .GetTemperature ()-273.15 #line:1321
            O000OOO000OO00O00 ['LD2_S1_in_temp']=O00OOOOOOO0O0OOOO #line:1322
            O0OO0O0OO0O0OOOO0 =OOOOO00O0000OO0O0 .GetMassFlow ()*3600.0 #line:1324
            O000OOO000OO00O00 ['LD2_mass_flow']=O0OO0O0OO0O0OOOO0 #line:1325
            OO00O0O0OOO0O00O0 =O00OO000O0O0OO0OO .GetPressure ()/1000.0 #line:1327
            O000OOO000OO00O00 ['LD2_S1_out_pres']=OO00O0O0OOO0O00O0 #line:1328
            O0O00O0O00O000000 =OOO0O0OO000O0O0OO .GetTemperature ()-273.15 #line:1330
            O000OOO000OO00O00 ['LD2_S1_out_temp']=O0O00O0O00O000000 #line:1331
            OOO0O00O000O00O0O =OOO000OOOO000O0OO .GetPressure ()/1000.0 #line:1335
            O000OOO000OO00O00 ['LD2_S2_in_pres']=OOO0O00O000O00O0O #line:1336
            O0OOOO000O000O0OO =OOO000OOOO000O0OO .GetTemperature ()-273.15 #line:1338
            O000OOO000OO00O00 ['LD2_S2_in_temp']=O0OOOO000O000O0OO #line:1339
            O0OO0OO000O00OO0O =OOO0O0O0O00O0OOOO .GetPressure ()/1000.0 #line:1341
            O000OOO000OO00O00 ['LD2_S2_out_pres']=O0OO0OO000O00OO0O #line:1342
            OO00000O00O00O000 =O0O0000O000OO0OOO .GetTemperature ()-273.15 #line:1344
            O000OOO000OO00O00 ['LD2_S2_out_temp']=OO00000O00O00O000 #line:1345
            OOO0OO0O0000O0O0O =O0O0O0O0O0000O00O .GetTemperature ()-273.15 #line:1347
            O000OOO000OO00O00 ['LD2_out_temp']=OOO0OO0O0000O0O0O #line:1348
            OO0OO0O0O00O0OOOO =OOOOO00O0000OO0O0 .GetMassEnthalpy ()#line:1353
            O0OO0OO000OO0O0OO ['LD2_S1_in_specific_enthalpy']=OO0OO0O0O00O0OOOO #line:1354
            O0OOOOOO0OOO00O00 =OO00O0O0OOO0O00O0 /OO0OOOO0O00OOO0O0 #line:1356
            O0OO0OO000OO0O0OO ['LD2_S1_pressure_ratio']=O0OOOOOO0OOO00O00 #line:1357
            O0O0000OO0OO00OO0 =abs (O00O0OO0OOO0OOOO0 .GetPowerGeneratedOrConsumed ())#line:1362
            O0OO0OO000OO0O0OO ['LD2_S1_polytropic_power']=O0O0000OO0OO00OO0 #line:1363
            OOOO00OOO0OOO0O00 =O00O0OO0OOO0OOOO0 .get_PolytropicHead ()#line:1365
            O0OO0OO000OO0O0OO ['LD2_S1_polytropic_head']=OOOO00OOO0OOO0O00 #line:1366
            O00OOO00O0OOO0OOO =O00OO000O0O0OO0OO .GetMassEnthalpy ()#line:1378
            O00O00O0O0OO0000O =OOO0O0OO000O0O0OO .GetMassEnthalpy ()#line:1382
            O0OO0OO000OO0O0OO ['LD2_S1_out_actual_specific_enthalpy']=O00O00O0O0OO0000O #line:1383
            O0O0OOOOO00OO0000 =O00OOO00O0OOO0OOO -OO0OO0O0O00O0OOOO #line:1385
            O00OOO0OOO0O00O0O =O00O00O0O0OO0000O -OO0OO0O0O00O0OOOO #line:1388
            O0OO0OO000OO0O0OO ['LD2_S1_actual_ethalpy_change']=O00OOO0OOO0O00O0O #line:1389
            if O00OOO0OOO0O00O0O ==0 :#line:1391
                O00OOO0OOO0O00O0O =1 #line:1392
            OOO000O000OO00000 =(O0O0OOOOO00OO0000 /O00OOO0OOO0O00O0O )*100 #line:1393
            O0OO0OO000OO0O0OO ['LD2_S1_polytropic_efficiency']=OOO000O000OO00000 #line:1394
            O0OOOOOO0OOOOOO0O =O0OO00OO0O0O00000 .get_DeltaT ()#line:1396
            O0OO0OO000OO0O0OO ['LD2_interclr_deltaT']=O0OOOOOO0OOOOOO0O #line:1397
            O0OO0OOO00O00OOO0 =O0OO00OO0O0O00000 .GetPowerGeneratedOrConsumed ()#line:1399
            O0OO0OO000OO0O0OO ['LD2_interclr_duty']=O0OO0OOO00O00OOO0 #line:1400
            O000O0O0OO00O00O0 =OOO000OOOO000O0OO .GetMassEnthalpy ()#line:1404
            O0OO0OO000OO0O0OO ['LD2_S2_in_specific_enthalpy']=O000O0O0OO00O00O0 #line:1405
            O0OOO00OO00OO0OO0 =O0OO0OO000O00OO0O /OOO0O00O000O00O0O #line:1407
            O0OO0OO000OO0O0OO ['LD2_S2_pressure_ratio']=O0OOO00OO00OO0OO0 #line:1408
            O00O0OO000O0OO0O0 =abs (O0O0O0O0O0O0OO000 .GetPowerGeneratedOrConsumed ())#line:1413
            O0OO0OO000OO0O0OO ['LD2_S2_polytropic_power']=O00O0OO000O0OO0O0 #line:1414
            O0OOO0OO00000OOO0 =O0O0O0O0O0O0OO000 .get_PolytropicHead ()#line:1416
            O0OO0OO000OO0O0OO ['LD2_S2_polytropic_head']=O0OOO0OO00000OOO0 #line:1417
            O00O00O0O0OO0OO00 =OOO0O0O0O00O0OOOO .GetMassEnthalpy ()#line:1429
            OOOOO00O00O00OO0O =O0O0000O000OO0OOO .GetMassEnthalpy ()#line:1433
            O0OO0OO000OO0O0OO ['LD2_S2_out_actual_specific_enthalpy']=OOOOO00O00O00OO0O #line:1434
            OOO00O0OOO0000000 =O00O00O0O0OO0OO00 -O000O0O0OO00O00O0 #line:1436
            O00OO0000OO0O000O =OOOOO00O00O00OO0O -O000O0O0OO00O00O0 #line:1439
            O0OO0OO000OO0O0OO ['LD2_S2_actual_ethalpy_change']=O00OO0000OO0O000O #line:1440
            if O00OO0000OO0O000O ==0 :#line:1441
                O00OO0000OO0O000O =1 #line:1442
            OOO0OOO0000OO0O0O =(OOO00O0OOO0000000 /O00OO0000OO0O000O )*100 #line:1443
            O0OO0OO000OO0O0OO ['LD2_S2_polytropic_efficiency']=OOO0OOO0000OO0O0O #line:1444
            OOOOO000OO0OOO000 =O00OO0000O0O0000O .get_DeltaT ()#line:1446
            O0OO0OO000OO0O0OO ['LD2_afterclr_deltaT']=OOOOO000OO0OOO000 #line:1447
            OO000O0O0O00000O0 =O00OO0000O0O0000O .GetPowerGeneratedOrConsumed ()#line:1449
            O0OO0OO000OO0O0OO ['LD2_afterclr_duty']=OO000O0O0O00000O0 #line:1450
            OO0O0O00OOO0O00OO =O0O0O0O0O0000O00O .GetMassEnthalpy ()#line:1454
            O0OO0OO000OO0O0OO ['LD2_out_specific_enthalpy']=OO0O0O00OOO0O00OO #line:1455
            O0OO0OO000OO0O0OO ['LD2_polytropic_efficiency']=(OOO000O000OO00000 +OOO0OOO0000OO0O0O )/2 #line:1460
            for O00000O00O0O00O00 in O0OO0OO000OO0O0OO .keys ():#line:1462
                O0OO0OO000OO0O0OO [O00000O00O0O00O00 ]=float ("{0:.2f}".format (O0OO0OO000OO0O0OO [O00000O00O0O00O00 ]))#line:1463
        if O0O0O00000O000O00 ['HD1']==1 :#line:1466
            print ("starting dwsim HD1")#line:1468
            OOOOO0000OOOO0O00 =OO0O0O0O0O0O00O00 .sim9 .GetFlowsheetSimulationObject ('HD1_in').GetAsObject ()#line:1472
            O00O0OO00O000O000 =OO0O0O0O0O0O00O00 .sim9 .GetFlowsheetSimulationObject ('HD1').GetAsObject ()#line:1473
            O0OOO0O0O0O000O0O =OO0O0O0O0O0O00O00 .sim9 .GetFlowsheetSimulationObject ('HD1_out_ideal').GetAsObject ()#line:1474
            OO0000O000OO0OOO0 =OO0O0O0O0O0O00O00 .sim9 .GetFlowsheetSimulationObject ('HD1_out_actual').GetAsObject ()#line:1475
            OOOOO0000OOOO0O00 .SetPressure (OO0000000OOOOOO00 ['CM_HD1_InPrsAlrmCtrl']*1000.0 )#line:1481
            OOOOO0000OOOO0O00 .SetTemperature (OO0000000OOOOOO00 ['CM_HD1_InTemp']+273.15 )#line:1482
            OO0000O000OO0OOO0 .SetPressure (OO0000000OOOOOO00 ['CM_HD1_DischPrs']*1000.0 )#line:1484
            OO0000O000OO0OOO0 .SetTemperature (OO0000000OOOOOO00 ['CM_HD1_CtrlTemp']+273.15 )#line:1485
            O00O0OO00O000O000 .set_POut (OO0000000OOOOOO00 ['CM_HD1_DischPrs']*1000.0 )#line:1487
            from DWSIM .GlobalSettings import Settings #line:1490
            Settings .SolverMode =0 #line:1491
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim9 )#line:1492
            OOO000000O0O0O00O ={}#line:1494
            OO000OO0O0OO0OOO0 =OOOOO0000OOOO0O00 .GetPressure ()/1000.0 #line:1497
            OOO000000O0O0O00O ['HD1_in_pres']=OO000OO0O0OO0OOO0 #line:1498
            O00OO00OOO0O00000 =OOOOO0000OOOO0O00 .GetTemperature ()-273.15 #line:1500
            OOO000000O0O0O00O ['HD1_in_temp']=O00OO00OOO0O00000 #line:1501
            O0OOO0O0O000000OO =OOOOO0000OOOO0O00 .GetMassFlow ()*3600.0 #line:1503
            OOO000000O0O0O00O ['HD1_mass_flow']=O0OOO0O0O000000OO #line:1504
            OO0O0OOO0OOO0OOOO =O0OOO0O0O0O000O0O .GetPressure ()/1000.0 #line:1506
            OOO000000O0O0O00O ['HD1_out_pres']=OO0O0OOO0OOO0OOOO #line:1507
            O000000000O0O00O0 =OO0000O000OO0OOO0 .GetTemperature ()-273.15 #line:1509
            OOO000000O0O0O00O ['HD1_out_temp']=O000000000O0O00O0 #line:1510
            OOOOOOO0O00O00000 =OOOOO0000OOOO0O00 .GetMassEnthalpy ()#line:1514
            O0OO0O000OOO000OO ['HD1_in_specific_enthalpy']=OOOOOOO0O00O00000 #line:1515
            OO0OOO0OOO00O00O0 =OO0O0OOO0OOO0OOOO /OO000OO0O0OO0OOO0 #line:1517
            O0OO0O000OOO000OO ['HD1_pressure_ratio']=OO0OOO0OOO00O00O0 #line:1518
            OOO0OO00000OO0OOO =abs (O00O0OO00O000O000 .GetPowerGeneratedOrConsumed ())#line:1523
            O0OO0O000OOO000OO ['HD1_polytropic_power']=OOO0OO00000OO0OOO #line:1524
            O0O0O00OO000OO0O0 =O00O0OO00O000O000 .get_PolytropicHead ()#line:1526
            O0OO0O000OOO000OO ['HD1_polytropic_head']=O0O0O00OO000OO0O0 #line:1527
            O000OO0O000O00000 =O0OOO0O0O0O000O0O .GetMassEnthalpy ()#line:1538
            O0OO0O000OOO000OO ['HD1_out_ideal_specific_enthalpy']=O000OO0O000O00000 #line:1539
            OOOO00O00O0OOO00O =OO0000O000OO0OOO0 .GetMassEnthalpy ()#line:1542
            O0OO0O000OOO000OO ['HD1_out_actual_specific_enthalpy']=OOOO00O00O0OOO00O #line:1543
            OO00000O00000OOO0 =O000OO0O000O00000 -OOOOOOO0O00O00000 #line:1545
            O0000O0O00O0O00O0 =OOOO00O00O0OOO00O -OOOOOOO0O00O00000 #line:1548
            if O0000O0O00O0O00O0 ==0 :#line:1551
                O0000O0O00O0O00O0 =1 #line:1552
            OOOO0O0OO000OOOO0 =(OO00000O00000OOO0 /O0000O0O00O0O00O0 )*100 #line:1553
            O0OO0O000OOO000OO ['HD1_polytropic_efficiency']=OOOO0O0OO000OOOO0 #line:1554
            for O00000O00O0O00O00 in O0OO0O000OOO000OO .keys ():#line:1556
                O0OO0O000OOO000OO [O00000O00O0O00O00 ]=float ("{0:.2f}".format (O0OO0O000OOO000OO [O00000O00O0O00O00 ]))#line:1557
        if O0O0O00000O000O00 ['HD2']==1 :#line:1560
            print ("starting dwsim HD2")#line:1562
            OOOO0O0OOOOOOOOO0 =OO0O0O0O0O0O00O00 .sim10 .GetFlowsheetSimulationObject ('HD2_in').GetAsObject ()#line:1565
            O00OO0OOO00O0O000 =OO0O0O0O0O0O00O00 .sim10 .GetFlowsheetSimulationObject ('HD2').GetAsObject ()#line:1566
            O00OO00O00OOOOOO0 =OO0O0O0O0O0O00O00 .sim10 .GetFlowsheetSimulationObject ('HD2_out_ideal').GetAsObject ()#line:1567
            OOO0OOOO00OOO0O0O =OO0O0O0O0O0O00O00 .sim10 .GetFlowsheetSimulationObject ('HD2_out_actual').GetAsObject ()#line:1568
            OOOO0O0OOOOOOOOO0 .SetPressure (OO0000000OOOOOO00 ['CM_HD2_InPrsAlrmCtrl']*1000.0 )#line:1574
            OOOO0O0OOOOOOOOO0 .SetTemperature (OO0000000OOOOOO00 ['CM_HD2_InTemp']+273.15 )#line:1575
            OOO0OOOO00OOO0O0O .SetPressure (OO0000000OOOOOO00 ['CM_HD2_DischPrs']*1000.0 )#line:1577
            OOO0OOOO00OOO0O0O .SetTemperature (OO0000000OOOOOO00 ['CM_HD2_CtrlTemp']+273.15 )#line:1578
            O00OO0OOO00O0O000 .set_POut (OO0000000OOOOOO00 ['CM_HD2_DischPrs']*1000.0 )#line:1580
            from DWSIM .GlobalSettings import Settings #line:1583
            Settings .SolverMode =0 #line:1584
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .sim10 )#line:1585
            O0000000000OOOOO0 ={}#line:1587
            O0000O0OOOO0O0000 =OOOO0O0OOOOOOOOO0 .GetPressure ()/1000.0 #line:1590
            O0000000000OOOOO0 ['HD2_in_pres']=O0000O0OOOO0O0000 #line:1591
            OOOOOO0O000O000O0 =OOOO0O0OOOOOOOOO0 .GetTemperature ()-273.15 #line:1593
            O0000000000OOOOO0 ['HD2_in_temp']=OOOOOO0O000O000O0 #line:1594
            O000O000O00O0OOOO =OOOO0O0OOOOOOOOO0 .GetMassFlow ()*3600.0 #line:1596
            O0000000000OOOOO0 ['HD2_mass_flow']=O000O000O00O0OOOO #line:1597
            OO00OOO000O0O0OOO =O00OO00O00OOOOOO0 .GetPressure ()/1000.0 #line:1599
            O0000000000OOOOO0 ['HD2_out_pres']=OO00OOO000O0O0OOO #line:1600
            OOOO000OOOO0OO0O0 =OOO0OOOO00OOO0O0O .GetTemperature ()-273.15 #line:1602
            O0000000000OOOOO0 ['HD2_out_temp']=OOOO000OOOO0OO0O0 #line:1603
            OO0OOO000OO00000O =OOOO0O0OOOOOOOOO0 .GetMassEnthalpy ()#line:1607
            OO00O00000O0OO0O0 ['HD2_in_specific_enthalpy']=OO0OOO000OO00000O #line:1608
            OOOO0000O0OO00O00 =OO00OOO000O0O0OOO /O0000O0OOOO0O0000 #line:1610
            OO00O00000O0OO0O0 ['HD2_pressure_ratio']=OOOO0000O0OO00O00 #line:1611
            OO00O000O000OOO0O =abs (O00OO0OOO00O0O000 .GetPowerGeneratedOrConsumed ())#line:1616
            OO00O00000O0OO0O0 ['HD2_polytropic_power']=OO00O000O000OOO0O #line:1617
            OOOOOO0O0OO0OO0O0 =O00OO0OOO00O0O000 .get_PolytropicHead ()#line:1619
            OO00O00000O0OO0O0 ['HD2_polytropic_head']=OOOOOO0O0OO0OO0O0 #line:1620
            O0OO000O0OOO0000O =O00OO00O00OOOOOO0 .GetMassEnthalpy ()#line:1631
            OO00O00000O0OO0O0 ['HD2_out_ideal_specific_enthalpy']=O0OO000O0OOO0000O #line:1632
            OOOO0O000000O0O0O =OOO0OOOO00OOO0O0O .GetMassEnthalpy ()#line:1635
            OO00O00000O0OO0O0 ['HD2_out_actual_specific_enthalpy']=OOOO0O000000O0O0O #line:1636
            OOOO0OOO0O0OO00OO =O0OO000O0OOO0000O -OO0OOO000OO00000O #line:1638
            OOOOO0OOO0O000OOO =OOOO0O000000O0O0O -OO0OOO000OO00000O #line:1641
            if OOOOO0OOO0O000OOO ==0 :#line:1644
                OOOOO0OOO0O000OOO =1 #line:1645
            OOOOOOO0000OO0OO0 =(OOOO0OOO0O0OO00OO /OOOOO0OOO0O000OOO )*100 #line:1646
            OO00O00000O0OO0O0 ['HD2_polytropic_efficiency']=OOOOOOO0000OO0OO0 #line:1647
            for O00000O00O0O00O00 in OO00O00000O0OO0O0 .keys ():#line:1649
                OO00O00000O0OO0O0 [O00000O00O0O00O00 ]=float ("{0:.2f}".format (OO00O00000O0OO0O0 [O00000O00O0O00O00 ]))#line:1650
        OOOO0000000O000OO =0.72 #line:1653
        O0000OO0O00OO000O =3.086 #line:1654
        OOOOOOO000OO0O00O =5 #line:1655
        O000O0OOO0000O00O =50000.0 #line:1656
        OO0OO00O0O00OO0OO =45000.0 #line:1657
        O0O0O0OOOO0O0OOO0 =45000.0 #line:1658
        OOO0OO00OOO0O0O00 =0.35 #line:1662
        OOO000000O0O00OOO =0.4 #line:1663
        OO0O0OOO0O00O0OO0 =8 #line:1664
        OOO00OO0000OO00O0 =6 #line:1665
        O000O0OO00OO00OO0 =6 #line:1666
        O0OO00000O0O00OO0 =8 #line:1667
        if O0O0O00000O000O00 ['ME1']==1 :#line:1669
            print ("starting dwsim ME1")#line:1670
            OOOO0OO0O0OOO0OO0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_Air_in').GetAsObject ()#line:1672
            OO00OO0OO000O00O0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_Heat_added').GetAsObject ()#line:1673
            OOOOOOOOOO00OO0O0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_compression').GetAsObject ()#line:1674
            O0OO00OO000O00OOO =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_compression_power').GetAsObject ()#line:1675
            OOOO0O0OOO00O0OO0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_compressed').GetAsObject ()#line:1676
            OOO0O0OO0OOOOOO0O =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_heat_addition').GetAsObject ()#line:1677
            O0O00OO000O0O0000 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_heated').GetAsObject ()#line:1678
            O0OOO0O000OO0O000 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_expansion').GetAsObject ()#line:1679
            O0OO0O0OOO0OO0000 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_brake_power').GetAsObject ()#line:1680
            O000OO00OO000O0O0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_Exhaust_gases').GetAsObject ()#line:1681
            O00O0OO0O0000O0OO =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_TC_exp').GetAsObject ()#line:1682
            OO0OO0O00O00O0OO0 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_TC_comp').GetAsObject ()#line:1683
            O0O0O0000OO00O00O =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_compressed_fresh_air').GetAsObject ()#line:1684
            OO000000O0OO00O0O =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_fresh_air_in').GetAsObject ()#line:1685
            OOOO0OO00O0O0OO00 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_scav_air_cooler').GetAsObject ()#line:1686
            O0OOO000O0000OO0O =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_cw_in').GetAsObject ()#line:1687
            OOO0OO00OOO000000 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_scav_air').GetAsObject ()#line:1688
            OO000O00OOOO0O0OO =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_CL').GetAsObject ()#line:1689
            OOO0O0000O0OOOO00 =OO0O0O0O0O0O00O00 .ME1_sim .GetFlowsheetSimulationObject ('ME1_HT').GetAsObject ()#line:1690
            OO0000000OOOOOO00 ['ME1_EG_CylAvg_ScavAirPistonUnderTemp']=(OO0000000OOOOOO00 ['ME1_EG_Cyl1_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME1_EG_Cyl2_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME1_EG_Cyl3_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME1_EG_Cyl4_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME1_EG_Cyl5_ScavAirPistonUnderTemp'])/5 #line:1693
            OO0000000OOOOOO00 ['ME1_PF_Flow']=(OO0000000OOOOOO00 ['ME1_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['ME1_FO_Flow_InstMass']*0.005 )#line:1695
            if OO0000000OOOOOO00 ['ME1_Misc_Spd']==0.0 :#line:1696
                OO0000000OOOOOO00 ['ME1_Misc_Spd']=1.0 #line:1697
            OO0000000OOOOOO00 ['ME1_Suction_volumetric_flow']=3.14 *(1 /4 )*(OOOO0000000O000OO **2 )*O0000OO0O00OO000O *OOOOOOO000OO0O00O *OO0000000OOOOOO00 ['ME1_Misc_Spd']*60 #line:1698
            OO0000000OOOOOO00 ['ME1_Total_fuel_flow']=OO0000000OOOOOO00 ['ME1_FG_Flow_InstMass']+OO0000000OOOOOO00 ['ME1_FO_Flow_InstMass']+OO0000000OOOOOO00 ['ME1_PF_Flow']#line:1701
            if OO0000000OOOOOO00 ['ME1_Total_fuel_flow']==0.0 :#line:1702
                OO0000000OOOOOO00 ['ME1_Total_fuel_flow']=1.0 #line:1703
            OO0000000OOOOOO00 ['ME1_Heat_added']=(OO0000000OOOOOO00 ['ME1_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:1704
            if 'ME1_EG_ScavAirMeanPrs'in O0OOO0OOO00000OO0 :#line:1711
                OO0OOO0O0OOOO0O0O =O0OOO0OOO00000OO0 ['ME1_EG_ScavAirMeanPrs']#line:1712
            else :#line:1713
                OO0OOO0O0OOOO0O0O =OO0000000OOOOOO00 ['ME1_EG_ScavAirMeanPrs']#line:1714
            OOOO0OO0O0OOO0OO0 .SetTemperature (OO0000000OOOOOO00 ['ME1_EG_CylAvg_ScavAirPistonUnderTemp']+273.15 )#line:1716
            OOOO0OO0O0OOO0OO0 .SetPressure (OO0OOO0O0OOOO0O0O *1000000 )#line:1718
            OOOO0OO0O0OOO0OO0 .SetVolumetricFlow (OO0000000OOOOOO00 ['ME1_Suction_volumetric_flow']/3600.0 )#line:1719
            OOOOOOOOOO00OO0O0 .set_POut (OO0000000OOOOOO00 ['ME1_Cyl_AvgFiringPrs']*1000000 )#line:1720
            OO00OO0OO000O00O0 .set_EnergyFlow (OO0000000OOOOOO00 ['ME1_Heat_added'])#line:1721
            O0OOO0O000OO0O000 .set_POut (OO0OOO0O0OOOO0O0O *1000000 )#line:1722
            OO000O00OOOO0O0OO .set_OutletTemperature (OO0000000OOOOOO00 ['ME1_EG_TC1_InTemp']+273.15 )#line:1723
            OO000000O0OO00O0O .SetTemperature (OO0000000OOOOOO00 ['ME1_EG_TC_AirInTempA']+273.15 )#line:1725
            OO0OO0O00O00O0OO0 .set_POut (OO0OOO0O0OOOO0O0O *1000000 )#line:1726
            OOOO0OO00O0O0OO00 .set_OutletTemperature (OO0000000OOOOOO00 ['ME1_EG_CylAvg_ScavAirPistonUnderTemp']+273.15 )#line:1727
            O0OOO000O0000OO0O .SetPressure (OO0000000OOOOOO00 ['ME1_EG_ScavAir_CWInPrs']*1000000 )#line:1728
            O0OOO000O0000OO0O .SetTemperature (OO0000000OOOOOO00 ['ME1_EG_ScavAir_CWInTemp']+273.15 )#line:1729
            OOO0O0000O0OOOO00 .set_OutletTemperature (OO0000000OOOOOO00 ['ME1_EG_ScavAir_CWOutTemp']+273.15 )#line:1730
            from DWSIM .GlobalSettings import Settings #line:1732
            Settings .SolverMode =0 #line:1733
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .ME1_sim )#line:1734
            OOOOO000O000OOOO0 ['ME1_Suction_volumetric_flow']=OO0000000OOOOOO00 ['ME1_Suction_volumetric_flow']#line:1736
            OOOOO000O000OOOO0 ['ME1_Combustion_air_flow']=OOOO0OO0O0OOO0OO0 .GetMassFlow ()*3600 #line:1737
            OOOOO000O000OOOO0 ['ME1_Total_fuel_flow']=OO0000000OOOOOO00 ['ME1_Total_fuel_flow']#line:1739
            OOOOO000O000OOOO0 ['ME1_AirFuel_ratio']=OOOOO000O000OOOO0 ['ME1_Combustion_air_flow']/OOOOO000O000OOOO0 ['ME1_Total_fuel_flow']#line:1740
            OOOOO000O000OOOO0 ['ME1_Heat_added']=OO0000000OOOOOO00 ['ME1_Heat_added']#line:1741
            OOOOO000O000OOOO0 ['ME1_Isentropic_compression_power']=abs (OOOOOOOOOO00OO0O0 .GetPowerGeneratedOrConsumed ())#line:1742
            OOOOO000O000OOOO0 ['ME1_Maximum_pressure']=OO0000000OOOOOO00 ['ME1_Cyl_AvgFiringPrs']*10 #line:1743
            OOOOO000O000OOOO0 ['ME1_CylTemperature_after_isentropic_compression']=OOOO0O0OOO00O0OO0 .GetTemperature ()-273.15 #line:1744
            OOOOO000O000OOOO0 ['ME1_CylTemperature_after_combustion']=O0O00OO000O0O0000 .GetTemperature ()-273.15 #line:1745
            OOOOO000O000OOOO0 ['ME1_Total_ideal_brake_power']=abs (O0OOO0O000OO0O000 .GetPowerGeneratedOrConsumed ())#line:1747
            OOOOO000O000OOOO0 ['ME1_Net_ideal_brake_power']=OOOOO000O000OOOO0 ['ME1_Total_ideal_brake_power']-OOOOO000O000OOOO0 ['ME1_Isentropic_compression_power']#line:1748
            OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']=OO0000000OOOOOO00 ['Sft1_Misc_Pwr']#line:1751
            if OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']==0.0 :#line:1752
                OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']=1.0 #line:1753
            OOOOO000O000OOOO0 ['ME1_Ideal_brake_thermal_efficiency']=(OOOOO000O000OOOO0 ['ME1_Net_ideal_brake_power']/OOOOO000O000OOOO0 ['ME1_Heat_added'])*100 #line:1755
            OOOOO000O000OOOO0 ['ME1_Actual_brake_thermal_efficiency']=(OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']/OOOOO000O000OOOO0 ['ME1_Heat_added'])*100 #line:1756
            OOOOO000O000OOOO0 ['ME1_Relative_efficiency']=(OOOOO000O000OOOO0 ['ME1_Actual_brake_thermal_efficiency']/OOOOO000O000OOOO0 ['ME1_Ideal_brake_thermal_efficiency'])*100 #line:1757
            OOOOO000O000OOOO0 ['ME1_Ideal_brake_specific_fuel_consumption']=OOOOO000O000OOOO0 ['ME1_Total_fuel_flow']/OOOOO000O000OOOO0 ['ME1_Net_ideal_brake_power']#line:1758
            OOOOO000O000OOOO0 ['ME1_Actual_brake_specific_fuel_consumption']=OOOOO000O000OOOO0 ['ME1_Total_fuel_flow']/OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']#line:1759
            OOOOO000O000OOOO0 ['ME1_Actual_brake_mean_effective_pressure']=(OOOOO000O000OOOO0 ['ME1_Net_actual_brake_power']/OO0000000OOOOOO00 ['ME1_Suction_volumetric_flow'])*36 #line:1760
            OOOOO000O000OOOO0 ['ME1_Ideal_brake_mean_effective_pressure']=(OOOOO000O000OOOO0 ['ME1_Net_ideal_brake_power']/OO0000000OOOOOO00 ['ME1_Suction_volumetric_flow'])*36 #line:1761
            OOOOO000O000OOOO0 ['ME1_Compression_pressure_ratio']=OOOOO000O000OOOO0 ['ME1_Maximum_pressure']/(OO0OOO0O0OOOO0O0O *10 )#line:1762
            OOOOO000O000OOOO0 ['ME1_TC_compression_power']=abs (OO0OO0O00O00O0OO0 .GetPowerGeneratedOrConsumed ())#line:1763
            OOO0OOO000OO0O0OO ['ME1_SAC_air_in_temperature']=O0O0O0000OO00O00O .GetTemperature ()-273.15 #line:1765
            OOO0OOO000OO0O0OO ['ME1_SAC_scav_air_in_SpecificEnthalpy']=O0O0O0000OO00O00O .GetMassEnthalpy ()#line:1766
            OOO0OOO000OO0O0OO ['ME1_SAC_scav_air_out_SpecificEnthalpy']=OOO0OO00OOO000000 .GetMassEnthalpy ()#line:1767
            OOO0OOO000OO0O0OO ['ME1_SAC_cw_duty']=OOOO0OO00O0O0OO00 .GetPowerGeneratedOrConsumed ()#line:1768
            OOO0OOO000OO0O0OO ['ME1_SAC_cw_flow_required']=O0OOO000O0000OO0O .GetMassFlow ()*3600 #line:1769
            OOOOO000O000OOOO0 =OOOOO000O000OOOO0 |OOO0OOO000OO0O0OO #line:1771
            for O00000O00O0O00O00 in OOOOO000O000OOOO0 .keys ():#line:1772
                OOOOO000O000OOOO0 [O00000O00O0O00O00 ]=float ("{0:.3f}".format (OOOOO000O000OOOO0 [O00000O00O0O00O00 ]))#line:1773
        if O0O0O00000O000O00 ['ME2']==1 :#line:1775
            print ("starting dwsim ME2")#line:1776
            O0000OOO0O0OOO000 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_Air_in').GetAsObject ()#line:1778
            OO000O00O0OO00O00 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_Heat_added').GetAsObject ()#line:1779
            O0OO0OO0OOOOOO00O =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_compression').GetAsObject ()#line:1780
            O0000OO0O0OO0OO00 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_compression_power').GetAsObject ()#line:1781
            OOOOO0000000OOO0O =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_compressed').GetAsObject ()#line:1782
            OO000O00O0O00O0O0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_heat_addition').GetAsObject ()#line:1783
            OO0O0OOO00OOOOO00 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_heated').GetAsObject ()#line:1784
            OOOO0OOO000O0OO0O =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_expansion').GetAsObject ()#line:1785
            OO00O00OO000OOO0O =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_brake_power').GetAsObject ()#line:1786
            OO000OOOO0OOO00O0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_Exhaust_gases').GetAsObject ()#line:1787
            OOOO0O0OOO0O00OO0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_TC_exp').GetAsObject ()#line:1788
            O0O00O0OOOOOO00O0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_TC_comp').GetAsObject ()#line:1789
            OO00O0000OO0O0000 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_compressed_fresh_air').GetAsObject ()#line:1790
            OOO000O0OOO0OOOOO =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_fresh_air_in').GetAsObject ()#line:1791
            OO0O0000OOO00OOO0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_scav_air_cooler').GetAsObject ()#line:1792
            OO00O00OOOO00OOO0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_cw_in').GetAsObject ()#line:1793
            O000000OOO00OO000 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_scav_air').GetAsObject ()#line:1794
            OOO0OOOO0OOOOO0O0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_CL').GetAsObject ()#line:1795
            O0O0O0000O0O0OOO0 =OO0O0O0O0O0O00O00 .ME2_sim .GetFlowsheetSimulationObject ('ME2_HT').GetAsObject ()#line:1796
            OO0000000OOOOOO00 ['ME2_EG_CylAvg_ScavAirPistonUnderTemp']=(OO0000000OOOOOO00 ['ME2_EG_Cyl1_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME2_EG_Cyl2_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME2_EG_Cyl3_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME2_EG_Cyl4_ScavAirPistonUnderTemp']+OO0000000OOOOOO00 ['ME2_EG_Cyl5_ScavAirPistonUnderTemp'])/5 #line:1799
            OO0000000OOOOOO00 ['ME2_PF_Flow']=(OO0000000OOOOOO00 ['ME2_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['ME2_FO_Flow_InstMass']*0.005 )#line:1801
            if OO0000000OOOOOO00 ['ME2_Misc_Spd']==0.0 :#line:1802
                OO0000000OOOOOO00 ['ME2_Misc_Spd']=1.0 #line:1803
            OO0000000OOOOOO00 ['ME2_Suction_volumetric_flow']=3.14 *(1 /4 )*(OOOO0000000O000OO **2 )*O0000OO0O00OO000O *OOOOOOO000OO0O00O *OO0000000OOOOOO00 ['ME2_Misc_Spd']*60 #line:1804
            OO0000000OOOOOO00 ['ME2_Total_fuel_flow']=OO0000000OOOOOO00 ['ME2_FG_Flow_InstMass']+OO0000000OOOOOO00 ['ME2_FO_Flow_InstMass']+OO0000000OOOOOO00 ['ME2_PF_Flow']#line:1805
            if OO0000000OOOOOO00 ['ME2_Total_fuel_flow']==0.0 :#line:1806
                OO0000000OOOOOO00 ['ME2_Total_fuel_flow']=1.0 #line:1807
            OO0000000OOOOOO00 ['ME2_Heat_added']=(OO0000000OOOOOO00 ['ME2_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:1808
            if 'ME2_EG_ScavAirMeanPrs'in O0OOO0OOO00000OO0 :#line:1810
                OOO0OOOOOO000000O =O0OOO0OOO00000OO0 ['ME2_EG_ScavAirMeanPrs']#line:1811
            else :#line:1812
                OOO0OOOOOO000000O =OO0000000OOOOOO00 ['ME2_EG_ScavAirMeanPrs']#line:1813
            O0000OOO0O0OOO000 .SetTemperature (OO0000000OOOOOO00 ['ME2_EG_CylAvg_ScavAirPistonUnderTemp']+273.15 )#line:1816
            O0000OOO0O0OOO000 .SetPressure (OOO0OOOOOO000000O *1000000 )#line:1817
            O0000OOO0O0OOO000 .SetVolumetricFlow (OO0000000OOOOOO00 ['ME2_Suction_volumetric_flow']/3600.0 )#line:1818
            O0OO0OO0OOOOOO00O .set_POut (OO0000000OOOOOO00 ['ME2_Cyl_AvgFiringPrs']*1000000 )#line:1819
            OO000O00O0OO00O00 .set_EnergyFlow (OO0000000OOOOOO00 ['ME2_Heat_added'])#line:1820
            OOOO0OOO000O0OO0O .set_POut (OOO0OOOOOO000000O *1000000 )#line:1821
            OOO0OOOO0OOOOO0O0 .set_OutletTemperature (OO0000000OOOOOO00 ['ME2_EG_TC1_InTemp']+273.15 )#line:1822
            OOO000O0OOO0OOOOO .SetTemperature (OO0000000OOOOOO00 ['ME2_EG_TC_AirInTempA']+273.15 )#line:1824
            O0O00O0OOOOOO00O0 .set_POut (OOO0OOOOOO000000O *1000000 )#line:1825
            OO0O0000OOO00OOO0 .set_OutletTemperature (OO0000000OOOOOO00 ['ME2_EG_CylAvg_ScavAirPistonUnderTemp']+273.15 )#line:1826
            OO00O00OOOO00OOO0 .SetPressure (OO0000000OOOOOO00 ['ME2_EG_ScavAir_CWInPrs']*1000000 )#line:1827
            OO00O00OOOO00OOO0 .SetTemperature (OO0000000OOOOOO00 ['ME2_EG_ScavAir_CWInTemp']+273.15 )#line:1828
            O0O0O0000O0O0OOO0 .set_OutletTemperature (OO0000000OOOOOO00 ['ME2_EG_ScavAir_CWOutTemp']+273.15 )#line:1829
            from DWSIM .GlobalSettings import Settings #line:1831
            Settings .SolverMode =0 #line:1832
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .ME2_sim )#line:1833
            O0OOOOOOO0OOO0000 ['ME2_Suction_volumetric_flow']=OO0000000OOOOOO00 ['ME2_Suction_volumetric_flow']#line:1835
            O0OOOOOOO0OOO0000 ['ME2_Combustion_air_flow']=O0000OOO0O0OOO000 .GetMassFlow ()*3600 #line:1836
            O0OOOOOOO0OOO0000 ['ME2_Total_fuel_flow']=OO0000000OOOOOO00 ['ME2_Total_fuel_flow']#line:1838
            O0OOOOOOO0OOO0000 ['ME2_AirFuel_ratio']=O0OOOOOOO0OOO0000 ['ME2_Combustion_air_flow']/O0OOOOOOO0OOO0000 ['ME2_Total_fuel_flow']#line:1839
            O0OOOOOOO0OOO0000 ['ME2_Heat_added']=OO0000000OOOOOO00 ['ME2_Heat_added']#line:1840
            O0OOOOOOO0OOO0000 ['ME2_Isentropic_compression_power']=abs (O0OO0OO0OOOOOO00O .GetPowerGeneratedOrConsumed ())#line:1841
            O0OOOOOOO0OOO0000 ['ME2_Maximum_pressure']=OO0000000OOOOOO00 ['ME2_Cyl_AvgFiringPrs']*10 #line:1842
            O0OOOOOOO0OOO0000 ['ME2_CylTemperature_after_isentropic_compression']=OOOOO0000000OOO0O .GetTemperature ()-273.15 #line:1843
            O0OOOOOOO0OOO0000 ['ME2_CylTemperature_after_combustion']=OO0O0OOO00OOOOO00 .GetTemperature ()-273.15 #line:1844
            O0OOOOOOO0OOO0000 ['ME2_Total_ideal_brake_power']=abs (OOOO0OOO000O0OO0O .GetPowerGeneratedOrConsumed ())#line:1846
            O0OOOOOOO0OOO0000 ['ME2_Net_ideal_brake_power']=O0OOOOOOO0OOO0000 ['ME2_Total_ideal_brake_power']-O0OOOOOOO0OOO0000 ['ME2_Isentropic_compression_power']#line:1847
            O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']=OO0000000OOOOOO00 ['Sft1_Misc_Pwr']#line:1848
            if O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']==0.0 :#line:1849
                O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']=1.0 #line:1850
            O0OOOOOOO0OOO0000 ['ME2_Ideal_brake_thermal_efficiency']=(O0OOOOOOO0OOO0000 ['ME2_Net_ideal_brake_power']/O0OOOOOOO0OOO0000 ['ME2_Heat_added'])*100 #line:1852
            O0OOOOOOO0OOO0000 ['ME2_Actual_brake_thermal_efficiency']=(O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']/O0OOOOOOO0OOO0000 ['ME2_Heat_added'])*100 #line:1853
            O0OOOOOOO0OOO0000 ['ME2_Relative_efficiency']=(O0OOOOOOO0OOO0000 ['ME2_Actual_brake_thermal_efficiency']/O0OOOOOOO0OOO0000 ['ME2_Ideal_brake_thermal_efficiency'])*100 #line:1854
            O0OOOOOOO0OOO0000 ['ME2_Ideal_brake_specific_fuel_consumption']=O0OOOOOOO0OOO0000 ['ME2_Total_fuel_flow']/O0OOOOOOO0OOO0000 ['ME2_Net_ideal_brake_power']#line:1855
            O0OOOOOOO0OOO0000 ['ME2_Actual_brake_specific_fuel_consumption']=O0OOOOOOO0OOO0000 ['ME2_Total_fuel_flow']/O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']#line:1856
            O0OOOOOOO0OOO0000 ['ME2_Actual_brake_mean_effective_pressure']=(O0OOOOOOO0OOO0000 ['ME2_Net_actual_brake_power']/OO0000000OOOOOO00 ['ME2_Suction_volumetric_flow'])*36 #line:1857
            O0OOOOOOO0OOO0000 ['ME2_Ideal_brake_mean_effective_pressure']=(O0OOOOOOO0OOO0000 ['ME2_Net_ideal_brake_power']/OO0000000OOOOOO00 ['ME2_Suction_volumetric_flow'])*36 #line:1858
            O0OOOOOOO0OOO0000 ['ME2_Compression_pressure_ratio']=O0OOOOOOO0OOO0000 ['ME2_Maximum_pressure']/(OOO0OOOOOO000000O *10 )#line:1859
            O0OOOOOOO0OOO0000 ['ME2_TC_compression_power']=abs (O0O00O0OOOOOO00O0 .GetPowerGeneratedOrConsumed ())#line:1860
            O00OOOO0O00OOOOOO ['ME2_SAC_air_in_temperature']=OO00O0000OO0O0000 .GetTemperature ()-273.15 #line:1862
            O00OOOO0O00OOOOOO ['ME2_SAC_scav_air_in_SpecificEnthalpy']=OO00O0000OO0O0000 .GetMassEnthalpy ()#line:1863
            O00OOOO0O00OOOOOO ['ME2_SAC_scav_air_out_SpecificEnthalpy']=O000000OOO00OO000 .GetMassEnthalpy ()#line:1864
            O00OOOO0O00OOOOOO ['ME2_SAC_cw_duty']=OO0O0000OOO00OOO0 .GetPowerGeneratedOrConsumed ()#line:1865
            O00OOOO0O00OOOOOO ['ME2_SAC_cw_flow_required']=OO00O00OOOO00OOO0 .GetMassFlow ()*3600 #line:1866
            O0OOOOOOO0OOO0000 =O0OOOOOOO0OOO0000 |O00OOOO0O00OOOOOO #line:1868
            for O00000O00O0O00O00 in O0OOOOOOO0OOO0000 .keys ():#line:1869
                O0OOOOOOO0OOO0000 [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O0OOOOOOO0OOO0000 [O00000O00O0O00O00 ]))#line:1870
        if O0O0O00000O000O00 ['GE1']==1 :#line:1872
            print ("starting dwsim GE1")#line:1873
            O000O00OO0O0O0O0O =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_Air_in').GetAsObject ()#line:1875
            OOO00000O00O000OO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_Heat_added').GetAsObject ()#line:1876
            OO0O0OO0OO0O0OOOO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_compression').GetAsObject ()#line:1877
            OOO000O00O0000OOO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_compression_power').GetAsObject ()#line:1878
            O00O000000OOO0OO0 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_compressed').GetAsObject ()#line:1879
            O0O000O00O0O000O0 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_heat_addition').GetAsObject ()#line:1880
            O0OOOOOOOOOO00O0O =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_heated').GetAsObject ()#line:1881
            OO0OOO0O0O0OO0000 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_expansion').GetAsObject ()#line:1882
            O000OOOO0O00OO0OO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_brake_power').GetAsObject ()#line:1883
            OO00OO0000OO000O0 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_Exhaust_gases').GetAsObject ()#line:1884
            OO00O0O0O0000O000 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_TC_exp').GetAsObject ()#line:1885
            O0O000O00O0O00000 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_TC_comp').GetAsObject ()#line:1886
            O0OO0O00O0O0O0OO0 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_compressed_fresh_air').GetAsObject ()#line:1887
            OOOOO0O0000000O0O =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_fresh_air_in').GetAsObject ()#line:1888
            O00O0OOOOOOO0O00O =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_scav_air_cooler').GetAsObject ()#line:1889
            O0000OOOO00O0O0OO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_cw_in').GetAsObject ()#line:1890
            O0OOO0O0O00OO0OOO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_scav_air').GetAsObject ()#line:1891
            O0O0OOOO0O000OOO0 =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_CL').GetAsObject ()#line:1892
            O0000O0OO0000OOOO =OO0O0O0O0O0O00O00 .GE1_sim .GetFlowsheetSimulationObject ('GE1_HT').GetAsObject ()#line:1893
            OO0000000OOOOOO00 ['GE1_CylAvg_CompressionPrs']=(OO0000000OOOOOO00 ['GE1_Cyl1_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl2_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl3_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl4_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl5_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl6_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl7_CompressionPrs']+OO0000000OOOOOO00 ['GE1_Cyl8_CompressionPrs'])/8 #line:1897
            if O0O0O00000O000O00 ['GE1']==1 and O0O0O00000O000O00 ['GE2']==1 :#line:1899
                OO0000000OOOOOO00 ['GE1_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE1GE2_Flow_InstMass']/2 #line:1900
            else :#line:1901
                OO0000000OOOOOO00 ['GE1_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE1GE2_Flow_InstMass']#line:1902
            OO0000000OOOOOO00 ['GE1_PF_Flow']=(OO0000000OOOOOO00 ['GE1_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['GE1_FO_flow']*0.005 )#line:1904
            if OO0000000OOOOOO00 ['GE1_Misc_Spd']==0.0 :#line:1905
                OO0000000OOOOOO00 ['GE1_Misc_Spd']=1.0 #line:1906
            OO0000000OOOOOO00 ['GE1_Suction_volumetric_flow']=(3.14 *(1 /4 )*(OOO0OO00OOO0O0O00 **2 )*OOO000000O0O00OOO *OO0O0OOO0O00O0OO0 *OO0000000OOOOOO00 ['GE1_Misc_Spd']*60 )/2 #line:1907
            OO0000000OOOOOO00 ['GE1_Total_fuel_flow']=OO0000000OOOOOO00 ['GE1_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE1_FO_flow']+OO0000000OOOOOO00 ['GE1_PF_Flow']#line:1908
            if OO0000000OOOOOO00 ['GE1_Total_fuel_flow']==0.0 :#line:1909
                OO0000000OOOOOO00 ['GE1_Total_fuel_flow']=1.0 #line:1910
            OO0000000OOOOOO00 ['GE1_Heat_added']=(OO0000000OOOOOO00 ['GE1_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:1911
            O000O00OO0O0O0O0O .SetTemperature (OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutTemp']+273.15 )#line:1914
            O000O00OO0O0O0O0O .SetPressure (OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutPrs']*1000000 )#line:1915
            O000O00OO0O0O0O0O .SetVolumetricFlow (OO0000000OOOOOO00 ['GE1_Suction_volumetric_flow']/3600.0 )#line:1916
            OO0O0OO0OO0O0OOOO .set_POut (OO0000000OOOOOO00 ['GE1_CylAvg_CompressionPrs']*1000000 )#line:1917
            OOO00000O00O000OO .set_EnergyFlow (OO0000000OOOOOO00 ['GE1_Heat_added'])#line:1918
            OO0OOO0O0O0OO0000 .set_POut (OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutPrs']*1000000 )#line:1919
            O0O0OOOO0O000OOO0 .set_OutletTemperature (OO0000000OOOOOO00 ['GE1_EG_TC1_InTemp']+273.15 )#line:1920
            OOOOO0O0000000O0O .SetTemperature (OO0000000OOOOOO00 ['GE1_EG_TC1_AirIntakeTemp']+273.15 )#line:1922
            O0O000O00O0O00000 .set_POut (OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutPrs']*1000000 )#line:1923
            O00O0OOOOOOO0O00O .set_OutletTemperature (OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutTemp']+273.15 )#line:1924
            O0000OOOO00O0O0OO .SetPressure (OO0000000OOOOOO00 ['GE1_CS_LTCFW_AirClrInPrs']*1000000 )#line:1925
            O0000OOOO00O0O0OO .SetTemperature (OO0000000OOOOOO00 ['GE1_CS_LTCFW_AirClrInTemp']+273.15 )#line:1926
            O0000O0OO0000OOOO .set_OutletTemperature (OO0000000OOOOOO00 ['GE1_CS_LTCFW_AirClrOutTemp']+273.15 )#line:1927
            from DWSIM .GlobalSettings import Settings #line:1929
            Settings .SolverMode =0 #line:1930
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .GE1_sim )#line:1931
            OOOO00O0O000000OO ['GE1_Suction_volumetric_flow']=OO0000000OOOOOO00 ['GE1_Suction_volumetric_flow']#line:1933
            OOOO00O0O000000OO ['GE1_Combustion_air_flow']=O000O00OO0O0O0O0O .GetMassFlow ()*3600 #line:1934
            OOOO00O0O000000OO ['GE1_Total_fuel_flow']=OO0000000OOOOOO00 ['GE1_Total_fuel_flow']#line:1936
            OOOO00O0O000000OO ['GE1_AirFuel_ratio']=OOOO00O0O000000OO ['GE1_Combustion_air_flow']/OOOO00O0O000000OO ['GE1_Total_fuel_flow']#line:1937
            OOOO00O0O000000OO ['GE1_Heat_added']=OO0000000OOOOOO00 ['GE1_Heat_added']#line:1938
            OOOO00O0O000000OO ['GE1_Isentropic_compression_power']=abs (OO0O0OO0OO0O0OOOO .GetPowerGeneratedOrConsumed ())#line:1939
            OOOO00O0O000000OO ['GE1_Maximum_pressure']=OO0000000OOOOOO00 ['GE1_CylAvg_CompressionPrs']*10 #line:1940
            OOOO00O0O000000OO ['GE1_CylTemperature_after_isentropic_compression']=O00O000000OOO0OO0 .GetTemperature ()-273.15 #line:1941
            OOOO00O0O000000OO ['GE1_CylTemperature_after_combustion']=O0OOOOOOOOOO00O0O .GetTemperature ()-273.15 #line:1942
            OOOO00O0O000000OO ['GE1_Total_ideal_brake_power']=abs (OO0OOO0O0O0OO0000 .GetPowerGeneratedOrConsumed ())#line:1944
            OOOO00O0O000000OO ['GE1_Net_ideal_brake_power']=OOOO00O0O000000OO ['GE1_Total_ideal_brake_power']-OOOO00O0O000000OO ['GE1_Isentropic_compression_power']#line:1945
            OOOO00O0O000000OO ['GE1_Net_actual_brake_power']=OO0000000OOOOOO00 ['GE1_Misc_Pwr']#line:1946
            if OOOO00O0O000000OO ['GE1_Net_actual_brake_power']==0.0 :#line:1947
                OOOO00O0O000000OO ['GE1_Net_actual_brake_power']=1.0 #line:1948
            OOOO00O0O000000OO ['GE1_Ideal_brake_thermal_efficiency']=(OOOO00O0O000000OO ['GE1_Net_ideal_brake_power']/OOOO00O0O000000OO ['GE1_Heat_added'])*100 #line:1950
            OOOO00O0O000000OO ['GE1_Actual_brake_thermal_efficiency']=(OOOO00O0O000000OO ['GE1_Net_actual_brake_power']/OOOO00O0O000000OO ['GE1_Heat_added'])*100 #line:1951
            OOOO00O0O000000OO ['GE1_Relative_efficiency']=(OOOO00O0O000000OO ['GE1_Actual_brake_thermal_efficiency']/OOOO00O0O000000OO ['GE1_Ideal_brake_thermal_efficiency'])*100 #line:1952
            OOOO00O0O000000OO ['GE1_Ideal_brake_specific_fuel_consumption']=OOOO00O0O000000OO ['GE1_Total_fuel_flow']/OOOO00O0O000000OO ['GE1_Net_ideal_brake_power']#line:1953
            OOOO00O0O000000OO ['GE1_Actual_brake_specific_fuel_consumption']=OOOO00O0O000000OO ['GE1_Total_fuel_flow']/OOOO00O0O000000OO ['GE1_Net_actual_brake_power']#line:1954
            OOOO00O0O000000OO ['GE1_Actual_brake_mean_effective_pressure']=(OOOO00O0O000000OO ['GE1_Net_actual_brake_power']/OO0000000OOOOOO00 ['GE1_Suction_volumetric_flow'])*36 #line:1955
            OOOO00O0O000000OO ['GE1_Ideal_brake_mean_effective_pressure']=(OOOO00O0O000000OO ['GE1_Net_ideal_brake_power']/OO0000000OOOOOO00 ['GE1_Suction_volumetric_flow'])*36 #line:1956
            OOOO00O0O000000OO ['GE1_Compression_pressure_ratio']=OOOO00O0O000000OO ['GE1_Maximum_pressure']/(OO0000000OOOOOO00 ['GE1_CS_AirClr_ChAirOutPrs']*10 )#line:1957
            OOOO00O0O000000OO ['GE1_TC_compression_power']=abs (O0O000O00O0O00000 .GetPowerGeneratedOrConsumed ())#line:1958
            O0O0OO00O0OOO0O00 ['GE1_SAC_air_in_temperature']=O0OO0O00O0O0O0OO0 .GetTemperature ()-273.15 #line:1960
            O0O0OO00O0OOO0O00 ['GE1_SAC_scav_air_in_SpecificEnthalpy']=O0OO0O00O0O0O0OO0 .GetMassEnthalpy ()#line:1961
            O0O0OO00O0OOO0O00 ['GE1_SAC_scav_air_out_SpecificEnthalpy']=O0OOO0O0O00OO0OOO .GetMassEnthalpy ()#line:1962
            O0O0OO00O0OOO0O00 ['GE1_SAC_cw_duty']=O00O0OOOOOOO0O00O .GetPowerGeneratedOrConsumed ()#line:1963
            O0O0OO00O0OOO0O00 ['GE1_SAC_cw_flow_required']=O0000OOOO00O0O0OO .GetMassFlow ()*3600 #line:1964
            OOOO00O0O000000OO =OOOO00O0O000000OO |O0O0OO00O0OOO0O00 #line:1966
            for O00000O00O0O00O00 in OOOO00O0O000000OO .keys ():#line:1967
                OOOO00O0O000000OO [O00000O00O0O00O00 ]=float ("{0:.3f}".format (OOOO00O0O000000OO [O00000O00O0O00O00 ]))#line:1968
        if O0O0O00000O000O00 ['GE2']==1 :#line:1970
            print ("starting dwsim GE2")#line:1971
            OOO0O00O00O00OO00 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_Air_in').GetAsObject ()#line:1973
            OOO0OO0OOOOOO0O0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_Heat_added').GetAsObject ()#line:1974
            OOOOO0000O00000O0 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_compression').GetAsObject ()#line:1975
            O0O0O0O0OO0O0OOO0 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_compression_power').GetAsObject ()#line:1976
            OOO000OO00O00OO0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_compressed').GetAsObject ()#line:1977
            OO0OOOOOO0O00OOO0 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_heat_addition').GetAsObject ()#line:1978
            OOO00O00O00OOOO0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_heated').GetAsObject ()#line:1979
            O0000O0O0O00O0O0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_expansion').GetAsObject ()#line:1980
            OOO00OO00O0OO00OO =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_brake_power').GetAsObject ()#line:1981
            OO00O00O0O0OOOO00 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_Exhaust_gases').GetAsObject ()#line:1982
            O00OO000OOO0O0OOO =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_TC_exp').GetAsObject ()#line:1983
            O00OOO0O0000OO00O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_TC_comp').GetAsObject ()#line:1984
            OOO00O0OOO0OOOO0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_compressed_fresh_air').GetAsObject ()#line:1985
            O00OOOOOOOO0O0O00 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_fresh_air_in').GetAsObject ()#line:1986
            OO0OOOO0O0O00000O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_scav_air_cooler').GetAsObject ()#line:1987
            O000OOOOO00OOOOO0 =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_cw_in').GetAsObject ()#line:1988
            O0O0OO0O0O0O0OO0O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_scav_air').GetAsObject ()#line:1989
            OO0O00O0O0O00O00O =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_CL').GetAsObject ()#line:1990
            OOO00O0OO000000OO =OO0O0O0O0O0O00O00 .GE2_sim .GetFlowsheetSimulationObject ('GE2_HT').GetAsObject ()#line:1991
            OO0000000OOOOOO00 ['GE2_CylAvg_CompressionPrs']=(OO0000000OOOOOO00 ['GE2_Cyl1_CompressionPrs']+OO0000000OOOOOO00 ['GE2_Cyl2_CompressionPrs']+OO0000000OOOOOO00 ['GE2_Cyl3_CompressionPrs']+OO0000000OOOOOO00 ['GE2_Cyl4_CompressionPrs']+OO0000000OOOOOO00 ['GE2_Cyl5_CompressionPrs']+OO0000000OOOOOO00 ['GE2_Cyl6_CompressionPrs'])/8 #line:1994
            if O0O0O00000O000O00 ['GE1']==1 and O0O0O00000O000O00 ['GE2']==1 :#line:1996
                OO0000000OOOOOO00 ['GE2_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE1GE2_Flow_InstMass']/2 #line:1997
            else :#line:1998
                OO0000000OOOOOO00 ['GE2_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE1GE2_Flow_InstMass']#line:1999
            OO0000000OOOOOO00 ['GE2_PF_Flow']=(OO0000000OOOOOO00 ['GE2_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['GE2_FO_flow']*0.005 )#line:2001
            if OO0000000OOOOOO00 ['GE2_Misc_Spd']==0.0 :#line:2002
                OO0000000OOOOOO00 ['GE2_Misc_Spd']=1.0 #line:2003
            OO0000000OOOOOO00 ['GE2_Suction_volumetric_flow']=(3.14 *(1 /4 )*(OOO0OO00OOO0O0O00 **2 )*OOO000000O0O00OOO *OOO00OO0000OO00O0 *OO0000000OOOOOO00 ['GE2_Misc_Spd']*60 )/2 #line:2004
            OO0000000OOOOOO00 ['GE2_Total_fuel_flow']=OO0000000OOOOOO00 ['GE2_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE2_FO_flow']+OO0000000OOOOOO00 ['GE2_PF_Flow']#line:2005
            if OO0000000OOOOOO00 ['GE2_Total_fuel_flow']==0.0 :#line:2006
                OO0000000OOOOOO00 ['GE2_Total_fuel_flow']=1.0 #line:2007
            OO0000000OOOOOO00 ['GE2_Heat_added']=(OO0000000OOOOOO00 ['GE2_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:2008
            OOO0O00O00O00OO00 .SetTemperature (OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutTemp']+273.15 )#line:2011
            OOO0O00O00O00OO00 .SetPressure (OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutPrs']*1000000 )#line:2012
            OOO0O00O00O00OO00 .SetVolumetricFlow (OO0000000OOOOOO00 ['GE2_Suction_volumetric_flow']/3600.0 )#line:2013
            OOOOO0000O00000O0 .set_POut (OO0000000OOOOOO00 ['GE2_CylAvg_CompressionPrs']*1000000 )#line:2014
            OOO0OO0OOOOOO0O0O .set_EnergyFlow (OO0000000OOOOOO00 ['GE2_Heat_added'])#line:2015
            O0000O0O0O00O0O0O .set_POut (OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutPrs']*1000000 )#line:2016
            OO0O00O0O0O00O00O .set_OutletTemperature (OO0000000OOOOOO00 ['GE2_EG_TC1_InTemp']+273.15 )#line:2017
            O00OOOOOOOO0O0O00 .SetTemperature (OO0000000OOOOOO00 ['GE2_EG_TC1_AirIntakeTemp']+273.15 )#line:2019
            O00OOO0O0000OO00O .set_POut (OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutPrs']*1000000 )#line:2020
            OO0OOOO0O0O00000O .set_OutletTemperature (OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutTemp']+273.15 )#line:2021
            O000OOOOO00OOOOO0 .SetPressure (OO0000000OOOOOO00 ['GE2_CS_LTCFW_AirClrInPrs']*1000000 )#line:2022
            O000OOOOO00OOOOO0 .SetTemperature (OO0000000OOOOOO00 ['GE2_CS_LTCFW_AirClrInTemp']+273.15 )#line:2023
            OOO00O0OO000000OO .set_OutletTemperature (OO0000000OOOOOO00 ['GE2_CS_LTCFW_AirClrOutTemp']+273.15 )#line:2024
            from DWSIM .GlobalSettings import Settings #line:2026
            Settings .SolverMode =0 #line:2027
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .GE2_sim )#line:2028
            O0OO00OO000000OOO ['GE2_Suction_volumetric_flow']=OO0000000OOOOOO00 ['GE2_Suction_volumetric_flow']#line:2030
            O0OO00OO000000OOO ['GE2_Combustion_air_flow']=OOO0O00O00O00OO00 .GetMassFlow ()*3600 #line:2031
            O0OO00OO000000OOO ['GE2_Total_fuel_flow']=OO0000000OOOOOO00 ['GE2_Total_fuel_flow']#line:2033
            O0OO00OO000000OOO ['GE2_AirFuel_ratio']=O0OO00OO000000OOO ['GE2_Combustion_air_flow']/O0OO00OO000000OOO ['GE2_Total_fuel_flow']#line:2034
            O0OO00OO000000OOO ['GE2_Heat_added']=OO0000000OOOOOO00 ['GE2_Heat_added']#line:2035
            O0OO00OO000000OOO ['GE2_Isentropic_compression_power']=abs (OOOOO0000O00000O0 .GetPowerGeneratedOrConsumed ())#line:2036
            O0OO00OO000000OOO ['GE2_Maximum_pressure']=OO0000000OOOOOO00 ['GE2_CylAvg_CompressionPrs']*10 #line:2037
            O0OO00OO000000OOO ['GE2_CylTemperature_after_isentropic_compression']=OOO000OO00O00OO0O .GetTemperature ()-273.15 #line:2038
            O0OO00OO000000OOO ['GE2_CylTemperature_after_combustion']=OOO00O00O00OOOO0O .GetTemperature ()-273.15 #line:2039
            O0OO00OO000000OOO ['GE2_Total_ideal_brake_power']=abs (O0000O0O0O00O0O0O .GetPowerGeneratedOrConsumed ())#line:2041
            O0OO00OO000000OOO ['GE2_Net_ideal_brake_power']=O0OO00OO000000OOO ['GE2_Total_ideal_brake_power']-O0OO00OO000000OOO ['GE2_Isentropic_compression_power']#line:2042
            O0OO00OO000000OOO ['GE2_Net_actual_brake_power']=OO0000000OOOOOO00 ['GE2_Misc_Pwr']#line:2043
            if O0OO00OO000000OOO ['GE2_Net_actual_brake_power']==0.0 :#line:2044
                O0OO00OO000000OOO ['GE2_Net_actual_brake_power']=1.0 #line:2045
            O0OO00OO000000OOO ['GE2_Ideal_brake_thermal_efficiency']=(O0OO00OO000000OOO ['GE2_Net_ideal_brake_power']/O0OO00OO000000OOO ['GE2_Heat_added'])*100 #line:2047
            O0OO00OO000000OOO ['GE2_Actual_brake_thermal_efficiency']=(O0OO00OO000000OOO ['GE2_Net_actual_brake_power']/O0OO00OO000000OOO ['GE2_Heat_added'])*100 #line:2048
            O0OO00OO000000OOO ['GE2_Relative_efficiency']=(O0OO00OO000000OOO ['GE2_Actual_brake_thermal_efficiency']/O0OO00OO000000OOO ['GE2_Ideal_brake_thermal_efficiency'])*100 #line:2049
            O0OO00OO000000OOO ['GE2_Ideal_brake_specific_fuel_consumption']=O0OO00OO000000OOO ['GE2_Total_fuel_flow']/O0OO00OO000000OOO ['GE2_Net_ideal_brake_power']#line:2050
            O0OO00OO000000OOO ['GE2_Actual_brake_specific_fuel_consumption']=O0OO00OO000000OOO ['GE2_Total_fuel_flow']/O0OO00OO000000OOO ['GE2_Net_actual_brake_power']#line:2051
            O0OO00OO000000OOO ['GE2_Actual_brake_mean_effective_pressure']=(O0OO00OO000000OOO ['GE2_Net_actual_brake_power']/OO0000000OOOOOO00 ['GE2_Suction_volumetric_flow'])*36 #line:2052
            O0OO00OO000000OOO ['GE2_Ideal_brake_mean_effective_pressure']=(O0OO00OO000000OOO ['GE2_Net_ideal_brake_power']/OO0000000OOOOOO00 ['GE2_Suction_volumetric_flow'])*36 #line:2053
            O0OO00OO000000OOO ['GE2_Compression_pressure_ratio']=O0OO00OO000000OOO ['GE2_Maximum_pressure']/(OO0000000OOOOOO00 ['GE2_CS_AirClr_ChAirOutPrs']*10 )#line:2054
            O0OO00OO000000OOO ['GE2_TC_compression_power']=abs (O00OOO0O0000OO00O .GetPowerGeneratedOrConsumed ())#line:2055
            O0OO0OO0O0O0O000O ['GE2_SAC_air_in_temperature']=OOO00O0OOO0OOOO0O .GetTemperature ()-273.15 #line:2057
            O0OO0OO0O0O0O000O ['GE2_SAC_scav_air_in_SpecificEnthalpy']=OOO00O0OOO0OOOO0O .GetMassEnthalpy ()#line:2058
            O0OO0OO0O0O0O000O ['GE2_SAC_scav_air_out_SpecificEnthalpy']=O0O0OO0O0O0O0OO0O .GetMassEnthalpy ()#line:2059
            O0OO0OO0O0O0O000O ['GE2_SAC_cw_duty']=OO0OOOO0O0O00000O .GetPowerGeneratedOrConsumed ()#line:2060
            O0OO0OO0O0O0O000O ['GE2_SAC_cw_flow_required']=O000OOOOO00OOOOO0 .GetMassFlow ()*3600 #line:2061
            O0OO00OO000000OOO =O0OO00OO000000OOO |O0OO0OO0O0O0O000O #line:2063
            for O00000O00O0O00O00 in O0OO00OO000000OOO .keys ():#line:2064
                O0OO00OO000000OOO [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O0OO00OO000000OOO [O00000O00O0O00O00 ]))#line:2065
        if O0O0O00000O000O00 ['GE3']==1 :#line:2067
            print ("starting dwsim GE3")#line:2068
            OOOOOO0O000OOOO00 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_Air_in').GetAsObject ()#line:2070
            OO00OOO0OO00OO00O =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_Heat_added').GetAsObject ()#line:2071
            O0000O0OOO00O00O0 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_compression').GetAsObject ()#line:2072
            O0O0O0OOOO0OOOO0O =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_compression_power').GetAsObject ()#line:2073
            O00OOO00OOOOOO0OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_compressed').GetAsObject ()#line:2074
            OOO00000OOOO000OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_heat_addition').GetAsObject ()#line:2075
            O0O0000O0O0O0000O =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_heated').GetAsObject ()#line:2076
            O0O0000O0O00O00OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_expansion').GetAsObject ()#line:2077
            O000OOOOOO000O0OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_brake_power').GetAsObject ()#line:2078
            OOOOO0OOO0OO0OOOO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_Exhaust_gases').GetAsObject ()#line:2079
            OOO0O0OO0O000O0OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_TC_exp').GetAsObject ()#line:2080
            O0OOOO00O0O0O0000 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_TC_comp').GetAsObject ()#line:2081
            OO00OO0000O0O0O00 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_compressed_fresh_air').GetAsObject ()#line:2082
            O0OOO0OOO00OOO0O0 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_fresh_air_in').GetAsObject ()#line:2083
            OOOOO000OO00O0000 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_scav_air_cooler').GetAsObject ()#line:2084
            OO0OOO00OOOO0O0OO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_cw_in').GetAsObject ()#line:2085
            O000OOOOOO0O00OOO =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_scav_air').GetAsObject ()#line:2086
            O00OO0000OO0O0000 =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_CL').GetAsObject ()#line:2087
            O0O00OO00O00OO00O =OO0O0O0O0O0O00O00 .GE3_sim .GetFlowsheetSimulationObject ('GE3_HT').GetAsObject ()#line:2088
            OO0000000OOOOOO00 ['GE3_CylAvg_CompressionPrs']=(OO0000000OOOOOO00 ['GE3_Cyl1_CompressionPrs']+OO0000000OOOOOO00 ['GE3_Cyl2_CompressionPrs']+OO0000000OOOOOO00 ['GE3_Cyl3_CompressionPrs']+OO0000000OOOOOO00 ['GE3_Cyl4_CompressionPrs']+OO0000000OOOOOO00 ['GE3_Cyl5_CompressionPrs']+OO0000000OOOOOO00 ['GE3_Cyl6_CompressionPrs'])/8 #line:2091
            if O0O0O00000O000O00 ['GE3']==1 and O0O0O00000O000O00 ['GE4']==1 :#line:2092
                OO0000000OOOOOO00 ['GE3_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE3GE4_Flow_InstMass']/2 #line:2093
            else :#line:2094
                OO0000000OOOOOO00 ['GE3_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE3GE4_Flow_InstMass']#line:2095
            OO0000000OOOOOO00 ['GE3_PF_Flow']=(OO0000000OOOOOO00 ['GE3_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['GE3_FO_flow']*0.005 )#line:2096
            if OO0000000OOOOOO00 ['GE3_Misc_Spd']==0.0 :#line:2097
                OO0000000OOOOOO00 ['GE3_Misc_Spd']=1.0 #line:2098
            OO0000000OOOOOO00 ['GE3_Suction_volumetric_flow']=(3.14 *(1 /4 )*(OOO0OO00OOO0O0O00 **2 )*OOO000000O0O00OOO *O000O0OO00OO00OO0 *OO0000000OOOOOO00 ['GE3_Misc_Spd']*60 )/2 #line:2099
            OO0000000OOOOOO00 ['GE3_Total_fuel_flow']=OO0000000OOOOOO00 ['GE3_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE3_FO_flow']+OO0000000OOOOOO00 ['GE3_PF_Flow']#line:2100
            if OO0000000OOOOOO00 ['GE3_Total_fuel_flow']==0.0 :#line:2101
                OO0000000OOOOOO00 ['GE3_Total_fuel_flow']=1.0 #line:2102
            OO0000000OOOOOO00 ['GE3_Heat_added']=(OO0000000OOOOOO00 ['GE3_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:2103
            OOOOOO0O000OOOO00 .SetTemperature (OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutTemp']+273.15 )#line:2106
            OOOOOO0O000OOOO00 .SetPressure (OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutPrs']*1000000 )#line:2107
            OOOOOO0O000OOOO00 .SetVolumetricFlow (OO0000000OOOOOO00 ['GE3_Suction_volumetric_flow']/3600.0 )#line:2108
            O0000O0OOO00O00O0 .set_POut (OO0000000OOOOOO00 ['GE3_CylAvg_CompressionPrs']*1000000 )#line:2109
            OO00OOO0OO00OO00O .set_EnergyFlow (OO0000000OOOOOO00 ['GE3_Heat_added'])#line:2110
            O0O0000O0O00O00OO .set_POut (OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutPrs']*1000000 )#line:2111
            O00OO0000OO0O0000 .set_OutletTemperature (OO0000000OOOOOO00 ['GE3_EG_TC1_InTemp']+273.15 )#line:2112
            O0OOO0OOO00OOO0O0 .SetTemperature (OO0000000OOOOOO00 ['GE3_EG_TC1_AirIntakeTemp']+273.15 )#line:2114
            O0OOOO00O0O0O0000 .set_POut (OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutPrs']*1000000 )#line:2115
            OOOOO000OO00O0000 .set_OutletTemperature (OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutTemp']+273.15 )#line:2116
            OO0OOO00OOOO0O0OO .SetPressure (OO0000000OOOOOO00 ['GE3_CS_LTCFW_AirClrInPrs']*1000000 )#line:2117
            OO0OOO00OOOO0O0OO .SetTemperature (OO0000000OOOOOO00 ['GE3_CS_LTCFW_AirClrInTemp']+273.15 )#line:2118
            O0O00OO00O00OO00O .set_OutletTemperature (OO0000000OOOOOO00 ['GE3_CS_LTCFW_AirClrOutTemp']+273.15 )#line:2119
            from DWSIM .GlobalSettings import Settings #line:2121
            Settings .SolverMode =0 #line:2122
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .GE3_sim )#line:2123
            O00OO0O00OO0OO0O0 ['GE3_Suction_volumetric_flow']=OO0000000OOOOOO00 ['GE3_Suction_volumetric_flow']#line:2125
            O00OO0O00OO0OO0O0 ['GE3_Combustion_air_flow']=OOOOOO0O000OOOO00 .GetMassFlow ()*3600 #line:2126
            O00OO0O00OO0OO0O0 ['GE3_Total_fuel_flow']=OO0000000OOOOOO00 ['GE3_Total_fuel_flow']#line:2128
            O00OO0O00OO0OO0O0 ['GE3_AirFuel_ratio']=O00OO0O00OO0OO0O0 ['GE3_Combustion_air_flow']/O00OO0O00OO0OO0O0 ['GE3_Total_fuel_flow']#line:2129
            O00OO0O00OO0OO0O0 ['GE3_Heat_added']=OO0000000OOOOOO00 ['GE3_Heat_added']#line:2130
            O00OO0O00OO0OO0O0 ['GE3_Isentropic_compression_power']=abs (O0000O0OOO00O00O0 .GetPowerGeneratedOrConsumed ())#line:2131
            O00OO0O00OO0OO0O0 ['GE3_Maximum_pressure']=OO0000000OOOOOO00 ['GE3_CylAvg_CompressionPrs']*10 #line:2132
            O00OO0O00OO0OO0O0 ['GE3_CylTemperature_after_isentropic_compression']=O00OOO00OOOOOO0OO .GetTemperature ()-273.15 #line:2133
            O00OO0O00OO0OO0O0 ['GE3_CylTemperature_after_combustion']=O0O0000O0O0O0000O .GetTemperature ()-273.15 #line:2134
            O00OO0O00OO0OO0O0 ['GE3_Total_ideal_brake_power']=abs (O0O0000O0O00O00OO .GetPowerGeneratedOrConsumed ())#line:2136
            O00OO0O00OO0OO0O0 ['GE3_Net_ideal_brake_power']=O00OO0O00OO0OO0O0 ['GE3_Total_ideal_brake_power']-O00OO0O00OO0OO0O0 ['GE3_Isentropic_compression_power']#line:2137
            O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']=OO0000000OOOOOO00 ['GE3_Misc_Pwr']#line:2138
            if O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']==0.0 :#line:2139
                O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']=1.0 #line:2140
            O00OO0O00OO0OO0O0 ['GE3_Ideal_brake_thermal_efficiency']=(O00OO0O00OO0OO0O0 ['GE3_Net_ideal_brake_power']/O00OO0O00OO0OO0O0 ['GE3_Heat_added'])*100 #line:2142
            O00OO0O00OO0OO0O0 ['GE3_Actual_brake_thermal_efficiency']=(O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']/O00OO0O00OO0OO0O0 ['GE3_Heat_added'])*100 #line:2143
            O00OO0O00OO0OO0O0 ['GE3_Relative_efficiency']=(O00OO0O00OO0OO0O0 ['GE3_Actual_brake_thermal_efficiency']/O00OO0O00OO0OO0O0 ['GE3_Ideal_brake_thermal_efficiency'])*100 #line:2144
            O00OO0O00OO0OO0O0 ['GE3_Ideal_brake_specific_fuel_consumption']=O00OO0O00OO0OO0O0 ['GE3_Total_fuel_flow']/O00OO0O00OO0OO0O0 ['GE3_Net_ideal_brake_power']#line:2145
            O00OO0O00OO0OO0O0 ['GE3_Actual_brake_specific_fuel_consumption']=O00OO0O00OO0OO0O0 ['GE3_Total_fuel_flow']/O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']#line:2146
            O00OO0O00OO0OO0O0 ['GE3_Actual_brake_mean_effective_pressure']=(O00OO0O00OO0OO0O0 ['GE3_Net_actual_brake_power']/OO0000000OOOOOO00 ['GE3_Suction_volumetric_flow'])*36 #line:2147
            O00OO0O00OO0OO0O0 ['GE3_Ideal_brake_mean_effective_pressure']=(O00OO0O00OO0OO0O0 ['GE3_Net_ideal_brake_power']/OO0000000OOOOOO00 ['GE3_Suction_volumetric_flow'])*36 #line:2148
            O00OO0O00OO0OO0O0 ['GE3_Compression_pressure_ratio']=O00OO0O00OO0OO0O0 ['GE3_Maximum_pressure']/(OO0000000OOOOOO00 ['GE3_CS_AirClr_ChAirOutPrs']*10 )#line:2149
            O00OO0O00OO0OO0O0 ['GE3_TC_compression_power']=abs (O0OOOO00O0O0O0000 .GetPowerGeneratedOrConsumed ())#line:2150
            O0OO00O0OO0OO0OO0 ['GE3_SAC_air_in_temperature']=OO00OO0000O0O0O00 .GetTemperature ()-273.15 #line:2152
            O0OO00O0OO0OO0OO0 ['GE3_SAC_scav_air_in_SpecificEnthalpy']=OO00OO0000O0O0O00 .GetMassEnthalpy ()#line:2153
            O0OO00O0OO0OO0OO0 ['GE3_SAC_scav_air_out_SpecificEnthalpy']=O000OOOOOO0O00OOO .GetMassEnthalpy ()#line:2154
            O0OO00O0OO0OO0OO0 ['GE3_SAC_cw_duty']=OOOOO000OO00O0000 .GetPowerGeneratedOrConsumed ()#line:2155
            O0OO00O0OO0OO0OO0 ['GE3_SAC_cw_flow_required']=OO0OOO00OOOO0O0OO .GetMassFlow ()*3600 #line:2156
            O00OO0O00OO0OO0O0 =O00OO0O00OO0OO0O0 |O0OO00O0OO0OO0OO0 #line:2158
            for O00000O00O0O00O00 in O00OO0O00OO0OO0O0 .keys ():#line:2159
                O00OO0O00OO0OO0O0 [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O00OO0O00OO0OO0O0 [O00000O00O0O00O00 ]))#line:2160
        if O0O0O00000O000O00 ['GE4']==1 :#line:2162
            print ("starting dwsim GE4")#line:2163
            OOOO000OO0O00000O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_Air_in').GetAsObject ()#line:2165
            O0O0OO0000OO00O0O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_Heat_added').GetAsObject ()#line:2166
            O0O0OO0OO0000O0O0 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_compression').GetAsObject ()#line:2167
            OOO00OOO000O0OO0O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_compression_power').GetAsObject ()#line:2168
            OO0000OO0O0OOO000 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_compressed').GetAsObject ()#line:2169
            O0OOOO00OO0O0000O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_heat_addition').GetAsObject ()#line:2170
            O00O0O000000OO000 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_heated').GetAsObject ()#line:2171
            O00O00OO00OO0O0OO =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_expansion').GetAsObject ()#line:2172
            O0OO00O0000O0OOOO =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_brake_power').GetAsObject ()#line:2173
            OOOOOOOOO0OOO0000 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_Exhaust_gases').GetAsObject ()#line:2174
            O0OOO00000OO000O0 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_TC_exp').GetAsObject ()#line:2175
            O0OOOOOO0O0O0OO0O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_TC_comp').GetAsObject ()#line:2176
            O0000O00OO0OOO0O0 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_compressed_fresh_air').GetAsObject ()#line:2177
            OO0OOO0OOOO000O0O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_fresh_air_in').GetAsObject ()#line:2178
            OOOOOOO000000OOOO =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_scav_air_cooler').GetAsObject ()#line:2179
            OOO00OO0000O0O0OO =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_cw_in').GetAsObject ()#line:2180
            OOO0000OO0OOOOOO0 =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_scav_air').GetAsObject ()#line:2181
            O00OOO000O00O000O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_CL').GetAsObject ()#line:2182
            OO0O000O0OO0OO00O =OO0O0O0O0O0O00O00 .GE4_sim .GetFlowsheetSimulationObject ('GE4_HT').GetAsObject ()#line:2183
            OO0000000OOOOOO00 ['GE4_CylAvg_CompressionPrs']=(OO0000000OOOOOO00 ['GE4_Cyl1_CompressionPrs']+OO0000000OOOOOO00 ['GE4_Cyl2_CompressionPrs']+OO0000000OOOOOO00 ['GE4_Cyl3_CompressionPrs']+OO0000000OOOOOO00 ['GE4_Cyl4_CompressionPrs']+OO0000000OOOOOO00 ['GE4_Cyl5_CompressionPrs']+OO0000000OOOOOO00 ['GE4_Cyl6_CompressionPrs'])/8 #line:2186
            if O0O0O00000O000O00 ['GE3']==1 and O0O0O00000O000O00 ['GE4']==1 :#line:2187
                OO0000000OOOOOO00 ['GE4_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE3GE4_Flow_InstMass']/2 #line:2188
            else :#line:2189
                OO0000000OOOOOO00 ['GE4_FO_flow']=OO0000000OOOOOO00 ['GE_FO_GE3GE4_Flow_InstMass']#line:2190
            OO0000000OOOOOO00 ['GE4_PF_Flow']=(OO0000000OOOOOO00 ['GE4_FG_Flow_InstMass']*0.01 )+(OO0000000OOOOOO00 ['GE4_FO_flow']*0.005 )#line:2191
            if OO0000000OOOOOO00 ['GE4_Misc_Spd']==0.0 :#line:2192
                OO0000000OOOOOO00 ['GE4_Misc_Spd']=1.0 #line:2193
            OO0000000OOOOOO00 ['GE4_Suction_volumetric_flow']=(3.14 *(1 /4 )*(OOO0OO00OOO0O0O00 **2 )*OOO000000O0O00OOO *O0OO00000O0O00OO0 *OO0000000OOOOOO00 ['GE4_Misc_Spd']*60 )/2 #line:2194
            OO0000000OOOOOO00 ['GE4_Total_fuel_flow']=OO0000000OOOOOO00 ['GE4_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE4_FO_flow']+OO0000000OOOOOO00 ['GE4_PF_Flow']#line:2195
            if OO0000000OOOOOO00 ['GE4_Total_fuel_flow']==0.0 :#line:2196
                OO0000000OOOOOO00 ['GE4_Total_fuel_flow']=1.0 #line:2197
            OO0000000OOOOOO00 ['GE4_Heat_added']=(OO0000000OOOOOO00 ['GE4_Total_fuel_flow']*O000O0OOO0000O00O )/3600 #line:2198
            OOOO000OO0O00000O .SetTemperature (OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutTemp']+273.15 )#line:2201
            OOOO000OO0O00000O .SetPressure (OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutPrs']*1000000 )#line:2202
            OOOO000OO0O00000O .SetVolumetricFlow (OO0000000OOOOOO00 ['GE4_Suction_volumetric_flow']/3600.0 )#line:2203
            O0O0OO0OO0000O0O0 .set_POut (OO0000000OOOOOO00 ['GE4_CylAvg_CompressionPrs']*1000000 )#line:2204
            O0O0OO0000OO00O0O .set_EnergyFlow (OO0000000OOOOOO00 ['GE4_Heat_added'])#line:2205
            O00O00OO00OO0O0OO .set_POut (OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutPrs']*1000000 )#line:2206
            O00OOO000O00O000O .set_OutletTemperature (OO0000000OOOOOO00 ['GE4_EG_TC1_InTemp']+273.15 )#line:2207
            OO0OOO0OOOO000O0O .SetTemperature (OO0000000OOOOOO00 ['GE4_EG_TC1_AirIntakeTemp']+273.15 )#line:2209
            O0OOOOOO0O0O0OO0O .set_POut (OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutPrs']*1000000 )#line:2210
            OOOOOOO000000OOOO .set_OutletTemperature (OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutTemp']+273.15 )#line:2211
            OOO00OO0000O0O0OO .SetPressure (OO0000000OOOOOO00 ['GE4_CS_LTCFW_AirClrInPrs']*1000000 )#line:2212
            OOO00OO0000O0O0OO .SetTemperature (OO0000000OOOOOO00 ['GE4_CS_LTCFW_AirClrInTemp']+273.15 )#line:2213
            OO0O000O0OO0OO00O .set_OutletTemperature (OO0000000OOOOOO00 ['GE4_CS_LTCFW_AirClrOutTemp']+273.15 )#line:2214
            from DWSIM .GlobalSettings import Settings #line:2216
            Settings .SolverMode =0 #line:2217
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .GE4_sim )#line:2218
            O00OOOOO00OO0O0O0 ['GE4_Suction_volumetric_flow']=OO0000000OOOOOO00 ['GE4_Suction_volumetric_flow']#line:2220
            O00OOOOO00OO0O0O0 ['GE4_Combustion_air_flow']=OOOO000OO0O00000O .GetMassFlow ()*3600 #line:2221
            O00OOOOO00OO0O0O0 ['GE4_Total_fuel_flow']=OO0000000OOOOOO00 ['GE4_Total_fuel_flow']#line:2223
            O00OOOOO00OO0O0O0 ['GE4_AirFuel_ratio']=O00OOOOO00OO0O0O0 ['GE4_Combustion_air_flow']/O00OOOOO00OO0O0O0 ['GE4_Total_fuel_flow']#line:2224
            O00OOOOO00OO0O0O0 ['GE4_Heat_added']=OO0000000OOOOOO00 ['GE4_Heat_added']#line:2225
            O00OOOOO00OO0O0O0 ['GE4_Isentropic_compression_power']=abs (O0O0OO0OO0000O0O0 .GetPowerGeneratedOrConsumed ())#line:2226
            O00OOOOO00OO0O0O0 ['GE4_Maximum_pressure']=OO0000000OOOOOO00 ['GE4_CylAvg_CompressionPrs']*10 #line:2227
            O00OOOOO00OO0O0O0 ['GE4_CylTemperature_after_isentropic_compression']=OO0000OO0O0OOO000 .GetTemperature ()-273.15 #line:2228
            O00OOOOO00OO0O0O0 ['GE4_CylTemperature_after_combustion']=O00O0O000000OO000 .GetTemperature ()-273.15 #line:2229
            O00OOOOO00OO0O0O0 ['GE4_Total_ideal_brake_power']=abs (O00O00OO00OO0O0OO .GetPowerGeneratedOrConsumed ())#line:2231
            O00OOOOO00OO0O0O0 ['GE4_Net_ideal_brake_power']=O00OOOOO00OO0O0O0 ['GE4_Total_ideal_brake_power']-O00OOOOO00OO0O0O0 ['GE4_Isentropic_compression_power']#line:2232
            O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']=OO0000000OOOOOO00 ['GE4_Misc_Pwr']#line:2233
            if O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']==0.0 :#line:2234
                O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']=1.0 #line:2235
            O00OOOOO00OO0O0O0 ['GE4_Ideal_brake_thermal_efficiency']=(O00OOOOO00OO0O0O0 ['GE4_Net_ideal_brake_power']/O00OOOOO00OO0O0O0 ['GE4_Heat_added'])*100 #line:2237
            O00OOOOO00OO0O0O0 ['GE4_Actual_brake_thermal_efficiency']=(O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']/O00OOOOO00OO0O0O0 ['GE4_Heat_added'])*100 #line:2238
            O00OOOOO00OO0O0O0 ['GE4_Relative_efficiency']=(O00OOOOO00OO0O0O0 ['GE4_Actual_brake_thermal_efficiency']/O00OOOOO00OO0O0O0 ['GE4_Ideal_brake_thermal_efficiency'])*100 #line:2239
            O00OOOOO00OO0O0O0 ['GE4_Ideal_brake_specific_fuel_consumption']=O00OOOOO00OO0O0O0 ['GE4_Total_fuel_flow']/O00OOOOO00OO0O0O0 ['GE4_Net_ideal_brake_power']#line:2240
            O00OOOOO00OO0O0O0 ['GE4_Actual_brake_specific_fuel_consumption']=O00OOOOO00OO0O0O0 ['GE4_Total_fuel_flow']/O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']#line:2241
            O00OOOOO00OO0O0O0 ['GE4_Actual_brake_mean_effective_pressure']=(O00OOOOO00OO0O0O0 ['GE4_Net_actual_brake_power']/OO0000000OOOOOO00 ['GE4_Suction_volumetric_flow'])*36 #line:2242
            O00OOOOO00OO0O0O0 ['GE4_Ideal_brake_mean_effective_pressure']=(O00OOOOO00OO0O0O0 ['GE4_Net_ideal_brake_power']/OO0000000OOOOOO00 ['GE4_Suction_volumetric_flow'])*36 #line:2243
            O00OOOOO00OO0O0O0 ['GE4_Compression_pressure_ratio']=O00OOOOO00OO0O0O0 ['GE4_Maximum_pressure']/(OO0000000OOOOOO00 ['GE4_CS_AirClr_ChAirOutPrs']*10 )#line:2244
            O00OOOOO00OO0O0O0 ['GE4_TC_compression_power']=abs (O0OOOOOO0O0O0OO0O .GetPowerGeneratedOrConsumed ())#line:2245
            O0OOO000O0O000O0O ['GE4_SAC_air_in_temperature']=O0000O00OO0OOO0O0 .GetTemperature ()-273.15 #line:2247
            O0OOO000O0O000O0O ['GE4_SAC_scav_air_in_SpecificEnthalpy']=O0000O00OO0OOO0O0 .GetMassEnthalpy ()#line:2248
            O0OOO000O0O000O0O ['GE4_SAC_scav_air_out_SpecificEnthalpy']=OOO0000OO0OOOOOO0 .GetMassEnthalpy ()#line:2249
            O0OOO000O0O000O0O ['GE4_SAC_cw_duty']=OOOOOOO000000OOOO .GetPowerGeneratedOrConsumed ()#line:2250
            O0OOO000O0O000O0O ['GE4_SAC_cw_flow_required']=OOO00OO0000O0O0OO .GetMassFlow ()*3600 #line:2251
            O00OOOOO00OO0O0O0 =O00OOOOO00OO0O0O0 |O0OOO000O0O000O0O #line:2253
            for O00000O00O0O00O00 in O00OOOOO00OO0O0O0 .keys ():#line:2254
                O00OOOOO00OO0O0O0 [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O00OOOOO00OO0O0O0 [O00000O00O0O00O00 ]))#line:2255
        if O0O0O00000O000O00 ['NG1']==1 :#line:2257
            print ("starting dwsim NG1")#line:2258
            if O00O0O0OO0OO0O0O0 ['NS_NG1-40101_PV']==1 and O00O0O0OO0OO0O0O0 ['NS_NG1-40102_PV']==1 and O00O0O0OO0OO0O0O0 ['NS_NG1-40103_PV']==1 :#line:2260
                OO0OO0OOO0O0O0O0O =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_air_comp').GetAsObject ()#line:2261
                O00OOO0OO0OO00000 =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_Air').GetAsObject ()#line:2262
                O00000OO0OO0O0OO0 =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_comp_out').GetAsObject ()#line:2263
                O0OO0OO000OO000O0 =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_clr').GetAsObject ()#line:2264
                OOOOOOO00O000O0OO =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_htr_in').GetAsObject ()#line:2265
                O0O00OO0O0OO0O0OO =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_htr').GetAsObject ()#line:2266
                O0OO00O0OOO0O0O00 =OO0O0O0O0O0O00O00 .NG1_sim .GetFlowsheetSimulationObject ('NG1_sep_in').GetAsObject ()#line:2267
                O00OOO0OO0OO00000 .SetTemperature (OO0000000OOOOOO00 ['Nav_Atm_AmbTemp']+273.15 )#line:2269
                O00OOO0OO0OO00000 .SetVolumetricFlow ((OO0000000OOOOOO00 ['Elec_NGen1_Flow']/0.78 )/3600 )#line:2271
                OO0OO0OOO0O0O0O0O .set_POut (OO0000000OOOOOO00 ['NS_NG1-40101_PV']*1000000 )#line:2272
                O0OO0OO000OO000O0 .set_OutletTemperature (OO0000000OOOOOO00 ['NS_NG1-40102_PV']+273.15 )#line:2273
                O0O00OO0O0OO0O0OO .set_OutletTemperature (OO0000000OOOOOO00 ['NS_NG1-40103_PV']+273.15 )#line:2274
                from DWSIM .GlobalSettings import Settings #line:2276
                Settings .SolverMode =0 #line:2277
                O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .NG1_sim )#line:2278
                O0OO00O0O0O0O0OO0 ['NG1_Air_flow_estimated']=O00OOO0OO0OO00000 .GetMassFlow ()*3600 #line:2280
                O0OO00O0O0O0O0OO0 ['NG1_Air_comp_in_SpecificEnthalpy']=O00OOO0OO0OO00000 .GetMassEnthalpy ()#line:2281
                O0OO00O0O0O0O0OO0 ['NG1_Air_comp_out_SpecificEnthalpy']=O00000OO0OO0O0OO0 .GetMassEnthalpy ()#line:2282
                O0OO00O0O0O0O0OO0 ['NG1_air_comp_polytropic_power']=abs (OO0OO0OOO0O0O0O0O .GetPowerGeneratedOrConsumed ())#line:2283
                O0OO00O0O0O0O0OO0 ['NG1_air_comp_out_temperature']=O00000OO0OO0O0OO0 .GetTemperature ()-273.15 #line:2284
                O0OO00O0O0O0O0OO0 ['NG1_cooling_duty']=O0OO0OO000OO000O0 .GetPowerGeneratedOrConsumed ()#line:2285
                O0OO00O0O0O0O0OO0 ['NG1_heating_duty']=abs (O0O00OO0O0OO0O0OO .GetPowerGeneratedOrConsumed ())#line:2286
                O0OO00O0O0O0O0OO0 ['NG1_htr_in_SpecificEnthalpy']=OOOOOOO00O000O0OO .GetMassEnthalpy ()#line:2287
                O0OO00O0O0O0O0OO0 ['NG1_htr_out_SpecificEnthalpy']=O0OO00O0OOO0O0O00 .GetMassEnthalpy ()#line:2288
                for O00000O00O0O00O00 in O0OO00O0O0O0O0OO0 .keys ():#line:2290
                    O0OO00O0O0O0O0OO0 [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O0OO00O0O0O0O0OO0 [O00000O00O0O00O00 ]))#line:2291
        if O0O0O00000O000O00 ['NG2']==1 :#line:2293
            print ("starting dwsim NG2")#line:2294
            if O00O0O0OO0OO0O0O0 ['NS_NG2-40101_PV']==1 and O00O0O0OO0OO0O0O0 ['NS_NG2-40102_PV']==1 and O00O0O0OO0OO0O0O0 ['NS_NG2-40103_PV']==1 :#line:2295
                OOOOOOO000OO0O0O0 =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_air_comp').GetAsObject ()#line:2297
                OO00OO0OOOOO0O0O0 =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_Air').GetAsObject ()#line:2298
                OOOOO00O000OOOOOO =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_comp_out').GetAsObject ()#line:2299
                OOO0OOOOOOO0OO00O =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_clr').GetAsObject ()#line:2300
                O00O00000O00O00O0 =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_htr_in').GetAsObject ()#line:2301
                OO00OO00O0O0OOO0O =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_htr').GetAsObject ()#line:2302
                O0OO0O0O000O00000 =OO0O0O0O0O0O00O00 .NG2_sim .GetFlowsheetSimulationObject ('NG2_sep_in').GetAsObject ()#line:2303
                OO00OO0OOOOO0O0O0 .SetTemperature (OO0000000OOOOOO00 ['Nav_Atm_AmbTemp']+273.15 )#line:2305
                OO00OO0OOOOO0O0O0 .SetVolumetricFlow ((OO0000000OOOOOO00 ['Elec_NGen2_Flow']/0.78 )/3600 )#line:2307
                OOOOOOO000OO0O0O0 .set_POut (OO0000000OOOOOO00 ['NS_NG2-40101_PV']*1000000 )#line:2308
                OOO0OOOOOOO0OO00O .set_OutletTemperature (OO0000000OOOOOO00 ['NS_NG2-40102_PV']+273.15 )#line:2309
                OO00OO00O0O0OOO0O .set_OutletTemperature (OO0000000OOOOOO00 ['NS_NG2-40103_PV']+273.15 )#line:2310
                from DWSIM .GlobalSettings import Settings #line:2312
                Settings .SolverMode =0 #line:2313
                O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .NG2_sim )#line:2314
                O0OOOO0OOO000OO0O ['NG2_Air_flow_estimated']=OO00OO0OOOOO0O0O0 .GetMassFlow ()*3600 #line:2316
                O0OOOO0OOO000OO0O ['NG2_Air_comp_in_SpecificEnthalpy']=OO00OO0OOOOO0O0O0 .GetMassEnthalpy ()#line:2317
                O0OOOO0OOO000OO0O ['NG2_Air_comp_out_SpecificEnthalpy']=OOOOO00O000OOOOOO .GetMassEnthalpy ()#line:2318
                O0OOOO0OOO000OO0O ['NG2_air_comp_polytropic_power']=abs (OOOOOOO000OO0O0O0 .GetPowerGeneratedOrConsumed ())#line:2319
                O0OOOO0OOO000OO0O ['NG2_air_comp_out_temperature']=OOOOO00O000OOOOOO .GetTemperature ()-273.15 #line:2320
                O0OOOO0OOO000OO0O ['NG2_cooling_duty']=OOO0OOOOOOO0OO00O .GetPowerGeneratedOrConsumed ()#line:2321
                O0OOOO0OOO000OO0O ['NG2_heating_duty']=abs (OO00OO00O0O0OOO0O .GetPowerGeneratedOrConsumed ())#line:2322
                O0OOOO0OOO000OO0O ['NG2_htr_in_SpecificEnthalpy']=O00O00000O00O00O0 .GetMassEnthalpy ()#line:2323
                O0OOOO0OOO000OO0O ['NG2_htr_out_SpecificEnthalpy']=O0OO0O0O000O00000 .GetMassEnthalpy ()#line:2324
                for O00000O00O0O00O00 in O0OOOO0OOO000OO0O .keys ():#line:2326
                    O0OOOO0OOO000OO0O [O00000O00O0O00O00 ]=float ("{0:.3f}".format (O0OOOO0OOO000OO0O [O00000O00O0O00O00 ]))#line:2327
        OOOO00OOO00OOOO00 =50000 #line:2331
        if O0O0O00000O000O00 ['AB_AB1']==1 and O0O0O00000O000O00 ['AB_AB2']==1 :#line:2332
                O00OOOOOOO00O0O00 =((OO0000000OOOOOO00 ['Blr_AuxBlr_FO_Flow_InstMass']*50000 )/3600 )/2 #line:2333
                OOOO00OO000O00O0O =((OO0000000OOOOOO00 ['Blr_AuxBlr_FO_Flow_InstMass']*50000 )/3600 )/2 #line:2334
        elif O0O0O00000O000O00 ['AB_AB1']==1 :#line:2335
                O00OOOOOOO00O0O00 =((OO0000000OOOOOO00 ['Blr_AuxBlr_FO_Flow_InstMass']*50000 )/3600 )#line:2336
                OOOO00OO000O00O0O =0 #line:2337
        elif O0O0O00000O000O00 ['AB_AB2']==1 :#line:2338
                OOOO00OO000O00O0O =((OO0000000OOOOOO00 ['Blr_AuxBlr_FO_Flow_InstMass']*50000 )/3600 )#line:2339
                O00OOOOOOO00O0O00 =0 #line:2340
        if O0O0O00000O000O00 ['AB_AB1']==1 :#line:2341
            print ("starting dwsim AB1")#line:2342
            O0O0O00OOOOO00OOO =OO0O0O0O0O0O00O00 .AB1_sim .GetFlowsheetSimulationObject ('AB1_steam').GetAsObject ()#line:2343
            O0O0O00OOOOO00OOO .SetPressure (OO0000000OOOOOO00 ['Blr_AuxBlr1_StmPrs']*1000000 )#line:2344
            from DWSIM .GlobalSettings import Settings #line:2346
            Settings .SolverMode =0 #line:2347
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .AB1_sim )#line:2348
            O0000O00O0OOO0O00 ['AB1_Heat_added']=O00OOOOOOO00O0O00 #line:2350
            O0000O00O0OOO0O00 ['AB1_Steam_temp']=O0O0O00OOOOO00OOO .GetTemperature ()-273.15 #line:2351
            O0000O00O0OOO0O00 ['AB1_Steam_SpecificEnthalpy']=O0O0O00OOOOO00OOO .GetMassEnthalpy ()#line:2352
            O0000O00O0OOO0O00 ['AB1_Steam_flow']=(O0000O00O0OOO0O00 ['AB1_Heat_added']/O0000O00O0OOO0O00 ['AB1_Steam_SpecificEnthalpy'])*3600 *0.8 #line:2353
        if O0O0O00000O000O00 ['AB_AB2']==1 :#line:2355
            print ("starting dwsim AB2")#line:2356
            O00000OOOO00O0O0O =OO0O0O0O0O0O00O00 .AB2_sim .GetFlowsheetSimulationObject ('AB2_steam').GetAsObject ()#line:2357
            O00000OOOO00O0O0O .SetPressure (OO0000000OOOOOO00 ['Blr_AuxBlr2_StmPrs']*1000000 )#line:2358
            from DWSIM .GlobalSettings import Settings #line:2360
            Settings .SolverMode =0 #line:2361
            O0OOO00OO000OOOO0 =OO0O0O0O0O0O00O00 .interf .CalculateFlowsheet2 (OO0O0O0O0O0O00O00 .AB2_sim )#line:2362
            OO00O0O0O00O00O00 ['AB2_Heat_added']=OOOO00OO000O00O0O #line:2364
            OO00O0O0O00O00O00 ['AB2_Steam_temp']=O00000OOOO00O0O0O .GetTemperature ()-273.15 #line:2365
            OO00O0O0O00O00O00 ['AB2_Steam_SpecificEnthalpy']=O00000OOOO00O0O0O .GetMassEnthalpy ()#line:2366
            OO00O0O0O00O00O00 ['AB2_Steam_flow']=(OO00O0O0O00O00O00 ['AB2_Heat_added']/OO00O0O0O00O00O00 ['AB2_Steam_SpecificEnthalpy'])*3600 *0.8 #line:2367
        OOO00O0OO0OO00O00 ={}#line:2374
        O000OOO0O0OO0OOO0 ={}#line:2375
        OOO000OO0OOO00OOO ={}#line:2376
        O0OO0OO00O0OO0000 ={}#line:2377
        if O0O0O00000O000O00 ['LNGV']==1 :#line:2381
            OO00OOOOOOOOOOO00 =OO0OOO0O00O0O0O0O ['LNGV_Qc']#line:2382
        else :#line:2383
            OO00OOOOOOOOOOO00 =0 #line:2384
        if O0O0O00000O000O00 ['WUH']==1 :#line:2385
            O000OO000O00O0O0O =OOOO000O0O0O0000O ['WUH_Qc']#line:2386
        else :#line:2387
            O000OO000O00O0O0O =0 #line:2388
        OOO00O0OO0OO00O00 ['Cargo_vapor_total_duty']=OO00OOOOOOOOOOO00 +O000OO000O00O0O0O #line:2389
        if O0O0O00000O000O00 ['FV']==1 :#line:2392
            O00000OO0OOO000OO =OO0OO000O0000OO0O ['FV_Qc']#line:2393
        else :#line:2394
            O00000OO0OOO000OO =0 #line:2395
        if O0O0O00000O000O00 ['BOGH']==1 :#line:2396
            O000000OOOO0OOO00 =O000OO000OO00O0OO ['BOGH_Qc']#line:2397
        else :#line:2398
            O000000OOOO0OOO00 =0 #line:2399
        OOO000OO0OOO00OOO ['FBOG_total_duty']=O00000OO0OOO000OO +O000000OOOO0OOO00 #line:2400
        if O0O0O00000O000O00 ['FV']==1 :#line:2404
            OOOO00OOOO0O00OOO =OO0OO000O0000OO0O ['FV_steam_required']#line:2405
        else :#line:2406
            OOOO00OOOO0O00OOO =0 #line:2407
        if O0O0O00000O000O00 ['BOGH']==1 :#line:2408
            OO0OOOOO00OO0OOOO =O000OO000OO00O0OO ['BOGH_steam_required']#line:2409
        else :#line:2410
            OO0OOOOO00OO0OOOO =0 #line:2411
        OOO000OO0OOO00OOO ['FBOG_total_steam']=OOOO00OOOO0O00OOO +OO0OOOOO00OO0OOOO #line:2412
        if O0O0O00000O000O00 ['HD1']==1 and O0O0O00000O000O00 ['HD2']==0 :#line:2416
            O000OOO0O0OO0OOO0 ['HD_polytropic_efficiency']=O0OO0O000OOO000OO ['HD1_polytropic_efficiency']#line:2417
        elif O0O0O00000O000O00 ['HD1']==0 and O0O0O00000O000O00 ['HD2']==1 :#line:2418
            O000OOO0O0OO0OOO0 ['HD_polytropic_efficiency']=OO00O00000O0OO0O0 ['HD2_polytropic_efficiency']#line:2419
        elif O0O0O00000O000O00 ['HD1']==1 and O0O0O00000O000O00 ['HD2']==1 :#line:2420
            O000OOO0O0OO0OOO0 ['HD_polytropic_efficiency']=(O0OO0O000OOO000OO ['HD1_polytropic_efficiency']+OO00O00000O0OO0O0 ['HD2_polytropic_efficiency'])/2 #line:2421
        if O0O0O00000O000O00 ['LD1']==1 and O0O0O00000O000O00 ['LD2']==0 :#line:2428
            O0OO0OO00O0OO0000 ['NBOG_polytropic_efficiency']=(O00O0OOOO0000O00O ['LD1_S1_polytropic_efficiency']+O00O0OOOO0000O00O ['LD1_S2_polytropic_efficiency'])/2 #line:2429
            O0OO0OO00O0OO0000 ['NBOG_polytropic_power']=(O00O0OOOO0000O00O ['LD1_S1_polytropic_power']+O00O0OOOO0000O00O ['LD1_S2_polytropic_power'])/2 #line:2430
        elif O0O0O00000O000O00 ['LD1']==0 and O0O0O00000O000O00 ['LD2']==1 :#line:2431
            O0OO0OO00O0OO0000 ['NBOG_polytropic_efficiency']=(O0OO0OO000OO0O0OO ['LD2_S1_polytropic_efficiency']+O0OO0OO000OO0O0OO ['LD2_S2_polytropic_efficiency'])/2 #line:2432
            O0OO0OO00O0OO0000 ['NBOG_polytropic_power']=(O0OO0OO000OO0O0OO ['LD2_S1_polytropic_power']+O0OO0OO000OO0O0OO ['LD2_S2_polytropic_power'])/2 #line:2433
        elif O0O0O00000O000O00 ['LD1']==1 and O0O0O00000O000O00 ['LD2']==1 :#line:2434
            O0OO0OO00O0OO0000 ['NBOG_polytropic_efficiency']=(O00O0OOOO0000O00O ['LD1_S1_polytropic_efficiency']+O00O0OOOO0000O00O ['LD1_S2_polytropic_efficiency']+O0OO0OO000OO0O0OO ['LD2_S1_polytropic_efficiency']+O0OO0OO000OO0O0OO ['LD2_S2_polytropic_efficiency'])/4 #line:2435
            O0OO0OO00O0OO0000 ['NBOG_polytropic_power']=(O00O0OOOO0000O00O ['LD1_S1_polytropic_power']+O00O0OOOO0000O00O ['LD1_S2_polytropic_power']+O0OO0OO000OO0O0OO ['LD2_S1_polytropic_power']+O0OO0OO000OO0O0OO ['LD2_S2_polytropic_power'])/4 #line:2436
        OO0000O0OOO00000O ={}#line:2440
        OO0000O0OOO00000O ['FG_Consumption_ME']=OO0000000OOOOOO00 ['ME1_FG_Flow_InstMass']+OO0000000OOOOOO00 ['ME2_FG_Flow_InstMass']#line:2443
        OO0000O0OOO00000O ['FG_Consumption_GE']=OO0000000OOOOOO00 ['GE1_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE2_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE3_FG_Flow_InstMass']+OO0000000OOOOOO00 ['GE4_FG_Flow_InstMass']#line:2444
        OO0000O0OOO00000O ['FO_Consumption_Aux_Boiler']=OO0000000OOOOOO00 ['Blr_AuxBlr_FO_Flow_InstMass']#line:2445
        if O00O0O0OO0OO0O0O0 ['NS_GPS_019_PV']==1 :#line:2446
            OO0000O0OOO00000O ['Speed']=OO0000000OOOOOO00 ['NS_GPS_019_PV']#line:2447
        else :#line:2448
            OO0000O0OOO00000O ['Speed']=9.9 #line:2449
        OO0000O0OOO00000O ['FG_Consumption_GCU']=OO0000000OOOOOO00 ['FG_GCU1_Flow']#line:2451
        OO0000O0OOO00000O ['FO_Consumption_ME']=OO0000000OOOOOO00 ['ME1_FO_Flow_InstMass']+OO0000000OOOOOO00 ['ME2_FO_Flow_InstMass']#line:2452
        OO0000O0OOO00000O ['FO_Consumption_GE']=OO0000000OOOOOO00 ['GE_FO_GE1GE2_Flow_InstMass']+OO0000000OOOOOO00 ['GE_FO_GE3GE4_Flow_InstMass']#line:2453
        OO0000O0OOO00000O ['Total_FG_Consumption']=OO0000O0OOO00000O ['FG_Consumption_ME']+OO0000O0OOO00000O ['FG_Consumption_GE']+OO0000O0OOO00000O ['FG_Consumption_GCU']#line:2454
        OO0000O0OOO00000O ['PF_Consumption_ME_FG']=OO0000O0OOO00000O ['FG_Consumption_ME']*0.01 #line:2455
        OO0000O0OOO00000O ['PF_Consumption_ME_FO']=OO0000O0OOO00000O ['FO_Consumption_ME']*0.005 #line:2456
        OO0000O0OOO00000O ['PF_Consumption_GE_FG']=OO0000O0OOO00000O ['FG_Consumption_GE']*0.01 #line:2457
        OO0000O0OOO00000O ['PF_Consumption_GE_FO']=OO0000O0OOO00000O ['FO_Consumption_GE']*0.005 #line:2458
        OO0000O0OOO00000O ['Total_FO_Consumption']=OO0000O0OOO00000O ['FO_Consumption_ME']+OO0000O0OOO00000O ['FO_Consumption_GE']+OO0000O0OOO00000O ['FO_Consumption_Aux_Boiler']+OO0000O0OOO00000O ['PF_Consumption_ME_FO']+OO0000O0OOO00000O ['PF_Consumption_GE_FO']#line:2459
        OO0000O0OOO00000O ['Total_Fuel_Consumption']=OO0000O0OOO00000O ['Total_FG_Consumption']+OO0000O0OOO00000O ['Total_FO_Consumption']+OO0000O0OOO00000O ['PF_Consumption_ME_FG']+OO0000O0OOO00000O ['PF_Consumption_GE_FG']#line:2460
        O0000OOOOOO0OO000 ={}#line:2462
        if O0O0O00000O000O00 ['Fuel_Economy']==1 :#line:2463
            if OO0000O0OOO00000O ['Speed']==0 :#line:2464
                O0000OOOOOO0OO000 ['Fuel_Economy']=0 #line:2465
            else :#line:2466
                O0000OOOOOO0OO000 ['Fuel_Economy']=OO0000O0OOO00000O ['Total_Fuel_Consumption']/OO0000O0OOO00000O ['Speed']#line:2467
        O0OO0OOO00O0OOO00 ={}#line:2472
        O000000O000O0OO0O =['FV_outputs','LNGV_outputs','BOGH_outputs','WUH_outputs','GWH_Stm_outputs','LD1_outputs','LD2_outputs','HD1_outputs','HD2_outputs','SC_outputs','Cargo_vapor_outputs','HD_outputs','NBOG_outputs','FBOG_outputs','Fuel_Consumption_outputs','Fuel_Economy_outputs','ME1_outputs','ME2_outputs','GE1_outputs','GE2_outputs','GE3_outputs','GE4_outputs','NG1_outputs','NG2_outputs','AB_AB1_outputs','AB_AB2_outputs']#line:2476
        O000OOO0O000OOOO0 =[OO0OO000O0000OO0O ,OO0OOO0O00O0O0O0O ,O000OO000OO00O0OO ,OOOO000O0O0O0000O ,OOO0OOO00OOOO0000 ,O00O0OOOO0000O00O ,O0OO0OO000OO0O0OO ,O0OO0O000OOO000OO ,OO00O00000O0OO0O0 ,OO0OO000OO0OO0O00 ,OOO00O0OO0OO00O00 ,O000OOO0O0OO0OOO0 ,O0OO0OO00O0OO0000 ,OOO000OO0OOO00OOO ,OO0000O0OOO00000O ,O0000OOOOOO0OO000 ,OOOOO000O000OOOO0 ,O0OOOOOOO0OOO0000 ,OOOO00O0O000000OO ,O0OO00OO000000OOO ,O00OO0O00OO0OO0O0 ,O00OOOOO00OO0O0O0 ,O0OO00O0O0O0O0OO0 ,O0OOOO0OOO000OO0O ,O0000O00O0OOO0O00 ,OO00O0O0O00O00O00 ]#line:2480
        for OO0OO0O0OO0O0O0OO in range (len (O000000O000O0OO0O )):#line:2481
            O0OO0OOO00O0OOO00 [O000000O000O0OO0O [OO0OO0O0OO0O0O0OO ]]=O000OOO0O000OOOO0 [OO0OO0O0OO0O0O0OO ]#line:2482
        O0OOOO0000O0O0OO0 =OO0OO000O0000OO0O |OO0OOO0O00O0O0O0O |O000OO000OO00O0OO |OOOO000O0O0O0000O |OOO0OOO00OOOO0000 |O00O0OOOO0000O00O |O0OO0OO000OO0O0OO |O0OO0O000OOO000OO |OO00O00000O0OO0O0 |OO0OO000OO0OO0O00 |OOO00O0OO0OO00O00 |O000OOO0O0OO0OOO0 |O0OO0OO00O0OO0000 |OOO000OO0OOO00OOO |OO0000O0OOO00000O |O0000OOOOOO0OO000 |OOOOO000O000OOOO0 |O0OOOOOOO0OOO0000 |OOOO00O0O000000OO |O0OO00OO000000OOO |O00OO0O00OO0OO0O0 |O00OOOOO00OO0O0O0 |O0OO00O0O0O0O0OO0 |O0OOOO0OOO000OO0O |O0000O00O0OOO0O00 |OO00O0O0O00O00O00 #line:2484
        return O0OO0OOO00O0OOO00 ,O0OOOO0000O0O0OO0 #line:2485
    def outputsLogging (O0O0000OOO0O00O00 ,O0OO000OO0OOO00O0 ,O0000000O0O0000O0 ,OO0000OO00OO00O00 ,OOOO00OO000OOOOO0 ):#line:2487
        OOOO0OO00O0OOOOOO =['FV','LNGV','BOGH','WUH','GWH_Stm','LD1','LD2','HD1','HD2','SC','Cargo_vapor','HD','FBOG','NBOG','Fuel_Consumption','Fuel_Economy','ME1','ME2','GE1','GE2','GE3','GE4','AB_AB1','AB_AB2']#line:2491
        if OOOO00OO000OOOOO0 ['NS_NG1-40101_PV']==1 and OOOO00OO000OOOOO0 ['NS_NG2-40101_PV']==1 :#line:2492
            OOOO0OO00O0OOOOOO =OOOO0OO00O0OOOOOO +['NG1','NG2']#line:2493
        for OO0O000OOOOOO00OO in OOOO0OO00O0OOOOOO :#line:2497
            if O0000000O0O0000O0 [OO0O000OOOOOO00OO ]==1 :#line:2499
                OOO0OOOOO0OOOOOOO =OO0O000OOOOOO00OO +"_output_history"#line:2500
                O0O0000OOO0O00O00 .cursor .execute ('select "column_name" from information_schema.columns where "table_name" = %s',[OOO0OOOOO0OOOOOOO ])#line:2501
                OOOOOO00O00OOOOOO =O0O0000OOO0O00O00 .cursor .fetchall ()#line:2502
                O0O0000OOO0O00O00 .conn .commit ()#line:2503
                O0O00000000OO00OO =[OO00OOO0000OOO000 [0 ]for OO00OOO0000OOO000 in OOOOOO00O00OOOOOO ]#line:2506
                O0O00000000OO00OO .remove ('TimeStamp_onboard')#line:2507
                OO0O000OOOOOO00OO =OO0O000OOOOOO00OO +"_outputs"#line:2511
                for O0OO0O0OO0O0OOOOO in O0O00000000OO00OO :#line:2512
                    if 'Performance_health'not in O0OO0O0OO0O0OOOOO :#line:2513
                        if np .isnan (O0OO000OO0OOO00O0 [OO0O000OOOOOO00OO ][O0OO0O0OO0O0OOOOO ]):#line:2517
                            print (O0OO0O0OO0O0OOOOO )#line:2519
                            print ('this is nan, setting to temporary value 0')#line:2522
                            O0OO000OO0OOO00O0 [OO0O000OOOOOO00OO ][O0OO0O0OO0O0OOOOO ]=0.0 #line:2523
                        O0O0000OOO0O00O00 .cursor .execute ('update public."Output_Tags" set "Value" = %s where "TagName" = %s',[float (O0OO000OO0OOO00O0 [OO0O000OOOOOO00OO ][O0OO0O0OO0O0OOOOO ]),O0OO0O0OO0O0OOOOO ])#line:2525
                        O0O0000OOO0O00O00 .conn .commit ()#line:2526
                OOO0OOOOOOOOO0O0O =f"'{OO0000OO00OO00O00}', "#line:2531
                for O0OO0O0OO0O0OOOOO in O0O00000000OO00OO :#line:2532
                    if 'Performance_health'not in O0OO0O0OO0O0OOOOO :#line:2533
                        OOO0OOOOOOOOO0O0O =OOO0OOOOOOOOO0O0O +f"{O0OO000OO0OOO00O0[OO0O000OOOOOO00OO][O0OO0O0OO0O0OOOOO]}, "#line:2534
                if OO0O000OOOOOO00OO [:-8 ]in ['Cargo_vapor','HD','FBOG','NBOG','Fuel_Consumption','Fuel_Economy','ME1','ME2','GE1','GE2','GE3','GE4','NG1','NG2','AB_AB1','AB_AB2']:#line:2535
                    OOO0OOOOOOOOO0O0O =OOO0OOOOOOOOO0O0O [:-2 ]#line:2536
                else :#line:2537
                    OOO0OOOOOOOOO0O0O =OOO0OOOOOOOOO0O0O +f"{100}"#line:2538
                OOO0OOOOOOOOO0O0O =f'insert into public."{OOO0OOOOO0OOOOOOO}" values({OOO0OOOOOOOOO0O0O})'#line:2539
                O0O0000OOO0O00O00 .cursor .execute (OOO0OOOOOOOOO0O0O )#line:2541
                O0O0000OOO0O00O00 .conn .commit ()#line:2542
    def runningStatus (O0OO0O0O0OOOOO00O ,O00OOOO00O000OOOO ,O000OOO00OOO00OO0 ):#line:2552
        OO0OOO00OO0OO0O00 ={}#line:2554
        if O00OOOO00O000OOOO ['FG_FV_DischFlow']>100 :#line:2555
            OO0OOO00OO0OO0O00 ['FV']=1 #line:2556
        else :#line:2557
            OO0OOO00OO0OO0O00 ['FV']=0 #line:2558
        if O00OOOO00O000OOOO ['CM_LNGVapr_Stop']==0 and O00OOOO00O000OOOO ['FG_Flow_VaprToAtm']>100 :#line:2561
            OO0OOO00OO0OO0O00 ['LNGV']=1 #line:2562
        else :#line:2563
            OO0OOO00OO0OO0O00 ['LNGV']=0 #line:2564
        if O00OOOO00O000OOOO ['FG_FV_DischFlow']>100 :#line:2566
            OO0OOO00OO0OO0O00 ['BOGH']=1 #line:2567
        else :#line:2568
            OO0OOO00OO0OO0O00 ['BOGH']=0 #line:2569
        if (O00OOOO00O000OOOO ['FG_FBOG_WuHtr_OutTempInd']-O00OOOO00O000OOOO ['FG_FBOG_WuHtr_InTempInd']>10 )and (O00OOOO00O000OOOO ['FG_FBOG_WuHtr_CondWtrTempInd']-O00OOOO00O000OOOO ['FG_FBOG_WuHtr_OutTempInd']>0 ):#line:2571
            OO0OOO00OO0OO0O00 ['WUH']=1 #line:2572
        else :#line:2573
            OO0OOO00OO0OO0O00 ['WUH']=0 #line:2574
        if (O00OOOO00O000OOOO ['FG_GW_MainHtr_OutTemp']-O00OOOO00O000OOOO ['FG_GW_MainHtr_RtnTemp']>5 )and O00OOOO00O000OOOO ['CM_GwCircPp1_Run']==1 :#line:2577
            OO0OOO00OO0OO0O00 ['GWH_Stm']=1 #line:2578
        else :#line:2580
            OO0OOO00OO0OO0O00 ['GWH_Stm']=0 #line:2581
        if O00OOOO00O000OOOO ['CM_LD1_Flow']>100 :#line:2585
            OO0OOO00OO0OO0O00 ['LD1']=1 #line:2586
        else :#line:2587
            OO0OOO00OO0OO0O00 ['LD1']=0 #line:2588
        if O00OOOO00O000OOOO ['CM_LD2_Flow']>100 :#line:2591
            OO0OOO00OO0OO0O00 ['LD2']=1 #line:2592
        else :#line:2593
            OO0OOO00OO0OO0O00 ['LD2']=0 #line:2594
        if O00OOOO00O000OOOO ['CM_HD1_Run']==1 and (O00OOOO00O000OOOO ['CM_HD1_DischPrs']-O00OOOO00O000OOOO ['CM_HD1_InPrsAlrmCtrl']>30 )and O00OOOO00O000OOOO ['CM_HD1_IGVPosCtrl']>5 :#line:2596
            OO0OOO00OO0OO0O00 ['HD1']=1 #line:2597
        else :#line:2598
            OO0OOO00OO0OO0O00 ['HD1']=0 #line:2599
        if O00OOOO00O000OOOO ['CM_HD2_Run']==1 and (O00OOOO00O000OOOO ['CM_HD2_DischPrs']-O00OOOO00O000OOOO ['CM_HD2_InPrsAlrmCtrl']>30 )and O00OOOO00O000OOOO ['CM_HD2_IGVPosCtrl']>5 :#line:2601
            OO0OOO00OO0OO0O00 ['HD2']=1 #line:2602
        else :#line:2603
            OO0OOO00OO0OO0O00 ['HD2']=0 #line:2604
        if O00OOOO00O000OOOO ['CM_LNGSubClr_CoolDownMode']==1 and O00OOOO00O000OOOO ['CM_LNGSubClr_Run']==1 :#line:2606
            OO0OOO00OO0OO0O00 ['SC']=1 #line:2607
        else :#line:2608
            OO0OOO00OO0OO0O00 ['SC']=0 #line:2609
        if O00OOOO00O000OOOO ['CM_GwHtr1_Run']==1 or O00OOOO00O000OOOO ['CM_GwHtr2_Run']==1 or O00OOOO00O000OOOO ['CM_GwHtr3_Run']==1 or O00OOOO00O000OOOO ['CM_GwHtr4_Run']==1 :#line:2633
            OO0OOO00OO0OO0O00 ['GWH_Elec']=1 #line:2634
        else :#line:2635
            OO0OOO00OO0OO0O00 ['GWH_Elec']=0 #line:2636
        if O00OOOO00O000OOOO ['CM_GwCircPp1_Run']==1 :#line:2638
            OO0OOO00OO0OO0O00 ['GWH_StmPP']=1 #line:2639
        else :#line:2640
            OO0OOO00OO0OO0O00 ['GWH_StmPP']=0 #line:2641
        if O00OOOO00O000OOOO ['CM_GwCircPp2_Run']==1 :#line:2643
            OO0OOO00OO0OO0O00 ['GWH_ElecPP']=1 #line:2644
        else :#line:2645
            OO0OOO00OO0OO0O00 ['GWH_ElecPP']=0 #line:2646
        if OO0OOO00OO0OO0O00 ['LNGV']==1 or OO0OOO00OO0OO0O00 ['WUH']==1 :#line:2650
            OO0OOO00OO0OO0O00 ['Cargo_vapor']=1 #line:2651
        else :#line:2652
            OO0OOO00OO0OO0O00 ['Cargo_vapor']=0 #line:2653
        if OO0OOO00OO0OO0O00 ['HD1']==1 or OO0OOO00OO0OO0O00 ['HD2']==1 :#line:2655
            OO0OOO00OO0OO0O00 ['HD']=1 #line:2656
        else :#line:2657
            OO0OOO00OO0OO0O00 ['HD']=0 #line:2658
        if OO0OOO00OO0OO0O00 ['FV']==1 or OO0OOO00OO0OO0O00 ['BOGH']==1 :#line:2660
            OO0OOO00OO0OO0O00 ['FBOG']=1 #line:2661
        else :#line:2662
            OO0OOO00OO0OO0O00 ['FBOG']=0 #line:2663
        if OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 :#line:2665
            OO0OOO00OO0OO0O00 ['NBOG']=1 #line:2666
        else :#line:2667
            OO0OOO00OO0OO0O00 ['NBOG']=0 #line:2668
        OO0OOO00OO0OO0O00 ['Fuel_Consumption']=1 #line:2670
        if O000OOO00OOO00OO0 ['NS_GPS_019_PV']==1 :#line:2672
            if O00OOOO00O000OOOO ['NS_GPS_019_PV']>1 :#line:2673
                OO0OOO00OO0OO0O00 ['Fuel_Economy']=1 #line:2674
            else :#line:2675
                OO0OOO00OO0OO0O00 ['Fuel_Economy']=0 #line:2676
        else :#line:2677
            OO0OOO00OO0OO0O00 ['Fuel_Economy']=0 #line:2678
        if OO0OOO00OO0OO0O00 ['GWH_Stm']==1 or OO0OOO00OO0OO0O00 ['GWH_Elec']==1 :#line:2680
            OO0OOO00OO0OO0O00 ['GWH']=1 #line:2681
            OO0OOO00OO0OO0O00 ['GWH_ExpTank']=1 #line:2682
        else :#line:2683
            OO0OOO00OO0OO0O00 ['GWH']=0 #line:2684
            OO0OOO00OO0OO0O00 ['GWH_ExpTank']=0 #line:2685
        if O000OOO00OOO00OO0 ['NS_IG-00531_PV']==1 :#line:2688
            if O00OOOO00O000OOOO ['FG_IG_SystemRun']==1 and O00OOOO00O000OOOO ['NS_IG-00531_PV']==1 :#line:2689
                OO0OOO00OO0OO0O00 ['IG']=1 #line:2690
            else :#line:2691
                OO0OOO00OO0OO0O00 ['IG']=0 #line:2692
        else :#line:2693
            if O00OOOO00O000OOOO ['FG_IG_SystemRun']==1 :#line:2694
                OO0OOO00OO0OO0O00 ['IG']=1 #line:2695
            else :#line:2696
                OO0OOO00OO0OO0O00 ['IG']=0 #line:2697
        if O00OOOO00O000OOOO ['Elec_NGen1_SystemRun']==1 :#line:2701
            OO0OOO00OO0OO0O00 ['NG1']=1 #line:2702
        else :#line:2703
            OO0OOO00OO0OO0O00 ['NG1']=0 #line:2704
        if O00OOOO00O000OOOO ['Elec_NGen2_SystemRun']==1 :#line:2705
            OO0OOO00OO0OO0O00 ['NG2']=1 #line:2706
        else :#line:2707
            OO0OOO00OO0OO0O00 ['NG2']=0 #line:2708
        if O00OOOO00O000OOOO ['ME1_FG_Flow_InstMass']>100 or O00OOOO00O000OOOO ['ME1_FO_Flow_InstMass']>100 :#line:2714
            OO0OOO00OO0OO0O00 ['ME1']=1 #line:2715
        else :#line:2716
            OO0OOO00OO0OO0O00 ['ME1']=0 #line:2717
        if O00OOOO00O000OOOO ['ME2_FG_Flow_InstMass']>100 or O00OOOO00O000OOOO ['ME2_FO_Flow_InstMass']>100 :#line:2719
            OO0OOO00OO0OO0O00 ['ME2']=1 #line:2720
        else :#line:2721
            OO0OOO00OO0OO0O00 ['ME2']=0 #line:2722
        if OO0OOO00OO0OO0O00 ['ME1']==1 :#line:2723
            OO0OOO00OO0OO0O00 ['MEEG_ECO1']=1 #line:2724
        else :#line:2725
            OO0OOO00OO0OO0O00 ['MEEG_ECO1']=0 #line:2726
        if OO0OOO00OO0OO0O00 ['ME2']==1 :#line:2727
            OO0OOO00OO0OO0O00 ['MEEG_ECO2']=1 #line:2728
        else :#line:2729
            OO0OOO00OO0OO0O00 ['MEEG_ECO2']=0 #line:2730
        if O00OOOO00O000OOOO ['GE1_Misc_Run']==1 :#line:2731
            OO0OOO00OO0OO0O00 ['GE1']=1 #line:2732
        else :#line:2733
            OO0OOO00OO0OO0O00 ['GE1']=0 #line:2734
        if O00OOOO00O000OOOO ['GE2_Misc_Run']==1 :#line:2735
            OO0OOO00OO0OO0O00 ['GE2']=1 #line:2736
        else :#line:2737
            OO0OOO00OO0OO0O00 ['GE2']=0 #line:2738
        if O00OOOO00O000OOOO ['GE3_Misc_Run']==1 :#line:2739
            OO0OOO00OO0OO0O00 ['GE3']=1 #line:2740
        else :#line:2741
            OO0OOO00OO0OO0O00 ['GE3']=0 #line:2742
        if O00OOOO00O000OOOO ['GE4_Misc_Run']==1 :#line:2743
            OO0OOO00OO0OO0O00 ['GE4']=1 #line:2744
        else :#line:2745
            OO0OOO00OO0OO0O00 ['GE4']=0 #line:2746
        if OO0OOO00OO0OO0O00 ['GE1']==1 or OO0OOO00OO0OO0O00 ['GE2']==1 :#line:2747
            OO0OOO00OO0OO0O00 ['GEEG_ECO1']=1 #line:2748
        else :#line:2749
            OO0OOO00OO0OO0O00 ['GEEG_ECO1']=0 #line:2750
        if OO0OOO00OO0OO0O00 ['GE3']==1 or OO0OOO00OO0OO0O00 ['GE4']==1 :#line:2751
            OO0OOO00OO0OO0O00 ['GEEG_ECO4']=1 #line:2752
        else :#line:2753
            OO0OOO00OO0OO0O00 ['GEEG_ECO4']=0 #line:2754
        if OO0OOO00OO0OO0O00 ['ME1']==1 or OO0OOO00OO0OO0O00 ['ME2']==1 :#line:2755
            OO0OOO00OO0OO0O00 ['MEEG']=1 #line:2756
        else :#line:2757
            OO0OOO00OO0OO0O00 ['MEEG']=0 #line:2758
        if OO0OOO00OO0OO0O00 ['GE1']==1 or OO0OOO00OO0OO0O00 ['GE2']==1 or OO0OOO00OO0OO0O00 ['GE3']==1 or OO0OOO00OO0OO0O00 ['GE4']==1 :#line:2759
            OO0OOO00OO0OO0O00 ['GEEG']=1 #line:2760
        else :#line:2761
            OO0OOO00OO0OO0O00 ['GEEG']=0 #line:2762
        if O000OOO00OOO00OO0 ['NS_MM048-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM648-XI_PV']==1 :#line:2782
            if O00OOOO00O000OOOO ['NS_MM048-XI_PV']==1 :#line:2783
                OO0OOO00OO0OO0O00 ['AB_AB1']=1 #line:2784
            else :#line:2785
                OO0OOO00OO0OO0O00 ['AB_AB1']=0 #line:2786
            if O00OOOO00O000OOOO ['NS_MM648-XI_PV']==1 :#line:2787
                OO0OOO00OO0OO0O00 ['AB_AB2']=1 #line:2788
            else :#line:2789
                OO0OOO00OO0OO0O00 ['AB_AB2']=0 #line:2790
        else :#line:2791
            if O00OOOO00O000OOOO ['Blr_AuxBlr1_Run']==1 and O00OOOO00O000OOOO ['Blr_AuxBlr_FO_Flow_InstMass']>5 :#line:2793
                OO0OOO00OO0OO0O00 ['AB_AB1']=1 #line:2794
            else :#line:2795
                OO0OOO00OO0OO0O00 ['AB_AB1']=0 #line:2796
            if O00OOOO00O000OOOO ['Blr_AuxBlr2_Run']==1 and O00OOOO00O000OOOO ['Blr_AuxBlr_FO_Flow_InstMass']>5 :#line:2798
                OO0OOO00OO0OO0O00 ['AB_AB2']=1 #line:2799
            else :#line:2800
                OO0OOO00OO0OO0O00 ['AB_AB2']=0 #line:2801
        if OO0OOO00OO0OO0O00 ['AB_AB1']==1 or OO0OOO00OO0OO0O00 ['AB_AB2']==1 :#line:2803
            OO0OOO00OO0OO0O00 ['AB']=1 #line:2804
        else :#line:2806
            OO0OOO00OO0OO0O00 ['AB']=0 #line:2807
        if O000OOO00OOO00OO0 ['NS_MM018-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM618-XI_PV']==1 :#line:2810
            if O00OOOO00O000OOOO ['NS_MM018-XI_PV']==1 :#line:2811
                OO0OOO00OO0OO0O00 ['LO_PuriME1']=1 #line:2812
            else :#line:2813
                OO0OOO00OO0OO0O00 ['LO_PuriME1']=0 #line:2814
            if O00OOOO00O000OOOO ['NS_MM618-XI_PV']==1 :#line:2815
                OO0OOO00OO0OO0O00 ['LO_PuriME2']=1 #line:2816
            else :#line:2817
                OO0OOO00OO0OO0O00 ['LO_PuriME2']=0 #line:2818
        else :#line:2819
            if O00OOOO00O000OOOO ['ME1_LO_Puri1_InTemp']>78 :#line:2820
                OO0OOO00OO0OO0O00 ['LO_PuriME1']=1 #line:2821
            else :#line:2822
                OO0OOO00OO0OO0O00 ['LO_PuriME1']=0 #line:2823
            if O00OOOO00O000OOOO ['ME2_LO_Puri1_InTemp']>78 :#line:2824
                OO0OOO00OO0OO0O00 ['LO_PuriME2']=1 #line:2825
            else :#line:2826
                OO0OOO00OO0OO0O00 ['LO_PuriME2']=0 #line:2827
        if O000OOO00OOO00OO0 ['NS_MM023-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM021-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM623-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM621-XI_PV']==1 :#line:2829
            if O00OOOO00O000OOOO ['NS_MM021-XI_PV']==1 :#line:2830
                OO0OOO00OO0OO0O00 ['LO_PuriGE1']=1 #line:2831
            else :#line:2832
                OO0OOO00OO0OO0O00 ['LO_PuriGE1']=0 #line:2833
            if O00OOOO00O000OOOO ['NS_MM023-XI_PV']==1 :#line:2834
                OO0OOO00OO0OO0O00 ['LO_PuriGE2']=1 #line:2835
            else :#line:2836
                OO0OOO00OO0OO0O00 ['LO_PuriGE2']=0 #line:2837
            if O00OOOO00O000OOOO ['NS_MM621-XI_PV']==1 :#line:2838
                OO0OOO00OO0OO0O00 ['LO_PuriGE3']=1 #line:2839
            else :#line:2840
                OO0OOO00OO0OO0O00 ['LO_PuriGE3']=0 #line:2841
            if O00OOOO00O000OOOO ['NS_MM623-XI_PV']==1 :#line:2842
                OO0OOO00OO0OO0O00 ['LO_PuriGE4']=1 #line:2843
            else :#line:2844
                OO0OOO00OO0OO0O00 ['LO_PuriGE4']=0 #line:2845
        else :#line:2846
            if O00OOOO00O000OOOO ['GE_LO_GE1GE2_Puri_InTemp']>83 or O00OOOO00O000OOOO ['GE_LO_GE1GE2_Puri2_InTemp']>83 :#line:2847
                OO0OOO00OO0OO0O00 ['LO_PuriGE1']=1 #line:2848
                OO0OOO00OO0OO0O00 ['LO_PuriGE2']=1 #line:2849
            else :#line:2850
                OO0OOO00OO0OO0O00 ['LO_PuriGE1']=0 #line:2851
                OO0OOO00OO0OO0O00 ['LO_PuriGE2']=0 #line:2852
            if O00OOOO00O000OOOO ['GE_LO_GE3GE4_Puri_InTemp']>83 or O00OOOO00O000OOOO ['GE_LO_GE3GE4_Puri2_InTemp']>83 :#line:2853
                OO0OOO00OO0OO0O00 ['LO_PuriGE3']=1 #line:2854
                OO0OOO00OO0OO0O00 ['LO_PuriGE4']=1 #line:2855
            else :#line:2856
                OO0OOO00OO0OO0O00 ['LO_PuriGE3']=0 #line:2857
                OO0OOO00OO0OO0O00 ['LO_PuriGE4']=0 #line:2858
        if O000OOO00OOO00OO0 ['NS_PP004-03MI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP043-03MI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP009-03MI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP044-03MI_PV']==1 :#line:2860
            if O00OOOO00O000OOOO ['NS_PP004-03MI_PV']==1 or O00OOOO00O000OOOO ['NS_PP043-03MI_PV']==1 :#line:2861
                OO0OOO00OO0OO0O00 ['LO_StrnTube1']=1 #line:2862
            else :#line:2863
                OO0OOO00OO0OO0O00 ['LO_StrnTube1']=0 #line:2864
            if O00OOOO00O000OOOO ['NS_PP009-03MI_PV']==1 or O00OOOO00O000OOOO ['NS_PP044-03MI_PV']==1 :#line:2865
                OO0OOO00OO0OO0O00 ['LO_StrnTube2']=1 #line:2866
            else :#line:2867
                OO0OOO00OO0OO0O00 ['LO_StrnTube2']=0 #line:2868
        else :#line:2869
            if OO0OOO00OO0OO0O00 ['ME1']==1 or OO0OOO00OO0OO0O00 ['ME2']==1 :#line:2870
                OO0OOO00OO0OO0O00 ['LO_StrnTube1']=1 #line:2871
                OO0OOO00OO0OO0O00 ['LO_StrnTube2']=1 #line:2872
            else :#line:2873
                OO0OOO00OO0OO0O00 ['LO_StrnTube1']=0 #line:2874
                OO0OOO00OO0OO0O00 ['LO_StrnTube2']=0 #line:2875
        OO0OOO00OO0OO0O00 ['VA']=1 #line:2877
        if O000OOO00OOO00OO0 ['NS_PP036-03XI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP037-03AXI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP038-03AXI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP038-03XC_PV']==1 :#line:2879
            if O00OOOO00O000OOOO ['NS_PP036-03XI_PV']==1 :#line:2880
                OO0OOO00OO0OO0O00 ['BLST_PP1']=1 #line:2881
            else :#line:2882
                OO0OOO00OO0OO0O00 ['BLST_PP1']=0 #line:2883
            if O00OOOO00O000OOOO ['NS_PP037-03AXI_PV']==1 :#line:2884
                OO0OOO00OO0OO0O00 ['BLST_PP2']=1 #line:2885
            else :#line:2886
                OO0OOO00OO0OO0O00 ['BLST_PP2']=0 #line:2887
            if O00OOOO00O000OOOO ['NS_PP038-03AXI_PV']==1 or O00OOOO00O000OOOO ['NS_PP038-03XC_PV']==1 :#line:2888
                OO0OOO00OO0OO0O00 ['BLST_PP3']=1 #line:2889
            else :#line:2890
                OO0OOO00OO0OO0O00 ['BLST_PP3']=0 #line:2891
        else :#line:2893
            OO0OOO00OO0OO0O00 ['BLST_PP1']=1 #line:2894
            OO0OOO00OO0OO0O00 ['BLST_PP2']=1 #line:2895
            OO0OOO00OO0OO0O00 ['BLST_PP3']=1 #line:2896
        OO0OOO00OO0OO0O00 ['BLST']=1 #line:2898
        OO0OOO00OO0OO0O00 ['BLG']=1 #line:2899
        OO0OOO00OO0OO0O00 ['CT1']=1 #line:2900
        OO0OOO00OO0OO0O00 ['CT2']=1 #line:2901
        OO0OOO00OO0OO0O00 ['CT3']=1 #line:2902
        OO0OOO00OO0OO0O00 ['CT4']=1 #line:2903
        if OO0OOO00OO0OO0O00 ['ME1']==1 :#line:2905
            OO0OOO00OO0OO0O00 ['FW_ME1SAC']=1 #line:2906
        else :#line:2907
            OO0OOO00OO0OO0O00 ['FW_ME1SAC']=0 #line:2908
        if OO0OOO00OO0OO0O00 ['ME2']==1 :#line:2909
            OO0OOO00OO0OO0O00 ['FW_ME2SAC']=1 #line:2910
        else :#line:2911
            OO0OOO00OO0OO0O00 ['FW_ME2SAC']=0 #line:2912
        if OO0OOO00OO0OO0O00 ['GE1']==1 :#line:2913
            OO0OOO00OO0OO0O00 ['FW_GE1SAC']=1 #line:2914
        else :#line:2915
            OO0OOO00OO0OO0O00 ['FW_GE1SAC']=0 #line:2916
        if OO0OOO00OO0OO0O00 ['GE2']==1 :#line:2917
            OO0OOO00OO0OO0O00 ['FW_GE2SAC']=1 #line:2918
        else :#line:2919
            OO0OOO00OO0OO0O00 ['FW_GE2SAC']=0 #line:2920
        if OO0OOO00OO0OO0O00 ['GE3']==1 :#line:2921
            OO0OOO00OO0OO0O00 ['FW_GE3SAC']=1 #line:2922
        else :#line:2923
            OO0OOO00OO0OO0O00 ['FW_GE3SAC']=0 #line:2924
        if OO0OOO00OO0OO0O00 ['GE4']==1 :#line:2925
            OO0OOO00OO0OO0O00 ['FW_GE4SAC']=1 #line:2926
        else :#line:2927
            OO0OOO00OO0OO0O00 ['FW_GE4SAC']=0 #line:2928
        if O000OOO00OOO00OO0 ['NS_PP040-03MI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP045-03MI_PV']==1 and O000OOO00OOO00OO0 ['NS_PP046-03MI_PV']==1 :#line:2930
            if O00OOOO00O000OOOO ['NS_PP040-03MI_PV']==1 :#line:2931
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP1']=1 #line:2932
            else :#line:2933
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP1']=0 #line:2934
            if O00OOOO00O000OOOO ['NS_PP045-03MI_PV']==1 :#line:2935
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP2']=1 #line:2936
            else :#line:2937
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP2']=0 #line:2938
            if O00OOOO00O000OOOO ['NS_PP046-03MI_PV']==1 :#line:2939
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP3']=1 #line:2940
            else :#line:2941
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP3']=0 #line:2942
        else :#line:2943
            if OO0OOO00OO0OO0O00 ['GE1']==1 or OO0OOO00OO0OO0O00 ['GE2']==1 or OO0OOO00OO0OO0O00 ['GE3']==1 or OO0OOO00OO0OO0O00 ['GE4']==1 :#line:2944
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP1']=1 #line:2945
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP2']=1 #line:2946
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP3']=1 #line:2947
            else :#line:2948
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP1']=0 #line:2949
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP2']=0 #line:2950
                OO0OOO00OO0OO0O00 ['FW_GEwtrCircPP3']=0 #line:2951
        if O00OOOO00O000OOOO ['Mach_CfwPp1_Run']==1 :#line:2953
            OO0OOO00OO0OO0O00 ['FW_CentralPP1']=1 #line:2954
        else :#line:2955
            OO0OOO00OO0OO0O00 ['FW_CentralPP1']=0 #line:2956
        if O00OOOO00O000OOOO ['Mach_CfwPp2_Run']==1 :#line:2957
            OO0OOO00OO0OO0O00 ['FW_CentralPP2']=1 #line:2958
        else :#line:2959
            OO0OOO00OO0OO0O00 ['FW_CentralPP2']=0 #line:2960
        if O00OOOO00O000OOOO ['Mach_CfwPp3_Run']==1 :#line:2961
            OO0OOO00OO0OO0O00 ['FW_CentralPP3']=1 #line:2962
        else :#line:2963
            OO0OOO00OO0OO0O00 ['FW_CentralPP3']=0 #line:2964
        OO0OOO00OO0OO0O00 ['FW_BoosterPP']=1 #line:2986
        if OO0OOO00OO0OO0O00 ['ME1']==1 :#line:2988
            OO0OOO00OO0OO0O00 ['FW_ME1CFWPP1']=1 #line:2989
            OO0OOO00OO0OO0O00 ['FW_ME1CFWPP2']=1 #line:2990
        else :#line:2991
            OO0OOO00OO0OO0O00 ['FW_ME1CFWPP1']=0 #line:2992
            OO0OOO00OO0OO0O00 ['FW_ME1CFWPP2']=0 #line:2993
        if OO0OOO00OO0OO0O00 ['ME2']==1 :#line:2995
            OO0OOO00OO0OO0O00 ['FW_ME2CFWPP1']=1 #line:2996
            OO0OOO00OO0OO0O00 ['FW_ME2CFWPP2']=1 #line:2997
        else :#line:2998
            OO0OOO00OO0OO0O00 ['FW_ME2CFWPP1']=0 #line:2999
            OO0OOO00OO0OO0O00 ['FW_ME2CFWPP2']=0 #line:3000
        if O00OOOO00O000OOOO ['Mach_CswPp1_Run']==1 :#line:3002
            OO0OOO00OO0OO0O00 ['FW_CSWPP1']=1 #line:3003
        else :#line:3004
            OO0OOO00OO0OO0O00 ['FW_CSWPP1']=0 #line:3005
        if O00OOOO00O000OOOO ['Mach_CswPp2_Run']==1 :#line:3006
            OO0OOO00OO0OO0O00 ['FW_CSWPP2']=1 #line:3007
        else :#line:3008
            OO0OOO00OO0OO0O00 ['FW_CSWPP2']=0 #line:3009
        if O00OOOO00O000OOOO ['Mach_CswPp3_Run']==1 :#line:3010
            OO0OOO00OO0OO0O00 ['FW_CSWPP3']=1 #line:3011
        else :#line:3012
            OO0OOO00OO0OO0O00 ['FW_CSWPP3']=0 #line:3013
        if O00OOOO00O000OOOO ['ME1_FO_Flow_InstMass']>30 or O00OOOO00O000OOOO ['ME2_FO_Flow_InstMass']>30 or O00OOOO00O000OOOO ['GE_FO_GE1GE2_Flow_InstMass']>30 or O00OOOO00O000OOOO ['GE_FO_GE3GE4_Flow_InstMass']>30 or O00OOOO00O000OOOO ['Blr_AuxBlr_FO_Flow_InstMass']>10 :#line:3021
            OO0OOO00OO0OO0O00 ['FO']=1 #line:3022
        else :#line:3023
            OO0OOO00OO0OO0O00 ['FO']=0 #line:3024
        if (O00OOOO00O000OOOO ['Mach_HFOPuri1_Run']==1 and O00OOOO00O000OOOO ['Mach_HFOPuri1_InTemp']>50 )or (O00OOOO00O000OOOO ['Mach_HFOPuri2_Run']==1 and O00OOOO00O000OOOO ['Mach_HFOPuri2_InTemp']>50 ):#line:3026
            OO0OOO00OO0OO0O00 ['FO_Puri']=1 #line:3027
        else :#line:3028
            OO0OOO00OO0OO0O00 ['FO_Puri']=0 #line:3029
        if O000OOO00OOO00OO0 ['NS_MM944-XI_PV']==1 :#line:3031
            if O00OOOO00O000OOOO ['NS_MM944-XI_PV']==1 :#line:3032
                OO0OOO00OO0OO0O00 ['INCIN']=1 #line:3033
            else :#line:3034
                OO0OOO00OO0OO0O00 ['INCIN']=0 #line:3035
        else :#line:3036
            OO0OOO00OO0OO0O00 ['INCIN']=0 #line:3037
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['ME1']==1 :#line:3040
            OO0OOO00OO0OO0O00 ['MEFG_ME1']=1 #line:3041
        else :#line:3042
            OO0OOO00OO0OO0O00 ['MEFG_ME1']=0 #line:3043
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['ME2']==1 :#line:3046
            OO0OOO00OO0OO0O00 ['MEFG_ME2']=1 #line:3047
        else :#line:3048
            OO0OOO00OO0OO0O00 ['MEFG_ME2']=0 #line:3049
        if OO0OOO00OO0OO0O00 ['MEFG_ME1']==1 or OO0OOO00OO0OO0O00 ['MEFG_ME2']==1 :#line:3051
            OO0OOO00OO0OO0O00 ['MEFG']=1 #line:3052
        else :#line:3053
            OO0OOO00OO0OO0O00 ['MEFG']=0 #line:3054
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['GE1']==1 :#line:3057
            OO0OOO00OO0OO0O00 ['GEFG_GE1']=1 #line:3058
        else :#line:3059
            OO0OOO00OO0OO0O00 ['GEFG_GE1']=0 #line:3060
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['GE2']==1 :#line:3063
            OO0OOO00OO0OO0O00 ['GEFG_GE2']=1 #line:3064
        else :#line:3065
            OO0OOO00OO0OO0O00 ['GEFG_GE2']=0 #line:3066
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['GE3']==1 :#line:3069
            OO0OOO00OO0OO0O00 ['GEFG_GE3']=1 #line:3070
        else :#line:3071
            OO0OOO00OO0OO0O00 ['GEFG_GE3']=0 #line:3072
        if (OO0OOO00OO0OO0O00 ['LD1']==1 or OO0OOO00OO0OO0O00 ['LD2']==1 )and OO0OOO00OO0OO0O00 ['GE4']==1 :#line:3075
            OO0OOO00OO0OO0O00 ['GEFG_GE4']=1 #line:3076
        else :#line:3077
            OO0OOO00OO0OO0O00 ['GEFG_GE4']=0 #line:3078
        if O000OOO00OOO00OO0 ['NS_MF001-03MI_PV']==1 :#line:3080
            if O00OOOO00O000OOOO ['NS_MF001-03MI_PV']==1 :#line:3081
                OO0OOO00OO0OO0O00 ['GEFG_Fan1']=1 #line:3082
            else :#line:3083
                OO0OOO00OO0OO0O00 ['GEFG_Fan1']=0 #line:3084
        else :#line:3085
            OO0OOO00OO0OO0O00 ['GEFG_Fan1']=0 #line:3086
        if O000OOO00OOO00OO0 ['NS_MF010-03MI_PV']==1 :#line:3088
            if O00OOOO00O000OOOO ['NS_MF010-03MI_PV']==1 :#line:3089
                OO0OOO00OO0OO0O00 ['GEFG_Fan2']=1 #line:3090
            else :#line:3091
                OO0OOO00OO0OO0O00 ['GEFG_Fan2']=0 #line:3092
        else :#line:3093
            OO0OOO00OO0OO0O00 ['GEFG_Fan2']=0 #line:3094
        if OO0OOO00OO0OO0O00 ['GEFG_GE1']==1 or OO0OOO00OO0OO0O00 ['GEFG_GE2']or OO0OOO00OO0OO0O00 ['GEFG_GE3']or OO0OOO00OO0OO0O00 ['GEFG_GE4']:#line:3096
            OO0OOO00OO0OO0O00 ['GEFG']=1 #line:3097
        else :#line:3098
            OO0OOO00OO0OO0O00 ['GEFG']=0 #line:3099
        if O00OOOO00O000OOOO ['FG_GCU1_Run']==1 :#line:3101
            OO0OOO00OO0OO0O00 ['GCU']=1 #line:3102
        else :#line:3103
            OO0OOO00OO0OO0O00 ['GCU']=0 #line:3104
        if OO0OOO00OO0OO0O00 ['GE1']==1 :#line:3108
            OO0OOO00OO0OO0O00 ['GEEG_SCR1']=1 #line:3109
        else :#line:3110
            OO0OOO00OO0OO0O00 ['GEEG_SCR1']=0 #line:3111
        if OO0OOO00OO0OO0O00 ['GE2']==1 :#line:3113
            OO0OOO00OO0OO0O00 ['GEEG_SCR2']=1 #line:3114
        else :#line:3115
            OO0OOO00OO0OO0O00 ['GEEG_SCR2']=0 #line:3116
        if OO0OOO00OO0OO0O00 ['GE3']==1 :#line:3118
            OO0OOO00OO0OO0O00 ['GEEG_SCR3']=1 #line:3119
        else :#line:3120
            OO0OOO00OO0OO0O00 ['GEEG_SCR3']=0 #line:3121
        if OO0OOO00OO0OO0O00 ['GE4']==1 :#line:3123
            OO0OOO00OO0OO0O00 ['GEEG_SCR4']=1 #line:3124
        else :#line:3125
            OO0OOO00OO0OO0O00 ['GEEG_SCR4']=0 #line:3126
        if O000OOO00OOO00OO0 ['NS_MM002-XI_PV']==1 :#line:3142
            if O00OOOO00O000OOOO ['NS_MM002-XI_PV']==1 :#line:3143
                OO0OOO00OO0OO0O00 ['FW_Gen1']=1 #line:3144
            else :#line:3145
                OO0OOO00OO0OO0O00 ['FW_Gen1']=0 #line:3146
        else :#line:3147
            OO0OOO00OO0OO0O00 ['FW_Gen1']=1 #line:3148
        if O000OOO00OOO00OO0 ['NS_MM602-XI_PV']==1 :#line:3150
            if O00OOOO00O000OOOO ['NS_MM602-XI_PV']==1 :#line:3151
                OO0OOO00OO0OO0O00 ['FW_Gen2']=1 #line:3152
            else :#line:3153
                OO0OOO00OO0OO0O00 ['FW_Gen2']=0 #line:3154
        else :#line:3155
            OO0OOO00OO0OO0O00 ['FW_Gen2']=1 #line:3156
        if O000OOO00OOO00OO0 ['NS_MM933-XI_PV']==1 :#line:3158
            if O00OOOO00O000OOOO ['NS_MM933-XI_PV']==1 :#line:3159
                OO0OOO00OO0OO0O00 ['FW_VFD_hydro_unit']=1 #line:3160
            else :#line:3161
                OO0OOO00OO0OO0O00 ['FW_VFD_hydro_unit']=0 #line:3162
        else :#line:3163
            OO0OOO00OO0OO0O00 ['FW_VFD_hydro_unit']=1 #line:3164
        if O000OOO00OOO00OO0 ['NS_MM908-03XI_PV']==1 :#line:3166
            if O00OOOO00O000OOOO ['NS_MM908-03XI_PV']==1 :#line:3167
                OO0OOO00OO0OO0O00 ['FW_Hot_water_pp']=1 #line:3168
            else :#line:3169
                OO0OOO00OO0OO0O00 ['FW_Hot_water_pp']=0 #line:3170
        else :#line:3171
            OO0OOO00OO0OO0O00 ['FW_Hot_water_pp']=1 #line:3172
        if O000OOO00OOO00OO0 ['NS_MM066-XI_PV']==1 and O000OOO00OOO00OO0 ['NS_MM666-XI_PV']==1 :#line:3174
            if O00OOOO00O000OOOO ['NS_MM066-XI_PV']==1 and O00OOOO00O000OOOO ['NS_MM666-XI_PV']==1 :#line:3175
                OO0OOO00OO0OO0O00 ['FW_Ref']=1 #line:3176
            else :#line:3177
                OO0OOO00OO0OO0O00 ['FW_Ref']=0 #line:3178
        else :#line:3179
            OO0OOO00OO0OO0O00 ['FW_Ref']=1 #line:3180
        if O000OOO00OOO00OO0 ['NS_CF013-03MC_PV']==1 :#line:3183
            if O00OOOO00O000OOOO ['NS_CF013-03MC_PV']==1 :#line:3184
                OO0OOO00OO0OO0O00 ['FW_CFW_PP1']=1 #line:3185
            else :#line:3186
                OO0OOO00OO0OO0O00 ['FW_CFW_PP1']=0 #line:3187
        else :#line:3188
            OO0OOO00OO0OO0O00 ['FW_CFW_PP1']=1 #line:3189
        if O000OOO00OOO00OO0 ['NS_CF014-03MC_PV']==1 :#line:3191
            if O00OOOO00O000OOOO ['NS_CF014-03MC_PV']==1 :#line:3192
                OO0OOO00OO0OO0O00 ['FW_CFW_PP2']=1 #line:3193
            else :#line:3194
                OO0OOO00OO0OO0O00 ['FW_CFW_PP2']=0 #line:3195
        else :#line:3196
            OO0OOO00OO0OO0O00 ['FW_CFW_PP2']=1 #line:3197
        if OO0OOO00OO0OO0O00 ['ME1']==1 :#line:3199
            OO0OOO00OO0OO0O00 ['FW_ME1bearings']=1 #line:3200
        else :#line:3201
            OO0OOO00OO0OO0O00 ['FW_ME1bearings']=0 #line:3202
        if OO0OOO00OO0OO0O00 ['ME2']==1 :#line:3204
            OO0OOO00OO0OO0O00 ['FW_ME2bearings']=1 #line:3205
        else :#line:3206
            OO0OOO00OO0OO0O00 ['FW_ME2bearings']=0 #line:3207
        if OO0OOO00OO0OO0O00 ['LO_PuriME1']==1 or OO0OOO00OO0OO0O00 ['LO_PuriME2']==1 or OO0OOO00OO0OO0O00 ['LO_PuriGE1']==1 or OO0OOO00OO0OO0O00 ['LO_PuriGE2']==1 or OO0OOO00OO0OO0O00 ['LO_PuriGE3']==1 or OO0OOO00OO0OO0O00 ['LO_PuriGE4']==1 or OO0OOO00OO0OO0O00 ['LO_StrnTube1']==1 or OO0OOO00OO0OO0O00 ['LO_StrnTube2']==1 :#line:3209
            OO0OOO00OO0OO0O00 ['LO']=1 #line:3210
        else :#line:3211
            OO0OOO00OO0OO0O00 ['LO']=0 #line:3212
        OO0OOO00OO0OO0O00 ['FW']=0 #line:3214
        OOOOOOOOOO000000O =[]#line:3216
        for OOO0OO0000O0OOO00 in OO0OOO00OO0OO0O00 .keys ():#line:3217
            if OOO0OO0000O0OOO00 [:3 ]=='FW_':#line:3218
                OOOOOOOOOO000000O .append (OOO0OO0000O0OOO00 )#line:3219
        for O0OOOOOOO00000OO0 in OOOOOOOOOO000000O :#line:3221
            if OO0OOO00OO0OO0O00 [O0OOOOOOO00000OO0 ]==1 :#line:3222
                OO0OOO00OO0OO0O00 ['FW']=1 #line:3223
                break #line:3224
        if O0OO0O0O0OOOOO00O .test_run ==1 :#line:3228
            for OOO0OO0000O0OOO00 in OO0OOO00OO0OO0O00 .keys ():#line:3229
                OO0OOO00OO0OO0O00 [OOO0OO0000O0OOO00 ]=1 #line:3230
        return OO0OOO00OO0OO0O00 #line:3231
    def cloudDataLogging (OOO000000O00OOOO0 ):#line:3235
        OOO000000O00OOOO0 .cursor .execute ('''select "Value" from public."Application_status" where "Item" = 'Input_file';''')#line:3237
        OOOO000OO0OOOOOO0 =OOO000000O00OOOO0 .cursor .fetchall ()#line:3238
        OOO000000O00OOOO0 .conn .commit ()#line:3239
        OO00O0O0OOO0OOO0O =OOOO000OO0OOOOOO0 [0 ][0 ]#line:3240
        OO000O000O000OO00 =OO00O0O0OOO0OOO0O [-19 :-11 ]#line:3242
        OOOOOO00OO0O000O0 =OOO000000O00OOOO0 .simfiles_path +'/'+OO000O000O000OO00 #line:3252
        O00000O000O00OO00 =natsorted (os .listdir (OOOOOO00OO0O000O0 ))#line:3253
        for OO00OO0000OO00O00 in range (len (O00000O000O00OO00 )):#line:3257
            if O00000O000O00OO00 [OO00OO0000OO00O00 ]==OO00O0O0OOO0OOO0O :#line:3259
                print ("previously flagged file is:",OO00O0O0OOO0OOO0O )#line:3260
                if OO00OO0000OO00O00 ==(len (O00000O000O00OO00 )-1 ):#line:3261
                    print ('no more file available')#line:3263
                    O0O0O00OO00OOOOO0 =natsorted (os .listdir (OOO000000O00OOOO0 .simfiles_path ))#line:3270
                    for OO00O000000OOOO00 in range (len (O0O0O00OO00OOOOO0 )):#line:3271
                        if O0O0O00OO00OOOOO0 [OO00O000000OOOO00 ]==OO000O000O000OO00 :#line:3272
                            if OO00O000000OOOO00 ==(len (O0O0O00OO00OOOOO0 )-1 ):#line:3273
                                print ("no more folder is available")#line:3274
                                OOOO00000O0O0O000 ='Holding'#line:3275
                                print ("switch to:",OOOO00000O0O0O000 )#line:3276
                            else :#line:3277
                                OO000O000O000OO00 =O0O0O00OO00OOOOO0 [OO00O000000OOOO00 +1 ]#line:3278
                                print ('next day folder is:',OO000O000O000OO00 )#line:3279
                                OOOOOO00OO0O000O0 =OOO000000O00OOOO0 .simfiles_path +'/'+OO000O000O000OO00 #line:3280
                                O00000O000O00OO00 =natsorted (os .listdir (OOOOOO00OO0O000O0 ))#line:3281
                                if len (O00000O000O00OO00 )==0 :#line:3282
                                    print ("new folder is empty")#line:3283
                                    OOOO00000O0O0O000 ='Holding'#line:3284
                                    print ("switch to:",OOOO00000O0O0O000 )#line:3285
                                else :#line:3286
                                    OO00O0O0OOO0OOO0O =O00000O000O00OO00 [0 ]#line:3287
                                    print ("sim file in next day folder:",OO00O0O0OOO0OOO0O )#line:3288
                                    print ("next file to read is:",OO00O0O0OOO0OOO0O )#line:3289
                                    if len (O00000O000O00OO00 )>1 :#line:3293
                                        OOOO00000O0O0O000 ='Playback'#line:3294
                                        print ("switch to :",OOOO00000O0O0O000 )#line:3296
                                    else :#line:3297
                                        OOOO00000O0O0O000 ='Normal'#line:3298
                                        print ("switch to:",OOOO00000O0O0O000 )#line:3299
                                    break #line:3301
                else :#line:3304
                    OO00O0O0OOO0OOO0O =O00000O000O00OO00 [OO00OO0000OO00O00 +1 ]#line:3305
                    print ("next file to read is:",OO00O0O0OOO0OOO0O )#line:3306
                    OO00O000O0OO0O0O0 =len (O00000O000O00OO00 )-OO00OO0000OO00O00 #line:3307
                    if OO00O000O0OO0O0O0 >2 :#line:3310
                        OOOO00000O0O0O000 ='Playback'#line:3311
                        print ("switch to :",OOOO00000O0O0O000 )#line:3313
                    else :#line:3314
                        OOOO00000O0O0O000 ='Normal'#line:3315
                    break #line:3316
        if OOOO00000O0O0O000 =='Normal':#line:3318
            OOOO0OOOOO000O000 =60 #line:3319
        elif OOOO00000O0O0O000 =='Playback':#line:3320
            OOOO0OOOOO000O000 =0.01 #line:3321
        elif OOOO00000O0O0O000 =='Holding':#line:3322
            OOOO0OOOOO000O000 =5 #line:3323
        else :#line:3324
            OOOO0OOOOO000O000 =5 #line:3325
        OOO000000O00OOOO0 .cursor .execute (f'''update public."Application_status" set "Value" = %s where "Item" = 'Input_file';''',[OO00O0O0OOO0OOO0O ])#line:3328
        OOO000000O00OOOO0 .conn .commit ()#line:3329
        OOO000000O00OOOO0 .cursor .execute ('''update public."Application_status" set "Value" = %s where "Item" = 'Status';''',[OOOO00000O0O0O000 ])#line:3330
        OOO000000O00OOOO0 .conn .commit ()#line:3331
        OOO000000O00OOOO0 .cursor .execute ('''update public."Application_status" set "Value" = %s where "Item" = 'Frequency';''',[str (OOOO0OOOOO000O000 )])#line:3332
        OOO000000O00OOOO0 .conn .commit ()#line:3333
        if OOOO00000O0O0O000 =='Normal'or OOOO00000O0O0O000 =='Playback':#line:3336
            print ('proceeding with status:',OOOO00000O0O0O000 )#line:3337
            O0O000O0O00O0O00O =OOO000000O00OOOO0 .simfiles_path +'/'+OO000O000O000OO00 +'/'+OO00O0O0OOO0OOO0O #line:3338
            with open (O0O000O0O00O0O00O )as O0O0OOOO00O00O0OO :#line:3339
                O000OO00OOOO000OO =O0O0OOOO00O00O0OO .readlines ()#line:3340
            print ("len of lines:",len (O000OO00OOOO000OO ))#line:3341
            if len (O000OO00OOOO000OO )==2 :#line:3343
                O0OO000O00OOOOO00 =O000OO00OOOO000OO [0 ]#line:3344
                OO000OO0OO000OO0O =O000OO00OOOO000OO [1 ]#line:3345
                O0OOO0000O00O00O0 =O0OO000O00OOOOO00 .split (',')#line:3348
                OO00000O00OOOO0O0 =OO000OO0OO000OO0O .split (',')#line:3349
                O0O0O0OO0O0O0O00O =['names','sample1']#line:3352
                O0OO000OO0O00O0OO =[O0OOO0000O00O00O0 ,OO00000O00OOOO0O0 ]#line:3353
                if len (O0OOO0000O00O00O0 )==len (OO00000O00OOOO0O0 ):#line:3356
                    OO00OO0OO0O0O0O0O ={}#line:3357
                    for OO00OO0000OO00O00 in range (len (O0OOO0000O00O00O0 )):#line:3358
                        OO00OO0OO0O0O0O0O [O0OOO0000O00O00O0 [OO00OO0000OO00O00 ]]=[OO00000O00OOOO0O0 [OO00OO0000OO00O00 ]]#line:3359
                else :#line:3360
                    print ("tags and samples size not same")#line:3361
            elif len (O000OO00OOOO000OO )==3 :#line:3363
                O0OO000O00OOOOO00 =O000OO00OOOO000OO [0 ]#line:3364
                OO000OO0OO000OO0O =O000OO00OOOO000OO [1 ]#line:3365
                O0OO0OO0OO00O00OO =O000OO00OOOO000OO [2 ]#line:3366
                O0OOO0000O00O00O0 =O0OO000O00OOOOO00 .split (',')#line:3368
                OO00000O00OOOO0O0 =OO000OO0OO000OO0O .split (',')#line:3369
                O0OO0O00OOO00OO0O =O0OO0OO0OO00O00OO .split (',')#line:3370
                O0O0O0OO0O0O0O00O =['names','sample1','sample2']#line:3372
                O0OO000OO0O00O0OO =[O0OOO0000O00O00O0 ,OO00000O00OOOO0O0 ,O0OO0O00OOO00OO0O ]#line:3373
                if len (O0OOO0000O00O00O0 )==len (OO00000O00OOOO0O0 )==len (O0OO0O00OOO00OO0O ):#line:3376
                    OO00OO0OO0O0O0O0O ={}#line:3377
                    for OO00OO0000OO00O00 in range (len (O0OOO0000O00O00O0 )):#line:3378
                        OO00OO0OO0O0O0O0O [O0OOO0000O00O00O0 [OO00OO0000OO00O00 ]]=[OO00000O00OOOO0O0 [OO00OO0000OO00O00 ],O0OO0O00OOO00OO0O [OO00OO0000OO00O00 ]]#line:3379
                else :#line:3380
                    print ("tags and samples size not same")#line:3381
            elif len (O000OO00OOOO000OO )==4 :#line:3383
                O0OO000O00OOOOO00 =O000OO00OOOO000OO [0 ]#line:3384
                OO000OO0OO000OO0O =O000OO00OOOO000OO [1 ]#line:3385
                O0OO0OO0OO00O00OO =O000OO00OOOO000OO [2 ]#line:3386
                OOO0OOO0O000O0O00 =O000OO00OOOO000OO [3 ]#line:3387
                O0OOO0000O00O00O0 =O0OO000O00OOOOO00 .split (',')#line:3389
                OO00000O00OOOO0O0 =OO000OO0OO000OO0O .split (',')#line:3390
                O0OO0O00OOO00OO0O =O0OO0OO0OO00O00OO .split (',')#line:3391
                O00O0OO000OOO0OO0 =OOO0OOO0O000O0O00 .split (',')#line:3392
                O0O0O0OO0O0O0O00O =['names','sample1','sample2','sample3']#line:3394
                O0OO000OO0O00O0OO =[O0OOO0000O00O00O0 ,OO00000O00OOOO0O0 ,O0OO0O00OOO00OO0O ,O00O0OO000OOO0OO0 ]#line:3395
                if len (O0OOO0000O00O00O0 )==len (OO00000O00OOOO0O0 )==len (O0OO0O00OOO00OO0O )==len (O00O0OO000OOO0OO0 ):#line:3398
                    OO00OO0OO0O0O0O0O ={}#line:3399
                    for OO00OO0000OO00O00 in range (len (O0OOO0000O00O00O0 )):#line:3400
                        OO00OO0OO0O0O0O0O [O0OOO0000O00O00O0 [OO00OO0000OO00O00 ]]=[OO00000O00OOOO0O0 [OO00OO0000OO00O00 ],O0OO0O00OOO00OO0O [OO00OO0000OO00O00 ],O00O0OO000OOO0OO0 [OO00OO0000OO00O00 ]]#line:3401
                else :#line:3402
                    print ("tags and samples size not same")#line:3403
            elif len (O000OO00OOOO000OO )==5 :#line:3405
                O0OO000O00OOOOO00 =O000OO00OOOO000OO [0 ]#line:3406
                OO000OO0OO000OO0O =O000OO00OOOO000OO [1 ]#line:3407
                O0OO0OO0OO00O00OO =O000OO00OOOO000OO [2 ]#line:3408
                OOO0OOO0O000O0O00 =O000OO00OOOO000OO [3 ]#line:3409
                OO0OO000000O00O00 =O000OO00OOOO000OO [4 ]#line:3410
                O0OOO0000O00O00O0 =O0OO000O00OOOOO00 .split (',')#line:3412
                OO00000O00OOOO0O0 =OO000OO0OO000OO0O .split (',')#line:3413
                O0OO0O00OOO00OO0O =O0OO0OO0OO00O00OO .split (',')#line:3414
                O00O0OO000OOO0OO0 =OOO0OOO0O000O0O00 .split (',')#line:3415
                O0OOOO00OO0OOOOOO =OO0OO000000O00O00 .split (',')#line:3416
                O0O0O0OO0O0O0O00O =['names','sample1','sample2','sample3','sample4']#line:3418
                O0OO000OO0O00O0OO =[O0OOO0000O00O00O0 ,OO00000O00OOOO0O0 ,O0OO0O00OOO00OO0O ,O00O0OO000OOO0OO0 ,O0OOOO00OO0OOOOOO ]#line:3419
                if len (O0OOO0000O00O00O0 )==len (OO00000O00OOOO0O0 )==len (O0OO0O00OOO00OO0O )==len (O00O0OO000OOO0OO0 )==len (O0OOOO00OO0OOOOOO ):#line:3422
                    OO00OO0OO0O0O0O0O ={}#line:3423
                    for OO00OO0000OO00O00 in range (len (O0OOO0000O00O00O0 )):#line:3424
                        OO00OO0OO0O0O0O0O [O0OOO0000O00O00O0 [OO00OO0000OO00O00 ]]=[OO00000O00OOOO0O0 [OO00OO0000OO00O00 ],O0OO0O00OOO00OO0O [OO00OO0000OO00O00 ],O00O0OO000OOO0OO0 [OO00OO0000OO00O00 ],O0OOOO00OO0OOOOOO [OO00OO0000OO00O00 ]]#line:3425
                else :#line:3426
                    print ("tags and samples size not same")#line:3427
            elif len (O000OO00OOOO000OO )==6 :#line:3429
                O0OO000O00OOOOO00 =O000OO00OOOO000OO [0 ]#line:3430
                OO000OO0OO000OO0O =O000OO00OOOO000OO [1 ]#line:3431
                O0OO0OO0OO00O00OO =O000OO00OOOO000OO [2 ]#line:3432
                OOO0OOO0O000O0O00 =O000OO00OOOO000OO [3 ]#line:3433
                OO0OO000000O00O00 =O000OO00OOOO000OO [4 ]#line:3434
                O0O0O0O0O0O000O0O =O000OO00OOOO000OO [5 ]#line:3435
                O0OOO0000O00O00O0 =O0OO000O00OOOOO00 .split (',')#line:3436
                OO00000O00OOOO0O0 =OO000OO0OO000OO0O .split (',')#line:3437
                O0OO0O00OOO00OO0O =O0OO0OO0OO00O00OO .split (',')#line:3438
                O00O0OO000OOO0OO0 =OOO0OOO0O000O0O00 .split (',')#line:3439
                O0OOOO00OO0OOOOOO =OO0OO000000O00O00 .split (',')#line:3440
                O0000O0OOO00000O0 =O0O0O0O0O0O000O0O .split (',')#line:3441
                O0O0O0OO0O0O0O00O =['names','sample1','sample2','sample3','sample4','sample5']#line:3442
                O0OO000OO0O00O0OO =[O0OOO0000O00O00O0 ,OO00000O00OOOO0O0 ,O0OO0O00OOO00OO0O ,O00O0OO000OOO0OO0 ,O0OOOO00OO0OOOOOO ,O0000O0OOO00000O0 ]#line:3443
                if len (O0OOO0000O00O00O0 )==len (OO00000O00OOOO0O0 )==len (O0OO0O00OOO00OO0O )==len (O00O0OO000OOO0OO0 )==len (O0OOOO00OO0OOOOOO )==len (O0000O0OOO00000O0 ):#line:3446
                    OO00OO0OO0O0O0O0O ={}#line:3447
                    for OO00OO0000OO00O00 in range (len (O0OOO0000O00O00O0 )):#line:3448
                        OO00OO0OO0O0O0O0O [O0OOO0000O00O00O0 [OO00OO0000OO00O00 ]]=[OO00000O00OOOO0O0 [OO00OO0000OO00O00 ],O0OO0O00OOO00OO0O [OO00OO0000OO00O00 ],O00O0OO000OOO0OO0 [OO00OO0000OO00O00 ],O0OOOO00OO0OOOOOO [OO00OO0000OO00O00 ],O0000O0OOO00000O0 [OO00OO0000OO00O00 ]]#line:3449
                else :#line:3451
                    print ("tags and samples size not same")#line:3452
            O0O00OOO00OO0O000 =len (O000OO00OOOO000OO )-1 #line:3455
            return OO00OO0OO0O0O0O0O ,O0O00OOO00OO0O000 ,OOOO00000O0O0O000 ,OOOO0OOOOO000O000 #line:3457
        else :#line:3459
            OO00OO0OO0O0O0O0O ={}#line:3460
            O0O00OOO00OO0O000 =0 #line:3461
            return OO00OO0OO0O0O0O0O ,O0O00OOO00OO0O000 ,OOOO00000O0O0O000 ,OOOO0OOOOO000O000 #line:3462
    def inputsLogging (OOOO000O00O00OO00 ,OOO0O0O00OO00OO00 ,OOOO000O00000OOOO ,O000O0OOOOOO00OOO ,OO0OO00O00O00O0O0 ):#line:3468
        OO000O0O00OOO0OOO =O000O0OOOOOO00OOO ['Nav_GPS1_UTC']#line:3470
        OOOO000O00O00OO00 .cursor .execute ('''update public."Application_status" set "Value" = %s where "Item" = 'TimeStamp_onboard';''',[OO000O0O00OOO0OOO ])#line:3471
        OOOO000O00O00OO00 .conn .commit ()#line:3472
        O0O0OO0O0OO00OO0O =datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")#line:3473
        if OOOO000O00O00OO00 .log_inputs_realtime ==1 :#line:3474
            for O0O0O000O00000O00 in OOOO000O00000OOOO :#line:3475
                if O0O0O000O00000O00 =='Nav_GPS1_UTC':#line:3476
                    OOOO000O00O00OO00 .cursor .execute ('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s',[OO000O0O00OOO0OOO ,O0O0O000O00000O00 ])#line:3477
                    OOOO000O00O00OO00 .conn .commit ()#line:3478
                else :#line:3479
                    if OO0OO00O00O00O0O0 [O0O0O000O00000O00 ]==1 :#line:3480
                        OO0000O0O000000OO =str (O000O0OOOOOO00OOO [O0O0O000O00000O00 ])#line:3481
                        O00O0OO0O00O0O000 =True #line:3482
                        if len (OO0000O0O000000OO )==0 :#line:3483
                            OO0000O0O000000OO =999 #line:3484
                            O00O0OO0O00O0O000 =False #line:3485
                        OOOO000O00O00OO00 .cursor .execute ('update public."Input_Tags" set "Value" = %s where "Standard_Key" = %s',[float (OO0000O0O000000OO ),O0O0O000O00000O00 ])#line:3492
                        OOOO000O00O00OO00 .conn .commit ()#line:3493
                        OOOO000O00O00OO00 .cursor .execute ('update public."Input_Tags" set "TimeStamp" = %s where "Standard_Key" = %s',[O0O0OO0O0OO00OO0O ,O0O0O000O00000O00 ])#line:3494
                        OOOO000O00O00OO00 .conn .commit ()#line:3495
        print ("value no. ",OOO0O0O00OO00OO00 ," is done. TimeStamp is :",O000O0OOOOOO00OOO ['Nav_GPS1_UTC'])#line:3497
        if OOOO000O00O00OO00 .log_inputs_history ==1 :#line:3499
            O00O0O0O0O0OO0OO0 =['Input_history1','Input_history2','Input_history3','Input_history4','Input_history5','Input_history6']#line:3500
            OOOO00OO0OO00O0O0 ={}#line:3501
            for OO0OOOO000OOO0OO0 in O000O0OOOOOO00OOO .keys ():#line:3502
                OO0000O0O000000OO =O000O0OOOOOO00OOO [OO0OOOO000OOO0OO0 ]#line:3503
                OO0OOOO000OOO0OO0 =OO0OOOO000OOO0OO0 .replace ("-","_")#line:3506
                OOOO00OO0OO00O0O0 [OO0OOOO000OOO0OO0 ]=OO0000O0O000000OO #line:3507
            for O00000O0000O0OOO0 in O00O0O0O0O0OO0OO0 :#line:3509
                OOOO000O00O00OO00 .cursor .execute ('select "column_name" from information_schema.columns where "table_name" = %s',[O00000O0000O0OOO0 ])#line:3510
                OO0OO00000OO0OO00 =OOOO000O00O00OO00 .cursor .fetchall ()#line:3511
                OOOO000O00O00OO00 .conn .commit ()#line:3512
                O000OOO00OO0O0O00 =[O000OO0OOOO0000OO [0 ]for O000OO0OOOO0000OO in OO0OO00000OO0OO00 ]#line:3514
                O000OOO00OO0O0O00 .remove ('Nav_GPS1_UTC')#line:3515
                O000OOO00OO0O0O00 .remove ('TimeStamp')#line:3516
                O0OOOOOOOOO00O0O0 =f'''insert into public."{O00000O0000O0OOO0}" values('{O0O0OO0O0OO00OO0O}', '{OO000O0O00OOO0OOO}','''#line:3519
                for O0OO0OO0OO00O0O0O in O000OOO00OO0O0O00 :#line:3520
                    O0OOOOOOOOO00O0O0 =O0OOOOOOOOO00O0O0 +f"{OOOO00OO0OO00O0O0[O0OO0OO0OO00O0O0O]}, "#line:3521
                O0OOOOOOOOO00O0O0 =O0OOOOOOOOO00O0O0 [:-2 ]+")"#line:3522
                OOOO000O00O00OO00 .cursor .execute (O0OOOOOOOOO00O0O0 )#line:3524
                OOOO000O00O00OO00 .conn .commit ()#line:3525
        return OO000O0O00OOO0OOO #line:3526
    def findConditionsStatus (O0OO00000OOO0O000 ,OO0000OOOOOOO00O0 ,O0O0OOOO0O000O000 ):#line:3529
        O0000O0O0O0OO0OO0 =False #line:3530
        OOO0OO0O00OO0O0OO =False #line:3531
        O00OOOOO000OO0OO0 =False #line:3532
        O0OOO0OOO0O000O00 =False #line:3533
        O00OOO0OO00000OOO =False #line:3534
        O000O0O00O00OO00O =False #line:3535
        O0OO000000O00O0OO =0 #line:3536
        OOOOO000O00OOO0OO =0 #line:3537
        OOO0O0OO0OO000O00 =True #line:3538
        if len (OO0000OOOOOOO00O0 )==2 :#line:3539
            if 'standard deviation'in OO0000OOOOOOO00O0 [0 ]:#line:3540
                O0000O0O0O0OO0OO0 =True #line:3541
                O0OO000000O00O0OO =int (OO0000OOOOOOO00O0 [1 ])#line:3542
            elif 'moving average'in OO0000OOOOOOO00O0 [0 ]:#line:3543
                OOO0OO0O00OO0O0OO =True #line:3544
                O0OO000000O00O0OO =int (OO0000OOOOOOO00O0 [1 ])#line:3545
            elif 'delta'in OO0000OOOOOOO00O0 [0 ]:#line:3546
                O00OOOOO000OO0OO0 =True #line:3547
                O0OO000000O00O0OO =int (OO0000OOOOOOO00O0 [1 ])#line:3548
            elif 'subtract'in OO0000OOOOOOO00O0 [0 ]:#line:3549
                O00OOO0OO00000OOO =True #line:3550
            elif 'sum'in OO0000OOOOOOO00O0 [0 ]:#line:3551
                O000O0O00O00OO00O =True #line:3552
            else :#line:3553
                OOO0O0OO0OO000O00 =False #line:3554
        elif len (OO0000OOOOOOO00O0 )>2 and ('subtract'in OO0000OOOOOOO00O0 [0 ]or 'sum'in OO0000OOOOOOO00O0 [0 ]):#line:3555
            if 'subtract'in OO0000OOOOOOO00O0 [0 ]:#line:3556
                O00OOO0OO00000OOO =True #line:3557
            elif 'sum'in OO0000OOOOOOO00O0 [0 ]:#line:3558
                O000O0O00O00OO00O =True #line:3559
            else :#line:3560
                OOO0O0OO0OO000O00 =False #line:3561
        elif len (OO0000OOOOOOO00O0 )==4 :#line:3562
            if 'moving average'in OO0000OOOOOOO00O0 [0 ]and 'delta'in OO0000OOOOOOO00O0 [2 ]:#line:3563
                O0OOO0OOO0O000O00 =True #line:3564
                O0OO000000O00O0OO =int (OO0000OOOOOOO00O0 [1 ])#line:3566
                OOOOO000O00OOO0OO =int (OO0000OOOOOOO00O0 [3 ])#line:3567
            else :#line:3568
                OOO0O0OO0OO000O00 =False #line:3569
        else :#line:3570
            OOO0O0OO0OO000O00 =False #line:3572
        if O0O0OOOO0O000O000 ==O0OO00000OOO0O000 .for_test :#line:3573
            print ("condition exists=>",OOO0O0OO0OO000O00 )#line:3576
            print ("condition list=>",OO0000OOOOOOO00O0 )#line:3577
        return O0000O0O0O0OO0OO0 ,OOO0OO0O00OO0O0OO ,O00OOOOO000OO0OO0 ,O00OOO0OO00000OOO ,O000O0O00O00OO00O ,O0OOO0OOO0O000O00 ,O0OO000000O00O0OO ,OOOOO000O00OOO0OO ,OOO0O0OO0OO000O00 #line:3581
    def calcAggregate (O00O0OO0OOOOOO0O0 ,O0OO0OO0OOOOOOO00 ,O0O0OO0OO00O0OOO0 ,OOOO000OOO0OO00OO ,OO00OO0OO000OO0OO ):#line:3583
        O00O000000O000000 =OO00OO0OO000OO0OO +"__"+OOOO000OOO0OO00OO #line:3584
        if O0O0OO0OO00O0OOO0 :#line:3585
            OO0OO000OOO00OO00 =sum (O00O0OO0OOOOOO0O0 .agg [O00O000000O000000 ])/len (O00O0OO0OOOOOO0O0 .agg [O00O000000O000000 ])#line:3586
        elif O0OO0OO0OOOOOOO00 :#line:3587
            OO0OO000OOO00OO00 =np .std (O00O0OO0OOOOOO0O0 .agg [O00O000000O000000 ])#line:3588
        return OO0OO000OOO00OO00 #line:3589
    def tagNotExists_inSampleList (OOOOO0OOOO00000OO ,OO0O00OO000000000 ,O000OOO0OO0O0O00O ,OO00O00O0OO0O0OO0 ,O0O0O0OOOOOO0O000 ):#line:3591
        OOOOO0OOOO00000OO .agg [OO00O00O0OO0O0OO0 ]=[O000OOO0OO0O0O00O [OO0O00OO000000000 ]]#line:3592
        O00OOO000000OOO0O =False #line:3593
        if O0O0O0OOOOOO0O000 ==OOOOO0OOOO00000OO .for_test :#line:3594
            print ("fell into function: tagNotExists_inSampleList(). latest samples are: ",OOOOO0OOOO00000OO .agg [OO00O00O0OO0O0OO0 ])#line:3595
        return O00OOO000000OOO0O #line:3596
    def tagExists_butSampleSizeTooShort (O00O000000O0OO000 ,O0OO0O0OOO00OO0O0 ,O0000OO0O000O0000 ,OOO0OOO0O0000O0OO ,OO0OO000OO0OO000O ):#line:3598
        O00O000000O0OO000 .agg [OOO0OOO0O0000O0OO ].append (O0000OO0O000O0000 [O0OO0O0OOO00OO0O0 ])#line:3599
        O0OOOO00O0OO00OOO =False #line:3600
        if OO0OO000OO0OO000O ==O00O000000O0OO000 .for_test :#line:3601
            print ("fell into function: tagExists_butSampleSizeTooShort(). latest samples are: ",O00O000000O0OO000 .agg [OOO0OOO0O0000O0OO ])#line:3602
        return O0OOOO00O0OO00OOO #line:3603
    def SampleSizeOneShort (OOOO000000O0O00O0 ,OO00OOO000OOO0O00 ,O0OO0000000000O0O ,OOOO0OO0000000OO0 ,O00OOOOO00OO00OOO ):#line:3605
        OOOO000000O0O00O0 .agg [OOOO0OO0000000OO0 ].append (O0OO0000000000O0O [OO00OOO000OOO0O00 ])#line:3606
        OO0O0O00OOO0OO000 =True #line:3607
        if O00OOOOO00OO00OOO ==OOOO000000O0O00O0 .for_test :#line:3608
            print ("fell into function: SampleSizeOneShort(). 1 is added now and latest samples are okay for calculation: ",OOOO000000O0O00O0 .agg [OOOO0OO0000000OO0 ])#line:3609
        return OO0O0O00OOO0OO000 #line:3610
    def SampleSizeOK (OOOOO000O00000O0O ,OOO0OO00OO0OO000O ,O00O0OOO0OOOOO0O0 ,O00O000OO0000OO00 ,OOOO00O0O0OOOOOO0 ):#line:3612
        OOOOO000O00000O0O .agg [O00O000OO0000OO00 ].pop (0 )#line:3613
        OOOOO000O00000O0O .agg [O00O000OO0000OO00 ].append (O00O0OOO0OOOOO0O0 [OOO0OO00OO0OO000O ])#line:3614
        OOOOOOO0OO00O000O =True #line:3615
        if OOOO00O0O0OOOOOO0 ==OOOOO000O00000O0O .for_test :#line:3616
            print ("fell into function: SampleSizeOK(). latest is appended now and oldest is popped, and latest samples are okay for calculation: ",OOOOO000O00000O0O .agg [O00O000OO0000OO00 ])#line:3617
        return OOOOOOO0OO00O000O #line:3618
    def tagNotExists_inMAvgList (OOOO0O0OOO00OO0OO ,OOO0OOOO0OO0OOO00 ,OOOOO00O00O00O0O0 ,O0O000O000O0OO0O0 ):#line:3620
        OO0O0O000O0O0O0OO =sum (OOOO0O0OOO00OO0OO .agg [OOOOO00O00O00O0O0 ])/len (OOOO0O0OOO00OO0OO .agg [OOOOO00O00O00O0O0 ])#line:3621
        OOOO0O0OOO00OO0OO .mavg_samples [OOOOO00O00O00O0O0 ]=[OO0O0O000O0O0O0OO ]#line:3622
        OO0O0000O000000O0 =False #line:3623
        if O0O000O000O0OO0O0 ==OOOO0O0OOO00OO0OO .for_test :#line:3624
            print ('at point ','point+1(point NA now)',' mavg samples for',OOOOO00O00O00O0O0 ,' are ',OOOO0O0OOO00OO0OO .mavg_samples ,'it ended up in tagNotExists_inMAvgList()')#line:3625
        return OO0O0000O000000O0 #line:3626
    def MAvgSampleSizeTooShort (O00O00OO0OO00O0O0 ,O00OO0OOOO00OOOO0 ,OO0000000OO0O0000 ,O0OO00O0OOO0OOOOO ):#line:3628
        OO0OO000OOOOOOO0O =sum (O00O00OO0OO00O0O0 .agg [OO0000000OO0O0000 ])/len (O00O00OO0OO00O0O0 .agg [OO0000000OO0O0000 ])#line:3629
        O00O00OO0OO00O0O0 .mavg_samples [OO0000000OO0O0000 ].append (OO0OO000OOOOOOO0O )#line:3630
        OO0O0OO000O0O0OO0 =False #line:3631
        if O0OO00O0OOO0OOOOO ==O00O00OO0OO00O0O0 .for_test :#line:3632
            print ('at point ','point+1(point NA now)',' mavg samples for',OO0000000OO0O0000 ,' are ',O00O00OO0OO00O0O0 .mavg_samples ,'it ended up in MAvgSampleSizeTooShort()')#line:3633
        return OO0O0OO000O0O0OO0 #line:3634
    def MAvgSampleSizeOneShort (OOO00OO0OOO0O00OO ,O00OOOOOO00OO0OOO ,O000OOO0O0OOOO000 ,O000OOOO00OOOOO00 ):#line:3636
        OOO0OO0O00O00000O =sum (OOO00OO0OOO0O00OO .agg [O000OOO0O0OOOO000 ])/len (OOO00OO0OOO0O00OO .agg [O000OOO0O0OOOO000 ])#line:3637
        OOO00OO0OOO0O00OO .mavg_samples [O000OOO0O0OOOO000 ].append (OOO0OO0O00O00000O )#line:3638
        OOO0000O0000OO0OO =True #line:3639
        if O000OOOO00OOOOO00 ==OOO00OO0OOO0O00OO .for_test :#line:3640
            print ('at point ','point+1(point NA now)',' mavg samples for',O000OOO0O0OOOO000 ,' are ',OOO00OO0OOO0O00OO .mavg_samples ,'it ended up in MAvgSampleSizeOneShort()')#line:3641
        return OOO0000O0000OO0OO #line:3642
    def MAvgSampleSizeOK (OO00OO00O00OO0000 ,O0OOO00OOO0OO00OO ,OO0O0000000O000OO ,O0OO0000000OOO000 ):#line:3644
        OO00OO00O00OO0000 .mavg_samples [OO0O0000000O000OO ].pop (0 )#line:3645
        O00OO0000O00OOOO0 =sum (OO00OO00O00OO0000 .agg [OO0O0000000O000OO ])/len (OO00OO00O00OO0000 .agg [OO0O0000000O000OO ])#line:3646
        OO00OO00O00OO0000 .mavg_samples [OO0O0000000O000OO ].append (O00OO0000O00OOOO0 )#line:3647
        OOOOO00O000O00000 =True #line:3648
        if O0OO0000000OOO000 ==OO00OO00O00OO0000 .for_test :#line:3649
            print ('at point ','point+1(point NA now)',' mavg samples for',OO0O0000000O000OO ,' are ',OO00OO00O00OO0000 .mavg_samples ,'it ended up in MAvgSampleSizeOK()')#line:3650
        return OOOOO00O000O00000 #line:3651
    def checkSamplesStatus (OOOO0O00OOO0000O0 ,O0OOOO0OO000OO0O0 ,OOO00OO000OO0000O ,O0OOOO00O0000OOOO ,OO00000O000OO0OOO ,O0O0000000O000O00 ,OO000000O0O00O00O ,OO0O0OO0O0OO0O0O0 ,O0OO00OOOO0000O00 ):#line:3653
        O0OO00OO0O000OO00 =O0OO00OOOO0000O00 +"__"+O0OOOO0OO000OO0O0 #line:3658
        if O0OO00OO0O000OO00 not in OOOO0O00OOO0000O0 .agg .keys ():#line:3659
            OO00000O000OO0OOO =OOOO0O00OOO0000O0 .tagNotExists_inSampleList (O0OOOO0OO000OO0O0 ,OOO00OO000OO0000O ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3660
        elif O0OO00OO0O000OO00 in OOOO0O00OOO0000O0 .agg .keys ():#line:3661
            if len (OOOO0O00OOO0000O0 .agg [O0OO00OO0O000OO00 ])+1 <O0OOOO00O0000OOOO :#line:3662
                OO00000O000OO0OOO =OOOO0O00OOO0000O0 .tagExists_butSampleSizeTooShort (O0OOOO0OO000OO0O0 ,OOO00OO000OO0000O ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3663
            elif len (OOOO0O00OOO0000O0 .agg [O0OO00OO0O000OO00 ])+1 ==O0OOOO00O0000OOOO :#line:3665
                OO00000O000OO0OOO =OOOO0O00OOO0000O0 .SampleSizeOneShort (O0OOOO0OO000OO0O0 ,OOO00OO000OO0000O ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3666
            elif len (OOOO0O00OOO0000O0 .agg [O0OO00OO0O000OO00 ])+1 >O0OOOO00O0000OOOO :#line:3668
                OO00000O000OO0OOO =OOOO0O00OOO0000O0 .SampleSizeOK (O0OOOO0OO000OO0O0 ,OOO00OO000OO0000O ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3669
        if O0OO00OOOO0000O00 ==OOOO0O00OOO0000O0 .for_test :#line:3672
            print ("samples_ok: ",OO00000O000OO0OOO )#line:3673
        if O0O0000000O000O00 :#line:3674
            if OO00000O000OO0OOO :#line:3676
                if O0OO00OOOO0000O00 ==OOOO0O00OOO0000O0 .for_test :#line:3677
                    print ("raw samples are collected well at point",'point+1(point NA now)')#line:3678
                if O0OO00OO0O000OO00 not in OOOO0O00OOO0000O0 .mavg_samples .keys ():#line:3680
                    OO00000O000OO0OOO =OOOO0O00OOO0000O0 .tagNotExists_inMAvgList (O0OOOO0OO000OO0O0 ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3686
                elif O0OO00OO0O000OO00 in OOOO0O00OOO0000O0 .mavg_samples .keys ():#line:3687
                    if len (OOOO0O00OOO0000O0 .mavg_samples [O0OO00OO0O000OO00 ])+1 <OO000000O0O00O00O :#line:3688
                        OO00000O000OO0OOO =OOOO0O00OOO0000O0 .MAvgSampleSizeTooShort (O0OOOO0OO000OO0O0 ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3689
                    elif len (OOOO0O00OOO0000O0 .mavg_samples [O0OO00OO0O000OO00 ])+1 ==OO000000O0O00O00O :#line:3690
                        OO00000O000OO0OOO =OOOO0O00OOO0000O0 .MAvgSampleSizeOneShort (O0OOOO0OO000OO0O0 ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3691
                    elif len (OOOO0O00OOO0000O0 .mavg_samples [O0OO00OO0O000OO00 ])+1 >OO000000O0O00O00O :#line:3692
                        OO00000O000OO0OOO =OOOO0O00OOO0000O0 .MAvgSampleSizeOK (O0OOOO0OO000OO0O0 ,O0OO00OO0O000OO00 ,O0OO00OOOO0000O00 )#line:3693
            if O0OO00OOOO0000O00 ==OOOO0O00OOO0000O0 .for_test :#line:3695
                if OO00000O000OO0OOO :#line:3696
                    print ("mavg samples are collected well at point",'point+1(point NA now)')#line:3697
        return OO00000O000OO0OOO #line:3698
    def moreThan (OOO000000OO0OO0OO ,O000O000OO0OOOO0O ,O0OO000OO0O0000OO ,O0OO000OOOO0OOO00 ,O0OO00OOO0O000OOO ,O00OO0O0000O000OO ,O00O00000O00000O0 ,OOOO00OOO0O0OO0O0 ):#line:3700
        O00OO0O0000O000OO =float (O00OO0O0000O000OO )#line:3701
        O00000OOO0O00O000 ,OO000OOO000O000OO ,OOOOO0OO0O0OO00O0 ,O0O0O00O0O0OO0O0O ,O0O000O00OO000OOO ,O0O00O0O00O0OOOO0 ,OOO0O00O0OOOOOOOO ,OO0OOO00000OOO0O0 ,OO000O00000O000O0 =OOO000000OO0OO0OO .findConditionsStatus (O0OO000OO0O0000OO ,OOOO00OOO0O0OO0O0 )#line:3703
        O0OO0OOO0OOOOO00O =1 #line:3704
        if OO000O00000O000O0 :#line:3707
            if O0O000O00OO000OOO ==True or O0O0O00O0O0OO0O0O ==True :#line:3708
                OOOOO00OO00O0OOO0 =True #line:3709
            else :#line:3710
                OOOOO00OO00O0OOO0 =False #line:3711
                OOOOO00OO00O0OOO0 =OOO000000OO0OO0OO .checkSamplesStatus (O0OO000OOOO0OOO00 ,O0OO00OOO0O000OOO ,OOO0O00O0OOOOOOOO ,OOOOO00OO00O0OOO0 ,O0O00O0O00O0OOOO0 ,OO0OOO00000OOO0O0 ,O0OO000OO0O0000OO ,OOOO00OOO0O0OO0O0 )#line:3712
            if OOOOO00OO00O0OOO0 ==False :#line:3714
                O0OO0O0O0OO00OOO0 ='Unknown'#line:3715
            elif OOOOO00OO00O0OOO0 :#line:3717
                O0000OOOO0OOOO000 =OOOO00OOO0O0OO0O0 +"__"+O0OO000OOOO0OOO00 #line:3718
                if O00000OOO0O00O000 ==True or OO000OOO000O000OO ==True :#line:3719
                    OO0O000OOO00OO00O =OOO000000OO0OO0OO .calcAggregate (O00000OOO0O00O000 ,OO000OOO000O000OO ,O0OO000OOOO0OOO00 ,OOOO00OOO0O0OO0O0 )#line:3721
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3722
                        print ("collected raw samples are: ",OOO000000OO0OO0OO .agg [OOOO00OOO0O0OO0O0 +"__"+O0OO000OOOO0OOO00 ],"threshold is: ",O00OO0O0000O000OO ,'calculated agg value:',OO0O000OOO00OO00O )#line:3723
                    if OO0O000OOO00OO00O >O00OO0O0000O000OO :#line:3725
                        O0OO0O0O0OO00OOO0 =True #line:3726
                    else :#line:3727
                        O0OO0O0O0OO00OOO0 =False #line:3728
                elif OOOOO0OO0O0OO00O0 :#line:3729
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3731
                        print ("collected raw samples are: ",OOO000000OO0OO0OO .agg [O0000OOOO0OOOO000 ],"threshold is: ",O00OO0O0000O000OO )#line:3732
                    if 'absolute'in O0OO000OO0O0000OO [0 ]:#line:3735
                        if abs (O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ]-OOO000000OO0OO0OO .agg [O0000OOOO0OOOO000 ][0 ])>O00OO0O0000O000OO :#line:3736
                            O0OO0O0O0OO00OOO0 =True #line:3737
                        else :#line:3738
                            O0OO0O0O0OO00OOO0 =False #line:3739
                    else :#line:3740
                        if O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ]-OOO000000OO0OO0OO .agg [O0000OOOO0OOOO000 ][0 ]>O00OO0O0000O000OO :#line:3741
                            if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3742
                                print ("current point",O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ])#line:3743
                                print ("point in sample",OOO000000OO0OO0OO .agg [O0000OOOO0OOOO000 ][0 ])#line:3744
                            O0OO0O0O0OO00OOO0 =True #line:3745
                        else :#line:3746
                            O0OO0O0O0OO00OOO0 =False #line:3747
                elif O0O00O0O00O0OOOO0 :#line:3750
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3751
                        print ("collected mavg samples are: ",OOO000000OO0OO0OO .mavg_samples [O0000OOOO0OOOO000 ],"threshold is: ",O00OO0O0000O000OO )#line:3752
                    if 'absolute'in O0OO000OO0O0000OO [2 ]:#line:3754
                        if abs (OOO000000OO0OO0OO .mavg_samples [O0000OOOO0OOOO000 ][-1 ]-OOO000000OO0OO0OO .mavg_samples [O0000OOOO0OOOO000 ][0 ])>O00OO0O0000O000OO :#line:3755
                            O0OO0O0O0OO00OOO0 =True #line:3756
                        else :#line:3757
                            O0OO0O0O0OO00OOO0 =False #line:3758
                    else :#line:3759
                        if OOO000000OO0OO0OO .mavg_samples [O0000OOOO0OOOO000 ][-1 ]-OOO000000OO0OO0OO .mavg_samples [O0000OOOO0OOOO000 ][0 ]>O00OO0O0000O000OO :#line:3760
                            O0OO0O0O0OO00OOO0 =True #line:3761
                        else :#line:3762
                            O0OO0O0O0OO00OOO0 =False #line:3763
                elif O0O0O00O0O0OO0O0O :#line:3765
                    O0OOO00O000O00OOO =O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ]#line:3766
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3767
                        print (O0OOO00O000O00OOO )#line:3768
                    for OOO0O0O00OOOOOOOO in range (1 ,len (O0OO000OO0O0000OO )):#line:3769
                        O0OOO00O000O00OOO =O0OOO00O000O00OOO -O0OO00OOO0O000OOO [O0OO000OO0O0000OO [OOO0O0O00OOOOOOOO ]]#line:3770
                        if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3771
                            print ("after loop value: ",O0OOO00O000O00OOO )#line:3772
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3773
                        print ("value after subtracting given keys: ",O0OOO00O000O00OOO )#line:3774
                    if 'absolute'in O000O000OO0OOOO0O :#line:3775
                        if abs (O0OOO00O000O00OOO )>O00OO0O0000O000OO :#line:3776
                            O0OO0O0O0OO00OOO0 =True #line:3777
                        else :#line:3778
                            O0OO0O0O0OO00OOO0 =False #line:3779
                    else :#line:3780
                        if O0OOO00O000O00OOO >O00OO0O0000O000OO :#line:3781
                            O0OO0O0O0OO00OOO0 =True #line:3782
                        else :#line:3783
                            O0OO0O0O0OO00OOO0 =False #line:3784
                elif O0O000O00OO000OOO :#line:3785
                    O0OOO00O000O00OOO =O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ]#line:3786
                    for OOO0O0O00OOOOOOOO in range (1 ,len (O0OO000OO0O0000OO )):#line:3787
                        O0OOO00O000O00OOO =O0OOO00O000O00OOO +O0OO00OOO0O000OOO [O0OO000OO0O0000OO [OOO0O0O00OOOOOOOO ]]#line:3788
                        if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3789
                            print ("after loop value: ",O0OOO00O000O00OOO )#line:3790
                    if OOOO00OOO0O0OO0O0 ==OOO000000OO0OO0OO .for_test :#line:3791
                        print ("value after adding given keys: ",O0OOO00O000O00OOO )#line:3792
                    if 'absolute'in O000O000OO0OOOO0O :#line:3793
                        if abs (O0OOO00O000O00OOO )>O00OO0O0000O000OO :#line:3794
                            O0OO0O0O0OO00OOO0 =True #line:3795
                        else :#line:3796
                            O0OO0O0O0OO00OOO0 =False #line:3797
                    else :#line:3798
                        if O0OOO00O000O00OOO >O00OO0O0000O000OO :#line:3799
                            O0OO0O0O0OO00OOO0 =True #line:3800
                        else :#line:3801
                            O0OO0O0O0OO00OOO0 =False #line:3802
        else :#line:3804
            if O0OO00OOO0O000OOO [O0OO000OOOO0OOO00 ]>O00OO0O0000O000OO :#line:3809
                O0OO0O0O0OO00OOO0 =True #line:3810
            else :#line:3811
                O0OO0O0O0OO00OOO0 =False #line:3812
        return O0OO0O0O0OO00OOO0 ,O00O00000O00000O0 #line:3814
    def lessThan (OOOO000O0O0O000O0 ,O000OOO0OOOOOOO0O ,O000O000OOOO0OOO0 ,OO0O0O0O0OOOO0OOO ,OOO0OO0O000O0O000 ,OO00OO0OO00O0000O ,OOOOOOO000OO00O00 ,OO000OOO0O0O000O0 ):#line:3816
        OO00OO0OO00O0000O =float (OO00OO0OO00O0000O )#line:3817
        OO0000OOOO0OO0OOO ,O0OO00OOO00OOOO0O ,OO0OOO0O000OO0O00 ,O0O00OO000000OOOO ,O0O00OOOOOOO00OOO ,O0OO00O00O0OOOO00 ,OO0O00O00OO0000OO ,O00OO0OOOOOOOO00O ,OOOOO0OOO0OO0O00O =OOOO000O0O0O000O0 .findConditionsStatus (O000O000OOOO0OOO0 ,OO000OOO0O0O000O0 )#line:3819
        O0O00O0O0OO0000OO =1 #line:3820
        if OOOOO0OOO0OO0O00O :#line:3823
            if O0O00OOOOOOO00OOO ==True or O0O00OO000000OOOO ==True :#line:3824
                OO0O00OOO0OOOO00O =True #line:3825
            else :#line:3826
                OO0O00OOO0OOOO00O =False #line:3827
                OO0O00OOO0OOOO00O =OOOO000O0O0O000O0 .checkSamplesStatus (OO0O0O0O0OOOO0OOO ,OOO0OO0O000O0O000 ,OO0O00O00OO0000OO ,OO0O00OOO0OOOO00O ,O0OO00O00O0OOOO00 ,O00OO0OOOOOOOO00O ,O000O000OOOO0OOO0 ,OO000OOO0O0O000O0 )#line:3828
            if OO0O00OOO0OOOO00O ==False :#line:3830
                O0OOOO0O00000O0OO ='Unknown'#line:3831
            elif OO0O00OOO0OOOO00O :#line:3833
                O0O00OOOOO0OO0O0O =OO000OOO0O0O000O0 +"__"+OO0O0O0O0OOOO0OOO #line:3834
                if OO0000OOOO0OO0OOO ==True or O0OO00OOO00OOOO0O ==True :#line:3835
                    OO0000O0OO00O0OO0 =OOOO000O0O0O000O0 .calcAggregate (OO0000OOOO0OO0OOO ,O0OO00OOO00OOOO0O ,OO0O0O0O0OOOO0OOO ,OO000OOO0O0O000O0 )#line:3837
                    if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3838
                        print ('points',OOOO000O0O0O000O0 .agg [O0O00OOOOO0OO0O0O ])#line:3839
                        print ('agg value:',OO0000O0OO00O0OO0 )#line:3840
                    if OO0000O0OO00O0OO0 <OO00OO0OO00O0000O :#line:3841
                        O0OOOO0O00000O0OO =True #line:3842
                    else :#line:3843
                        O0OOOO0O00000O0OO =False #line:3844
                elif OO0OOO0O000OO0O00 :#line:3845
                    if 'absolute'in O000O000OOOO0OOO0 [0 ]:#line:3848
                        if abs (OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ]-OOOO000O0O0O000O0 .agg [O0O00OOOOO0OO0O0O ][0 ])<OO00OO0OO00O0000O :#line:3849
                            O0OOOO0O00000O0OO =True #line:3850
                        else :#line:3851
                            O0OOOO0O00000O0OO =False #line:3852
                    else :#line:3853
                        if OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ]-OOOO000O0O0O000O0 .agg [O0O00OOOOO0OO0O0O ][0 ]<OO00OO0OO00O0000O :#line:3854
                            if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3855
                                print ("current point",OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ])#line:3856
                                print ("point in sample",OOOO000O0O0O000O0 .agg [O0O00OOOOO0OO0O0O ][0 ])#line:3857
                            O0OOOO0O00000O0OO =True #line:3858
                        else :#line:3859
                            O0OOOO0O00000O0OO =False #line:3860
                elif O0OO00O00O0OOOO00 :#line:3862
                    if 'absolute'in O000O000OOOO0OOO0 [2 ]:#line:3864
                        if abs (OOOO000O0O0O000O0 .mavg_samples [O0O00OOOOO0OO0O0O ][-1 ]-OOOO000O0O0O000O0 .mavg_samples [O0O00OOOOO0OO0O0O ][0 ])<OO00OO0OO00O0000O :#line:3865
                            O0OOOO0O00000O0OO =True #line:3866
                        else :#line:3867
                            O0OOOO0O00000O0OO =False #line:3868
                    else :#line:3869
                        if OOOO000O0O0O000O0 .mavg_samples [O0O00OOOOO0OO0O0O ][-1 ]-OOOO000O0O0O000O0 .mavg_samples [O0O00OOOOO0OO0O0O ][0 ]<OO00OO0OO00O0000O :#line:3870
                            O0OOOO0O00000O0OO =True #line:3871
                        else :#line:3872
                            O0OOOO0O00000O0OO =False #line:3873
                elif O0O00OO000000OOOO :#line:3875
                    OOOOO00O00O0O00OO =OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ]#line:3876
                    for O0OO0O000O0O0OO0O in range (1 ,len (O000O000OOOO0OOO0 )):#line:3877
                        OOOOO00O00O0O00OO =OOOOO00O00O0O00OO -OOO0OO0O000O0O000 [O000O000OOOO0OOO0 [O0OO0O000O0O0OO0O ]]#line:3878
                        if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3879
                            print ("after loop value: ",OOOOO00O00O0O00OO )#line:3880
                    if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3881
                        print ("value after subtracting given keys: ",OOOOO00O00O0O00OO )#line:3882
                    if 'absolute'in O000OOO0OOOOOOO0O :#line:3883
                        if abs (OOOOO00O00O0O00OO )<OO00OO0OO00O0000O :#line:3884
                            O0OOOO0O00000O0OO =True #line:3885
                        else :#line:3886
                            O0OOOO0O00000O0OO =False #line:3887
                    else :#line:3888
                        if OOOOO00O00O0O00OO <OO00OO0OO00O0000O :#line:3889
                            O0OOOO0O00000O0OO =True #line:3890
                        else :#line:3891
                            O0OOOO0O00000O0OO =False #line:3892
                elif O0O00OOOOOOO00OOO :#line:3893
                    OOOOO00O00O0O00OO =OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ]#line:3894
                    for O0OO0O000O0O0OO0O in range (1 ,len (O000O000OOOO0OOO0 )):#line:3895
                        OOOOO00O00O0O00OO =OOOOO00O00O0O00OO +OOO0OO0O000O0O000 [O000O000OOOO0OOO0 [O0OO0O000O0O0OO0O ]]#line:3896
                        if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3897
                            print ("after loop value: ",OOOOO00O00O0O00OO )#line:3898
                    if OO000OOO0O0O000O0 ==OOOO000O0O0O000O0 .for_test :#line:3899
                        print ("value after adding given keys: ",OOOOO00O00O0O00OO )#line:3900
                    if 'absolute'in O000OOO0OOOOOOO0O :#line:3901
                        if abs (OOOOO00O00O0O00OO )<OO00OO0OO00O0000O :#line:3902
                            O0OOOO0O00000O0OO =True #line:3903
                        else :#line:3904
                            O0OOOO0O00000O0OO =False #line:3905
                    else :#line:3906
                        if OOOOO00O00O0O00OO <OO00OO0OO00O0000O :#line:3907
                            O0OOOO0O00000O0OO =True #line:3908
                        else :#line:3909
                            O0OOOO0O00000O0OO =False #line:3910
        else :#line:3912
            if OOO0OO0O000O0O000 [OO0O0O0O0OOOO0OOO ]<OO00OO0OO00O0000O :#line:3918
                O0OOOO0O00000O0OO =True #line:3919
            else :#line:3920
                O0OOOO0O00000O0OO =False #line:3921
        return O0OOOO0O00000O0OO ,OOOOOOO000OO00O00 #line:3923
    def equalTo (OO0O00O0OO0OO0OO0 ,O0OOO0OOOO0000O0O ,OO0OO00O0O0O0O0O0 ,O0O0OO0OO0OO0OOO0 ,O0OOO000OOO0O0O0O ,O0000O00000O00O00 ,OOO000OOOO0OOO00O ,O00O0OO0O00O000O0 ):#line:3925
        O0000O00000O00O00 =float (O0000O00000O00O00 )#line:3926
        O0OO0OOO00O000OOO ,OO00O0O0OO00O000O ,O0O0000O0OOOO0OOO ,O000O00O000OOO00O ,O000O000000O0OOOO ,O00O00OOO0OO0000O ,O0000O0OO0O00O00O ,O00OO0O000O00OOO0 ,O0OOOO0O0OO00OOOO =OO0O00O0OO0OO0OO0 .findConditionsStatus (OO0OO00O0O0O0O0O0 ,O00O0OO0O00O000O0 )#line:3928
        O00OO00O000O0OOO0 =1 #line:3929
        if O0OOOO0O0OO00OOOO :#line:3932
            if O000O000000O0OOOO ==True or O000O00O000OOO00O ==True :#line:3933
                OO0O0000O00OOOO00 =True #line:3934
            else :#line:3935
                OO0O0000O00OOOO00 =False #line:3936
                OO0O0000O00OOOO00 =OO0O00O0OO0OO0OO0 .checkSamplesStatus (O0O0OO0OO0OO0OOO0 ,O0OOO000OOO0O0O0O ,O0000O0OO0O00O00O ,OO0O0000O00OOOO00 ,O00O00OOO0OO0000O ,O00OO0O000O00OOO0 ,OO0OO00O0O0O0O0O0 ,O00O0OO0O00O000O0 )#line:3937
            if OO0O0000O00OOOO00 ==False :#line:3939
                OOOOO00OO0OO0O000 ='Unknown'#line:3940
            elif OO0O0000O00OOOO00 :#line:3942
                OO00000OOO0OOO00O =O00O0OO0O00O000O0 +"__"+O0O0OO0OO0OO0OOO0 #line:3943
                if O0OO0OOO00O000OOO ==True or OO00O0O0OO00O000O ==True :#line:3944
                    O0OO000000OOO00O0 =OO0O00O0OO0OO0OO0 .calcAggregate (O0OO0OOO00O000OOO ,OO00O0O0OO00O000O ,O0O0OO0OO0OO0OOO0 ,O00O0OO0O00O000O0 )#line:3946
                    if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:3947
                        print ('points',OO0O00O0OO0OO0OO0 .agg [OO00000OOO0OOO00O ])#line:3948
                        print ('agg value:',O0OO000000OOO00O0 )#line:3949
                    if O0OO000000OOO00O0 ==O0000O00000O00O00 :#line:3950
                        OOOOO00OO0OO0O000 =True #line:3951
                    else :#line:3952
                        OOOOO00OO0OO0O000 =False #line:3953
                elif O0O0000O0OOOO0OOO :#line:3954
                    if 'absolute'in OO0OO00O0O0O0O0O0 [0 ]:#line:3957
                        if abs (O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]-OO0O00O0OO0OO0OO0 .agg [OO00000OOO0OOO00O ][0 ])==O0000O00000O00O00 :#line:3958
                            OOOOO00OO0OO0O000 =True #line:3959
                        else :#line:3960
                            OOOOO00OO0OO0O000 =False #line:3961
                    else :#line:3962
                        if O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]-OO0O00O0OO0OO0OO0 .agg [OO00000OOO0OOO00O ][0 ]==O0000O00000O00O00 :#line:3963
                            if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:3964
                                print ("current point",O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ])#line:3965
                                print ("point in sample",OO0O00O0OO0OO0OO0 .agg [OO00000OOO0OOO00O ][0 ])#line:3966
                            OOOOO00OO0OO0O000 =True #line:3967
                        else :#line:3968
                            OOOOO00OO0OO0O000 =False #line:3969
                elif O00O00OOO0OO0000O :#line:3971
                    if 'absolute'in OO0OO00O0O0O0O0O0 [2 ]:#line:3973
                        if abs (OO0O00O0OO0OO0OO0 .mavg_samples [OO00000OOO0OOO00O ][-1 ]-OO0O00O0OO0OO0OO0 .mavg_samples [OO00000OOO0OOO00O ][0 ])==O0000O00000O00O00 :#line:3974
                            OOOOO00OO0OO0O000 =True #line:3975
                        else :#line:3976
                            OOOOO00OO0OO0O000 =False #line:3977
                    else :#line:3978
                        if OO0O00O0OO0OO0OO0 .mavg_samples [OO00000OOO0OOO00O ][-1 ]-OO0O00O0OO0OO0OO0 .mavg_samples [OO00000OOO0OOO00O ][0 ]==O0000O00000O00O00 :#line:3979
                            OOOOO00OO0OO0O000 =True #line:3980
                        else :#line:3981
                            OOOOO00OO0OO0O000 =False #line:3982
                elif O000O00O000OOO00O :#line:3984
                    OOO0O0OOO0O000OO0 =O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]#line:3985
                    for O0O0O00000000OO00 in range (1 ,len (OO0OO00O0O0O0O0O0 )):#line:3986
                        OOO0O0OOO0O000OO0 =OOO0O0OOO0O000OO0 -O0OOO000OOO0O0O0O [OO0OO00O0O0O0O0O0 [O0O0O00000000OO00 ]]#line:3987
                        if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:3988
                            print ("after loop value: ",OOO0O0OOO0O000OO0 )#line:3989
                    if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:3990
                        print ("value after subtracting given keys: ",OOO0O0OOO0O000OO0 )#line:3991
                    if 'absolute'in O0OOO0OOOO0000O0O :#line:3992
                        if abs (OOO0O0OOO0O000OO0 )==O0000O00000O00O00 :#line:3993
                            OOOOO00OO0OO0O000 =True #line:3994
                        else :#line:3995
                            OOOOO00OO0OO0O000 =False #line:3996
                    else :#line:3997
                        if OOO0O0OOO0O000OO0 ==O0000O00000O00O00 :#line:3998
                            OOOOO00OO0OO0O000 =True #line:3999
                        else :#line:4000
                            OOOOO00OO0OO0O000 =False #line:4001
                elif O000O000000O0OOOO :#line:4002
                    OOO0O0OOO0O000OO0 =O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]#line:4003
                    for O0O0O00000000OO00 in range (1 ,len (OO0OO00O0O0O0O0O0 )):#line:4004
                        OOO0O0OOO0O000OO0 =OOO0O0OOO0O000OO0 +O0OOO000OOO0O0O0O [OO0OO00O0O0O0O0O0 [O0O0O00000000OO00 ]]#line:4005
                        if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:4006
                            print ("after loop value: ",OOO0O0OOO0O000OO0 )#line:4007
                    if O00O0OO0O00O000O0 ==OO0O00O0OO0OO0OO0 .for_test :#line:4008
                        print ("value after adding given keys: ",OOO0O0OOO0O000OO0 )#line:4009
                    if 'absolute'in O0OOO0OOOO0000O0O :#line:4010
                        if abs (OOO0O0OOO0O000OO0 )==O0000O00000O00O00 :#line:4011
                            OOOOO00OO0OO0O000 =True #line:4012
                        else :#line:4013
                            OOOOO00OO0OO0O000 =False #line:4014
                    else :#line:4015
                        if OOO0O0OOO0O000OO0 ==O0000O00000O00O00 :#line:4016
                            OOOOO00OO0OO0O000 =True #line:4017
                        else :#line:4018
                            OOOOO00OO0OO0O000 =False #line:4019
        else :#line:4029
            if 'Intermediate'in O0O0OO0OO0OO0OOO0 :#line:4030
                if O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]==0 :#line:4032
                    OOOOO00OO0OO0O000 =False #line:4033
                elif O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]==1 :#line:4034
                    OOOOO00OO0OO0O000 =True #line:4035
                elif O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]==2 :#line:4036
                    OOOOO00OO0OO0O000 ='Unknown'#line:4037
            else :#line:4038
                if O0OOO000OOO0O0O0O [O0O0OO0OO0OO0OOO0 ]==O0000O00000O00O00 :#line:4039
                    OOOOO00OO0OO0O000 =True #line:4040
                else :#line:4041
                    OOOOO00OO0OO0O000 =False #line:4042
        return OOOOO00OO0OO0O000 ,OOO000OOOO0OOO00O #line:4044
    def outOfRange (O0OOO0O0O00O00O00 ,O0OO0O0OO0OO0O0OO ,OO0O0O0OO0O00OOOO ,O0O00O00000OOOOO0 ,OO00O0000OOOO000O ,OO0O0OOOOO0000OOO ,O0OO0000000O00O0O ,OOOOO0O0OO00O0O00 ):#line:4046
        OO0O0OOOOO0000OOO =OO0O0OOOOO0000OOO .replace ("]","")#line:4048
        OO0O0OOOOO0000OOO =OO0O0OOOOO0000OOO .replace ("[","")#line:4049
        OO0O0OOOOO0000OOO =OO0O0OOOOO0000OOO .replace ("'","")#line:4050
        OO0O0OOOOO0000OOO =OO0O0OOOOO0000OOO .split (",")#line:4051
        OOO0O00O0O0OO000O =float (OO0O0OOOOO0000OOO [0 ])#line:4052
        OO0OO000000OO0O00 =float (OO0O0OOOOO0000OOO [1 ])#line:4053
        if 'standard deviation'in O0OO0O0OO0OO0O0OO or 'moving average'in O0OO0O0OO0OO0O0OO :#line:4056
            O00O0OO00O0O00000 =OO0O0O0OO0O00OOOO [0 ]#line:4057
            if 'standard deviation'in O0OO0O0OO0OO0O0OO :#line:4058
                O00OOO00OOO0O00O0 =True #line:4059
            else :#line:4060
                O00OOO00OOO0O00O0 =False #line:4061
            if 'moving average'in O0OO0O0OO0OO0O0OO :#line:4062
                OOOOOO0OO0O0OO0O0 =True #line:4063
            else :#line:4064
                OOOOOO0OO0O0OO0O0 =False #line:4065
            O000OO000OOO0000O =int (OO0O0O0OO0O00OOOO [1 ])#line:4067
            O000OO00O000000O0 =1 #line:4068
            OOO000O00O00O000O =OOOOO0O0OO00O0O00 +"__"+O0O00O00000OOOOO0 #line:4069
            if OOO000O00O00O000O not in O0OOO0O0O00O00O00 .agg .keys ():#line:4070
                O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ]=[OO00O0000OOOO000O [O0O00O00000OOOOO0 ]]#line:4071
                O00O00O0O00O0O00O ='Unknown'#line:4072
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4073
                    print ("samples exist, but too short, appending one for now")#line:4074
                    print ('points',O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])#line:4075
            elif OOO000O00O00O000O in O0OOO0O0O00O00O00 .agg .keys ()and len (O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])+1 <O000OO000OOO0000O :#line:4077
                O00O00O0O00O0O00O ='Unknown'#line:4078
                O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ].append (OO00O0000OOOO000O [O0O00O00000OOOOO0 ])#line:4080
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4081
                    print ("samples exist, but too short, appending one for now")#line:4082
                    print ('points',O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])#line:4083
                O0OO0000000O00O0O ==False #line:4084
            elif OOO000O00O00O000O in O0OOO0O0O00O00O00 .agg .keys ()and len (O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])+1 ==O000OO000OOO0000O :#line:4085
                O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ].append (OO00O0000OOOO000O [O0O00O00000OOOOO0 ])#line:4087
                OOO0OO0O00OOOO00O =O0OOO0O0O00O00O00 .calcAggregate (O00OOO00OOO0O00O0 ,OOOOOO0OO0O0OO0O0 ,O0OOO0O0O00O00O00 .agg ,O0O00O00000OOOOO0 ,OOOOO0O0OO00O0O00 )#line:4088
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4089
                    print ("samples exist, but one short, appended one now and samples are OK for calculation")#line:4090
                    print ('points',O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])#line:4091
                    print ('agg value:',OOO0OO0O00OOOO00O )#line:4092
                    print ("low val:",OOO0O00O0O0OO000O )#line:4093
                    print ("high val:",OO0OO000000OO0O00 )#line:4094
                if OOO0OO0O00OOOO00O <OOO0O00O0O0OO000O or OOO0OO0O00OOOO00O >OO0OO000000OO0O00 :#line:4096
                    O00O00O0O00O0O00O =True #line:4097
                else :#line:4098
                    O00O00O0O00O0O00O =False #line:4099
            elif OOO000O00O00O000O in O0OOO0O0O00O00O00 .agg .keys ()and len (O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])+1 >O000OO000OOO0000O :#line:4101
                O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ].pop (0 )#line:4102
                O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ].append (OO00O0000OOOO000O [O0O00O00000OOOOO0 ])#line:4103
                OOO0OO0O00OOOO00O =O0OOO0O0O00O00O00 .calcAggregate (O00OOO00OOO0O00O0 ,OOOOOO0OO0O0OO0O0 ,O0O00O00000OOOOO0 ,OOOOO0O0OO00O0O00 )#line:4104
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4105
                    print ("samples more than sample size, appended latest and popped oldest and samples are OK for calculation")#line:4106
                    print ('points',O0OOO0O0O00O00O00 .agg [OOO000O00O00O000O ])#line:4107
                    print ('agg value:',OOO0OO0O00OOOO00O )#line:4108
                    print ("low val:",OOO0O00O0O0OO000O )#line:4109
                    print ("high val:",OO0OO000000OO0O00 )#line:4110
                if OOO0OO0O00OOOO00O <OOO0O00O0O0OO000O or OOO0OO0O00OOOO00O >OO0OO000000OO0O00 :#line:4112
                    O00O00O0O00O0O00O =True #line:4113
                else :#line:4114
                    O00O00O0O00O0O00O =False #line:4115
        elif 'subtract'in O0OO0O0OO0OO0O0OO or 'sum'in O0OO0O0OO0OO0O0OO :#line:4117
            if 'subtract'in O0OO0O0OO0OO0O0OO :#line:4118
                O0000000000O0O0OO =OO00O0000OOOO000O [O0O00O00000OOOOO0 ]#line:4119
                for OOOO000OO00000OO0 in range (1 ,len (OO0O0O0OO0O00OOOO )):#line:4120
                    O0000000000O0O0OO =O0000000000O0O0OO -OO00O0000OOOO000O [OO0O0O0OO0O00OOOO [OOOO000OO00000OO0 ]]#line:4121
                    if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4122
                        print ("after loop value: ",O0000000000O0O0OO )#line:4123
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4124
                    print ("value after subtracting given keys: ",O0000000000O0O0OO )#line:4125
                if 'absolute'in O0OO0O0OO0OO0O0OO :#line:4126
                    if abs (O0000000000O0O0OO )<OOO0O00O0O0OO000O or abs (O0000000000O0O0OO )>OO0OO000000OO0O00 :#line:4127
                        O00O00O0O00O0O00O =True #line:4128
                    else :#line:4129
                        O00O00O0O00O0O00O =False #line:4130
                else :#line:4131
                    if O0000000000O0O0OO <OOO0O00O0O0OO000O or O0000000000O0O0OO >OO0OO000000OO0O00 :#line:4132
                        O00O00O0O00O0O00O =True #line:4133
                    else :#line:4134
                        O00O00O0O00O0O00O =False #line:4135
            elif 'sum'in O0OO0O0OO0OO0O0OO :#line:4136
                O0000000000O0O0OO =OO00O0000OOOO000O [O0O00O00000OOOOO0 ]#line:4137
                for OOOO000OO00000OO0 in range (1 ,len (OO0O0O0OO0O00OOOO )):#line:4138
                    O0000000000O0O0OO =O0000000000O0O0OO +OO00O0000OOOO000O [OO0O0O0OO0O00OOOO [OOOO000OO00000OO0 ]]#line:4139
                    if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4140
                        print ("after loop value: ",O0000000000O0O0OO )#line:4141
                if OOOOO0O0OO00O0O00 ==O0OOO0O0O00O00O00 .for_test :#line:4142
                    print ("value after adding given keys: ",O0000000000O0O0OO )#line:4143
                if 'absolute'in O0OO0O0OO0OO0O0OO :#line:4144
                    if abs (O0000000000O0O0OO )<OOO0O00O0O0OO000O or abs (O0000000000O0O0OO )>OO0OO000000OO0O00 :#line:4145
                        O00O00O0O00O0O00O =True #line:4146
                    else :#line:4147
                        O00O00O0O00O0O00O =False #line:4148
                else :#line:4149
                    if O0000000000O0O0OO <OOO0O00O0O0OO000O or O0000000000O0O0OO >OO0OO000000OO0O00 :#line:4150
                        O00O00O0O00O0O00O =True #line:4151
                    else :#line:4152
                        O00O00O0O00O0O00O =False #line:4153
        else :#line:4155
            if OO00O0000OOOO000O [O0O00O00000OOOOO0 ]<OOO0O00O0O0OO000O or OO00O0000OOOO000O [O0O00O00000OOOOO0 ]>OO0OO000000OO0O00 :#line:4156
                O00O00O0O00O0O00O =True #line:4157
            else :#line:4158
                O00O00O0O00O0O00O =False #line:4159
        return O00O00O0O00O0O00O ,O0OO0000000O00O0O #line:4161
    def inRange (O00O000O0OOOOOO00 ,OO0O0OO0O000000O0 ,O0OO0O000OO00O0O0 ,OO0O0O0OOOOOO00OO ,OOOOO0OOO0000O0OO ,O00OO00OO0O0O0OO0 ,O0OO0OOOOOOO0O0OO ,OOO000O0000O00000 ):#line:4164
        O00OO00OO0O0O0OO0 =O00OO00OO0O0O0OO0 .replace ("]","")#line:4166
        O00OO00OO0O0O0OO0 =O00OO00OO0O0O0OO0 .replace ("[","")#line:4167
        O00OO00OO0O0O0OO0 =O00OO00OO0O0O0OO0 .replace ("'","")#line:4168
        O00OO00OO0O0O0OO0 =O00OO00OO0O0O0OO0 .split (",")#line:4169
        O000OOOO0OO000O00 =float (O00OO00OO0O0O0OO0 [0 ])#line:4171
        O0O00000OOO0000OO =float (O00OO00OO0O0O0OO0 [1 ])#line:4172
        if 'standard deviation'in OO0O0OO0O000000O0 or 'moving average'in OO0O0OO0O000000O0 :#line:4174
            OO0O000OO0O0OO00O =O0OO0O000OO00O0O0 [0 ]#line:4175
            if 'standard deviation'in OO0O0OO0O000000O0 :#line:4176
                O00O00O0O0O000O00 =True #line:4177
            else :#line:4178
                O00O00O0O0O000O00 =False #line:4179
            if 'moving average'in OO0O0OO0O000000O0 :#line:4180
                O00OO00000O0OO00O =True #line:4181
            else :#line:4182
                O00OO00000O0OO00O =False #line:4183
            O00OOO0O0OOOO0O00 =int (O0OO0O000OO00O0O0 [1 ])#line:4184
            O0OOOO000OO000O0O =1 #line:4185
            O000OOOO0OO00OOO0 =OOO000O0000O00000 +"__"+OO0O0O0OOOOOO00OO #line:4186
            if O000OOOO0OO00OOO0 not in O00O000O0OOOOOO00 .agg .keys ():#line:4187
                O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ]=[OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]]#line:4188
                O0OOO000000OO000O ='Unknown'#line:4189
                if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4190
                    print ("samples exist, but too short, appending one for now")#line:4191
                    print ('points',O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])#line:4192
            elif O000OOOO0OO00OOO0 in O00O000O0OOOOOO00 .agg .keys ()and len (O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])+1 <O00OOO0O0OOOO0O00 :#line:4194
                O0OOO000000OO000O ='Unknown'#line:4195
                O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ].append (OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ])#line:4196
                if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4197
                    print ("samples exist, but too short, appending one for now")#line:4198
                    print ('points',O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])#line:4199
                O0OO0OOOOOOO0O0OO ==False #line:4201
            elif O000OOOO0OO00OOO0 in O00O000O0OOOOOO00 .agg .keys ()and len (O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])+1 ==O00OOO0O0OOOO0O00 :#line:4202
                    O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ].append (OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ])#line:4203
                    O0O0O0O0OO0O0000O =O00O000O0OOOOOO00 .calcAggregate (O00O00O0O0O000O00 ,O00OO00000O0OO00O ,OO0O0O0OOOOOO00OO ,OOO000O0000O00000 )#line:4204
                    if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4205
                        print ("samples exist, but one short, appended one now and samples are OK for calculation")#line:4206
                        print ('points',O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])#line:4207
                        print ('agg value:',O0O0O0O0OO0O0000O )#line:4208
                        print ("low val:",O000OOOO0OO000O00 )#line:4209
                        print ("high val:",O0O00000OOO0000OO )#line:4210
                    if (O0O0O0O0OO0O0000O >O000OOOO0OO000O00 or O0O0O0O0OO0O0000O ==O000OOOO0OO000O00 )and (O0O0O0O0OO0O0000O <O0O00000OOO0000OO or O0O0O0O0OO0O0000O ==O0O00000OOO0000OO ):#line:4211
                        O0OOO000000OO000O =True #line:4212
                    else :#line:4213
                        O0OOO000000OO000O =False #line:4214
            elif O000OOOO0OO00OOO0 in O00O000O0OOOOOO00 .agg .keys ()and len (O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])+1 >O00OOO0O0OOOO0O00 :#line:4215
                    O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ].pop (0 )#line:4216
                    O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ].append (OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ])#line:4217
                    O0O0O0O0OO0O0000O =O00O000O0OOOOOO00 .calcAggregate (O00O00O0O0O000O00 ,O00OO00000O0OO00O ,OO0O0O0OOOOOO00OO ,OOO000O0000O00000 )#line:4218
                    if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4219
                        print ("samples more than sample size, appended latest and popped oldest and samples are OK for calculation")#line:4220
                        print ('points',O00O000O0OOOOOO00 .agg [O000OOOO0OO00OOO0 ])#line:4221
                        print ('agg value:',O0O0O0O0OO0O0000O )#line:4222
                        print ("low val:",O000OOOO0OO000O00 )#line:4223
                        print ("high val:",O0O00000OOO0000OO )#line:4224
                    if (O0O0O0O0OO0O0000O >O000OOOO0OO000O00 or O0O0O0O0OO0O0000O ==O000OOOO0OO000O00 )and (O0O0O0O0OO0O0000O <O0O00000OOO0000OO or O0O0O0O0OO0O0000O ==O0O00000OOO0000OO ):#line:4226
                        O0OOO000000OO000O =True #line:4227
                    else :#line:4228
                        O0OOO000000OO000O =False #line:4229
        elif 'subtract'in OO0O0OO0O000000O0 or 'sum'in OO0O0OO0O000000O0 :#line:4231
            if 'subtract'in OO0O0OO0O000000O0 :#line:4232
                OOOO00000O0OO0000 =OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]#line:4233
                for OO0O0O0O0O0O0O0OO in range (1 ,len (O0OO0O000OO00O0O0 )):#line:4234
                    OOOO00000O0OO0000 =OOOO00000O0OO0000 -OOOOO0OOO0000O0OO [O0OO0O000OO00O0O0 [OO0O0O0O0O0O0O0OO ]]#line:4235
                    if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4236
                        print ("after loop value: ",OOOO00000O0OO0000 )#line:4237
                if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4238
                    print ("value after subtracting given keys: ",OOOO00000O0OO0000 )#line:4239
                if 'absolute'in OO0O0OO0O000000O0 :#line:4240
                    if (abs (OOOO00000O0OO0000 )>O000OOOO0OO000O00 or abs (OOOO00000O0OO0000 )==O000OOOO0OO000O00 )and (abs (OOOO00000O0OO0000 )<O0O00000OOO0000OO or abs (OOOO00000O0OO0000 )==O0O00000OOO0000OO ):#line:4241
                        O0OOO000000OO000O =True #line:4242
                    else :#line:4243
                        O0OOO000000OO000O =False #line:4244
                else :#line:4245
                    if (OOOO00000O0OO0000 >O000OOOO0OO000O00 or OOOO00000O0OO0000 ==O000OOOO0OO000O00 )and (OOOO00000O0OO0000 <O0O00000OOO0000OO or OOOO00000O0OO0000 ==O0O00000OOO0000OO ):#line:4246
                        O0OOO000000OO000O =True #line:4247
                    else :#line:4248
                        O0OOO000000OO000O =False #line:4249
            elif 'sum'in OO0O0OO0O000000O0 :#line:4250
                OOOO00000O0OO0000 =OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]#line:4251
                for OO0O0O0O0O0O0O0OO in range (1 ,len (O0OO0O000OO00O0O0 )):#line:4252
                    OOOO00000O0OO0000 =OOOO00000O0OO0000 +OOOOO0OOO0000O0OO [O0OO0O000OO00O0O0 [OO0O0O0O0O0O0O0OO ]]#line:4253
                    if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4254
                        print ("after loop value: ",OOOO00000O0OO0000 )#line:4255
                if OOO000O0000O00000 ==O00O000O0OOOOOO00 .for_test :#line:4256
                    print ("value after adding given keys: ",OOOO00000O0OO0000 )#line:4257
                if 'absolute'in OO0O0OO0O000000O0 :#line:4258
                    if (abs (OOOO00000O0OO0000 )>O000OOOO0OO000O00 or abs (OOOO00000O0OO0000 )==O000OOOO0OO000O00 )and (abs (OOOO00000O0OO0000 )<O0O00000OOO0000OO or abs (OOOO00000O0OO0000 )==O0O00000OOO0000OO ):#line:4259
                        O0OOO000000OO000O =True #line:4260
                    else :#line:4261
                        O0OOO000000OO000O =False #line:4262
                else :#line:4263
                    if (OOOO00000O0OO0000 >O000OOOO0OO000O00 or OOOO00000O0OO0000 ==O000OOOO0OO000O00 )and (OOOO00000O0OO0000 <O0O00000OOO0000OO or OOOO00000O0OO0000 ==O0O00000OOO0000OO ):#line:4264
                        O0OOO000000OO000O =True #line:4265
                    else :#line:4266
                        O0OOO000000OO000O =False #line:4267
        else :#line:4269
            if (OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]>O000OOOO0OO000O00 or OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]==O000OOOO0OO000O00 )and (OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]<O0O00000OOO0000OO or OOOOO0OOO0000O0OO [OO0O0O0OOOOOO00OO ]==O0O00000OOO0000OO ):#line:4270
                O0OOO000000OO000O =True #line:4271
            else :#line:4272
                O0OOO000000OO000O =False #line:4273
        return O0OOO000000OO000O ,O0OO0OOOOOOO0O0OO #line:4275
    def eventSoFar (OO0O00O0O0O0OO0O0 ,O00000OO000000OO0 ,O0O00OO000O0OOOO0 ,OOO00O0OO000O00O0 ,O00O00O0OOO000OOO ):#line:4277
        if O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 ==True :#line:4278
            OOO00O0OO000O00O0 =True #line:4279
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4280
                print ('fell into condition 1 of eventsofar func')#line:4281
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='AND'and OOO00O0OO000O00O0 ==True :#line:4282
            OOO00O0OO000O00O0 =True #line:4283
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4284
                print ('fell into condition 2 of eventsofar func')#line:4285
        elif O00000OO000000OO0 ==False and O0O00OO000O0OOOO0 =='AND'and OOO00O0OO000O00O0 ==True :#line:4286
            OOO00O0OO000O00O0 =False #line:4287
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4288
                print ('fell into condition 3 of eventsofar func')#line:4289
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='AND'and OOO00O0OO000O00O0 =='Unknown':#line:4290
            OOO00O0OO000O00O0 ='Unknown'#line:4291
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4292
                print ('fell into condition 4 of eventsofar func')#line:4293
        elif O00000OO000000OO0 =='Unknown'and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 ==True :#line:4294
            OOO00O0OO000O00O0 =True #line:4295
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4296
                print ('fell into condition 5 of eventsofar func')#line:4297
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 =='Unknown':#line:4298
            OOO00O0OO000O00O0 =True #line:4299
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4300
                print ('fell into condition 6 of eventsofar func')#line:4301
        elif O00000OO000000OO0 =='Unknown'and O0O00OO000O0OOOO0 =='AND'and OOO00O0OO000O00O0 ==True :#line:4302
            OOO00O0OO000O00O0 ='Unknown'#line:4304
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4305
                print ('fell into condition 7 of eventsofar func')#line:4306
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 ==True :#line:4307
            OOO00O0OO000O00O0 =True #line:4309
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4310
                print ('fell into condition 8 of eventsofar func')#line:4311
        elif O00000OO000000OO0 ==False and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 ==True :#line:4312
            OOO00O0OO000O00O0 =True #line:4313
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4314
                print ('fell into condition 9 of eventsofar func')#line:4315
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='OR'and OOO00O0OO000O00O0 ==False :#line:4316
            OOO00O0OO000O00O0 =True #line:4317
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4318
                print ('fell into condition 10 of eventsofar func')#line:4319
        elif O00000OO000000OO0 ==True and O0O00OO000O0OOOO0 =='AND'and OOO00O0OO000O00O0 ==False :#line:4320
            OOO00O0OO000O00O0 =False #line:4321
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4322
                print ('fell into condition 11 of eventsofar func')#line:4323
        elif (O00000OO000000OO0 =='Unknown'and OOO00O0OO000O00O0 ==False )and (O0O00OO000O0OOOO0 =='AND'):#line:4324
            OOO00O0OO000O00O0 =False #line:4325
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4326
                print ('fell into condition 12 of eventsofar func')#line:4327
        elif (O00000OO000000OO0 =='Unknown'and OOO00O0OO000O00O0 ==False )and (O0O00OO000O0OOOO0 =='OR'):#line:4328
            OOO00O0OO000O00O0 ='Unknown'#line:4329
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4330
                print ('fell into condition 13 of eventsofar func')#line:4331
        elif (O00000OO000000OO0 ==False and OOO00O0OO000O00O0 =='Unknown')and (O0O00OO000O0OOOO0 =='OR'):#line:4332
            OOO00O0OO000O00O0 ='Unknown'#line:4333
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4334
                print ('fell into condition 14 of eventsofar func')#line:4335
        elif (O00000OO000000OO0 ==False and OOO00O0OO000O00O0 =='Unknown')and (O0O00OO000O0OOOO0 =='AND'):#line:4336
            OOO00O0OO000O00O0 =False #line:4337
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4338
                print ('fell into condition 15 of eventsofar func')#line:4339
        elif (O00000OO000000OO0 =='Unknown'and OOO00O0OO000O00O0 =='Unknown')and (O0O00OO000O0OOOO0 =='OR'or O0O00OO000O0OOOO0 =='AND'):#line:4340
            OOO00O0OO000O00O0 ='Unknown'#line:4341
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4342
                print ('fell into condition 16 of eventsofar func')#line:4343
        elif (O00000OO000000OO0 ==False and OOO00O0OO000O00O0 ==False )and (O0O00OO000O0OOOO0 =='OR'or O0O00OO000O0OOOO0 =='AND'):#line:4344
            OOO00O0OO000O00O0 =False #line:4345
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4346
                print ('fell into condition 17 of eventsofar func')#line:4347
        else :#line:4348
            OOO00O0OO000O00O0 ='Unknown'#line:4349
            if O00O00O0OOO000OOO ==OO0O00O0O0O0OO0O0 .for_test :#line:4350
                print ('fell into last else condition of eventsofar func')#line:4351
        return OOO00O0OO000O00O0 #line:4353
    def lineStatus (OOOO000OO000OO0O0 ,OOOOOOOO0O0000000 ,OO000OO00OO0O0OOO ,O0000OO000OO0OO0O ,O0OOO00O0000O0000 ,OOO0OO0OOO0OOO0O0 ,O0000O00O0O0OO00O ,OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0OO00O00OOO000OO ,OOO000O0O00OOO00O ,OO000O00O000000OO ,O00O0O000OO0OOOOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ):#line:4356
        if OOOOOOOO0O0000000 ==True :#line:4359
            if str (O00O0O000OO0OOOOO )=='0.0':#line:4361
                print ('implement is 0, so event of this line is Unknown')#line:4362
                OO000OO00OO0O0OOO ='Unknown'#line:4363
                OOOOOOOO0O0000000 =True #line:4364
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4365
                    print ("this line is not implemented, event is: ",OO000OO00OO0O0OOO )#line:4366
                    print ("-------------")#line:4367
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4368
            elif O0OO00O00OOO000OO =='>':#line:4369
                OO000OO00OO0O0OOO ,OOOOOOOO0O0000000 =OOOO000OO000OO0O0 .moreThan (OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0000O00O0O0OO00O ,O0OOO00O0000O0000 ,OOO000O0O00OOO00O ,OOOOOOOO0O0000000 ,O0OO00O0OOO00000O )#line:4371
                if 'True'in O0O000000O0O0OO00 :#line:4375
                    OO000OO00OO0O0OOO =OOOO000OO000OO0O0 .persistenceCheck (OO000OO00OO0O0OOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ,O0000O00O0O0OO00O )#line:4376
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4378
                    print ("this line's status:",OO000OO00OO0O0OOO ,"logic:",OO000O00O000000OO ,"status comes from above:",O0000OO000OO0OO0O )#line:4380
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4381
            elif O0OO00O00OOO000OO =='<':#line:4383
                OO000OO00OO0O0OOO ,OOOOOOOO0O0000000 =OOOO000OO000OO0O0 .lessThan (OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0000O00O0O0OO00O ,O0OOO00O0000O0000 ,OOO000O0O00OOO00O ,OOOOOOOO0O0000000 ,O0OO00O0OOO00000O )#line:4385
                if 'True'in O0O000000O0O0OO00 :#line:4387
                    OO000OO00OO0O0OOO =OOOO000OO000OO0O0 .persistenceCheck (OO000OO00OO0O0OOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ,O0000O00O0O0OO00O )#line:4388
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4390
                    print ("this line's status:",OO000OO00OO0O0OOO ,"logic:",OO000O00O000000OO ,"status comes from above:",O0000OO000OO0OO0O )#line:4392
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4393
            elif O0OO00O00OOO000OO =='=':#line:4395
                OO000OO00OO0O0OOO ,OOOOOOOO0O0000000 =OOOO000OO000OO0O0 .equalTo (OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0000O00O0O0OO00O ,O0OOO00O0000O0000 ,OOO000O0O00OOO00O ,OOOOOOOO0O0000000 ,O0OO00O0OOO00000O )#line:4397
                if 'True'in O0O000000O0O0OO00 :#line:4399
                    OO000OO00OO0O0OOO =OOOO000OO000OO0O0 .persistenceCheck (OO000OO00OO0O0OOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ,O0000O00O0O0OO00O )#line:4400
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4402
                    print ("this line's status:",OO000OO00OO0O0OOO ,"logic:",OO000O00O000000OO ,"status comes from above:",O0000OO000OO0OO0O )#line:4404
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4405
            elif O0OO00O00OOO000OO =='][':#line:4407
                OO000OO00OO0O0OOO ,OOOOOOOO0O0000000 =OOOO000OO000OO0O0 .outOfRange (OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0000O00O0O0OO00O ,O0OOO00O0000O0000 ,OOO000O0O00OOO00O ,OOOOOOOO0O0000000 ,O0OO00O0OOO00000O )#line:4409
                if 'True'in O0O000000O0O0OO00 :#line:4411
                    OO000OO00OO0O0OOO =OOOO000OO000OO0O0 .persistenceCheck (OO000OO00OO0O0OOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ,O0000O00O0O0OO00O )#line:4412
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4414
                    print ("this line's status:",OO000OO00OO0O0OOO ,"logic:",OO000O00O000000OO ,"status comes from above:",O0000OO000OO0OO0O )#line:4416
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4417
            elif O0OO00O00OOO000OO =='[]'or O0OO00O00OOO000OO =='NOT ][':#line:4419
                OO000OO00OO0O0OOO ,OOOOOOOO0O0000000 =OOOO000OO000OO0O0 .inRange (OO00O00OOOOOOOOOO ,O0000000OOOO00OOO ,O0000O00O0O0OO00O ,O0OOO00O0000O0000 ,OOO000O0O00OOO00O ,OOOOOOOO0O0000000 ,O0OO00O0OOO00000O )#line:4421
                if 'True'in O0O000000O0O0OO00 :#line:4423
                    OO000OO00OO0O0OOO =OOOO000OO000OO0O0 .persistenceCheck (OO000OO00OO0O0OOO ,O0O000000O0O0OO00 ,O000O00O0O00OOOOO ,O0OO00O0OOO00000O ,O0000O00O0O0OO00O )#line:4424
                if O0OO00O0OOO00000O ==OOOO000OO000OO0O0 .for_test :#line:4426
                    print ("this line's status:",OO000OO00OO0O0OOO ,"logic:",OO000O00O000000OO ,"status comes from above:",O0000OO000OO0OO0O )#line:4428
                O0000OO000OO0OO0O =OOOO000OO000OO0O0 .eventSoFar (OO000OO00OO0O0OOO ,OO000O00O000000OO ,O0000OO000OO0OO0O ,O0OO00O0OOO00000O )#line:4429
        else :#line:4430
            OOOOOOOO0O0000000 =False #line:4431
        return O0000OO000OO0OO0O ,OOOOOOOO0O0000000 #line:4433
    def createVariables (OO000000OOOO000O0 ,O000OO00O000O0000 ,OOOO0OO0OOO00OO0O ):#line:4435
        O0OO0OO00O00O0000 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Problem_Name']#line:4437
        OOO0OOO000OOOO00O =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Standard_Key']#line:4439
        O0OOO0OOOOOO0OO00 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Additional condition']#line:4440
        O0OO000O0000O0O00 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Additional condition'].split (",")#line:4441
        O0O000O0OOOO00OO0 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Condition']#line:4442
        OO0O00O00O0O0OO00 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Threshold']#line:4443
        OOOO000O00OOOO00O =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 -1 ]['Logic']#line:4444
        O0000OOO0OO000OOO =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Implement']#line:4445
        if OO000000OOOO000O0 .test_run ==1 :#line:4446
            if OOO0OOO000OOOO00O =='NS_IG010-XA_PV'or OOO0OOO000OOOO00O =='NS_AN_NG2-00273_PV':#line:4447
                O0000OOO0OO000OOO =0 #line:4448
            else :#line:4449
                O0000OOO0OO000OOO =1 #line:4450
        O000000OOOOO00O00 =OOOO0OO0OOO00OO0O .loc [O000OO00O000O0000 ]['Persistence'].split (",")#line:4451
        OOOO0O0000000OO0O =1 #line:4452
        if 'True'in O000000OOOOO00O00 :#line:4453
            OOOO0O0000000OO0O =int (O000000OOOOO00O00 [1 ])#line:4454
        return O0OO0OO00O00O0000 ,OOO0OOO000OOOO00O ,O0OOO0OOOOOO0OO00 ,O0OO000O0000O0O00 ,O0O000O0OOOO00OO0 ,OO0O00O00O0O0OO00 ,OOOO000O00OOOO00O ,O0000OOO0OO000OOO ,O000000OOOOO00O00 ,OOOO0O0000000OO0O #line:4459
    def persistenceCheck (OOOOOOO0O0O000O0O ,O00OOOO0OOOOOOO00 ,O0O00OO00O0OO0OOO ,OO00O0O000OO0OOOO ,O00OOOOO0OOO0O0OO ,OOOO00OOO000O0OO0 ):#line:4461
        O0000O0000O000OO0 =O00OOOOO0OOO0O0OO +"__"+OOOO00OOO000O0OO0 #line:4463
        if O00OOOO0OOOOOOO00 ==True and ('True'in O0O00OO00O0OO0OOO ):#line:4464
            if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4465
                print ("persistence to apply")#line:4466
            if O00OOOO0OOOOOOO00 ==True and O0000O0000O000OO0 not in OOOOOOO0O0O000O0O .persistence .keys ():#line:4467
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ]=[O00OOOO0OOOOOOO00 ]#line:4468
                O00OOOO0OOOOOOO00 ='Unknown'#line:4469
                if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4470
                    print ("fell into 1st condition of persistence (no samples present). event is: ",O00OOOO0OOOOOOO00 )#line:4471
            elif (O0000O0000O000OO0 in OOOOOOO0O0O000O0O .persistence .keys ())and len (OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ])+1 <OO00O0O000OO0OOOO :#line:4472
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ].append (O00OOOO0OOOOOOO00 )#line:4473
                O00OOOO0OOOOOOO00 ='Unknown'#line:4474
                if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4475
                    print ("fell into 2nd condition of persistence (sample exist but short). event is: ",O00OOOO0OOOOOOO00 )#line:4476
            elif (O0000O0000O000OO0 in OOOOOOO0O0O000O0O .persistence .keys ())and len (OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ])+1 ==OO00O0O000OO0OOOO :#line:4477
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ].append (O00OOOO0OOOOOOO00 )#line:4478
                O00OOOO0OOOOOOO00 =True #line:4479
                if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4480
                    print ("fell into 3rd condition of persistence (samples are one short, but appended one now and now equal to persistence duration). event is: ",O00OOOO0OOOOOOO00 )#line:4481
            elif (O0000O0000O000OO0 in OOOOOOO0O0O000O0O .persistence .keys ())and len (OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ])+1 >OO00O0O000OO0OOOO :#line:4482
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ].pop (0 )#line:4483
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ].append (O00OOOO0OOOOOOO00 )#line:4484
                O00OOOO0OOOOOOO00 =True #line:4485
                if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4486
                    print ("fell into 4th condition of persistence (samples more than persistence duration, latest is appended and oldest is popped). event is: ",O00OOOO0OOOOOOO00 )#line:4487
        elif ('True'in O0O00OO00O0OO0OOO )and O00OOOO0OOOOOOO00 !=True :#line:4488
            if O0000O0000O000OO0 in OOOOOOO0O0O000O0O .persistence .keys ():#line:4489
                OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ]=[]#line:4490
                if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4491
                    print ("fell into 5th condition of persistence (persistence is reset as event is not active). event is: ",O00OOOO0OOOOOOO00 )#line:4492
        if O00OOOOO0OOO0O0OO ==OOOOOOO0O0O000O0O .for_test :#line:4494
            if O0000O0000O000OO0 in OOOOOOO0O0O000O0O .persistence .keys ():#line:4495
                print ("persistence stored for ",O0000O0000O000OO0 ," are: ",OOOOOOO0O0O000O0O .persistence [O0000O0000O000OO0 ])#line:4496
            else :#line:4497
                print ("persistence check => ",O0000O0000O000OO0 ," is yet not available in persistence dict because it has not been triggered yet, probably due to additional condition.")#line:4498
        return O00OOOO0OOOOOOO00 #line:4499
    def rcaTemplatesReader (OOOOOO00000OOO000 ,O000OOOOOO00OOO0O ,OO0OO000000OO0OO0 ,O0O00O0OOOO0O0000 ,OO00O00O00000OO00 ):#line:4504
        OO0OOO0OOO000O0O0 ={}#line:4506
        OO00OO0OOO0O00O00 ={}#line:4507
        O0O0OO0O0O000000O =['LD1','LD2','HD1','HD2','LNGV','FV','BOGH','WUH','GWH','SC','IG','NG1','NG2','ME1','ME2','MEEG','GEEG','AB','VA','LO','BLST','BLG','GE1','GE2','GE3','GE4','CT1','CT2','CT3','CT4','FW','FO','MEFG','GEFG','GCU','INCIN']#line:4511
        for OOOOO00O0OO0O000O in range (len (O000OOOOOO00OOO0O )):#line:4515
            if O0O00O0OOOO0O0000 [O0O0OO0O0O000000O [OOOOO00O0OO0O000O ]]==1 :#line:4516
                print (f"starting rca template: {O0O0OO0O0O000000O[OOOOO00O0OO0O000O]}")#line:4517
                O0000O0O00OOOO000 =O000OOOOOO00OOO0O [OOOOO00O0OO0O000O ]#line:4518
                O0000O0O00OOOO000 =O0000O0O00OOOO000 .loc [:,:'Implement']#line:4522
                O0000O0O00OOOO000 .fillna ('blank',inplace =True )#line:4523
                O000OOO00000OOOOO =O0000O0O00OOOO000 ['Implement']==1.0 #line:4525
                O0000O0O00OOOO000 =O0000O0O00OOOO000 [O000OOO00000OOOOO ].reset_index ()#line:4527
                O0000O0O00OOOO000 =O0000O0O00OOOO000 .drop (columns =['index'],axis =1 )#line:4528
                O0OOO000OOO000O00 ='start_of_sheet'#line:4532
                OOO0O0O0O0OO00O00 =True #line:4534
                O0000OO00O0O00OO0 ='none'#line:4535
                for OOO00OO0OOOOO0OOO in range (len (O0000O0O00OOOO000 .index )):#line:4543
                    OOOOOOO0O0O000000 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Problem_Name']#line:4544
                    OO0OOO000OOO00000 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Standard_Key']#line:4546
                    O0O0OOOOO0O00OO0O =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Additional condition']#line:4547
                    O0OOO0OO0000OOOO0 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Additional condition'].split (",")#line:4548
                    OO0O0OOO00OO0OOOO =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Condition']#line:4549
                    OOOO0O0O0O00OO0O0 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Threshold']#line:4550
                    O0OOO00O0000O0OO0 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Persistence'].split (",")#line:4551
                    OO00O0OO0O0O0O00O =1 #line:4552
                    if 'True'in O0OOO00O0000O0OO0 :#line:4553
                        OO00O0OO0O0O0O00O =int (O0OOO00O0000O0OO0 [1 ])#line:4554
                    OOOO0OO000O0000O0 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Implement']#line:4555
                    if OOOOOO00000OOO000 .test_run ==1 :#line:4556
                        if OO0OOO000OOO00000 =='NS_IG010-XA_PV'or OO0OOO000OOO00000 =='NS_AN_NG2-00273_PV':#line:4557
                            OOOO0OO000O0000O0 =0 #line:4558
                        else :#line:4559
                            OOOO0OO000O0000O0 =1 #line:4560
                    OOO0O0OOO0O00OOOO =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Level']#line:4562
                    O000O000OOO0OO0OO =str (O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Run Check'])#line:4563
                    if OOO0O0OOO0O00OOOO =='COMPONENT':#line:4565
                        if O000O000OOO0OO0OO =='1.0':#line:4566
                            if O0O00O0OOOO0O0000 [OOOOOOO0O0O000000 ]==1 :#line:4567
                                OOO0O0O0O0OO00O00 =True #line:4568
                            else :#line:4569
                                OOO0O0O0O0OO00O00 =False #line:4570
                        else :#line:4571
                            OOO0O0O0O0OO00O00 =True #line:4572
                    if OOO0O0O0O0OO00O00 :#line:4574
                        if OOOOOOO0O0O000000 !=O0OOO000OOO000O00 and OO00O00O00000OO00 [OOOOOOO0O0O000000 ]==1 :#line:4577
                            O0OOO000OOO000O00 =OOOOOOO0O0O000000 #line:4578
                            OO00OO0OOO0O00O00 [OOOOOOO0O0O000000 ]=O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Parent_Node']#line:4579
                            O0OO00OO000O0OO00 =True #line:4581
                            if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4582
                                    print (OOOOOOO0O0O000000 ,"started")#line:4583
                            if O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Standard_Key']=='blank':#line:4585
                                O000OOO000000O0O0 ='Unknown'#line:4586
                                O0OO00OO000O0OO00 =False #line:4587
                            else :#line:4589
                                O000OOO000000O0O0 =False #line:4590
                            if str (OOOO0OO000O0000O0 )=='0.0':#line:4592
                                O000OOO000000O0O0 ='Unknown'#line:4593
                                O0OO00OO000O0OO00 =True #line:4594
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4595
                                    print ("this line is not implemented, event is: ",O000OOO000000O0O0 )#line:4596
                            elif OO0O0OOO00OO0OOOO =='>':#line:4598
                                O000OOO000000O0O0 ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .moreThan (O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0OOO000OOO00000 ,OO0OO000000OO0OO0 ,OOOO0O0O0O00OO0O0 ,O0OO00OO000O0OO00 ,OOOOOOO0O0O000000 )#line:4601
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4602
                                    print ("data of 1st line: ",OO0OOO000OOO00000 ," ",OO0O0OOO00OO0OOOO ," ",OOOO0O0O0O00OO0O0 ," ",O0OOO0OO0000OOOO0 )#line:4603
                                    print ("event of 1st line: ",O000OOO000000O0O0 )#line:4604
                            elif OO0O0OOO00OO0OOOO =='<':#line:4606
                                O000OOO000000O0O0 ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lessThan (O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0OOO000OOO00000 ,OO0OO000000OO0OO0 ,OOOO0O0O0O00OO0O0 ,O0OO00OO000O0OO00 ,OOOOOOO0O0O000000 )#line:4608
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4609
                                    print ("data of 1st line: ",OO0OOO000OOO00000 ," ",OO0O0OOO00OO0OOOO ," ",OOOO0O0O0O00OO0O0 ," ",O0OOO0OO0000OOOO0 )#line:4610
                                    print ("event of 1st line: ",O000OOO000000O0O0 )#line:4611
                            elif OO0O0OOO00OO0OOOO =='=':#line:4613
                                O000OOO000000O0O0 ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .equalTo (O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0OOO000OOO00000 ,OO0OO000000OO0OO0 ,OOOO0O0O0O00OO0O0 ,O0OO00OO000O0OO00 ,OOOOOOO0O0O000000 )#line:4615
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4616
                                    print ("data of 1st line: ",OO0OOO000OOO00000 ," ",OO0O0OOO00OO0OOOO ," ",OOOO0O0O0O00OO0O0 ," ",O0OOO0OO0000OOOO0 )#line:4617
                                    print ("event of 1st line: ",O000OOO000000O0O0 )#line:4618
                            elif OO0O0OOO00OO0OOOO =='][':#line:4620
                                O000OOO000000O0O0 ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .outOfRange (O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0OOO000OOO00000 ,OO0OO000000OO0OO0 ,OOOO0O0O0O00OO0O0 ,O0OO00OO000O0OO00 ,OOOOOOO0O0O000000 )#line:4622
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4623
                                    print ("data of 1st line: ",OO0OOO000OOO00000 ," ",OO0O0OOO00OO0OOOO ," ",OOOO0O0O0O00OO0O0 ," ",O0OOO0OO0000OOOO0 )#line:4624
                                    print ("event of 1st line: ",O000OOO000000O0O0 )#line:4625
                            elif OO0O0OOO00OO0OOOO =='[]'or OO0O0OOO00OO0OOOO =='NOT ][':#line:4627
                                O000OOO000000O0O0 ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .inRange (O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0OOO000OOO00000 ,OO0OO000000OO0OO0 ,OOOO0O0O0O00OO0O0 ,O0OO00OO000O0OO00 ,OOOOOOO0O0O000000 )#line:4629
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4630
                                    print ("data of 1st line: ",OO0OOO000OOO00000 ," ",OO0O0OOO00OO0OOOO ," ",OOOO0O0O0O00OO0O0 ," ",O0OOO0OO0000OOOO0 )#line:4631
                                    print ("event of 1st line: ",O000OOO000000O0O0 )#line:4632
                            if 'True'in O0OOO00O0000O0OO0 :#line:4637
                                O000OOO000000O0O0 =OOOOOO00000OOO000 .persistenceCheck (O000OOO000000O0O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 ,OO0OOO000OOO00000 )#line:4638
                            OOO0O0000O0000OOO =O000OOO000000O0O0 #line:4641
                            if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4642
                                print (OOOOOOO0O0O000000 ,"=> after line 1 event so far =>",OOO0O0000O0000OOO ,", and it will go to the lines below")#line:4643
                                print ("-------------")#line:4644
                            if OOO00OO0OOOOO0OOO +1 <len (O0000O0O00OOOO000 .index )and O0OO00OO000O0OO00 ==True :#line:4646
                                O0O00OOO00O00O00O =OOO00OO0OOOOO0OOO +1 #line:4648
                                O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O =OOOOOO00000OOO000 .createVariables (O0O00OOO00O00O00O ,O0000O0O00OOOO000 )#line:4649
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4650
                                    print ("line 2 data =>",O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 )#line:4651
                                if O00000OO0OOOO00OO !=O0OOO000OOO000O00 :#line:4653
                                    O0OO00OO000O0OO00 =False #line:4654
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4655
                                        print ("********* end of rule *********")#line:4656
                                        print ("this line has another scenario started, so this line will not be processed")#line:4657
                                if O0OO00OO000O0OO00 ==True :#line:4658
                                    OOO0O0000O0000OOO ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lineStatus (O0OO00OO000O0OO00 ,O000OOO000000O0O0 ,OOO0O0000O0000OOO ,OO0OO000000OO0OO0 ,O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 )#line:4660
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4661
                                        print (OOOOOOO0O0O000000 ,"after line 2 =>",OOO0O0000O0000OOO )#line:4662
                                        print ("-------------")#line:4663
                            if OOO00OO0OOOOO0OOO +2 <len (O0000O0O00OOOO000 .index )and O0OO00OO000O0OO00 ==True :#line:4665
                                O0O00OOO00O00O00O =OOO00OO0OOOOO0OOO +2 #line:4667
                                O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O =OOOOOO00000OOO000 .createVariables (O0O00OOO00O00O00O ,O0000O0O00OOOO000 )#line:4668
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4669
                                    print ("line 3 data =>",O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 )#line:4670
                                if O00000OO0OOOO00OO !=O0OOO000OOO000O00 :#line:4672
                                    O0OO00OO000O0OO00 =False #line:4673
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4674
                                        print ("********* end of rule *********")#line:4675
                                        print ("this line has another scenario started, this line will not be processed")#line:4676
                                if O0OO00OO000O0OO00 ==True :#line:4677
                                    OOO0O0000O0000OOO ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lineStatus (O0OO00OO000O0OO00 ,O000OOO000000O0O0 ,OOO0O0000O0000OOO ,OO0OO000000OO0OO0 ,O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 )#line:4679
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4680
                                        print (OOOOOOO0O0O000000 ,"after line 3 =>",OOO0O0000O0000OOO )#line:4681
                                        print ("-------------")#line:4682
                            if OOO00OO0OOOOO0OOO +3 <len (O0000O0O00OOOO000 .index )and O0OO00OO000O0OO00 ==True :#line:4684
                                O0O00OOO00O00O00O =OOO00OO0OOOOO0OOO +3 #line:4686
                                O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O =OOOOOO00000OOO000 .createVariables (O0O00OOO00O00O00O ,O0000O0O00OOOO000 )#line:4687
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4688
                                    print ("line 4 data =>",O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 )#line:4689
                                if O00000OO0OOOO00OO !=O0OOO000OOO000O00 :#line:4691
                                    O0OO00OO000O0OO00 =False #line:4692
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4693
                                        print ("********* end of rule *********")#line:4694
                                        print ("this line has another scenario started, this line will not be processed")#line:4695
                                if O0OO00OO000O0OO00 ==True :#line:4696
                                    OOO0O0000O0000OOO ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lineStatus (O0OO00OO000O0OO00 ,O000OOO000000O0O0 ,OOO0O0000O0000OOO ,OO0OO000000OO0OO0 ,O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 )#line:4698
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4699
                                        print (OOOOOOO0O0O000000 ,"after line 4 =>",OOO0O0000O0000OOO )#line:4700
                                        print ("-------------")#line:4701
                            if OOO00OO0OOOOO0OOO +4 <len (O0000O0O00OOOO000 .index )and O0OO00OO000O0OO00 ==True :#line:4703
                                O0O00OOO00O00O00O =OOO00OO0OOOOO0OOO +4 #line:4705
                                O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O =OOOOOO00000OOO000 .createVariables (O0O00OOO00O00O00O ,O0000O0O00OOOO000 )#line:4706
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4707
                                    print ("line 5 data =>",O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 )#line:4708
                                if O00000OO0OOOO00OO !=O0OOO000OOO000O00 :#line:4710
                                    O0OO00OO000O0OO00 =False #line:4711
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4712
                                        print ("********* end of rule *********")#line:4713
                                        print ("this line has another scenario started, this line will not be processed")#line:4714
                                if O0OO00OO000O0OO00 ==True :#line:4715
                                    OOO0O0000O0000OOO ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lineStatus (O0OO00OO000O0OO00 ,O000OOO000000O0O0 ,OOO0O0000O0000OOO ,OO0OO000000OO0OO0 ,O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 )#line:4717
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4718
                                        print (OOOOOOO0O0O000000 ,"after line 5 =>",OOO0O0000O0000OOO )#line:4719
                                        print ("-------------")#line:4720
                            if OOO00OO0OOOOO0OOO +5 <len (O0000O0O00OOOO000 .index )and O0OO00OO000O0OO00 ==True :#line:4722
                                O0O00OOO00O00O00O =OOO00OO0OOOOO0OOO +5 #line:4724
                                O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O =OOOOOO00000OOO000 .createVariables (O0O00OOO00O00O00O ,O0000O0O00OOOO000 )#line:4725
                                if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4726
                                    print ("line 6 data =>",O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 )#line:4727
                                if O00000OO0OOOO00OO !=O0OOO000OOO000O00 :#line:4729
                                    O0OO00OO000O0OO00 =False #line:4730
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4731
                                        print ("********* end of rule *********")#line:4732
                                        print ("this line has another scenario started, this line will not be processed")#line:4733
                                if O0OO00OO000O0OO00 ==True :#line:4734
                                    OOO0O0000O0000OOO ,O0OO00OO000O0OO00 =OOOOOO00000OOO000 .lineStatus (O0OO00OO000O0OO00 ,O000OOO000000O0O0 ,OOO0O0000O0000OOO ,OO0OO000000OO0OO0 ,O00000OO0OOOO00OO ,OO0OOO000OOO00000 ,O0O0OOOOO0O00OO0O ,O0OOO0OO0000OOOO0 ,OO0O0OOO00OO0OOOO ,OOOO0O0O0O00OO0O0 ,OOO0OO00OOOOOO000 ,OOOO0OO000O0000O0 ,O0OOO00O0000O0OO0 ,OO00O0OO0O0O0O00O ,OOOOOOO0O0O000000 )#line:4736
                                    if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4737
                                        print (OOOOOOO0O0O000000 ,"after line 6 =>",OOO0O0000O0000OOO )#line:4738
                                        print ("-------------")#line:4739
                            if 'Intermediate'in OOOOOOO0O0O000000 :#line:4742
                                if OOO0O0000O0000OOO ==True :#line:4743
                                    OOO000OO0O00OO0OO =1 #line:4744
                                elif OOO0O0000O0000OOO ==False :#line:4745
                                    OOO000OO0O00OO0OO =0 #line:4746
                                elif OOO0O0000O0000OOO =='Unknown':#line:4747
                                    OOO000OO0O00OO0OO =2 #line:4748
                                OO0OO000000OO0OO0 [OOOOOOO0O0O000000 ]=OOO000OO0O00OO0OO #line:4750
                                OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ]=OOO000OO0O00OO0OO #line:4751
                            else :#line:4753
                                OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ]=OOO0O0000O0000OOO #line:4754
                            if OOOOOOO0O0O000000 ==OOOOOO00000OOO000 .for_test :#line:4757
                                if OOOOOO00000OOO000 .agg_test in OOOOOO00000OOO000 .agg :#line:4758
                                    print (OOOOOO00000OOO000 .agg [OOOOOO00000OOO000 .agg_test ])#line:4759
                                print ("final result of ",OOOOOO00000OOO000 .for_test ,"is =>",OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ])#line:4760
                                print ("----------------------------------")#line:4761
                        elif OO00O00O00000OO00 [OOOOOOO0O0O000000 ]==0 :#line:4762
                            OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ]='Unknown_TagNA'#line:4763
                            OO00OO0OOO0O00O00 [OOOOOOO0O0O000000 ]=O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Parent_Node']#line:4764
                    else :#line:4766
                        if ('Intermediate'not in OOOOOOO0O0O000000 )and (OOOOOOO0O0O000000 !=O0000OO00O0O00OO0 ):#line:4767
                            OO00OO0OOO0O00O00 [OOOOOOO0O0O000000 ]=O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Parent_Node']#line:4768
                            OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ]='Unknown_ComponentNotRunning'#line:4769
                        O0000OO00O0O00OO0 =OOOOOOO0O0O000000 #line:4770
            elif O0O00O0OOOO0O0000 [O0O0OO0O0O000000O [OOOOO00O0OO0O000O ]]==0 :#line:4773
                O0000O0O00OOOO000 =O000OOOOOO00OOO0O [OOOOO00O0OO0O000O ]#line:4775
                O0000OO00O0O00OO0 ='none'#line:4776
                for OOO00OO0OOOOO0OOO in range (len (O0000O0O00OOOO000 .index )):#line:4777
                    OOOOOOO0O0O000000 =O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Problem_Name']#line:4778
                    if ('Intermediate'not in OOOOOOO0O0O000000 )and (OOOOOOO0O0O000000 !=O0000OO00O0O00OO0 ):#line:4779
                        OO0OOO0OOO000O0O0 [OOOOOOO0O0O000000 ]='Unknown_AssetNotRunning'#line:4782
                        OO00OO0OOO0O00O00 [OOOOOOO0O0O000000 ]=O0000O0O00OOOO000 .loc [OOO00OO0OOOOO0OOO ]['Parent_Node']#line:4783
                    O0000OO00O0O00OO0 =OOOOOOO0O0O000000 #line:4784
        for O0000O00OO0OO0O0O in OO0OOO0OOO000O0O0 .keys ():#line:4787
            OO0OOO0OOO000O0O0 [O0000O00OO0OO0O0O ]=str (OO0OOO0OOO000O0O0 [O0000O00OO0OO0O0O ])#line:4788
        return OO0OOO0OOO000O0O0 ,OO00OO0OOO0O00O00 #line:4791
    def logStatusandParentNode (O0O000O00OO00O0O0 ,O00OOO0O0OOO0OO00 ,OO0O0O0O0O0O0OO00 ):#line:4793
        O0O000O00OO00O0O0 .cursor .execute ('truncate table public."RCA_update"')#line:4795
        O0O000O00OO00O0O0 .conn .commit ()#line:4796
        OO000OOOO00OOO0OO ={}#line:4797
        for OOOOOO0OOO0OOOO0O in O00OOO0O0OOO0OO00 .keys ():#line:4799
            OO000OOOO00OOO0OO [OOOOOO0OOO0OOOO0O ]=[str (O00OOO0O0OOO0OO00 [OOOOOO0OOO0OOOO0O ]),OO0O0O0O0O0O0OO00 [OOOOOO0OOO0OOOO0O ]]#line:4800
        for OOOOOO0OOO0OOOO0O in OO000OOOO00OOO0OO .keys ():#line:4805
            O0O000O00OO00O0O0 .cursor .execute ('insert into public."RCA_update" values(%s, %s, %s, %s)',[datetime .now (),OOOOOO0OOO0OOOO0O ,OO000OOOO00OOO0OO [OOOOOO0OOO0OOOO0O ][0 ],OO000OOOO00OOO0OO [OOOOOO0OOO0OOOO0O ][1 ]])#line:4807
            O0O000O00OO00O0O0 .conn .commit ()#line:4808
        return OO000OOOO00OOO0OO #line:4810
    def RCAlevels (OO000O0OOO000000O ,O0O0000O000OOOO0O ):#line:4812
        OO000O0OOO000000O .cursor .execute ('truncate table public."RCA_levels"')#line:4813
        OO000O0OOO000000O .conn .commit ()#line:4814
        OO000O0OOO000000O .cursor .execute ('''select "scenarioName" from public."RCA_update" where "ParentNode" = 'None';''')#line:4819
        OO00000OOOO00OO00 =OO000O0OOO000000O .cursor .fetchall ()#line:4820
        OO000O0OOO000000O .conn .commit ()#line:4821
        OO00OOO000O0000O0 =[]#line:4822
        for OOO0OO00O0OO0O0O0 in OO00000OOOO00OO00 :#line:4823
            OO00OOO000O0000O0 .append (OOO0OO00O0OO0O0O0 [0 ])#line:4824
        O0O000O0O00O0OOO0 ={}#line:4828
        OO0O00O0OO00OO0O0 ={}#line:4829
        for O0OO0O00OOO0OO00O in OO00OOO000O0000O0 :#line:4831
            if O0OO0O00OOO0OO00O in O0O0000O000OOOO0O .keys ():#line:4832
                O0O000O0O00O0OOO0 [O0OO0O00OOO0OO00O ]=[]#line:4833
            OOO0O0OO0OO0O00OO =O0OO0O00OOO0OO00O #line:4834
            OO0000O0O0O000O00 =[]#line:4835
            OO000O0OOO000000O .cursor .execute ('select "scenarioName" from public."RCA_update" where "ParentNode" = %s',[O0OO0O00OOO0OO00O ])#line:4836
            OO00000OOOO00OO00 =OO000O0OOO000000O .cursor .fetchall ()#line:4837
            OO000O0OOO000000O .conn .commit ()#line:4838
            for OOO0OO00O0OO0O0O0 in OO00000OOOO00OO00 :#line:4840
                OO0000O0O0O000O00 .append (OOO0OO00O0OO0O0O0 [0 ])#line:4841
                if OOO0OO00O0OO0O0O0 [0 ]in O0O0000O000OOOO0O .keys ():#line:4844
                    O0O000O0O00O0OOO0 [O0OO0O00OOO0OO00O ].append (OOO0OO00O0OO0O0O0 [0 ])#line:4845
            for OOO0OOO0O0O0O0O00 in OO0000O0O0O000O00 :#line:4847
                OOOOO00OOO00O0O00 =OOO0OOO0O0O0O0O00 #line:4848
                OOOOO00OOO0000O00 =[]#line:4849
                OO000O0OOO000000O .cursor .execute ('select "scenarioName" from public."RCA_update" where "ParentNode" = %s',[OOO0OOO0O0O0O0O00 ])#line:4851
                OO00000OOOO00OO00 =OO000O0OOO000000O .cursor .fetchall ()#line:4852
                OO000O0OOO000000O .conn .commit ()#line:4853
                for OOO0OO00O0OO0O0O0 in OO00000OOOO00OO00 :#line:4855
                    OOOOO00OOO0000O00 .append (OOO0OO00O0OO0O0O0 [0 ])#line:4856
                for OOOO0O0O00OO0OO00 in OOOOO00OOO0000O00 :#line:4860
                    O0O0O0OO0O00OOO0O =OOOO0O0O00OO0OO00 #line:4861
                    OOO0000OOO00000OO =[]#line:4863
                    OO000O0OOO000000O .cursor .execute ('select "scenarioName" from public."RCA_update" where "ParentNode" = %s',[OOOO0O0O00OO0OO00 ])#line:4864
                    OO00000OOOO00OO00 =OO000O0OOO000000O .cursor .fetchall ()#line:4865
                    OO000O0OOO000000O .conn .commit ()#line:4866
                    for OOO0OO00O0OO0O0O0 in OO00000OOOO00OO00 :#line:4868
                        OOO0000OOO00000OO .append (OOO0OO00O0OO0O0O0 [0 ])#line:4869
                    if len (OOO0000OOO00000OO )>0 :#line:4870
                        OOOO0OO0OOOO0O0OO =OOO0000OOO00000OO [0 ]#line:4871
                        for O00OOOOO0000000OO in range (1 ,len (OOO0000OOO00000OO )):#line:4872
                            OOOO0OO0OOOO0O0OO =OOOO0OO0OOOO0O0OO +","+OOO0000OOO00000OO [O00OOOOO0000000OO ]#line:4873
                    else :#line:4874
                        OOOO0OO0OOOO0O0OO =""#line:4875
                    OO0O00O000O0O0O00 =['LDC1','LDC2','HDC1','HDC2','FVAP','LNGVAP','BOGHTR','WUHTR','GWHSTM','SCLR']#line:4877
                    O00000O000OOOO000 =['LD1','LD2','HD1','HD2','FV','LNGV','BOGH','WUH','GWHS','SC']#line:4878
                    for O00OOOOO0000000OO in range (len (OO0O00O000O0O0O00 )):#line:4879
                        OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO .replace (OO0O00O000O0O0O00 [O00OOOOO0000000OO ]+"_",O00000O000OOOO000 [O00OOOOO0000000OO ]+"_")#line:4880
                        OOOOO00OOO00O0O00 =OOOOO00OOO00O0O00 .replace (OO0O00O000O0O0O00 [O00OOOOO0000000OO ]+"_",O00000O000OOOO000 [O00OOOOO0000000OO ]+"_")#line:4881
                    OO000O0OOO000000O .cursor .execute ('insert into public."RCA_levels" values(%s, %s, %s, %s)',[OOO0O0OO0OO0O00OO ,OOOOO00OOO00O0O00 ,O0O0O0OO0O00OOO0O ,OOOO0OO0OOOO0O0OO ])#line:4883
                    OO000O0OOO000000O .conn .commit ()#line:4884
                    OO0O00O0OO00OO0O0 [O0O0O0OO0O00OOO0O ]=OOOO0OO0OOOO0O0OO #line:4885
        return O0O000O0O00O0OOO0 ,OO0O00O0OO00OO0O0 #line:4887
    def applyInferredStatus (O00O000OO000O0000 ,OOO0000O0OOO00OOO ):#line:4889
        O00O000OO000O0000 .cursor .execute ('select "Level3_Scenario", "Level4_RootCauses" from public."RCA_levels"')#line:4890
        O00O0OO000000OOOO =O00O000OO000O0000 .cursor .fetchall ()#line:4891
        O00O000OO000O0000 .conn .commit ()#line:4892
        O0O000OOOO000O000 ={}#line:4894
        for O0O0O0OO0OO0O0O0O in O00O0OO000000OOOO :#line:4895
            O0O000OOOO000O000 [O0O0O0OO0OO0O0O0O [0 ]]=O0O0O0OO0OO0O0O0O [1 ].split (",")#line:4896
        for O0000O00O00O00O00 in O0O000OOOO000O000 .keys ():#line:4898
            if len (O0O000OOOO000O000 [O0000O00O00O00O00 ])>1 :#line:4899
                for OOOO0O0OO0OOOOOO0 in O0O000OOOO000O000 [O0000O00O00O00O00 ]:#line:4900
                    if OOOO0O0OO0OOOOOO0 in OOO0000O0OOO00OOO .keys ():#line:4901
                        if str (OOO0000O0OOO00OOO [OOOO0O0OO0OOOOOO0 ])=='True'and (str (OOO0000O0OOO00OOO [O0000O00O00O00O00 ])=='False'or str (OOO0000O0OOO00OOO [O0000O00O00O00O00 ])=='Unknown'):#line:4902
                            O00O000OO000O0000 .cursor .execute ('''update public."RCA_update" set "Status" = 'InferredTrue' where "scenarioName" = %s''',[O0000O00O00O00O00 ])#line:4904
                            O00O000OO000O0000 .conn .commit ()#line:4905
                            OOO0000O0OOO00OOO [O0000O00O00O00O00 ]='InferredTrue'#line:4906
        return OOO0000O0OOO00OOO #line:4907
    def updateRCAstatus (OO0O0O0O0OOO00OOO ,OO0O00OOOO0O00O00 ,O0OOOOO00O00OOOO0 ,OO0O00000O0OOO0O0 ,OOO0O00O0OO0O0O00 ,OOO00OO0O0O00OOO0 ,O00OOO000O00OO000 ,OOO00O0OOO0OOOOO0 ):#line:4909
        O000OO0O00O00OO0O =['LD1','LD2','HD1','HD2','LNGV','FV','BOGH','WUH','GWH','SC','IG','NG1','NG2','ME1','ME2','MEEG','GEEG','AB','VA','LO','BLST','BLG','GE1','GE2','GE3','GE4','CT1','CT2','CT3','CT4','FW','FO','MEFG','GEFG','GCU','INCIN']#line:4913
        if OO0O0O0O0OOO00OOO .compare_pre_and_curr_status ==1 :#line:4918
            for O0000O0OO00O00000 in OO0O00OOOO0O00O00 .keys ():#line:4919
                if O0000O0OO00O00000 not in OO0O00000O0OOO0O0 .keys ():#line:4920
                    OO0O00000O0OOO0O0 [O0000O0OO00O00000 ]='NAnow_Modified'#line:4921
            for O0000O0OO00O00000 in OOO00OO0O0O00OOO0 :#line:4924
                if O0000O0OO00O00000 not in OO0O00OOOO0O00O00 .keys ():#line:4925
                    if O0000O0OO00O00000 in OO0O00000O0OOO0O0 :#line:4926
                        OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[OOO0O00O0OO0O0O00 ,OO0O00000O0OOO0O0 [O0000O0OO00O00000 ]]#line:4927
                    else :#line:4930
                        OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[OOO0O00O0OO0O0O00 ,'NAnow_Modified']#line:4931
                    OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."Prestatus" values(%s,%s,%s)',[O0000O0OO00O00000 ,OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][0 ],OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][1 ]])#line:4932
        for O0000O0OO00O00000 in OOO00OO0O0O00OOO0 :#line:4936
            O0O0OO000O0OO00OO =O0000O0OO00O00000 .split ("_")[0 ]#line:4944
            O00OOO0OOOOOOO00O =OO0O00000O0OOO0O0 [O0000O0OO00O00000 ]#line:4956
            if OO0O0O0O0OOO00OOO .test_run ==1 :#line:4958
                O00OOO0OOOOOOO00O ='True'#line:4959
            if O00OOO0OOOOOOO00O =='True'or O00OOO0OOOOOOO00O =='InferredTrue':#line:4960
                OOOOOOOO000O0O0O0 =OOO00O0OOO0OOOOO0 [O0000O0OO00O00000 ]#line:4971
                OO0OOO00OOOOOOOO0 ={}#line:4972
                O0OO00O0O000OO000 ={}#line:4973
                if len (OOOOOOOO000O0O0O0 )==0 :#line:4975
                    OOOOOOO0000O00OO0 ='None'#line:4976
                    O0O000OOOO0O0O00O ='None'#line:4977
                else :#line:4978
                    OOOOOOOO000O0O0O0 =OOOOOOOO000O0O0O0 .split (",")#line:4979
                    OO0OOO00OOOOOOOO0 ={}#line:4980
                    O0OO00O0O000OO000 ={}#line:4981
                    for OOOOO0O0OO0O0OO0O in OOOOOOOO000O0O0O0 :#line:4982
                        if OOOOO0O0OO0O0OO0O in OO0O00000O0OOO0O0 .keys ():#line:4983
                            O0OO0OOOOO0O0O00O =str (OO0O00000O0OOO0O0 [OOOOO0O0OO0O0OO0O ])#line:4984
                        else :#line:4985
                            O0OO0OOOOO0O0O00O ='Unknown'#line:4986
                        OOOOO0O0OO0O0OO0O =OOOOO0O0OO0O0OO0O .split ("_")#line:4989
                        OOOOO0O0OO0O0OO0O ="_".join (OOOOO0O0OO0O0OO0O [1 :])#line:4990
                        if O0OO0OOOOO0O0O00O =='True':#line:4991
                            OO0OOO00OOOOOOOO0 [OOOOO0O0OO0O0OO0O ]=O0OO0OOOOO0O0O00O #line:4992
                        elif O0OO0OOOOO0O0O00O =='Unknown':#line:4996
                            O0OO00O0O000OO000 [OOOOO0O0OO0O0OO0O ]=O0OO0OOOOO0O0O00O #line:4997
                        else :#line:4998
                            O0OO0OOOOO0O0O00O ='False'#line:5000
                            O0OO00O0O000OO000 [OOOOO0O0OO0O0OO0O ]=O0OO0OOOOO0O0O00O #line:5001
                    if len (OO0OOO00OOOOOOOO0 )==0 :#line:5002
                        OOOOOOO0000O00OO0 ='None'#line:5003
                    else :#line:5004
                        OOOOOOO0000O00OO0 =json .dumps (OO0OOO00OOOOOOOO0 )#line:5005
                    if len (O0OO00O0O000OO000 )==0 :#line:5006
                        O0O000OOOO0O0O00O ='None'#line:5007
                    else :#line:5008
                        O0O000OOOO0O0O00O =json .dumps (O0OO00O0O000OO000 )#line:5009
                    OO0O00OOO0OO00OOO ='{}"'#line:5010
                    for O0O00OOOO00OO0000 in OO0O00OOO0OO00OOO :#line:5011
                        OOOOOOO0000O00OO0 =OOOOOOO0000O00OO0 .replace (O0O00OOOO00OO0000 ,"")#line:5012
                        OOOOOOO0000O00OO0 =OOOOOOO0000O00OO0 .replace (",","   ---   ")#line:5013
                        O0O000OOOO0O0O00O =O0O000OOOO0O0O00O .replace (O0O00OOOO00OO0000 ,"")#line:5014
                        O0O000OOOO0O0O00O =O0O000OOOO0O0O00O .replace (",","   ---   ")#line:5015
                O0OOO0OO000O0OO0O =O0000O0OO00O00000 .split ("_")#line:5023
                O0OOO0OO000O0OO0O ="_".join (O0OOO0OO000O0OO0O [1 :])#line:5024
                OO0O0O0O0OOO00OOO .cursor .execute ('select "Level3_Scenario", "ScenarioStatus", "Level4_ActiveRootCauses", "Level4_OtherRootCauses" from public."RCA_Active" where "ScenarioID" = %s',[O0000O0OO00O00000 ])#line:5029
                O0OO000OO0OOOOOOO =OO0O0O0O0OOO00OOO .cursor .fetchall ()#line:5030
                OO0O0O0O0OOO00OOO .conn .commit ()#line:5031
                O0O0O0OOO0OO0O00O ="%d/%m/%Y %H:%M:%S"#line:5033
                O00O000OOOOOO0OO0 =pd .to_datetime (datetime .now (),format =O0O0O0OOO0OO0O00O )#line:5034
                OO0OOOO0O0OO0OO0O =O0000O0OO00O00000 +" => "+O00OOO000O00OO000 [O0000O0OO00O00000 ]+" --- "#line:5037
                if len (OO0OOO00OOOOOOOO0 .keys ())>0 :#line:5038
                    for O0OO0OOO00000OO00 in OO0OOO00OOOOOOOO0 .keys ():#line:5039
                        O0OO0OOO00000OO00 =O0O0OO000O0OO00OO +"_"+O0OO0OOO00000OO00 #line:5040
                        OO0OOOO0O0OO0OO0O =OO0OOOO0O0OO0OO0O +O0OO0OOO00000OO00 +" => "+O00OOO000O00OO000 [O0OO0OOO00000OO00 ]+" --- "#line:5041
                OO0OOOO0O0OO0OO0O =OO0OOOO0O0OO0OO0O [:-5 ]#line:5042
                if OO0O0O0O0OOO00OOO .hide_rules ==1 :#line:5043
                    OO0OOOO0O0OO0OO0O ='NA'#line:5044
                if len (O0OO000OO0OOOOOOO )==0 :#line:5045
                        OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)',[str (O00O000OOOOOO0OO0 ),O0OOO0OO000O0OO0O ,O00OOO0OOOOOOO00O ,OOOOOOO0000O00OO0 ,O0O000OOOO0O0O00O ,O0000O0OO00O00000 ,OOO0O00O0OO0O0O00 ,OO0OOOO0O0OO0OO0O ])#line:5047
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5048
                        OO000OOOOO0OO000O =OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][1 ]#line:5050
                        OO0O0OO0OOO00O00O =OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][0 ]#line:5051
                        OO0O0OO0OOO00O00O =pd .to_datetime (OO0O0OO0OOO00O00O )#line:5053
                        O0OOOOOO00000OO0O =pd .to_datetime (OOO0O00O0OO0O0O00 )#line:5055
                        O0OOOO0O0O0OO000O =(O0OOOOOO00000OO0O -OO0O0OO0OOO00O00O ).total_seconds ()/60 #line:5057
                        O0OOOO0O0O0OO000O =float ("{0:.2f}".format (O0OOOO0O0O0OO000O ))#line:5059
                        OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',[str (OO0O0OO0OOO00O00O ),str (O0OOOOOO00000OO0O ),int (O0OOOO0O0O0OO000O ),O0OOO0OO000O0OO0O ,OO000OOOOO0OO000O ,O00OOO0OOOOOOO00O ,OOOOOOO0000O00OO0 ,O0O000OOOO0O0O00O ,O0000O0OO00O00000 ,str (O00O000OOOOOO0OO0 ),OO0OOOO0O0OO0OO0O ,"Open","None"])#line:5061
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5062
                        OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[str (O0OOOOOO00000OO0O ),O00OOO0OOOOOOO00O ]#line:5065
                else :#line:5067
                    OOOOOO00OOO00O0OO =O0OO000OO0OOOOOOO [0 ]#line:5068
                    O0OOOOOOOO0OOOOOO =OOOOOO00OOO00O0OO [0 ]#line:5069
                    OO000OOOOO0OO000O =OOOOOO00OOO00O0OO [1 ]#line:5070
                    O0000O0O000O0OO00 =OOOOOO00OOO00O0OO [2 ]#line:5071
                    O0OOO000000OO0OO0 =OOOOOO00OOO00O0OO [3 ]#line:5072
                    OO0O0OO0OOO00O00O =OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][0 ]#line:5074
                    OO0O0OO0OOO00O00O =pd .to_datetime (OO0O0OO0OOO00O00O )#line:5078
                    O0OOOOOO00000OO0O =pd .to_datetime (OOO0O00O0OO0O0O00 )#line:5079
                    OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[str (OO0O0OO0OOO00O00O ),O00OOO0OOOOOOO00O ]#line:5081
                    if O0OOO0OO000O0OO0O !=O0OOOOOOOO0OOOOOO or O00OOO0OOOOOOO00O !=OO000OOOOO0OO000O or OOOOOOO0000O00OO0 !=O0000O0O000O0OO00 or O0O000OOOO0O0O00O !=O0OOO000000OO0OO0 :#line:5084
                        OO0O0O0O0OOO00OOO .cursor .execute ('delete from public."RCA_Active" where "ScenarioID" = %s',[O0000O0OO00O00000 ])#line:5085
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5086
                        OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."RCA_Active" values (%s, %s, %s, %s, %s, %s, %s, %s)',[str (O00O000OOOOOO0OO0 ),O0OOO0OO000O0OO0O ,O00OOO0OOOOOOO00O ,OOOOOOO0000O00OO0 ,O0O000OOOO0O0O00O ,O0000O0OO00O00000 ,OOO0O00O0OO0O0O00 ,OO0OOOO0O0OO0OO0O ])#line:5087
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5088
                        O0OOOO0O0O0OO000O =(O0OOOOOO00000OO0O -OO0O0OO0OOO00O00O ).total_seconds ()/60 #line:5090
                        O0OOOO0O0O0OO000O =float ("{0:.2f}".format (O0OOOO0O0O0OO000O ))#line:5091
                        OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',[str (OO0O0OO0OOO00O00O ),str (O0OOOOOO00000OO0O ),int (O0OOOO0O0O0OO000O ),O0OOO0OO000O0OO0O ,OO000OOOOO0OO000O ,O00OOO0OOOOOOO00O ,OOOOOOO0000O00OO0 ,O0O000OOOO0O0O00O ,O0000O0OO00O00000 ,str (O00O000OOOOOO0OO0 ),OO0OOOO0O0OO0OO0O ,"Open","None"])#line:5093
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5094
                        OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[str (O0OOOOOO00000OO0O ),O00OOO0OOOOOOO00O ]#line:5095
            elif O00OOO0OOOOOOO00O =='False'or O00OOO0OOOOOOO00O =='Unknown'or O00OOO0OOOOOOO00O =='Unknown_AssetNotRunning'or O00OOO0OOOOOOO00O =='NAnow_Modified'or O00OOO0OOOOOOO00O =='Unknown_ComponentNotRunning':#line:5098
                OO0O0O0O0OOO00OOO .cursor .execute ('delete from public."RCA_Active" where "ScenarioID" = %s',[O0000O0OO00O00000 ])#line:5099
                OO0O0O0O0OOO00OOO .conn .commit ()#line:5100
                OO000OOOOO0OO000O =OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][1 ]#line:5101
                O0O0O0OOO0OO0O00O ="%d/%m/%Y %H:%M:%S"#line:5104
                O00O000OOOOOO0OO0 =pd .to_datetime (datetime .now (),format =O0O0O0OOO0OO0O00O )#line:5105
                OO0O0OO0OOO00O00O =OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][0 ]#line:5106
                OO0O0OO0OOO00O00O =pd .to_datetime (OO0O0OO0OOO00O00O )#line:5108
                O0OOOOOO00000OO0O =pd .to_datetime (OOO0O00O0OO0O0O00 )#line:5110
                O0OOO0OO000O0OO0O =O0000O0OO00O00000 .replace (O0O0OO000O0OO00OO +"_","")#line:5118
                if OO000OOOOO0OO000O !=O00OOO0OOOOOOO00O :#line:5122
                        O0OOOO0O0O0OO000O =(O0OOOOOO00000OO0O -OO0O0OO0OOO00O00O ).total_seconds ()/60 #line:5123
                        O0OOOO0O0O0OO000O =float ("{0:.2f}".format (O0OOOO0O0O0OO000O ))#line:5124
                        OOOOOOO0000O00OO0 ='None'#line:5126
                        O0O000OOOO0O0O00O ='None'#line:5127
                        OO0O0O0O0OOO00OOO .cursor .execute ('insert into public."RCA_history" values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',[str (OO0O0OO0OOO00O00O ),str (O0OOOOOO00000OO0O ),int (O0OOOO0O0O0OO000O ),O0OOO0OO000O0OO0O ,OO000OOOOO0OO000O ,O00OOO0OOOOOOO00O ,OOOOOOO0000O00OO0 ,O0O000OOOO0O0O00O ,O0000O0OO00O00000 ,str (O00O000OOOOOO0OO0 ),'NA',"Open","None"])#line:5130
                        OO0O0O0O0OOO00OOO .conn .commit ()#line:5131
                        OO0O00OOOO0O00O00 [O0000O0OO00O00000 ]=[str (O0OOOOOO00000OO0O ),O00OOO0OOOOOOO00O ]#line:5132
        for O0000O0OO00O00000 in OO0O00OOOO0O00O00 .keys ():#line:5134
            OO0O0O0O0OOO00OOO .cursor .execute ('update public."Prestatus" set "TimeStamp" = %s where "Scenario" = %s',[OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][0 ],O0000O0OO00O00000 ])#line:5136
            OO0O0O0O0OOO00OOO .conn .commit ()#line:5137
            OO0O0O0O0OOO00OOO .cursor .execute ('update public."Prestatus" set "Status" = %s where "Scenario" = %s',[OO0O00OOOO0O00O00 [O0000O0OO00O00000 ][1 ],O0000O0OO00O00000 ])#line:5138
            OO0O0O0O0OOO00OOO .conn .commit ()#line:5139
        return OO0O00OOOO0O00O00 #line:5141
    def saveHOS (OOOO0O00O0OOO000O ,OOO0O0O0O0OO000OO ,O0O00O00O0O0O00O0 ,O0000O00OOOO00OO0 ,OOOOOOOO00O00OO00 ,OOOO0O000O0O00OO0 ,O00O0OO00OO00O0OO ,O000O0O00OO00000O ):#line:5144
        OOO0O0O0O0OO000OO =pd .to_datetime (OOO0O0O0O0OO000OO ,format ="%Y-%m-%d %H:%M:%S")#line:5148
        OOOOOOOO00O00OO00 =pd .to_datetime (OOOOOOOO00O00OO00 ,format ="%Y-%m-%d %H:%M:%S")#line:5149
        O000OOO0O000O0O0O =[]#line:5162
        for O00O00OO0000O00O0 in O00O0OO00OO00O0OO .keys ():#line:5163
            O000OOO0O000O0O0O .append (O00O00OO0000O00O0 )#line:5164
            O000OOO0O000O0O0O =O000OOO0O000O0O0O +O00O0OO00OO00O0OO [O00O00OO0000O00O0 ]#line:5165
        for O00O0OOO0OO0OOOO0 in O0000O00OOOO00OO0 .keys ():#line:5167
            if O00O0OOO0OO0OOOO0 not in O000OOO0O000O0O0O :#line:5168
                print (O00O0OOO0OO0OOOO0 ,"=> not present in hierarchy")#line:5169
        O0OO0O00O0O0O0OOO =False #line:5172
        OOOOOO000O0O00000 ={}#line:5175
        for O00O00OO0000O00O0 in O00O0OO00OO00O0OO .keys ():#line:5176
            if O0O00O00O0O0O00O0 [O00O00OO0000O00O0 ]==1 and OOOO0O000O0O00OO0 [O00O00OO0000O00O0 ]==1 :#line:5177
                OOO0O0O0OOOOO0O0O =OOOOOOOO00O00OO00 -OOO0O0O0O0OO000OO #line:5178
                OOO0O0O0OOOOO0O0O =OOO0O0O0OOOOO0O0O .total_seconds ()#line:5179
                if OOO0O0O0OOOOO0O0O >180.0 :#line:5180
                    OOO0O0O0OOOOO0O0O =60.0 #line:5181
                OOO0O0O0OOOOO0O0O =OOO0O0O0OOOOO0O0O /3600 #line:5182
                OOOOOO000O0O00000 [O00O00OO0000O00O0 ]=O000O0O00OO00000O [O00O00OO0000O00O0 ]+OOO0O0O0OOOOO0O0O #line:5183
            else :#line:5184
                OOOOOO000O0O00000 [O00O00OO0000O00O0 ]=O000O0O00OO00000O [O00O00OO0000O00O0 ]#line:5185
            if len (O00O0OO00OO00O0OO [O00O00OO0000O00O0 ])>0 :#line:5187
                for O0O0000O0OO000000 in O00O0OO00OO00O0OO [O00O00OO0000O00O0 ]:#line:5188
                    if O0O00O00O0O0O00O0 [O0O0000O0OO000000 ]==1 and OOOO0O000O0O00OO0 [O0O0000O0OO000000 ]==1 :#line:5189
                        OOO0O0O0OOOOO0O0O =OOOOOOOO00O00OO00 -OOO0O0O0O0OO000OO #line:5190
                        OOO0O0O0OOOOO0O0O =OOO0O0O0OOOOO0O0O .total_seconds ()#line:5191
                        if OOO0O0O0OOOOO0O0O >180.0 :#line:5192
                            OOO0O0O0OOOOO0O0O =60.0 #line:5193
                        OOO0O0O0OOOOO0O0O =OOO0O0O0OOOOO0O0O /3600 #line:5194
                        OOOOOO000O0O00000 [O0O0000O0OO000000 ]=O000O0O00OO00000O [O0O0000O0OO000000 ]+OOO0O0O0OOOOO0O0O #line:5195
                    else :#line:5196
                        OOOOOO000O0O00000 [O0O0000O0OO000000 ]=O000O0O00OO00000O [O0O0000O0OO000000 ]#line:5197
        if OOO0O0O0O0OO000OO .date ()!=OOOOOOOO00O00OO00 .date ():#line:5199
            O0OO0O00O0O0O0OOO =True #line:5200
            print ('new day started, so dailyHOS to write')#line:5201
        if O0OO0O00O0O0O0OOO :#line:5202
            for O00O00OO0000O00O0 in O00O0OO00OO00O0OO .keys ():#line:5203
                OOOO000OO000OOO0O =OOOOOO000O0O00000 [O00O00OO0000O00O0 ]#line:5204
                if OOOO000OO000OOO0O >24.0 and OOOO000OO000OOO0O <24.3 :#line:5205
                    OOOO000OO000OOO0O =24.0 #line:5206
                OOOO000OO000OOO0O ="{0:.3f}".format (OOOO000OO000OOO0O )#line:5207
                OOOO0O00O0OOO000O .cursor .execute ('insert into public."DailyHOS" values(%s,%s,%s,%s)',[str (OOO0O0O0O0OO000OO .date ()),O00O00OO0000O00O0 ,"-",OOOO000OO000OOO0O ])#line:5208
                OOOO0O00O0OOO000O .conn .commit ()#line:5209
                OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "DailyHOS" = %s where "Asset" = %s',[OOOO000OO000OOO0O ,O00O00OO0000O00O0 ])#line:5210
                OOOO0O00O0OOO000O .conn .commit ()#line:5211
                O000O0O00OO00000O [O00O00OO0000O00O0 ]=0 #line:5212
                if len (O00O0OO00OO00O0OO [O00O00OO0000O00O0 ])>0 :#line:5213
                    for O0O0000O0OO000000 in O00O0OO00OO00O0OO [O00O00OO0000O00O0 ]:#line:5214
                        OOOO000OO000OOO0O =OOOOOO000O0O00000 [O0O0000O0OO000000 ]#line:5215
                        if OOOO000OO000OOO0O >24.0 and OOOO000OO000OOO0O <24.3 :#line:5216
                            OOOO000OO000OOO0O =24.0 #line:5217
                        OOOO000OO000OOO0O ="{0:.3f}".format (OOOO000OO000OOO0O )#line:5218
                        OOOO0O00O0OOO000O .cursor .execute ('insert into public."DailyHOS" values(%s,%s,%s,%s)',[str (OOO0O0O0O0OO000OO .date ()),O00O00OO0000O00O0 ,O0O0000O0OO000000 ,OOOO000OO000OOO0O ])#line:5219
                        OOOO0O00O0OOO000O .conn .commit ()#line:5220
                        OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "DailyHOS" = %s where "Asset" = %s',[OOOO000OO000OOO0O ,O0O0000O0OO000000 ])#line:5221
                        OOOO0O00O0OOO000O .conn .commit ()#line:5222
                        O000O0O00OO00000O [O0O0000O0OO000000 ]=0 #line:5223
            OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "TodaySoFar" = 0')#line:5224
            OOOO0O00O0OOO000O .conn .commit ()#line:5225
        else :#line:5227
            for O00O00OO0000O00O0 in O00O0OO00OO00O0OO .keys ():#line:5228
                OOOO000OO000OOO0O ="{0:.3f}".format (OOOOOO000O0O00000 [O00O00OO0000O00O0 ])#line:5229
                OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s',[OOOO000OO000OOO0O ,O00O00OO0000O00O0 ])#line:5231
                OOOO0O00O0OOO000O .conn .commit ()#line:5232
                O000O0O00OO00000O [O00O00OO0000O00O0 ]=float (OOOO000OO000OOO0O )#line:5233
                if len (O00O0OO00OO00O0OO [O00O00OO0000O00O0 ])>0 :#line:5234
                    for O0O0000O0OO000000 in O00O0OO00OO00O0OO [O00O00OO0000O00O0 ]:#line:5235
                        OOOO000OO000OOO0O ="{0:.3f}".format (OOOOOO000O0O00000 [O0O0000O0OO000000 ])#line:5236
                        OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "TodaySoFar" = %s where "Asset" = %s',[OOOO000OO000OOO0O ,O0O0000O0OO000000 ])#line:5237
                        OOOO0O00O0OOO000O .conn .commit ()#line:5238
                        O000O0O00OO00000O [O0O0000O0OO000000 ]=float (OOOO000OO000OOO0O )#line:5239
        for OO00O0O0OOO0O000O in O0000O00OOOO00OO0 .keys ():#line:5245
            O0O000000OO000O0O =O0000O00OOOO00OO0 [OO00O0O0OOO0O000O ]#line:5246
            OO0O0OOO00O0O0O0O =OOOO0O000O0O00OO0 [OO00O0O0OOO0O000O ]#line:5247
            if O0O00O00O0O0O00O0 [OO00O0O0OOO0O000O ]==1 and OO0O0OOO00O0O0O0O ==1 :#line:5250
                OOO00O0000OOO000O =OOOOOOOO00O00OO00 -OOO0O0O0O0OO000OO #line:5251
                OOO00O0000OOO000O =OOO00O0000OOO000O .total_seconds ()#line:5252
                if OOO00O0000OOO000O >180.0 :#line:5253
                    OOO00O0000OOO000O =60.0 #line:5254
                OOO00O0000OOO000O =OOO00O0000OOO000O /3600 #line:5255
                O0000OOOO0OO0O00O =O0O000000OO000O0O +OOO00O0000OOO000O #line:5257
                if O0000OOOO0OO0O00O <0 :#line:5258
                    O0000OOOO0OO0O00O =0 #line:5259
            else :#line:5260
                O0000OOOO0OO0O00O =O0O000000OO000O0O #line:5261
            O0000O00OOOO00OO0 [OO00O0O0OOO0O000O ]=O0000OOOO0OO0O00O #line:5263
            O0O00O00O0O0O00O0 [OO00O0O0OOO0O000O ]=OO0O0OOO00O0O0O0O #line:5264
        for OO00O0O0OOO0O000O in O0000O00OOOO00OO0 .keys ():#line:5265
            OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "HOS" = %s where "Asset" = %s',["{0:.3f}".format (O0000O00OOOO00OO0 [OO00O0O0OOO0O000O ]),OO00O0O0OOO0O000O ])#line:5266
            OOOO0O00O0OOO000O .conn .commit ()#line:5267
            OOOO0O00O0OOO000O .cursor .execute ('update public."HOS" set "TimeStamp" = %s where "Asset" = %s',[str (OOOOOOOO00O00OO00 ),OO00O0O0OOO0O000O ])#line:5268
            OOOO0O00O0OOO000O .conn .commit ()#line:5269
        OOO0O0O0O0OO000OO =OOOOOOOO00O00OO00 #line:5271
        return OOO0O0O0O0OO000OO ,O0O00O00O0O0O00O0 ,O0000O00OOOO00OO0 ,O000O0O00OO00000O #line:5275
    def maintenanceAlarm (O0OOO0O0000O00O00 ,O0O0000O0000OO000 ,OOOO00O00O000OOO0 ):#line:5278
        OO0OOOO0O0OOO0000 =24 *7 #line:5279
        O0OO0O000OO00O000 =np .array ([720 ,1440 ,2160 ,2880 ,3600 ,4320 ,5040 ,5760 ,6480 ,7200 ,7920 ,8640 ,9360 ,10080 ,10800 ,11520 ,12240 ,12960 ,13680 ,14400 ,15120 ,15840 ,16560 ,17280 ,18000 ,18720 ,19440 ,20160 ,20880 ,21600 ,22320 ,23040 ,23760 ,24480 ,25200 ,25920 ,26640 ,27360 ,28080 ,28800 ,29520 ,30240 ,30960 ,31680 ,32400 ,33120 ,33840 ,34560 ,35280 ,36000 ,36720 ,37440 ,38160 ,38880 ,39600 ,40320 ,41040 ,41760 ,42480 ,43200 ])#line:5285
        O0OOO00O0O0OO0OO0 =np .array ([2160 ,4320 ,6480 ,8640 ,10800 ,12960 ,15120 ,17280 ,19440 ,21600 ,23760 ,25920 ,28080 ,30240 ,32400 ,34560 ,36720 ,38880 ,41040 ,43200 ])#line:5287
        O0OO0O0000O00O000 =np .array ([4320 ,8640 ,12960 ,17280 ,21600 ,25920 ,30240 ,34560 ,38880 ,43200 ])#line:5288
        O0O0O0O00OOO0O0O0 =np .array ([8640 ,17280 ,25920 ,34560 ,43200 ])#line:5289
        OO000OO0OOOO000O0 =np .array ([10000 ,20000 ,30000 ,40000 ,50000 ])#line:5290
        O00OO0OOO0O0OO0O0 =np .array ([21600 ,43200 ])#line:5291
        O000OOOO00OOO0O00 =np .array ([43200 ])#line:5292
        OOO000O00OOO0O0OO =np .array ([86400 ])#line:5293
        OOO0O0OOOO00OOO0O =O0OO0O000OO00O000 +OO0OOOO0O0OOO0000 #line:5294
        O0OOOO0O0O00O000O =O0OOO00O0O0OO0OO0 +OO0OOOO0O0OOO0000 #line:5295
        OOO0OO0OO0O0O0OO0 =O0OO0O0000O00O000 +OO0OOOO0O0OOO0000 #line:5296
        OO000OOOOOOO00O0O =O0O0O0O00OOO0O0O0 +OO0OOOO0O0OOO0000 #line:5297
        O0000000O0OOO00O0 =OO000OO0OOOO000O0 +OO0OOOO0O0OOO0000 #line:5298
        OO0O0OOO00O0O0OOO =O000OOOO00OOO0O00 +OO0OOOO0O0OOO0000 #line:5299
        OOOO0O00OOO0OO00O =OOO000O00OOO0O0OO +OO0OOOO0O0OOO0000 #line:5300
        OOOO0O0O0O0OO000O =O00OO0OOO0O0OO0O0 +OO0OOOO0O0OOO0000 #line:5301
        O000O0000OOO0O00O =datetime .now ()#line:5302
        O000O0000OOO0O00O =pd .to_datetime (O000O0000OOO0O00O ,format ="%d/%m/%Y %H:%M:%S")#line:5303
        O0O0000O0000OO000 =pd .to_datetime (O0O0000O0000OO000 )#line:5304
        OOOO0O0OO0O000000 =O000O0000OOO0O00O -O0O0000O0000OO000 #line:5305
        O00OO0O0O0OO00OOO =OOOO0O0OO0O000000 .total_seconds ()/3600 #line:5306
        O0OOO0O0000O00O00 .cursor .execute ('''update public."Calender_time" set "TimeStamp" = %s where "Kind" = 'Elapsed_time';''',[str (O000O0000OOO0O00O )])#line:5313
        O0OOO0O0000O00O00 .conn .commit ()#line:5314
        O0OOO0O0000O00O00 .cursor .execute ('''update public."Calender_time" set "Value" = %s where "Kind" = 'Elapsed_time';''',[O00OO0O0O0OO00OOO ])#line:5315
        O0OOO0O0000O00O00 .conn .commit ()#line:5316
        O0OO0O00O0OO00O0O =datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")#line:5317
        O00OO0O0OOO00O000 =['LD1_half_year_HOS','LD1_year_HOS','LD1_5years_HOS','LD2_half_year_HOS','LD2_year_HOS','LD2_5years_HOS','HD1_3months_HOS','HD1_half_year_HOS','HD1_year_HOS','HD1_5years_HOS','HD1_10years_HOS','HD2_3months_HOS','HD2_half_year_HOS','HD2_year_HOS','HD2_5years_HOS','HD2_10years_HOS','SC_10000hrs_HOS','SC_3months_HOS','SC_year_HOS','SC_5years_HOS','FV_half_year_HOS','FV_year_HOS','FV_30months_HOS','FV_5years_HOS','LNGV_half_year_HOS','LNGV_year_HOS','LNGV_30months_HOS','LNGV_5years_HOS','GWHS_month_HOS','GWHS_year_HOS','GWHS_5years_HOS']#line:5322
        for O000OOOOO0O0O0O0O in OOOO00O00O000OOO0 .keys ():#line:5324
            if O000OOOOO0O0O0O0O in ['LD1','LD2','HD1','HD2','FV','LNGV','GWHS','SC']:#line:5325
                O00O0OOO0O00O0000 =[O000OOOOO0O0O0O0O +'_month_HOS',O000OOOOO0O0O0O0O +'_3months_HOS',O000OOOOO0O0O0O0O +'_half_year_HOS',O000OOOOO0O0O0O0O +'_year_HOS',O000OOOOO0O0O0O0O +'_10000hrs_HOS',O000OOOOO0O0O0O0O +'_30months_HOS',O000OOOOO0O0O0O0O +'_5years_HOS',O000OOOOO0O0O0O0O +'_10years_HOS']#line:5330
                O0OO0O0O0O0OOO0O0 ={O000OOOOO0O0O0O0O +'_month_HOS':O0OO0O000OO00O000 ,O000OOOOO0O0O0O0O +'_3months_HOS':O0OOO00O0O0OO0OO0 ,O000OOOOO0O0O0O0O +'_half_year_HOS':O0OO0O0000O00O000 ,O000OOOOO0O0O0O0O +'_year_HOS':O0O0O0O00OOO0O0O0 ,O000OOOOO0O0O0O0O +'_10000hrs_HOS':OO000OO0OOOO000O0 ,O000OOOOO0O0O0O0O +'_30months_HOS':O00OO0OOO0O0OO0O0 ,O000OOOOO0O0O0O0O +'_5years_HOS':O000OOOO00OOO0O00 ,O000OOOOO0O0O0O0O +'_10years_HOS':OOO000O00OOO0O0OO }#line:5334
                O0OOOOOO0O00O00O0 ={O000OOOOO0O0O0O0O +'_month_HOS':OOO0O0OOOO00OOO0O ,O000OOOOO0O0O0O0O +'_3months_HOS':O0OOOO0O0O00O000O ,O000OOOOO0O0O0O0O +'_half_year_HOS':OOO0OO0OO0O0O0OO0 ,O000OOOOO0O0O0O0O +'_year_HOS':OO000OOOOOOO00O0O ,O000OOOOO0O0O0O0O +'_10000hrs_HOS':O0000000O0OOO00O0 ,O000OOOOO0O0O0O0O +'_30months_HOS':OOOO0O0O0O0OO000O ,O000OOOOO0O0O0O0O +'_5years_HOS':OO0O0OOO00O0O0OOO ,O000OOOOO0O0O0O0O +'_10years_HOS':OOOO0O00OOO0OO00O }#line:5340
                O0O0O0O0OO0O00O00 =['half_year_calender','year_calender','5years_calender']#line:5342
                OOOOO0OO00OOOOO00 ={'half_year_calender':O0OO0O0000O00O000 ,'year_calender':O0O0O0O00OOO0O0O0 ,'5years_calender':O000OOOO00OOO0O00 }#line:5343
                O0OO000OO000O000O ={'half_year_calender':OOO0OO0OO0O0O0OO0 ,'year_calender':OO000OOOOOOO00O0O ,'5years_calender':OO0O0OOO00O0O0OOO }#line:5344
                for O0OOOO00O0O00O000 in O00O0OOO0O00O0000 :#line:5346
                    if O0OOOO00O0O00O000 in O00OO0O0OOO00O000 :#line:5347
                        for OO0O0000OO00OOOOO in range (len (O0OO0O0O0O0OOO0O0 [O0OOOO00O0O00O000 ])):#line:5348
                            if int (OOOO00O00O000OOO0 [O000OOOOO0O0O0O0O ])>=O0OO0O0O0O0OOO0O0 [O0OOOO00O0O00O000 ][OO0O0000OO00OOOOO ]and int (OOOO00O00O000OOO0 [O000OOOOO0O0O0O0O ])<=O0OOOOOO0O00O00O0 [O0OOOO00O0O00O000 ][OO0O0000OO00OOOOO ]:#line:5349
                                O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s',[1 ,O0OOOO00O0O00O000 ])#line:5350
                                O0OOO0O0000O00O00 .conn .commit ()#line:5351
                                O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s',[O0OO0O00O0OO00O0O ,O0OOOO00O0O00O000 ])#line:5352
                                O0OOO0O0000O00O00 .conn .commit ()#line:5353
                                break #line:5355
                            else :#line:5357
                                O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s',[0 ,O0OOOO00O0O00O000 ])#line:5358
                                O0OOO0O0000O00O00 .conn .commit ()#line:5359
                                O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s',[O0OO0O00O0OO00O0O ,O0OOOO00O0O00O000 ])#line:5360
                                O0OOO0O0000O00O00 .conn .commit ()#line:5361
                for O0OOOO00O0O00O000 in O0O0O0O0OO0O00O00 :#line:5363
                    for OO0O0000OO00OOOOO in range (len (OOOOO0OO00OOOOO00 [O0OOOO00O0O00O000 ])):#line:5364
                        if int (O00OO0O0O0OO00OOO )>=OOOOO0OO00OOOOO00 [O0OOOO00O0O00O000 ][OO0O0000OO00OOOOO ]and int (O00OO0O0O0OO00OOO )<=O0OO000OO000O000O [O0OOOO00O0O00O000 ][OO0O0000OO00OOOOO ]:#line:5365
                            O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s',[1 ,O0OOOO00O0O00O000 ])#line:5366
                            O0OOO0O0000O00O00 .conn .commit ()#line:5367
                            O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s',[O0OO0O00O0OO00O0O ,O0OOOO00O0O00O000 ])#line:5368
                            O0OOO0O0000O00O00 .conn .commit ()#line:5369
                            break #line:5370
                        else :#line:5372
                            O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "Value" = %s where "Alarm" = %s',[0 ,O0OOOO00O0O00O000 ])#line:5373
                            O0OOO0O0000O00O00 .conn .commit ()#line:5374
                            O0OOO0O0000O00O00 .cursor .execute ('update public."Maintenance_Alarm" set "TimeStamp" = %s where "Alarm" = %s',[O0OO0O00O0OO00O0O ,O0OOOO00O0O00O000 ])#line:5375
                            O0OOO0O0000O00O00 .conn .commit ()#line:5376
    def saveAlertCount (OOOOO0OO00OO0OO00 ):#line:5378
        OO00000O0000000O0 ={}#line:5379
        O0OO0000O00OOOOO0 =['LD1','LD2','HD1','HD2','LNGV','FV','BOGH','WUH','GWH','SC','IG','NG1','NG2','ME1','ME2','MEEG','GEEG','AB','VA','LO','BLST','BLG','GE1','GE2','GE3','GE4','CT1','CT2','CT3','CT4','FW','FO','MEFG','GEFG','GCU','INCIN']#line:5383
        for OO0O0OOO0000OOOO0 in O0OO0000O00OOOOO0 :#line:5384
            OOOOO0OO00OO0OO00 .cursor .execute (f'''select "ScenarioID" from public."RCA_Active" where "ScenarioID" like '{OO0O0OOO0000OOOO0}%';''')#line:5385
            OO00O0OO0OOOOOO0O =OOOOO0OO00OO0OO00 .cursor .fetchall ()#line:5386
            OOOOO0OO00OO0OO00 .conn .commit ()#line:5387
            OO00000O0000000O0 [OO0O0OOO0000OOOO0 ]=len (OO00O0OO0OOOOOO0O )#line:5389
        for O0O0O00OO0OO00OO0 in OO00000O0000000O0 .keys ():#line:5392
            OO0O0OOO0000OOOO0 =O0O0O00OO0OO00OO0 #line:5393
            OO00OOOOO0OO0OO0O =OO00000O0000000O0 [O0O0O00OO0OO00OO0 ]#line:5394
            OOOOO0OO00OO0OO00 .cursor .execute ('update public."Active_count" set "Alert_count" = %s where "Asset" = %s',[OO00OOOOO0OO0OO0O ,OO0O0OOO0000OOOO0 ])#line:5396
            OOOOO0OO00OO0OO00 .conn .commit ()#line:5397
            OOOOO0OO00OO0OO00 .cursor .execute ('update public."Active_count" set "TimeStamp" = %s where "Asset" = %s',[datetime .now ().strftime ("%Y-%m-%d %H:%M:%S"),OO0O0OOO0000OOOO0 ])#line:5398
            OOOOO0OO00OO0OO00 .conn .commit ()#line:5399
    def totalAvailableScenarios (O0O0000O000000O0O ):#line:5401
        OOO0OOOOO0000O000 ={}#line:5403
        OOOOOOO0000O0O0O0 =['LD1','LD2','HD1','HD2','LNGV','FV','BOGH','WUH','GWH','SC','IG','NG1','NG2','ME1','ME2','MEEG','GEEG','AB','VA','LO','BLST','BLG','GE1','GE2','GE3','GE4','CT1','CT2','CT3','CT4','FW','FO','MEFG','GEFG','GCU','INCIN']#line:5406
        for O00OOOOOOOO000OO0 in OOOOOOO0000O0O0O0 :#line:5408
            O0O0000O000000O0O .cursor .execute (f'''select "Level3_ScenarioName" from public."RCA_ID" where "Level3_ScenarioName" like '{O00OOOOOOOO000OO0}%';''')#line:5409
            O0OO0OOOO0OO0O00O =O0O0000O000000O0O .cursor .fetchall ()#line:5410
            O0O0000O000000O0O .conn .commit ()#line:5411
            OOO0OOOOO0000O000 [O00OOOOOOOO000OO0 ]=len (O0OO0OOOO0OO0O00O )#line:5413
        for O0O0000O0000OO0O0 in OOO0OOOOO0000O000 .keys ():#line:5416
            O00OOOOOOOO000OO0 =O0O0000O0000OO0O0 #line:5417
            O00OO00000O00O0OO =OOO0OOOOO0000O000 [O0O0000O0000OO0O0 ]#line:5418
            O0O0000O000000O0O .cursor .execute ('update public."Active_count" set "Total_count" = %s where "Asset" = %s',[O00OO00000O00O0OO ,O00OOOOOOOO000OO0 ])#line:5419
            O0O0000O000000O0O .conn .commit ()#line:5420
    def runningStatusLogging (OO000O0OO00OOO00O ,O0O0OOOO000OO0O00 ,O0O0O00O00OO0O00O ):#line:5422
        OO00OOO00OOO0O000 =['Cargo_vapor','HD','FBOG','NBOG','Fuel_Consumption','Fuel_Economy']#line:5424
        for OOOO0O000OO00OOO0 in O0O0OOOO000OO0O00 .keys ():#line:5427
            O00OO0OOO0OO000O0 =f'''update public."Running_status_update" set "Status" = {O0O0OOOO000OO0O00[OOOO0O000OO00OOO0]} where "Asset" = '{OOOO0O000OO00OOO0}';'''#line:5428
            OO000O0OO00OOO00O .cursor .execute (O00OO0OOO0OO000O0 )#line:5429
            OO000O0OO00OOO00O .conn .commit ()#line:5430
        O00O0000OO0OOO0O0 ="Running_status_history"#line:5433
        OO000O0OO00OOO00O .cursor .execute ('select "column_name" from information_schema.columns where "table_name" = %s',[O00O0000OO0OOO0O0 ])#line:5434
        OO000O000O00000O0 =OO000O0OO00OOO00O .cursor .fetchall ()#line:5435
        OO000O0OO00OOO00O .conn .commit ()#line:5436
        O0O0O000O0OOO0O00 =[OOOOOOOO0O00OOO00 [0 ].replace ("_running_status","")for OOOOOOOO0O00OOO00 in OO000O000O00000O0 ][1 :]#line:5437
        O00OO0OOO0OO000O0 =f"'{O0O0O00O00OO0O00O}', "#line:5440
        for OOOOOOOO00000OOOO in O0O0O000O0OOO0O00 :#line:5441
            O00OO0OOO0OO000O0 =O00OO0OOO0OO000O0 +f"{O0O0OOOO000OO0O00[OOOOOOOO00000OOOO]}, "#line:5442
        O00OO0OOO0OO000O0 =O00OO0OOO0OO000O0 [:-2 ]+")"#line:5443
        O00OO0OOO0OO000O0 =f'insert into public."Running_status_history" values({O00OO0OOO0OO000O0}'#line:5444
        OO000O0OO00OOO00O .cursor .execute (O00OO0OOO0OO000O0 )#line:5446
        OO000O0OO00OOO00O .conn .commit ()#line:5447
    def importRCAtemplates (OO00O00000O0O00OO ):#line:5449
        O0000O000O00O0OO0 =['LD1','LD2','HD1','HD2','LNGV','FV','BOGH','WUH','GWH','SC','IG','NG1','NG2','ME1','ME2','MEEG','GEEG','AB','VA','LO','BLST','BLG','GE1','GE2','GE3','GE4','CT1','CT2','CT3','CT4','FW','FO','MEFG','GEFG','GCU','INCIN']#line:5453
        OO0OO00OO0O0OO000 =OO00O00000O0O00OO .RCA_mastersheet_path #line:5455
        O00OO0O0000OO000O =io .BytesIO ()#line:5456
        with open (OO0OO00OO0O0OO000 ,'rb')as O0OOOO0OOO0000OO0 :#line:5457
            O000000000O000O00 =msoffcrypto .OfficeFile (O0OOOO0OOO0000OO0 )#line:5458
            O000000000O000O00 .load_key (OO00O00000O0O00OO .ent )#line:5459
            O000000000O000O00 .decrypt (O00OO0O0000OO000O )#line:5460
        OOOO000O0OOOOO0O0 =[]#line:5504
        for OOO0O00OOOO0000OO in O0000O000O00O0OO0 :#line:5505
            OOOO000O0OOOOO0O0 .append (pd .read_excel (O00OO0O0000OO000O ,sheet_name =OOO0O00OOOO0000OO ))#line:5506
        for OO000O000OO0OO0OO in OOOO000O0OOOOO0O0 :#line:5508
            OO000O000OO0OO0OO .at [0 ,'Parent_Node']='None'#line:5509
        return OOOO000O0OOOOO0O0 #line:5511
    def rcaID (O0O0O00O0O0O00000 ,O00O00000OO000OOO ):#line:5513
        O0OO000O000O0O0O0 ={}#line:5514
        for O00OOOOOOO00OOO0O in range (len (O00O00000OO000OOO )):#line:5515
            OO0000OOOOOO0OOO0 =O00O00000OO000OOO [O00OOOOOOO00OOO0O ]#line:5516
            OO0000OOOOOO0OOO0 =OO0000OOOOOO0OOO0 .loc [:,['Problem_Name','Level','Implement','Priority','AdviceMessage']]#line:5518
            OO0000OOOOOO0OOO0 .rename (columns ={'Problem_Name':'Level3_ScenarioName'},inplace =True )#line:5519
            OOOO0O0O00O0OOOOO =OO0000OOOOOO0OOO0 ['Level']=='SCENARIO'#line:5520
            OO0000OOOOOO0OOO0 =OO0000OOOOOO0OOO0 [OOOO0O0O00O0OOOOO ]#line:5521
            OOOO0O0O00O0OOOOO =OO0000OOOOOO0OOO0 ['Implement']==1.0 #line:5522
            OO0000OOOOOO0OOO0 =OO0000OOOOOO0OOO0 [OOOO0O0O00O0OOOOO ]#line:5523
            if O00OOOOOOO00OOO0O ==0 :#line:5524
                O00O0O000OO000O0O =OO0000OOOOOO0OOO0 .copy ()#line:5525
            else :#line:5526
                O00O0O000OO000O0O =pd .concat ([O00O0O000OO000O0O ,OO0000OOOOOO0OOO0 ],axis =0 )#line:5527
        O00O0O000OO000O0O =O00O0O000OO000O0O .drop_duplicates ('Level3_ScenarioName',keep ='first').reset_index ()#line:5528
        O0O0O00O0O0O00000 .cursor .execute ('truncate table public."RCA_ID"')#line:5532
        O0O0O00O0O0O00000 .conn .commit ()#line:5533
        for O00OOOOOOO00OOO0O in range (len (O00O0O000OO000O0O .index )):#line:5534
            OOO0O0OO0OO000OO0 =O00O0O000OO000O0O .loc [O00OOOOOOO00OOO0O ]['Level3_ScenarioName']#line:5535
            O00O0O0OOOO0O0OO0 =O00O0O000OO000O0O .loc [O00OOOOOOO00OOO0O ]['Level']#line:5536
            O00O0O000OOOOO0O0 =O00O0O000OO000O0O .loc [O00OOOOOOO00OOO0O ]['Implement']#line:5537
            O0O0OO0O0O0O000OO =O00O0O000OO000O0O .loc [O00OOOOOOO00OOO0O ]['Priority']#line:5538
            O0O0O000OO0OO00OO =O00O0O000OO000O0O .loc [O00OOOOOOO00OOO0O ]['AdviceMessage']#line:5539
            O0O0O00O0O0O00000 .cursor .execute ('insert into public."RCA_ID" values (%s, %s, %s, %s, %s)',[OOO0O0OO0OO000OO0 ,O00O0O0OOOO0O0OO0 ,int (O00O0O000OOOOO0O0 ),float (O0O0OO0O0O0O000OO ),O0O0O000OO0OO00OO ])#line:5540
            O0O0O00O0O0O00000 .conn .commit ()#line:5541
        O00OOO00OO0OOOOO0 =O00O0O000OO000O0O ['Level3_ScenarioName'].values .tolist ()#line:5543
        return O00OOO00OO0OOOOO0 #line:5544
    def updateSignal (O00O00OO0OO0OO000 ):#line:5546
        O00O00OO0OO0OO000 .cursor .execute ('select * from public."Templates_update"')#line:5547
        O0OO00OOO0O000OO0 =O00O00OO0OO0OO000 .cursor .fetchall ()#line:5548
        O00O00OO0OO0OO000 .conn .commit ()#line:5549
        O000O00OOOO0O0000 =O0OO00OOO0O000OO0 [0 ][1 ]#line:5551
        return O000O00OOOO0O0000 #line:5553
    def findRules (OO0OO0OOO0000OO00 ,OOO000O00O0OO0OO0 ):#line:5555
        OO0OO0OOO0000OO00 .cursor .execute ('truncate public."RCA_rules"')#line:5556
        OO0OO0OOO0000OO00 .conn .commit ()#line:5557
        OOOOO0O00OOOOO0OO ={}#line:5558
        O00OOOO0OO0O00000 ={}#line:5559
        for O00000O000OOO0O0O in OOO000O00O0OO0OO0 :#line:5560
            O00000O000OOO0O0O .fillna ('blank',inplace =True )#line:5561
            O000OOOOOO0OO000O ='none'#line:5562
            for OO0OOOOOOOOOOO0OO in range (len (O00000O000OOO0O0O .index )):#line:5563
                OOO0O0O0OO000OOO0 =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Problem_Name']#line:5564
                if OOO0O0O0OO000OOO0 !=O000OOOOOO0OO000O :#line:5565
                    OOOO0OOOO00OO0O0O =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Standard_Key']#line:5567
                    O00O00OO000O0O0OO =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Additional condition']#line:5568
                    OOOO0O0O0000OOOO0 =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Condition']#line:5569
                    OOO00OOOO000OOOOO =str (O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Threshold'])#line:5570
                    OO00OOO0O000OOOOO =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Logic']#line:5571
                    if OOOO0OOOO00OO0O0O !='blank':#line:5572
                        if 'Intermediate'in OOOO0OOOO00OO0O0O :#line:5573
                            O0OO000O000000000 =f" ({OOOOO0O00OOOOO0OO[OOOO0OOOO00OO0O0O]}) {OO00OOO0O000OOOOO} "#line:5574
                            O0OO000O000000000 =O0OO000O000000000 .replace ("blank","")#line:5575
                            O0OO000O000000000 =O0OO000O000000000 .strip ()#line:5576
                            OOOOO0O00OOOOO0OO [OOO0O0O0OO000OOO0 ]=O0OO000O000000000 #line:5577
                            O0000OO00OO0OOOOO =O00OOOO0OO0O00000 [OOOO0OOOO00OO0O0O ]#line:5579
                            O00OOOO0OO0O00000 [OOO0O0O0OO000OOO0 ]=O0000OO00OO0OOOOO #line:5580
                        else :#line:5582
                            O0OO000O000000000 =f" {OOOO0OOOO00OO0O0O} {OOOO0O0O0000OOOO0} {OOO00OOOO000OOOOO} {O00O00OO000O0O0OO} {OO00OOO0O000OOOOO} "#line:5583
                            O0OO000O000000000 =O0OO000O000000000 .replace ("blank","")#line:5584
                            O0OO000O000000000 =O0OO000O000000000 .strip ()#line:5585
                            OOOOO0O00OOOOO0OO [OOO0O0O0OO000OOO0 ]=O0OO000O000000000 #line:5586
                            O0000OO00OO0OOOOO =OOOO0OOOO00OO0O0O #line:5588
                            O00OOOO0OO0O00000 [OOO0O0O0OO000OOO0 ]=O0000OO00OO0OOOOO #line:5589
                    elif OOOO0OOOO00OO0O0O =='blank':#line:5590
                        OOOOO0O00OOOOO0OO [OOO0O0O0OO000OOO0 ]='None'#line:5591
                        O00OOOO0OO0O00000 [OOO0O0O0OO000OOO0 ]='None'#line:5592
                    O000OOOOOO0OO000O =OOO0O0O0OO000OOO0 #line:5593
                elif OOO0O0O0OO000OOO0 ==O000OOOOOO0OO000O :#line:5594
                    OOOO0OOOO00OO0O0O =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Standard_Key']#line:5597
                    O00O00OO000O0O0OO =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Additional condition']#line:5599
                    OOOO0O0O0000OOOO0 =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Condition']#line:5600
                    OOO00OOOO000OOOOO =str (O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Threshold'])#line:5601
                    OO00OOO0O000OOOOO =O00000O000OOO0O0O .loc [OO0OOOOOOOOOOO0OO ]['Logic']#line:5602
                    if OOOO0OOOO00OO0O0O !='blank':#line:5603
                        if 'Intermediate'in OOOO0OOOO00OO0O0O :#line:5604
                            O0OO000O000000000 =O0OO000O000000000 +f" ({OOOOO0O00OOOOO0OO[OOOO0OOOO00OO0O0O]}) {OO00OOO0O000OOOOO} "#line:5605
                            O0OO000O000000000 =O0OO000O000000000 .replace ("blank","")#line:5606
                            O0OO000O000000000 =O0OO000O000000000 .replace ("  "," ")#line:5607
                            O0OO000O000000000 =O0OO000O000000000 .strip ()#line:5608
                            OOOOO0O00OOOOO0OO [OOO0O0O0OO000OOO0 ]=O0OO000O000000000 #line:5609
                            O0000OO00OO0OOOOO =O0000OO00OO0OOOOO +", "+O00OOOO0OO0O00000 [OOOO0OOOO00OO0O0O ]#line:5611
                            O00OOOO0OO0O00000 [OOO0O0O0OO000OOO0 ]=O0000OO00OO0OOOOO #line:5612
                        else :#line:5614
                            O0OO000O000000000 =O0OO000O000000000 +f" {OOOO0OOOO00OO0O0O} {OOOO0O0O0000OOOO0} {OOO00OOOO000OOOOO} {O00O00OO000O0O0OO} {OO00OOO0O000OOOOO} "#line:5615
                            O0OO000O000000000 =O0OO000O000000000 .replace ("blank","")#line:5616
                            O0OO000O000000000 =O0OO000O000000000 .replace ("  "," ")#line:5617
                            O0OO000O000000000 =O0OO000O000000000 .strip ()#line:5618
                            OOOOO0O00OOOOO0OO [OOO0O0O0OO000OOO0 ]=O0OO000O000000000 #line:5619
                            O0000OO00OO0OOOOO =O0000OO00OO0OOOOO +", "+OOOO0OOOO00OO0O0O #line:5621
                            O00OOOO0OO0O00000 [OOO0O0O0OO000OOO0 ]=O0000OO00OO0OOOOO #line:5622
                    O000OOOOOO0OO000O =OOO0O0O0OO000OOO0 #line:5623
        for OO0O00OO0O0OO0000 in OOOOO0O00OOOOO0OO .keys ():#line:5625
            if OO0OO0OOO0000OO00 .hide_rules ==1 :#line:5626
                OOOOO0O00OOOOO0OO [OO0O00OO0O0OO0000 ]='NA'#line:5627
            OO0OO0OOO0000OO00 .cursor .execute ('insert into public."RCA_rules" values(%s,%s,%s)',[OO0O00OO0O0OO0000 ,OOOOO0O00OOOOO0OO [OO0O00OO0O0OO0000 ],O00OOOO0OO0O00000 [OO0O00OO0O0OO0000 ]])#line:5628
            OO0OO0OOO0000OO00 .conn .commit ()#line:5629
        return OOOOO0O00OOOOO0OO ,O00OOOO0OO0O00000 #line:5631
    def alarmLoggingforNoKPIassets (O000OOOO0O00000O0 ,O0O0OOOO00O0OOOO0 ,OO0OO0O00O000O000 ):#line:5633
        for OO00OOOO0OO0OOOOO in O0O0OOOO00O0OOOO0 :#line:5634
            O000OOOO0O00000O0 .cursor .execute ('update public."Output_Tags" set "Value" = %s where "TagName" = %s',[float (OO0OO0O00O000O000 [OO00OOOO0OO0OOOOO ]),OO00OOOO0OO0OOOOO ])#line:5635
            O000OOOO0O00000O0 .conn .commit ()#line:5636
    def findtargetScenarios (O000OOOOO0OO00OO0 ,O000O0OO0O0000OO0 ,O0OO00O0000O00OOO ):#line:5638
        O00O0O0O000OOOOO0 ={}#line:5639
        for OOOO0O0000O0OO0O0 in O000O0OO0O0000OO0 .keys ():#line:5644
            O00O0OOOOO00000O0 =True #line:5645
            if O000O0OO0O0000OO0 [OOOO0O0000O0OO0O0 ]=='None':#line:5646
                O00O0OOOOO00000O0 =True #line:5647
            else :#line:5648
                OOO000OOO0O0OOOO0 =O000O0OO0O0000OO0 [OOOO0O0000O0OO0O0 ].split (", ")#line:5649
                for O0O0O000000O0OOO0 in OOO000OOO0O0OOOO0 :#line:5650
                    if O0O0O000000O0OOO0 in O0OO00O0000O00OOO .keys ():#line:5652
                        if O0OO00O0000O00OOO [O0O0O000000O0OOO0 ]==0 :#line:5653
                            O00O0OOOOO00000O0 =False #line:5654
                            break #line:5655
            if O00O0OOOOO00000O0 :#line:5657
                O00O0O0O000OOOOO0 [OOOO0O0000O0OO0O0 ]=1 #line:5658
            else :#line:5659
                O00O0O0O000OOOOO0 [OOOO0O0000O0OO0O0 ]=0 #line:5660
        return O00O0O0O000OOOOO0 #line:5666
def main ():#line:5669
    import argparse #line:5670
    O0O00O0O0O00000O0 =argparse .ArgumentParser (description ="Enter arguments")#line:5671
    O0O00O0O0O00000O0 .add_argument ("-H","--host",required =True ,help ="Hostname or IP address")#line:5673
    O0O00O0O0O00000O0 .add_argument ("-U","--user",required =True ,help ="Username")#line:5674
    O0O00O0O0O00000O0 .add_argument ("-P","--password",required =True ,help ="Password")#line:5675
    O0O00O0O0O00000O0 .add_argument ("-p","--port",required =True ,help ="port")#line:5676
    O0O00O0O0O00000O0 .add_argument ("-D","--database",required =True ,help ="PostgreSQL database")#line:5677
    O0O00O0O0O00000O0 .add_argument ("-X","--excelpwd",required =True ,help ="Excel sheet password")#line:5678
    O0O00O0O0O00000O0 .add_argument ("-d","--dwsimpath",required =False ,help ="DWSIM Path")#line:5679
    OO0O00O0OO000000O =O0O00O0O0O00000O0 .parse_args ()#line:5681
    OO0O00O0OOOOO0OO0 =OO0O00O0OO000000O .host #line:5684
    O00OOOO0OO0OO0000 =OO0O00O0OO000000O .user #line:5685
    O0OOO0000O0OO00OO =OO0O00O0OO000000O .password #line:5686
    O0OOO0O00O00O00OO =OO0O00O0OO000000O .database #line:5687
    OOOOOOOOOO0O0OOO0 =OO0O00O0OO000000O .port #line:5688
    O00O0000O00000000 =OO0O00O0OO000000O .excelpwd #line:5689
    OO0O0OOO000000OO0 =OO0O00O0OO000000O .dwsimpath #line:5690
    if OO0O0OOO000000OO0 ==None :#line:5692
        OO0O0OOO000000OO0 =''#line:5693
    print (f"Host: {OO0O00O0OOOOO0OO0}")#line:5696
    print (f"Database: {O0OOO0O00O00O00OO}")#line:5697
    print (f"User: {O00OOOO0OO0OO0000}")#line:5698
    OO0O0O00000OO0000 =slmApplication (O00OOOO0OO0OO0000 ,O0OOO0000O0OO00OO ,O00O0000O00000000 ,OO0O00O0OOOOO0OO0 ,O0OOO0O00O00O00OO ,OOOOOOOOOO0O0OOO0 ,OO0O0OOO000000OO0 )#line:5700
    O0O0OOO000O0O0OO0 =OO0O0O00000OO0000 .importRCAtemplates ()#line:5713
    OOOO00OO00O0000O0 =OO0O0O00000OO0000 .rcaID (O0O0OOO000O0O0OO0 )#line:5716
    OO0O0O00000OO0000 .cursor .execute ('''select "TimeStamp" from public."Calender_time" where "Kind" = 'Start_of_run';''')#line:5719
    O0OOO0OOOOO00OO0O =OO0O0O00000OO0000 .cursor .fetchall ()#line:5720
    OO0O0O00000OO0000 .conn .commit ()#line:5721
    OOOO000O0OO00O000 =O0OOO0OOOOO00OO0O [0 ][0 ]#line:5722
    O0OO0OO0O00000000 ={}#line:5724
    OO0O0O00000OO0000 .cursor .execute ('select * from public."Prestatus"')#line:5725
    O0OOO0OOOOO00OO0O =OO0O0O00000OO0000 .cursor .fetchall ()#line:5726
    OO0O0O00000OO0000 .conn .commit ()#line:5727
    O0OO0OO0O00000000 ={}#line:5729
    for O0O00O0OO00000000 in O0OOO0OOOOO00OO0O :#line:5730
        O0OO0OO0O00000000 [O0O00O0OO00000000 [0 ]]=[O0O00O0OO00000000 [1 ],O0O00O0OO00000000 [2 ]]#line:5731
    O0O00O00OOO0O00OO ={}#line:5735
    OO0O0OOOO00OOO0OO ={}#line:5736
    OO0O0O00000OO0000 .cursor .execute ('select "Asset", "HOS", "TodaySoFar" from public."HOS"')#line:5737
    OOO0OOOOOOO00O0OO =OO0O0O00000OO0000 .cursor .fetchall ()#line:5738
    OO0O0O00000OO0000 .conn .commit ()#line:5739
    for O0O00O0OO00000000 in OOO0OOOOOOO00O0OO :#line:5740
        O0O00O00OOO0O00OO [O0O00O0OO00000000 [0 ]]=O0O00O0OO00000000 [1 ]#line:5741
        OO0O0OOOO00OOO0OO [O0O00O0OO00000000 [0 ]]=O0O00O0OO00000000 [2 ]#line:5742
    O0O000O00O0OOOOOO ={}#line:5749
    for O0O00O0OO00000000 in O0O00O00OOO0O00OO .keys ():#line:5750
        O0O000O00O0OOOOOO [O0O00O0OO00000000 ]=1 #line:5751
    OOO00O0OOO000OOO0 =True #line:5755
    OO0O0O00000OO0000 .cursor .execute ('select "Standard_Key" from public."Input_Tags"')#line:5758
    O0OOO0OOOOO00OO0O =OO0O0O00000OO0000 .cursor .fetchall ()#line:5759
    OO0O0O00000OO0000 .conn .commit ()#line:5760
    OO000O0OO0OO0OOOO =[]#line:5762
    for O0O00O0OO00000000 in O0OOO0OOOOO00OO0O :#line:5763
        OO000O0OO0OO0OOOO .append (O0O00O0OO00000000 [0 ])#line:5764
    OO0O0O00000OO0000 .cursor .execute ('''select "TagName" from public."Output_Tags" where "Description" = 'To display instead of KPI';''')#line:5768
    O0OOO0OOOOO00OO0O =OO0O0O00000OO0000 .cursor .fetchall ()#line:5769
    OO0O0O00000OO0000 .conn .commit ()#line:5770
    O00OO00O0O0O00OO0 =[]#line:5771
    for O0O00O0OO00000000 in O0OOO0OOOOO00OO0O :#line:5772
        O00OO00O0O0O00OO0 .append (O0O00O0OO00000000 [0 ])#line:5773
    OO000O00OO0OOOOOO =1 #line:5777
    while OOO00O0OOO000OOO0 :#line:5779
        OOO0O00OO0OOO0O0O ,O0OO0OOO0OO00000O ,O0O0OO00000000OOO ,O0000OO00000O0OO0 =OO0O0O00000OO0000 .cloudDataLogging ()#line:5781
        print ("no. of total tags in simfile: ",len (OOO0O00OO0OOO0O0O .keys ()))#line:5782
        if O0O0OO00000000OOO =='Playback'or O0O0OO00000000OOO =='Normal':#line:5783
            for OOO00OOOO0O00O000 in range (O0OO0OOO0OO00000O ):#line:5784
                O00000OOO00O00O0O ={}#line:5785
                O0OOO000O00000O00 ={}#line:5786
                for O00O0O000O0O000OO in OO000O0OO0OO0OOOO :#line:5787
                    if O00O0O000O0O000OO =='Nav_GPS1_UTC':#line:5788
                        O00000OOO00O00O0O [O00O0O000O0O000OO ]=OOO0O00OO0OOO0O0O [O00O0O000O0O000OO ][OOO00OOOO0O00O000 ]#line:5789
                    else :#line:5790
                        if O00O0O000O0O000OO in OOO0O00OO0OOO0O0O .keys ():#line:5791
                            O0OOO000O00000O00 [O00O0O000O0O000OO ]=1 #line:5792
                            O0OO000O0O000000O =OOO0O00OO0OOO0O0O [O00O0O000O0O000OO ][OOO00OOOO0O00O000 ]#line:5794
                            if len (O0OO000O0O000000O )==0 :#line:5795
                                O0OO000O0O000000O =99 #line:5796
                            O00000OOO00O00O0O [O00O0O000O0O000OO ]=float (O0OO000O0O000000O )#line:5797
                        else :#line:5798
                            O0OOO000O00000O00 [O00O0O000O0O000OO ]=0 #line:5799
                            O00000OOO00O00O0O [O00O0O000O0O000OO ]=99 #line:5800
                OOO0O00OO0O00O00O =OO0O0O00000OO0000 .inputsLogging (OOO00OOOO0O00O000 ,OO000O0OO0OO0OOOO ,O00000OOO00O00O0O ,O0OOO000O00000O00 )#line:5810
                if OO000O00OO0OOOOOO ==1 or OO000O00OO0OOOOOO ==0 :#line:5812
                    OO0000OO00O00O0OO ={}#line:5813
                    OO000O00OOOOOOOO0 =['NS_GPS_019_PV','NS_PP004-03MI_PV','NS_PP043-03MI_PV','NS_PP009-03MI_PV','NS_PP044-03MI_PV','NS_PP036-03XI_PV','NS_PP037-03AXI_PV','NS_PP038-03AXI_PV','NS_PP038-03XC_PV','NS_PP040-03MI_PV','NS_PP045-03MI_PV','NS_PP046-03MI_PV','NS_PP061-03MI_PV','NS_PP030-03MI_PV','NS_PP058-03MI_PV','NS_PP033-03MI_PV','NS_PP059-03MI_PV','NS_MM048-XI_PV','NS_MM648-XI_PV','NS_MM018-XI_PV','NS_MM618-XI_PV','NS_MM023-XI_PV','NS_MM021-XI_PV','NS_MM623-XI_PV','NS_MM621-XI_PV','NS_NG1-40101_PV','NS_NG1-40102_PV','NS_NG1-40103_PV','NS_NG2-40101_PV','NS_NG2-40102_PV','NS_NG2-40103_PV','NS_MM944-XI_PV','NS_MF001-03MI_PV','NS_MF010-03MI_PV','NS_IG-00531_PV','NS_CF013-03MC_PV','NS_CF014-03MC_PV','NS_MM002-XI_PV','NS_MM602-XI_PV','NS_MM908-03XI_PV','NS_MM066-XI_PV','NS_MM666-XI_PV','NS_MM933-XI_PV']#line:5820
                    for O0O00O0OO00000000 in OO000O00OOOOOOOO0 :#line:5821
                        if O0O00O0OO00000000 in O00000OOO00O00O0O .keys ():#line:5823
                            OO00OO0O0000OOO00 =True #line:5824
                        else :#line:5825
                            OO00OO0O0000OOO00 =False #line:5826
                        if OO00OO0O0000OOO00 ==True and O00000OOO00O00O0O [O0O00O0OO00000000 ]==99 :#line:5827
                            OO0000OO00O00O0OO [O0O00O0OO00000000 ]=0 #line:5828
                        elif OO00OO0O0000OOO00 ==True :#line:5829
                            OO0000OO00O00O0OO [O0O00O0OO00000000 ]=1 #line:5830
                        else :#line:5831
                            OO0000OO00O00O0OO [O0O00O0OO00000000 ]=0 #line:5832
                O0O00OO0O0OOOO000 =OO0O0O00000OO0000 .runningStatus (O00000OOO00O00O0O ,OO0000OO00O00O0OO )#line:5834
                OO0O0O00000OO0000 .runningStatusLogging (O0O00OO0O0OOOO000 ,OOO0O00OO0O00O00O )#line:5841
                print ('running status logged')#line:5842
                print ("---------")#line:5843
                O00000O0OO000OO00 ,OO000OOO000O0OOOO =OO0O0O00000OO0000 .dwsimSimulation (O00000OOO00O00O0O ,O0O00OO0O0OOOO000 ,OOO0O00OO0O00O00O ,OO0000OO00O00O0OO )#line:5844
                print ("dwsim outputs are calculated")#line:5846
                print ("---------")#line:5847
                OO0O0O00000OO0000 .outputsLogging (O00000O0OO000OO00 ,O0O00OO0O0OOOO000 ,OOO0O00OO0O00O00O ,OO0000OO00O00O0OO )#line:5848
                if 'NS_IG004-XA_PV'in O00000OOO00O00O0O .keys ():#line:5850
                    OO0O0O00000OO0000 .alarmLoggingforNoKPIassets (O00OO00O0O0O00OO0 ,O00000OOO00O00O0O )#line:5851
                O00000OOO00O00O0O =O00000OOO00O00O0O |OO000OOO000O0OOOO #line:5853
                OO0OOOO00OOOO0O0O =OO0O0O00000OO0000 .updateSignal ()#line:5859
                if OO0OOOO00OOOO0O0O =='1':#line:5860
                    O0O0OOO000O0O0OO0 =OO0O0O00000OO0000 .importRCAtemplates ()#line:5862
                    OOOO00OO00O0000O0 =OO0O0O00000OO0000 .rcaID (O0O0OOO000O0O0OO0 )#line:5864
                    print ("rca templates and rca id were re-read after templates were updated by user")#line:5865
                if OO000O00OO0OOOOOO ==1 :#line:5871
                    O000OOO0OOO00O0O0 ,O000000O0O0O0OO0O =OO0O0O00000OO0000 .findRules (O0O0OOO000O0O0OO0 )#line:5872
                if OO000O00OO0OOOOOO ==1 or '2023-07-09 00:0'in OOO0O00OO0O00O00O :#line:5877
                    print ("finding target scenarios at start of program in case of simfiles updated after 0709")#line:5878
                    O0O0O000OO00OOO0O =OO0O0O00000OO0000 .findtargetScenarios (O000000O0O0O0OO0O ,O0OOO000O00000O00 )#line:5881
                O00000O0O00000OO0 ,O0O00O0O00OOOOO00 =OO0O0O00000OO0000 .rcaTemplatesReader (O0O0OOO000O0O0OO0 ,O00000OOO00O00O0O ,O0O00OO0O0OOOO000 ,O0O0O000OO00OOO0O )#line:5885
                print ("status and parent node are read")#line:5886
                print ("---------")#line:5887
                OO0OO0O00O0OO0O00 =OO0O0O00000OO0000 .logStatusandParentNode (O00000O0O00000OO0 ,O0O00O0O00OOOOO00 )#line:5889
                print ("rca update history is logged")#line:5894
                if OO000O00OO0OOOOOO ==1 :#line:5896
                    O0O0OOOO0000OO0O0 ,O000O0O000O00O0OO =OO0O0O00000OO0000 .RCAlevels (O0O00O00OOO0O00OO )#line:5897
                    print ("rca levels done")#line:5898
                    OO0O0O00000OO0000 .totalAvailableScenarios ()#line:5899
                    O0O0OOOO00OOOO00O =OOO0O00OO0O00O00O #line:5900
                    OO000O00OO0OOOOOO =0 #line:5903
                if OO0OOOO00OOOO0O0O =='1':#line:5905
                    O0O0OOOO0000OO0O0 ,O000O0O000O00O0OO =OO0O0O00000OO0000 .RCAlevels (O0O00O00OOO0O00OO )#line:5906
                    print ("rca levels done")#line:5907
                    OO0O0O00000OO0000 .totalAvailableScenarios ()#line:5908
                    OO0O0O00000OO0000 .cursor .execute ('''update public."Templates_update" set "Status" = '0' where "Activity" = 'RCA_templates_updated';''')#line:5910
                    OO0O0O00000OO0000 .conn .commit ()#line:5911
                    print ("rca levels and no. of scenarios updated after templates were updated by user")#line:5912
                    O000OOO0OOO00O0O0 =OO0O0O00000OO0000 .findRules (O0O0OOO000O0O0OO0 )#line:5914
                O00000O0O00000OO0 =OO0O0O00000OO0000 .applyInferredStatus (O00000O0O00000OO0 )#line:5917
                print ("inferred status applied")#line:5918
                O0OO0OO0O00000000 =OO0O0O00000OO0000 .updateRCAstatus (O0OO0OO0O00000000 ,O0O00OO0O0OOOO000 ,O00000O0O00000OO0 ,OOO0O00OO0O00O00O ,OOOO00OO00O0000O0 ,O000OOO0OOO00O0O0 ,O000O0O000O00O0OO )#line:5920
                print ("rca status is done")#line:5921
                O0O0OOOO00OOOO00O ,O0O000O00O0OOOOOO ,O0O00O00OOO0O00OO ,OO0O0OOOO00OOO0OO =OO0O0O00000OO0000 .saveHOS (O0O0OOOO00OOOO00O ,O0O000O00O0OOOOOO ,O0O00O00OOO0O00OO ,OOO0O00OO0O00O00O ,O0O00OO0O0OOOO000 ,O0O0OOOO0000OO0O0 ,OO0O0OOOO00OOO0OO )#line:5922
                print ("HOS are saved")#line:5923
                OO0O0O00000OO0000 .maintenanceAlarm (OOOO000O0OO00O000 ,O0O00O00OOO0O00OO )#line:5924
                print ("maintenance alarms checked")#line:5925
                OO0O0O00000OO0000 .saveAlertCount ()#line:5926
                print ("Alert count updated")#line:5927
                print ("All done! Time_onboard: ",OOO0O00OO0O00O00O ,"--- Time_now:",datetime .now ())#line:5930
                print ("================================================")#line:5931
                time .sleep (O0000OO00000O0OO0 )#line:5934
                if OOO00OOOO0O00O000 ==O0OO0OOO0OO00000O -1 :#line:5935
                    print ("reading new cloud inputs. TimeStamp is :",datetime .now ())#line:5936
                    OOO00O0OOO000OOO0 =True #line:5937
        else :#line:5940
            print ("Holding mode")#line:5941
            time .sleep (O0000OO00000O0OO0 )#line:5942
            OOO00O0OOO000OOO0 =True #line:5943
if __name__ =='__main__':#line:5946
    main ()#line:5947
