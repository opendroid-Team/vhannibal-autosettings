from enigma import eTimer
from random import choice
import re, glob, shutil, os, urllib2, urllib, time, sys
from os import statvfs
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from enigma import *
from Config import *
from Language import _
try:
        import zipfile
except:
        pass

Directory = os.path.dirname(sys.modules[__name__].__file__)
MinStart = int(choice(range(59)))

def DownloadPlugin(link):
        try:
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'VAS')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                Setting = open('/tmp/Plugin.zip', 'w')
                Setting.write(link)
                Setting.close()
                try:
                        os.system('unzip -o /tmp/Plugin.zip -d  /usr/lib/enigma2/python/Plugins/Extensions')
                except:
                        return

        except:
                return

        return True


def TimerControl():
        now = time.localtime(time.time())
        Ora = str(now[3]).zfill(2) + ':' + str(now[4]).zfill(2) + ':' + str(now[5]).zfill(2)
        Date = str(now[2]).zfill(2) + '-' + str(now[1]).zfill(2) + '-' + str(now[0])
        return '%s ora: %s' % (Date, Ora)


def StartSavingTerrestrialChannels():

        def ForceSearchBouquetTerrestrial():
                for file in sorted(glob.glob('/etc/enigma2/*.tv')):
                        f = open(file, 'r').read()
                        x = f.strip().lower()
                        if x.find('eeee0000') != -1:
                                if x.find('82000') == -1 and x.find('c0000') == -1:
                                        return file

        def ResearchBouquetTerrestrial(search):
                for file in sorted(glob.glob('/etc/enigma2/*.tv')):
                        f = open(file, 'r').read()
                        x = f.strip().lower()
                        x1 = f.strip()
                        if x1.find('#NAME') != -1:
                                if x.lower().find(search.lower()) != -1:
                                        if x.find('eeee0000') != -1:
                                                return file


        def SaveTrasponderService():
                TrasponderListOldLamedb = open(Directory + '/NGsetting/Temp/TrasponderListOldLamedb', 'w')
                ServiceListOldLamedb = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb', 'w')
                Trasponder = False
                inTransponder = False
                inService = False
                try:
                        LamedbFile = open('/etc/enigma2/lamedb')
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
                                if line.find('eeee0000') != -1:
                                        Trasponder = True
                                        if inTransponder:
                                                TrasponderListOldLamedb.write(line)
                                                line = LamedbFile.readline()
                                                TrasponderListOldLamedb.write(line)
                                                line = LamedbFile.readline()
                                                TrasponderListOldLamedb.write(line)
                                        if inService:
                                                tmp = line.split(':')
                                                ServiceListOldLamedb.write(tmp[0] + ':' + tmp[1] + ':' + tmp[2] + ':' + tmp[3] + ':' + tmp[4] + ':0\n')
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
                ReadingTempServicelist = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb').readlines()
                for jx in ReadingTempServicelist:
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
                for file in os.listdir('/etc/enigma2/'):
                        if re.search('^userbouquet.*.tv', file):
                                f = open('/etc/enigma2/' + file, 'r')
                                x = f.read()
                                if re.search('#NAME Digitale Terrestre', x, flags=re.IGNORECASE):
                                        return '/etc/enigma2/' + file

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


