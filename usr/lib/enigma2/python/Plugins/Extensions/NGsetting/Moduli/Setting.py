import glob
import os
import re
import shutil
import sys
import time
from .Config import *
from .Language import _
from .Lcn import *
from .Select import *
import zipfile
from urllib.request import urlopen, Request
try:
    from requests import get
except ImportError:
    get = None

PY3 = sys.version_info[0] >= 3

Directory = os.path.dirname(sys.modules[__name__].__file__)
ee2ldb = '/etc/enigma2/lamedb'
ServOldLamedb = '/NGsetting/Temp/ServiceListOldLamedb'
TransOldLamedb = '/NGsetting/Temp/TrasponderListOldLamedb'
TerChArch = '/NGsetting/Temp/TerrestrialChannelListArchive'
SelBack = Directory + '/Moduli/NGsetting/SelectBack'
SSelect = Directory + '/Moduli/NGsetting/Select'
DIGTV = 'eeee0000'
keepdtt = False


def TimerControl():
        now = time.localtime(time.time())
        Ora = str(now[3]).zfill(2) + ':' + str(now[4]).zfill(2) + ':' + str(now[5]).zfill(2)
        Date = str(now[2]).zfill(2) + '-' + str(now[1]).zfill(2) + '-' + str(now[0])
        return '%s ora: %s' % (Date, Ora)


def StartSavingTerrestrialChannels():

        def ForceSearchBouquetTerrestrial():
                for file in sorted(glob.glob("/etc/enigma2/*.tv")):
                        f = open(file, "r").read()
                        x = f.strip().lower()
                        if x.find('eeee') != -1:
                                # if x.find('82000') == -1 and x.find('c0000') == -1:
                                return file
                                break

        def ResearchBouquetTerrestrial(search):
                for file in sorted(glob.glob("/etc/enigma2/*.tv")):
                        f = open(file, "r").read()
                        x = f.strip().lower()
                        x1 = f.strip()
                        if x1.find("#NAME") != -1:
                                if x.lower().find(search.lower()) != -1:
                                        if x.find('eeee') != -1:
                                                return file
                                                break

        def SaveTrasponderService():
                TrasponderListOldLamedb = open(Directory + '/NGsetting/Temp/TrasponderListOldLamedb', 'w')
                ServiceListOldLamedb = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb', 'w')
                Trasponder = False
                inTransponder = False
                inService = False
                try:
                        LamedbFile = open('/etc/enigma2/lamedb', 'r')
                        while 1:
                                line = LamedbFile.readline()
                                if not line:
                                        break
                                if not (inTransponder or inService):
                                        if line.find('transponders') == 0:
                                                inTransponder = True
                                        if line.find('services') == 0:
                                                inService = True
                                if line.find('end') == 0:
                                        inTransponder = False
                                        inService = False
                                line = line.lower()
                                # if line.find(DIGTV[:4]) != -1:
                                if line.find('eeee') != -1:
                                        Trasponder = True
                                        if inTransponder:
                                                TrasponderListOldLamedb.write(line)
                                                line = LamedbFile.readline()
                                                TrasponderListOldLamedb.write(line)
                                                line = LamedbFile.readline()
                                                TrasponderListOldLamedb.write(line)
                                        if inService:
                                                tmp = line.split(':')
                                                ServiceListOldLamedb.write(tmp[0] + ":" + tmp[1] + ":" + tmp[2] + ":" + tmp[3] + ":" + tmp[4] + ":0\n")
                                                line = LamedbFile.readline()
                                                ServiceListOldLamedb.write(line)
                                                line = LamedbFile.readline()
                                                ServiceListOldLamedb.write(line)
                        TrasponderListOldLamedb.close()
                        ServiceListOldLamedb.close()
                        if not Trasponder:
                                os.system('rm -fr ' + Directory + '/NGsetting/Temp/TrasponderListOldLamedb')
                                os.system('rm -fr ' + Directory + '/NGsetting/Temp/ServiceListOldLamedb')
                except:
                        pass
                return Trasponder

        def CreateBouquetForce():
                WritingBouquetTemporary = open(Directory + '/NGsetting/Temp/TerrestrialChannelListArchive', 'w')
                WritingBouquetTemporary.write('#NAME terrestre\n')
                ReadingTempServicelist = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb', 'r').readlines()
                for jx in ReadingTempServicelist:
                        # if jx.find(DIGTV[:4]) != -1:
                        if jx.find('eeee') != -1:
                                String = jx.split(':')
                                WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n' % (hex(int(String[4]))[2:], String[0], String[2], String[3], String[1]))
                WritingBouquetTemporary.close()

        def SaveBouquetTerrestrial():
                NameDirectory = ResearchBouquetTerrestrial('terr')
                if not NameDirectory:
                        NameDirectory = ForceSearchBouquetTerrestrial()
                try:
                        shutil.copyfile(NameDirectory, Directory + '/NGsetting/Temp/TerrestrialChannelListArchive')
                        return True
                except:
                        pass

        Service = SaveTrasponderService()
        if Service:
                if not SaveBouquetTerrestrial():
                        CreateBouquetForce()
                return True


