#!C:\Python27\python.exe
"""
     this is python program to check which website is going down at which time using uptimerrobot api,
     how to use-
     step 1- run program writing python robot.py in windows
     step 2-install mysqldb (optional) # using command pip install MySQLdb
     step 3- install requests package (required) # using command pip install requests
     
  
 
"""
mysql_db_installed=0
proceed_without_MySQLdb_installed=0
import socket

try:
 import MySQLdb
 mysql_db_installed=1
 proceed_without_MySQLdb_installed=1
except ImportError, e:
    print "mysqldb package are not installed"

try:
 import requests
except ImportError, e:
    print "requests package are not installed, you must install it" 

try:
     from ConfigParser import *
except ImportError:
    print "could not import ConfigParser"
    
#supress any mysql warning
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning) 

api=""
api_ini_file_present=0
#in case if ini file is present but value is empty
api_is_empty_in_ini=0 
# you can change it where you want to save your api key
ini_path="D:\\api.ini"  


con= MySQLdb.connect("localhost","root","","uptime_robot1")
cursor=con.cursor()
Config=ConfigParser()
# check if api configuration file are present on disk
def check_ini_if_present(): 
    print "ini file are getting checked"
    global api_ini_file_present
   
    try:
        with open(ini_path) as f:
            Config.readfp(f)
        api_ini_file_present=1

    except IOError:
        api_ini_file_present=0

#if API configuration file are not present then this function will create a one
def create_ini():
    print "api configuration file are getting created"
    cfgfile = open(ini_path,'w')
    Config.add_section('api_key')
    Config.set('api_key','api',"")
    Config.write(cfgfile)
    cfgfile.close()
# each time program will run,this function will be caaled to read API from configuration file
def read_api_from_ini():
    global api
    global api_is_empty_in_ini
    Config.read(ini_path)
    api=Config.get('api_key', 'api')
    if len(api)==0:
        api_is_empty_in_ini=0
        print "api configuration file found but api number is empty"
    else:
        api_is_empty_in_ini=1
        print "api configuration file found with api number %s" %api
    return api

def write_api_into_ini(api):
    Config.set('api_key', 'api', api)
    with open('D:\\api.ini', 'w') as configfile:
        Config.write(configfile)

    
    
    
def insert_into_db_after_add_monitor(api,id,frnd_name,m_url,m_type):
    try:
        cursor.execute('INSERT INTO monitor VALUES ("%s","%s","%s","%s","%s")' % (api,id,frnd_name,m_url,m_type))
        con.commit()
    except:
        con.rollback()
            
           

def del_from_database(api,id):
    sql ="DELETE * FROM monitor WHERE api= %s and id=%s" %(api,id)  
    try :
        cursor.execute(sql)
        con.commit
    except :
        con.rollback
        print "could not saved into databse" 
def create_db() :
    try:
        sql='CREATE DATABASE IF NOT EXISTS robot'
        cursor.execute(sql)
    except :
        print "database could not be created"
    
def create_table():
    try:
        
        sql1 = """CREATE TABLE IF NOT EXISTS account (
            id int NOT NULL AUTO_INCREMENT,
            api  CHAR(40) NOT NULL,
            status  CHAR(20),
            monitor_limit INT,  
            uo_monitor INT,
            down_monitor INT,
            paused_monitor INT,
            PRIMARY KEY (id))"""
          
        cursor.execute(sql1)
    except :
        print "table could not be created"

def show_total_table():
    print ("total table is %d" % cursor.execute("SHOW TABLES"))
    for (table_name,) in cursor:
        print(table_name)
        
def show_all_monitor_detail (api):
            cursor.execute("SELECT * FROM monitor")
            #num_fields = len(cursor.description)
            #field_names = [i[0] for i in cursor.description]
            #print field_names
            sql="SELECT * FROM monitor WHERE api='%s'" %api
            cursor.execute(sql)
            rows=cursor.fetchall()
            for r in rows :
                print ("api is :- %s" %r[0])
                print ("id :- %s" %r[1])
                print ("friendly name:- %s" %r[2])
                print("url :-%s"%r[3])
                print("monitor type:- %s" %r[4])

def show_monitor_detail_by_name(api,frnd):
    sql="SELECT * FROM monitor WHERE api='%s' AND frnd='%s'" %(api,frnd)
    cursor.execute(sql)
    rows=cursor.fetchall()
    if len(rows)==0:
        print"no result found ,make sure friendly name is correct"
        return
    for r in rows :
        print ("api is :- %s" %r[0])
        print ("id :- %s" %r[1])
        print ("friendly name:- %s" %r[2])
        print("url :-%s"%r[3])
        print("monitor type:- %s" %r[4]) 
        

