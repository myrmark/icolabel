import keyring
import os
import pymysql
import subprocess
import sys

from datetime import datetime
from pick import pick
from time import sleep

user = os.getlogin()
dbpw = keyring.get_password("172.28.88.47", "simdbuploader")


def sqlquery(query): #column,table,where,value
    db = pymysql.connect(host="172.28.88.47",user="simdbuploader",password=dbpw,database="simdb")
    cursor = db.cursor()
    #cursor.execute(f"SELECT {column} FROM simdb.product_label WHERE pn='{itemnumber}'")
    cursor.execute(f"{query}")
    try:
        result = cursor.fetchone()[0]
    except Exception:
        result = False
    return(result)
    db.commit()
    db.close()
    
    
def dbupload(cmd1, cmd2):
    db = pymysql.connect(host="172.28.88.47",user="simdbuploader",password=dbpw,database="simdb")
    cursor = db.cursor()
    #sql= "INSERT INTO simdb.racks (customerid, projectid, articlenumber, rackserial, routerserial, customerserialprefix, customerserial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    #val = (serial, projectid, sap, simids['simid1'], sims['sim1'], simids['simid2'], sims['sim2'], simids['simid3'], sims['sim3'], simids['simid4'], sims['sim4'], simids['simid5'], sims['sim5'], simids['simid6'], sims['sim6'], simids['simid7'], sims['sim7'], simids['simid8'], sims['sim8'], simids['simid9'], sims['sim9'], simids['simid10'], sims['sim10'], simids['simid11'], sims['sim11'], simids['simid12'], sims['sim12'], simids['simid13'], sims['sim13'], simids['simid14'], sims['sim14'], simids['simid15'], sims['sim15'], simids['simid16'], sims['sim16'], firmwares['modemfirmware1'], firmwares['modemfirmware2'], firmwares['modemfirmware3'], firmwares['modemfirmware4'], firmwares['modemfirmware5'], firmwares['modemfirmware6'], imeis['imei1'], imeis['imei2'], imeis['imei3'], imeis['imei4'], imeis['imei5'], imeis['imei6'], modems['modem1'], modems['modem2'], modems['modem3'], modems['modem4'], modems['modem5'], modems['modem6'], wifis['wifi0'], wifis['wifi1'], mac, imp, mo)
    cursor.execute(cmd1, cmd2)
    db.commit()
    cursor.close()
    db.close()
    
    
def print_label(serial,sap,sapdb,unitname,concatenateserial,rackserial,user,printer,labelsize):
    cmd = "glabels-batch-qt  "\
        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/router_rack.glabels  "\
        f"-D  serial={serial}  "\
        f"-D  sap={sap}  "\
        f"-D  sapdb={sapdb}  "\
        f"-D  name={unitname}  "\
        f"-D  custs={concatenateserial}  "\
        f"-D  rackserial={rackserial}  "\
        f"-o  /home/{user}/labelfiles/{serial}.pdf".split("  ")
    subprocess.run(cmd)
    logisticsQR = str(serial)+" - "+str(rackserial)
    cmd = "glabels-batch-qt  "\
        f"/mnt/fs/Icomera/Line/Supply Chain/Production/Glabels/Templates/logisticslabel.glabels  "\
        f"-D  serial={logisticsQR}  "\
        f"-o  /home/{user}/labelfiles/{serial}l.pdf".split("  ")
    subprocess.run(cmd)
    sleep(1)
    cmd = f"lp -n 1 -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}.pdf -c /home/{user}/labelfiles/{serial}l.pdf -d {printer} -o media={labelsize}".split()
    subprocess.run(cmd)
    

title = 'Select printer: '
options = ['TTP-644MT', 'ME340_production', 'Zebra_ZT230_production', 'ME340_lager', 'Zebra_ZT230_lager']
printer, index = pick(options, title)
title = 'Choose label size: '
options = ['60x30mm', '100x20mm', '101x152mm']
labelsize, index = pick(options, title)
sap = input('Enter your SAP number: ')
customerid = sqlquery(f"SELECT customerid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")
projectid = sqlquery(f"SELECT projectid FROM simdb.custspecificracks WHERE articlenumber='{sap}'")


while True:
  