def TransferBouquetTerrestrialFinal():

        def RestoreTerrestrial():
                for file in os.listdir("/etc/enigma2/"):
                        if re.search('^userbouquet.*.tv', file):
                                f = open("/etc/enigma2/" + file, "r")
                                x = f.read()
                                if re.search('#NAME Digitale Terrestre', x, flags=re.IGNORECASE) or re.search('#NAME DTT', x, flags=re.IGNORECASE):  # for disa51
                                        return "/etc/enigma2/" + file

        try:
                TerrestrialChannelListArchive = open(Directory + '/NGsetting/Temp/TerrestrialChannelListArchive').readlines()
                DirectoryUserBouquetTerrestrial = RestoreTerrestrial()
                if DirectoryUserBouquetTerrestrial:
                        TrasfBouq = open(DirectoryUserBouquetTerrestrial, 'w')
                        for Line in TerrestrialChannelListArchive:
                                if Line.lower().find('#name') != -1:
                                        TrasfBouq.write('#NAME Digitale Terrestre\n')
                                else:
                                        TrasfBouq.write(Line)
                        TrasfBouq.close()
                        return True
        except:
                return False


def SearchDTT():
        dtt_list = []
        for dtt_file in sorted(glob.glob("/etc/enigma2/userbouquet.*.tv")):
                dtbq = open(dtt_file, "r").read()
                dtbq_lines = dtbq.strip().lower()
                if "eee" in dtbq_lines:
                        dtt_list.append(os.path.basename(dtt_file))

        if not dtt_list:
                return False
        else:
                return dtt_list


def SearchIPTV():
        iptv_list = []
        for iptv_file in sorted(glob.glob("/etc/enigma2/userbouquet.*.tv")):
                usbq = open(iptv_file, "r").read()
                usbq_lines = usbq.strip().lower()
                if "http" in usbq_lines:
                        iptv_list.append(os.path.basename(iptv_file))
        if not iptv_list:
                return False
        else:
                return iptv_list