def show_monitor_detail_by_id(api,id):
    sql="SELECT * FROM monitor WHERE api='%s' AND id='%s'" %(api,id)
    cursor.execute(sql)
    rows=cursor.fetchall()
    if len(rows)==0:
        print"no result found ,make sure id is correct"
        return
    for r in rows :
        print ("api is :- %s" %r[0])
        print ("id :- %s" %r[1])
        print ("friendly name:- %s" %r[2])
        print("url :-%s"%r[3])
        print("monitor type:- %s" %r[4]) 
                
                
           
class robot:
        def __init__(self):
           return
        
        
    
        def check_api(self,api):
            argu={'apiKey':api,'format':'json','noJsonCallback':'1'}
            get_data=requests.get("https://api.uptimerobot.com/getAccountDetails",params=argu)
            data=get_data.json()
            stat=data['stat']
            if stat != "ok" :
                return 0
            else:
                return 1    
        
        def is_connected(self):
            try:
                REMOTE_SERVER = "www.google.com"
                host = socket.gethostbyname(REMOTE_SERVER)
                s = socket.create_connection((host, 80), 2)
                return True
            except:
                pass
            return False
            
        def show_account_detail(self,acc_dict):
            print('monitor limit :- {limit}'.format(**acc_dict))
            print('monitor interval:- {inter}'.format(**acc_dict))            
            print('up monitor :- {up_monitor}'.format(**acc_dict))            
            print('down monitor :- {d_monitor}'.format(**acc_dict))            
            print('paused monitor:- {paused}'.format(**acc_dict))
            print "go to main menu (Y/n)"
            while 1:
                op=raw_input()
                if op.isalpha():
                    if op =='y'or op=='Y':
                        return
                else:
                    print "press y or n only"
                    continue
            
            
       
          
        
        def get_account_detail(self,api):
             argu={'apiKey':api,'format':'json','noJsonCallback':'1'}
             get_data=requests.get("https://api.uptimerobot.com/getAccountDetails",params=argu)
             data=get_data.json()
             m_limit=data['account']['monitorLimit']
             m_interval=data['account']['monitorInterval']
             m_up_monitors=data['account']['upMonitors']
             d_up_monitors=data['account']['downMonitors']
             p_up_monitors=data['account']['pausedMonitors']
             acc_dict={'limit':m_limit,'inter':m_interval,'up_monitor':m_up_monitors,'d_monitor':d_up_monitors,'paused':p_up_monitors}
             self.show_account_detail(acc_dict)
        
        
        def get_monitor_by_id(self,api):
            
    
                
           while 1:
               key= raw_input("enter your monitor key")
               if len(key)==0:
                   print "key cant be blank"
                   continue
               break
           
           if self.is_connected() :
               argu={'apiKey':api,'alertContacts':'1','responseTimes':'1','responseTimesAverage':'180','monitors':key,'customUptimeRatio':'180','format':'json','noJsonCallback':'1'}
    
               url="https://api.uptimerobot.com/getMonitors"
               get_data=requests.get(url,params=argu)
               data=get_data.json()
               status=data['stat']
               if not status =="ok":
                   print "id is not valid"
                   return
               status = data.get('monitors').get('monitor')[0].get('status')
               
               id = data.get('monitors').get('monitor')[0].get('id')
               frndly_name=data.get('monitors').get('monitor')[0].get('friendlyname')
               all_time_up_ratio=data.get('monitors').get('monitor')[0].get('alltimeuptimeratio')
               url = data.get('monitors').get('monitor')[0].get('url')
               m_interval = data.get('monitors').get('monitor')[0].get('interval')
               id = data.get('monitors').get('monitor')[0].get('id')
               print "\t\t## monitor detail ##"
               print ("id -\t %s" %id)
               print ("friendly name -\t %s" %frndly_name)
               print ("All time up ratio-\t %s" %all_time_up_ratio)
               print ("url-\t %s" %url)
               print ("monitor interval-\t %s" %m_interval)
               response_times=data.get('monitors').get('monitor')[0].get('responsetime')
               for j in range(len(response_times)):
                    r_time=response_times[j]
                    m_date=r_time.get('datetime')
                    val=r_time.get('value')
                    print "response time %s with value %s"%( m_date,val)
               while 1:
                   op=raw_input("press G to go to main ")
                   if op.isalpha():
                       if op =='g'or op=='G':
                           return
                       else :
                           continue
                   else :
                         print "only alphabet are allowed"
                         continue
                   break
           else :
               print "You Are not connected to Internet"
               print "results are coming from local databases"
               show_monitor_detail_by_id(api,key)
                
                    
           
        
        def get_monitor_by_name(self,api,call_by_delete_fun=0):
            
            
            monitor_present=0
            m_date=""
            val=""
            
            while 1:
                name=raw_input("enter monitor friendly name\n")
                if len(name)==0 :
                    print "name can be blank"
                    continue
                break
            
            if not self.is_connected()  :
                print "You Are not connected to Internet"
                print "results are showing from databases"
                show_monitor_detail_by_name(api,name)
                return
            argu={'apiKey':api,'format':'json','noJsonCallback':'1','responseTimes':'1','responseTimesAverage':'180','customUptimeRatio':'180'}
    
            url="https://api.uptimerobot.com/getMonitors"
            get_data=requests.get(url,params=argu)
            data=get_data.json()
            status=data['stat']
            if not status =="ok":
                   print "no monitor is found from this name"
                   return
            monitors = data.get('monitors').get('monitor')
            for i in range(len(monitors)):
                monitor = monitors[i]
                if monitor.get('friendlyname') == name:
                     monitor_present=1
                     status = monitor.get('status')
                     alltimeuptimeratio = monitor.get('alltimeuptimeratio')
                     response_times=monitor.get('responsetime')
                     for j in range(len(response_times)):
                         r_time=response_times[j]
                         m_date=r_time.get('datetime')
                         val=r_time.get('value')
                     
            
            if monitor_present ==1:
                
                 print ("monitor %s is found" % name)
                 print ("status is :- %s" %status)
                 print ("all time up time ratio :- %s" % alltimeuptimeratio)
                 print "response time %s with value %s"%( m_date,val)
               
             
            else :
                print "no monitor is found, make sure name is correct"
                while 1:
                    choice= raw_input("Do you want to try again (Y/N)\n")
                    if len(choice) !=0 and choice.isalpha() :
                        if choice =="y" or choice == "Y":
                             self.get_monitor_by_name(api)
                        elif choice =="n"or choice=="N":
                             return
                        else :
                            print "only y and N are allowed"
                    
                    else :
                        print "input are not valid"


        
        
        
        def get_all_monitor(self,api):
            
            if not self.is_connected()  :
                print "You Are not connected to Internet"
                print "results are showing from databases"
                if mysql_db_installed==1 and  proceed_without_MySQLdb_installed==1:
                    show_all_monitor_detail(api)
                return
            argu={'apiKey':api,'alertContacts':'1','responseTimes':'1','responseTimesAverage':'180','customUptimeRatio':'180','format':'json','noJsonCallback':'1'}
            url="https://api.uptimerobot.com/getMonitors"
            get_data=requests.get(url,params=argu)
            data=get_data.json()
            status=data['stat']
            if not status =="ok":
                print "you dont have any monitor,but you can add new monitor"
                return
            monitors = data.get('monitors').get('monitor')
            for i in range(len(monitors)):
                monitor = monitors[i]
                status=monitor.get('status')
                id=monitor.get('id')
                f_name=monitor.get('friendlyname')
                url=monitor.get('url')
                m_type=monitor.get('type')
                if m_type =="1":
                    m_type="HTTP"
                elif m_type=="2":
                    m_type="HTTPS"
                elif : m_type="3":
                    m_type="FTP"
                elif :m_type=="4":
                    m_type="SMTP"
                
                all_time_up_ratio=monitor.get('alltimeuptimeratio')
                print ("monitor no. %d" %i)
                print ("url :- %s"%url)
                print ("friendly name :- %s"%f_name)
                print ("monitor id :- %s"%id)
                print ("monitor type :- %s"%m_type)
                print ("status :- %s"%status)
                print ("all time up ratio :- %s"%all_time_up_ratio)
                response_times=monitor.get('responsetime')
                for j in range(len(response_times)):
                    r_time=response_times[j]
                    m_date=r_time.get('datetime')
                    val=r_time.get('value')
                    print "response time %s with value %s"%( m_date,val)

        
        def get_monitor_detail(self,api):
            print "1-get all monitor detail"
            print "2- get a single monitor detail by their id"
            print "3- get a single monitor detail by friendly name"
            
            while 1:
                choice=raw_input("Enter your options\n")
                try:
                    int(choice)
                    break;
                except ValueError:
                    print("That's not an integer value!")
                    continue
            
            if choice=="1":
                self.get_all_monitor(api)
            elif choice=="2":
                self.get_monitor_by_id(api)
            elif choice=="3":
                self.get_monitor_by_name(api)
            else :
                print "you entered wrong choice"
                self.get_monitor_detail(api)
                    
        def add_monitor(self,api):
            if self.is_connected() == 0:
                print "you are not connected to internet"
                return
            frnd_name=""
            m_url=""
            m_type=""
            while 1:
                frnd_name=raw_input("enter monitor friendly name eg. google,facebook\n")
                if len(frnd_name)==0:
                    print "sorry we can't proceed without frirndly name, type quit to go to main  "
                    continue
                if frnd_name=="quit":
                    return
                break;
            while 1:
                m_url=raw_input("enter url\n")
                if len(m_url)==0:
                    print "sorry we can't proceed without url type quit to go to main  "
                    continue
                if m_url=="quit":
                    return
                break;
            while 1:
                m_type=raw_input("enter monitor type, 1 for http\n 2 for keyword\n 3 for ping\n 4 for port\n")
                if len(m_type)==0:
                    print "sorry we can't proceed without monitor type, type quit to go to main  "
                    continue
                if m_type=="quit":
                    return
                break;
            argu={'apiKey':api,'format':'json','noJsonCallback':'1','monitorFriendlyName':frnd_name,'monitorURL':m_url,'monitorType':m_type}
            url="https://api.uptimerobot.com/newMonitor"
            get_data=requests.get(url,params=argu)
            data=get_data.json()
            status=data['stat']
            if status=="ok" :
                id=data['monitor']['id']

                print "new monitor is successfully added"
                print ("status is %s" %status)
                print ("id is (write down it) %s" %id)
                print proceed_without_MySQLdb_installed
                if mysql_db_installed==1 and proceed_without_MySQLdb_installed==1:
                    insert_into_db_after_add_monitor(api,id,frnd_name,m_url,m_type)
               
        def del_monitor(self,api):
            
            monitor_present=0
            
            while 1:
                name=raw_input("enter monitor friendly name\n")
                if len(name)==0 :
                    print "name can be blank"
                    continue
                break
            
            if not self.is_connected()  :
                print "You Are not connected to Internet"
                return
            argu={'apiKey':api,'format':'json','noJsonCallback':'1'}
    
            url="https://api.uptimerobot.com/getMonitors"
            get_data=requests.get(url,params=argu)
            data=get_data.json()
            status=data['stat']
            if not status =="ok":
                   print "no monitor is found from this name"
                   return
            monitors = data.get('monitors').get('monitor')
            for i in range(len(monitors)):
                monitor = monitors[i]
                if monitor.get('friendlyname') == name:
                     monitor_present=1
                     status = monitor.get('status')
                     id=monitor.get('id')
                     
            
            if monitor_present ==1:
                print ("monitor %s is found" % name)
                argu={'apiKey':api,'monitorID':id,'format':'json','noJsonCallback':1}
                url="https://api.uptimerobot.com/deleteMonitor"
                send_request=requests.get(url,params=argu)
                data=send_request.json()
                status=data['stat']
                if status =="ok":
                    print "monitor is successfully deleted"
                    if mysql_db_installed==1 and proceed_without_MySQLdb_installed==1:
                        del_from_database(api,id)
                else :
                    print "monitor could not be deleted"
               
             
            else :
                print "no monitor is found, make sure name is correct"
         
            
            
            