def StartProcess(link, type, Personal):

        def LamedbRestore():
                try:
                        TrasponderListNewLamedb = open(Directory + '/NGsetting/Temp/TrasponderListNewLamedb', 'w')
                        ServiceListNewLamedb = open(Directory + '/NGsetting/Temp/ServiceListNewLamedb', 'w')
                        inTransponder = False
                        inService = False
                        infile = open('/etc/enigma2/lamedb')
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
                        WritingLamedbFinal.write('eDVB services /4/\n')
                        TrasponderListNewLamedb = open(Directory + '/NGsetting/Temp/TrasponderListNewLamedb').readlines()
                        for x in TrasponderListNewLamedb:
                                WritingLamedbFinal.write(x)

                        try:
                                TrasponderListOldLamedb = open(Directory + '/NGsetting/Temp/TrasponderListOldLamedb').readlines()
                                for x in TrasponderListOldLamedb:
                                        WritingLamedbFinal.write(x)

                        except:
                                pass

                        WritingLamedbFinal.write('end\n')
                        ServiceListNewLamedb = open(Directory + '/NGsetting/Temp/ServiceListNewLamedb').readlines()
                        for x in ServiceListNewLamedb:
                                WritingLamedbFinal.write(x)

                        try:
                                ServiceListOldLamedb = open(Directory + '/NGsetting/Temp/ServiceListOldLamedb').readlines()
                                for x in ServiceListOldLamedb:
                                        WritingLamedbFinal.write(x)

                        except:
                                pass

                        WritingLamedbFinal.write('end\n')
                        WritingLamedbFinal.close()
                        return True
                except:
                        return False

        def DownloadSettingAgg(link):
                try:
                        req = urllib2.Request(link)
                        req.add_header('User-Agent', 'VAS')
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()
                        Setting = open(Directory + '/NGsetting/Temp/listaE2.zip', 'w')
                        Setting.write(link)
                        Setting.close()
                        if os.path.exists(Directory + '/NGsetting/Temp/listaE2.zip'):
                                os.system('mkdir ' + Directory + '/NGsetting/Temp/setting')
                                try:
                                        os.system('unzip ' + Directory + '/NGsetting/Temp/listaE2.zip -d  ' + Directory + '/NGsetting/Temp/setting')
                                except:
                                        pass

                                os.system('mkdir ' + Directory + '/NGsetting/Temp/enigma2')
                                os.system('find ' + Directory + '/NGsetting/Temp/setting -type f -print | sed \'s/ /" "/g\'| awk \'{ str=$0; sub(/\\.\\//, "", str); gsub(/.*\\//, "", str);print "mv " $0 " ' + Directory + '/NGsetting/Temp/enigma2/"str }\' | sh')
                                if os.path.exists(Directory + '/NGsetting/Temp/enigma2/lamedb'):
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
                        os.system('mkdir ' + Directory + '/NGsetting/SelectFolder')
                        jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select')
                        jjw = jw.readlines()
                        jw.close()
                        count = 1
                        list = []
                        for x in jjw:
                                try:
                                        jx = x.split('---')
                                        newfile = 'userbouquet.NgSetting' + str(count) + '.tv'
                                        os.system('cp /etc/enigma2/' + jx[0] + ' /' + Directory + '/NGsetting/SelectFolder/' + newfile)
                                        list.append((newfile, jx[1]))
                                        count = count + 1
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
                                        os.system('cp -rf ' + Directory + '/NGsetting/SelectFolder/' + jx[0] + '  /etc/enigma2/')
                                except:
                                        pass

                except:
                        pass

                return True

        def CreateUserbouquetPersonalSetting():
                try:
                        jw = open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack')
                        jjw = jw.readlines()
                        jw.close()
                except:
                        pass

                jRewriteBouquet = open('/etc/enigma2/bouquets.tv')
                RewriteBouquet = jRewriteBouquet.readlines()
                jRewriteBouquet.close()
                WriteBouquet = open('/etc/enigma2/bouquets.tv', 'w')
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
                        Counter = Counter + 1

                WriteBouquet.close()

        def TransferNewSetting():
                try:
                        os.system('rm -rf /etc/enigma2/lamedb')
                        os.system('rm -rf /etc/enigma2/*.radio')
                        os.system('rm -rf /etc/enigma2/*.tv')
                        os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/*.tv  /etc/enigma2/')
                        os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/*.radio  /etc/enigma2/')
                        os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/lamedb  /etc/enigma2/')
                        if not os.path.exists('/etc/enigma2/blacklist'):
                                os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/blacklist /etc/enigma2/')
                        if not os.path.exists('/etc/enigma2/whitelist'):
                                os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/whitelist /etc/enigma2/')
                        os.system('cp -rf ' + Directory + '/NGsetting/Temp/enigma2/satellites.xml /etc/tuxbox/')
                except:
                        return

                return True

        Status = True
        if int(type) == 1:
                SavingProcessTerrestrialChannels = StartSavingTerrestrialChannels()
                os.system('cp -r /etc/enigma2/ ' + Directory + '/NGsetting/enigma2')
        if not DownloadSettingAgg(link):
                os.system('cp   ' + Directory + '/NGsetting/enigma2/* /etc/enigma2')
                os.system('rm -fr ' + Directory + '/NGsetting/enigma2')
                Status = False
        else:
                personalsetting = False
                if int(Personal) == 1:
                        personalsetting = SavePersonalSetting()
                if TransferNewSetting():
                        if personalsetting:
                                if TransferPersonalSetting():
                                        CreateUserbouquetPersonalSetting()
                                        os.system('rm -fr ' + Directory + '/NGsetting/SelectFolder')
                                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/SelectBack /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select')
                        os.system('rm -fr ' + Directory + '/NGsetting/enigma2')
                else:
                        os.system('cp   ' + Directory + '/NGsetting/enigma2/* /etc/enigma2')
                        os.system('rm -fr ' + Directory + '/NGsetting/Temp/*')
                        Status = False
                if int(type) == 1 and Status:
                        if SavingProcessTerrestrialChannels:
                                if LamedbRestore():
                                        TransferBouquetTerrestrialFinal()
        os.system('rm -fr ' + Directory + '/NGsetting/Temp/*')
        return Status


class NgSetting:

        def __init__(self, session = None):
                self.session = session
                self.iTimer1 = eTimer()
                self.iTimer2 = eTimer()
                self.iTimer3 = eTimer()
                self.iTimer1.callback.append(self.startTimerSetting)
                self.iTimer2.callback.append(self.startTimerSetting)
                self.iTimer3.callback.append(self.startTimerSetting)

        def gotSession(self, session):
                self.session = session
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
                if int(AutoTimer) == 1:
                        self.TimerSetting()

        def StopTimer(self):
                try:
                        self.iTimer1.stop()
                except:
                        pass

                try:
                        self.iTimer2.stop()
                except:
                        pass

                try:
                        self.iTimer3.stop()
                except:
                        pass

        def TimerSetting(self):
                try:
                        self.StopTimer()
                except:
                        pass

                now = time.time()
                ttime = time.localtime(now)
                start_time1 = time.mktime([ttime[0], ttime[1], ttime[2], 6, MinStart, 0, ttime[6], ttime[7], ttime[8]])
                start_time2 = time.mktime([ttime[0], ttime[1], ttime[2], 14, MinStart, 0, ttime[6], ttime[7], ttime[8]])
                start_time3 = time.mktime([ttime[0], ttime[1], ttime[2], 22, MinStart, 0, ttime[6], ttime[7], ttime[8]])
                if start_time1 < now + 60:
                        start_time1 += 86400
                if start_time2 < now + 60:
                        start_time2 += 86400
                if start_time3 < now + 60:
                        start_time3 += 86400
                delta1 = int(start_time1 - now)
                delta2 = int(start_time2 - now)
                delta3 = int(start_time3 - now)
                self.iTimer1.start(1000 * delta1, True)
                self.iTimer2.start(1000 * delta2, True)
                self.iTimer3.start(1000 * delta3, True)

        def startTimerSetting(self, Auto = False):
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()

                def OnDsl():
                        try:
                                urllib2.urlopen('http://www.google.it', None, 3)
                                return True
                        except:
                                return False

                        return

                if OnDsl():
                        for date, name, link in DownloadSetting():
                                if name == NameSat:
                                        if date > Data or Auto:
                                                if StartProcess(link, Type, Personal):
                                                        now = time.time()
                                                        jt = time.localtime(now)
                                                        DowDate = str(jt[2]).zfill(2) + '-' + str(jt[1]).zfill(2) + '-' + str(jt[0]) + '   ' + str(jt[3]).zfill(2) + ':' + str(jt[4]).zfill(2) + ':' + str(jt[5]).zfill(2)
                                                        WriteSave(name, AutoTimer, Type, date, Personal, DowDate)
                                                        eDVBDB.getInstance().reloadServicelist()
                                                        eDVBDB.getInstance().reloadBouquets()
                                                        self.session.open(MessageBox, _('New Setting Vhannibal') + name + _(' of ') + ConverDate(date) + _(' updated'), MessageBox.TYPE_INFO, timeout=5)
                                                else:
                                                        self.session.open(MessageBox, _('Sorry!\nError Download Setting'), MessageBox.TYPE_ERROR, timeout=5)
                                        break

                self.TimerSetting()