def StartProcess(link, type, Personal):

        def LamedbRestore():
                try:
                        TrasponderListNewLamedb = open(Directory + '/NGsetting/Temp/TrasponderListNewLamedb', 'w')
                        ServiceListNewLamedb = open(Directory + '/NGsetting/Temp/ServiceListNewLamedb', 'w')
                        inTransponder = False
                        inService = False
                        infile = open('/etc/enigma2/lamedb', 'r')
                        while 1:
                                line = infile.readline()
                                if not line:
                                        break
                                if not (inTransponder or inService):
                                        if line.find('transponders') == 0:
                                                inTransponder = True
                                        if line.find('services') == 0:
                                                inService = True
                                if line.find('end') == 0:
                                        inTransponder = False
                                        inService = False
                                if inTransponder:
                                        TrasponderListNewLamedb.write(line)
                                if inService:
                                        ServiceListNewLamedb.write(line)
                        TrasponderListNewLamedb.close()
                        ServiceListNewLamedb.close()
                        WritingLamedbFinal = open('/etc/enigma2/lamedb', 'w')
                        WritingLamedbFinal.write("eDVB services /4/\n")
                        TrasponderListNewLamedb = open(Directory + '/NGsetting/Temp/TrasponderListNewLamedb', 'r').readlines()
                        for x in TrasponderListNewLamedb:
                                WritingLamedbFinal.write(x)
                        try:
                                TrasponderListOldLamedb = open(Directory + '/NGsetting/Temp/TrasponderListOldLamedb', 'r').readlines()
                                for x in TrasponderListOldLamedb:
                                        WritingLamedbFinal.write(x)
                        except:
                                pass
                        WritingLamedbFinal.write("end\n")
                        ServiceListNewLamedb = open(Directory + '/NGsetting/Temp/ServiceListNewLamedb', 'r').readlines()
                        for x in ServiceListNewLamedb:
                                WritingLamedbFinal.write(x)
                        try:
                                ServiceListOldLamedb = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb', 'r').readlines()
                                for x in ServiceListOldLamedb:
                                        WritingLamedbFinal.write(x)
                        except:
                                pass
                        WritingLamedbFinal.write("end\n")
                        WritingLamedbFinal.close()
                        return True
                except:
                        return False

        def DownloadSettingAgg(link):
                foldsettmp = Directory + '/NGsetting/Temp/listaE2.zip'
                tmpe2 = Directory + '/NGsetting/Temp/enigma2'
                tmpextr = Directory + '/NGsetting/Temp/setting'
                dir_name = '/tmp/unzipped'
                if not os.path.exists(tmpe2):
                        os.system('mkdir ' + tmpe2)
                if not os.path.exists(tmpextr):
                        os.system('mkdir ' + tmpextr)
                try:
                        if PY3 and get:
                                link_zip = get(link)
                                with open(foldsettmp, 'wb') as f:
                                        f.write(link_zip.content)
                        else:
                                req = Request(link)
                                req.add_header('User-Agent', "VAS14")
                                response = urlopen(req)
                                rlink = response.read()
                                response.close()
                                Setting = open(foldsettmp, 'w')
                                Setting.write(rlink)
                                Setting.close()
                        if os.path.exists(foldsettmp):
                                try:
                                        image_zip = zipfile.ZipFile(Directory + '/NGsetting/Temp/listaE2.zip')
                                        image_zip.extractall(tmpextr)
                                        dir_setting = os.listdir(tmpextr)
                                        name_setting = dir_setting[0]
                                        dir_name = tmpextr + '/' + name_setting
                                        print('1 dir name=', dir_name)
                                        for filename in glob.glob(os.path.join(dir_name, '*')):
                                                shutil.copy(filename, tmpe2)
                                except:
                                        if os.path.exists(tmpextr):
                                                cmd = "rm -rf '" + tmpextr + "'"
                                                os.system(cmd)
                                        cmd2 = "unzip -o -q '" + foldsettmp + " -d " + tmpextr
                                        os.system(cmd2)
                                        for root, dirs, files in os.walk(tmpextr):
                                                for name_setting in dirs:
                                                        dir_name = tmpextr + '/' + name_setting
                                                        print('2 dir name=', dir_name)
                                        for filename in glob.glob(os.path.join(dir_name, '*')):
                                                shutil.copy(filename, tmpe2)
                                if os.path.exists(Directory + "/NGsetting/Temp/enigma2/lamedb"):
                                        return True
                        return False
                except:
                        return

        def SaveList(list):
                jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack', 'w')
                for dir, name in list:
                        jw.write(dir + '---' + name + '\n')
                jw.close()

        def SavePersonalSetting():
                try:
                        if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectFolder'):
                                os.system('mkdir /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectFolder')
                        jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select')
                        jjw = jw.readlines()
                        jw.close()
                        count = 1
                        list = []
                        for x in jjw:
                                try:
                                        jx = x.split('---')
                                        newfile = 'userbouquet.NgSetting' + str(count) + '.tv'
                                        os.system('cp -rf /etc/enigma2/' + jx[0] + ' /' + Directory + '/NGsetting/SelectFolder/' + newfile)
                                        list.append((newfile, jx[1]))
                                        count += 1
                                except:
                                        pass
                        SaveList(list)
                except:
                        return
                return True

        def TransferPersonalSetting():
                try:
                        jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack')
                        jjw = jw.readlines()
                        jw.close()
                        for x in jjw:
                                try:
                                        jx = x.split('---')
                                        os.system("cp -rf " + Directory + '/NGsetting/SelectFolder/' + jx[0] + "  /etc/enigma2/")
                                except:
                                        pass
                except:
                        pass
                return True

        def CreateUserbouquetPersonalSetting():
                try:
                        jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack', 'r')
                        jjw = jw.readlines()
                        jw.close()
                except:
                        pass
                jRewriteBouquet = open("/etc/enigma2/bouquets.tv", 'r')
                RewriteBouquet = jRewriteBouquet.readlines()
                jRewriteBouquet.close()
                WriteBouquet = open("/etc/enigma2/bouquets.tv", "w")
                Counter = 0
                for xx in RewriteBouquet:
                        if Counter == 1:
                                for x in jjw:
                                        if x[0].strip() != '':
                                                try:
                                                        jx = x.split('---')
                                                        WriteBouquet.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + jx[0].strip() + '" ORDER BY bouquet\n')
                                                except:
                                                        pass
                                WriteBouquet.write(xx)
                        else:
                                WriteBouquet.write(xx)
                        Counter += 1
                WriteBouquet.close()

        def KeepIPTV():
                iptv_to_save = SearchIPTV()
                if iptv_to_save:
                        for iptv in iptv_to_save:
                                os.system("cp -rf /etc/enigma2/" + iptv + " " + Directory + "/NGsetting/Temp/enigma2/" + iptv)

        def KeepDTT():
                dtt_to_save = SearchDTT()
                if dtt_to_save:
                        for dtt in dtt_to_save:
                                os.system("cp -rf /etc/enigma2/" + dtt + " " + Directory + "/NGsetting/Temp/enigma2/" + dtt)

        def TransferNewSetting():
                try:
                        if keepdtt is True:
                                KeepDTT()
                        KeepIPTV()
                        os.system("rm -rf /etc/enigma2/lamedb")
                        os.system("rm -rf /etc/enigma2/*.radio")
                        os.system("rm -rf /etc/enigma2/*.tv")
                        os.system('rm -rf /etc/enigma2/*.del')
                        os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/*.tv /etc/enigma2/")
                        os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/*.radio /etc/enigma2/")
                        os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/lamedb /etc/enigma2/")
                        if not os.path.exists("/etc/enigma2/blacklist"):
                                os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/blacklist /etc/enigma2/")
                        if not os.path.exists("/etc/enigma2/whitelist"):
                                os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/whitelist /etc/enigma2/")
                        os.system("cp -rf " + Directory + "/NGsetting/Temp/enigma2/satellites.xml /etc/tuxbox/")
                except:
                        return
                return True
        Status = True
        if int(type) == 1:
                SavingProcessTerrestrialChannels = StartSavingTerrestrialChannels()
                os.system('cp -rf /etc/enigma2/ ' + Directory + '/NGsetting/enigma2')
        if not DownloadSettingAgg(link):
                os.system('cp -rf ' + Directory + '/NGsetting/enigma2/* /etc/enigma2')
                os.system('rm -rf ' + Directory + '/NGsetting/enigma2')
                Status = False
        else:
                personalsetting = False
                if int(Personal) == 1:
                        personalsetting = SavePersonalSetting()
                if TransferNewSetting():
                        if personalsetting:
                                if TransferPersonalSetting():
                                        CreateUserbouquetPersonalSetting()
                                        os.system('rm -rf ' + Directory + '/NGsetting/SelectFolder')
                                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select')
                        os.system('rm -rf ' + Directory + '/NGsetting/enigma2')
                else:
                        os.system('cp -rf ' + Directory + '/NGsetting/enigma2/* /etc/enigma2')
                        os.system('rm -rf ' + Directory + '/NGsetting/Temp/*')
                        Status = False
                if int(type) == 1 and Status:
                        if SavingProcessTerrestrialChannels:
                                if LamedbRestore():
                                        TransferBouquetTerrestrialFinal()
        # os.system('rm -rf ' + DirFolder + '/NGsetting/Temp/*')  # Delete all files and run a rescue reload
        return Status