if __name__== '__main__' :
    user=robot()
    
    if mysql_db_installed==1:
        create_db()
        create_table()
    else:
        while 1:
            ch=raw_input("do you want to proceed without local database, (y/n)\n")
            if len(ch==0):
                print "input vant be empty\n"
                continue
            if ch =="y" or ch=="Y":
                proceed_without_MySQLdb_installed=1
                break
            else:
                print "ok! first download MySQLdb package for python "+\
                    "windows user may try https://pypi.python.org/pypi/MySQL-python"
                proceed_without_MySQLdb_installed=0
     
    if mysql_db_installed==0 and proceed_without_MySQLdb_installed==0:
        exit()
    check_ini_if_present()
    if api_ini_file_present==0:
        print "configuration file does not exist"
        create_ini()
    
    if api_ini_file_present==1:
        read_api_from_ini()
    
    if api_is_empty_in_ini==0:
        while 1 :# check is api is valid or not
            api=raw_input("enter your api,if you dont have go to upimerobot.com and register\n")
            if user.check_api(api) ==0 :
                print "api is not valid"
                continue;
            else :
                print "api is valid"
                write_api_into_ini(api)

                break;
    while 1:
        print "1-get account detail"
        print "2-get monitor detail"
        print "3-add monitor"
        print "4-delete monitor"
        while 1:
            choice=raw_input("Enter your options\n")
            try:
                int(choice)
                break;
            except ValueError:
                print("That's not an integer value!")
                continue
        
        if choice=="1":
            user.get_account_detail(api)
        elif choice=="2":
            user.get_monitor_detail(api)
        elif choice=="3":
            user.add_monitor(api)
        elif choice=="4":
            user.del_monitor(api)
   
    