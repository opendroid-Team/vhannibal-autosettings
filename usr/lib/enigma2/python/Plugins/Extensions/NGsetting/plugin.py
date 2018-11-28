from Components.Label import Label
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.MultiContent import MultiContentEntryText
from enigma import *
import sys, os
from Moduli.Setting import *
from Moduli.Config import *
from Moduli.Language import _
from Moduli.Lcn import *
from Moduli.Select import *
Version = '1.4'

class MenuListiSettingE2(MenuList):

        def __init__(self, list):
                MenuList.__init__(self, list, True, eListboxPythonMultiContent)
                self.l.setFont(0, gFont('Regular', 25))
                self.l.setItemHeight(45)


class MenuListiSettingE2A(MenuList):

        def __init__(self, list):
                MenuList.__init__(self, list, True, eListboxPythonMultiContent)
                self.l.setFont(0, gFont('Regular', 25))
                self.l.setItemHeight(45)


class MenuiSettingE2(Screen, ConfigListScreen):

        def __init__(self, session):
                self.session = session
                skin = '%s/Skin/Main.xml' % os.path.dirname(sys.modules[__name__].__file__)
                f = open(skin, 'r')
                self.skin = f.read()
                f.close()
                Screen.__init__(self, session)
                self['actions'] = ActionMap(['OkCancelActions', 'ShortcutActions', 'WizardActions', 'ColorActions', 'SetupActions', 'NumberActions', 'MenuActions', 'HelpActions', 'EPGSelectActions'], 
                     {'ok': self.keyOK,
                      'up': self.keyUp,
                      'down': self.keyDown,
                      'blue': self.Auto,
                      'green': self.Lcn,
                      'yellow': self.Select,
                      'cancel': self.exitplug,
                      'left': self.keyRightLeft,
                      'right': self.keyRightLeft,
                      'red': self.exitplug}, -1)
                self['autotimer'] = Label('')
                self['namesat'] = Label('')
                self['text'] = Label('')
                self['dataDow'] = Label('')
                self['Green'] = Pixmap()
                self['Blue'] = Pixmap()
                self['Yellow'] = Pixmap()
                self['Green'].hide()
                self['Yellow'].show()
                self['Blue'].show()
                self['Key_Lcn'] = Label('')
                self.LcnOn = False
                if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Date') and os.path.exists('/etc/enigma2/lcndb'):
                        self['Key_Lcn'].setText(_('Lcn'))
                        self.LcnOn = True
                        self['Green'].show()
                self['Key_Red'] = Label(_('Exit'))
                self['Key_Green'] = Label(_('Setting Installed:'))
                self['Key_Personal'] = Label('')
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
                self['A'] = MenuListiSettingE2A([])
                self['B'] = MenuListiSettingE2([])
                self['B'].selectionEnabled(1)
                self['A'].selectionEnabled(1)
                self.currentlist = 'B'
                self.ServerOn = True
                self.DubleClick = True
                self.MenuA()
                self.List = DownloadSetting()
                self.MenuB()
                self.iTimer = eTimer()
                self.iTimer.callback.append(self.keyRightLeft)
                self.iTimer.start(1000, True)
                self.iTimer1 = eTimer()
                self.iTimer1.callback.append(self.StartSetting)
                self.Message = eTimer()
                self.Message.callback.append(self.MessagePlugin)
                self.OnWriteAuto = eTimer()
                self.OnWriteAuto.callback.append(self.WriteAuto)
                self.StopAutoWrite = False
                self.ExitPlugin = eTimer()
                self.ExitPlugin.callback.append(self.PluginClose)
                self.Reload = eTimer()
                self.Reload.callback.append(self.ReloadGui)
                self.onShown.append(self.ReturnSelect)
                self.onShown.append(self.Info)
                self.VersPlugin = Plugin()
                if self.VersPlugin:
                        if self.VersPlugin[0][1] != Version:
                                self.Message.start(2000, True)

        def PluginClose(self):
                try:
                        self.ExitPlugin.stop()
                except:
                        pass

                self.close()

        def exitplug(self):
                if self.DubleClick:
                        self.ExitPlugin.start(7000, True)
                        self.DubleClick = False
                        self.MenuB()
                else:
                        self.PluginClose()

        def MessagePlugin(self):
                self.session.openWithCallback(self.DownloadPlugin, MessageBox, _('New version %s \nWant to install?') % self.VersPlugin[0][1], MessageBox.TYPE_YESNO, timeout=20)

        def DownloadPlugin(self, conf):
                if conf:
                        if DownloadPlugin('http://www.vhannibal.net/' + self.VersPlugin[0][0]):
                                self.session.open(MessageBox, _('New version %s downloaded successfully\nRestart enigma2.. ...') % self.VersPlugin[0][1], MessageBox.TYPE_INFO)
                                self.Reload.start(2000, True)
                        os.system('rm -fr /tmp/Plugin.zip')

        def ReloadGui(self):
                quitMainloop(3)

        def Select(self):
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
                if str(Personal).strip() == '0':
                        self['Key_Personal'].setText(_('Favourites: Yes'))
                        Personal = '1'
                        self.session.open(MenuSelect)
                else:
                        self['Key_Personal'].setText(_('Favourites: No'))
                        Personal = '0'
                WriteSave(NameSat, AutoTimer, Type, Data, Personal, DowDate)

        def ReturnSelect(self):
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
                if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select') or os.path.getsize('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Select') < 20:
                        self['Key_Personal'].setText(_('Favourites: No'))
                        WriteSave(NameSat, AutoTimer, Type, Data, '0', DowDate)

        def Lcn(self):
                if self.LcnOn:
                        lcn = LCN()
                        lcn.read()
                        if len(lcn.lcnlist) > 0:
                                lcn.writeBouquet()
                                lcn.reloadBouquets()
                                self.session.open(MessageBox, _('Sorting Lcn Completed'), MessageBox.TYPE_INFO, timeout=5)

        def Auto(self):
                if self.StopAutoWrite:
                        return
                self.StopAutoWrite = True
                iTimerClass.StopTimer()
                self.AutoTimer, self.NameSat, self.Data, self.Type, self.Personal, self.DowDate = Load()
                if int(self.AutoTimer) == 0:
                        self['autotimer'].setText(_('AutoUpdate: Yes'))
                        self.AutoTimer = '1'
                        iTimerClass.TimerSetting()
                else:
                        self['autotimer'].setText(_('AutoUpdate: No'))
                        self.AutoTimer = '0'
                self.OnWriteAuto.start(500, True)

        def WriteAuto(self):
                self.StopAutoWrite = False
                WriteSave(self.NameSat, self.AutoTimer, self.Type, self.Data, self.Personal, self.DowDate)

        def Info(self):
                AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
                if int(AutoTimer) == 0:
                        TypeTimer = 'No'
                else:
                        TypeTimer = 'Yes'
                if int(Personal) == 0:
                        jPersonal = 'No'
                else:
                        jPersonal = 'Yes'
                if str(Data) == '0':
                        newdate = ''
                else:
                        newdate = ' - ' + ConverDate(Data)
                if str(DowDate) == '0':
                        newDowDate = _('Last Update: Unregistered')
                else:
                        newDowDate = _('Last Update: ') + DowDate
                self['Key_Personal'].setText(_('Favourites: ') + jPersonal)
                self['autotimer'].setText(_('AutoUpdate: ') + TypeTimer)
                self['namesat'].setText(NameSat + newdate)
                self['dataDow'].setText(newDowDate)

        def hauptListEntryMenuA(self, name, type):
                res = [(name, type)]
                res.append(MultiContentEntryText(pos=(35, 7), size=(170, 40), font=0, text=name, flags=RT_HALIGN_CENTER))
                res.append(MultiContentEntryText(pos=(0, 0), size=(4, 0), font=0, text=type, flags=RT_HALIGN_LEFT))
                return res

        def hauptListEntryMenuB(self, name, date, link, name1, date1):
                res = [(name, date, link, name1, date1)]
                res.append(MultiContentEntryText(pos=(15, 7), size=(435, 40), font=0, text=name, flags=RT_HALIGN_LEFT))
                res.append(MultiContentEntryText(pos=(460, 7), size=(210, 40), font=0, text=date1, color=16777215, flags=RT_HALIGN_LEFT))
                res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=link, flags=RT_HALIGN_LEFT))
                res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=name1, flags=RT_HALIGN_LEFT))
                res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=date, flags=RT_HALIGN_LEFT))
                return res

        def MenuA(self):
                self.jA = []
                self.jA.append(self.hauptListEntryMenuA('Mono', 'hot'))
                self.jA.append(self.hauptListEntryMenuA('Dual', 'dual'))
                self.jA.append(self.hauptListEntryMenuA('Trial', 'trial'))
                self.jA.append(self.hauptListEntryMenuA('Quadri', 'quadri'))
                self.jA.append(self.hauptListEntryMenuA('Motor', 'motor'))
                self['A'].setList(self.jA)

        def MenuB(self):
                self.jB = []
                if not self.DubleClick:
                        self.ServerOn = False
                        self.jB.append(self.hauptListEntryMenuB('', '', '', '', ''))
                        self.jB.append(self.hauptListEntryMenuB(_('Coder: m43c0 & ftp21'), '', '', '', ''))
                        self.jB.append(self.hauptListEntryMenuB(_('Skinner: mmark'), '', '', '', ''))
                        self.jB.append(self.hauptListEntryMenuB(_('Vhannibal Official Plugin'), '', '', '', ''))
                        self.jB.append(self.hauptListEntryMenuB(_('www.vhannibal.net'), '', '', '', ''))
                        self['B'].setList(self.jB)
                        return
                for date, name, link in self.List:
                        if name.lower().find(self['A'].getCurrent()[0][1]) != -1:
                                self.jB.append(self.hauptListEntryMenuB(str(name.title()), str(date), str(link), str(name), ConverDate(str(date))))

                if not self.jB:
                        self.jB.append(self.hauptListEntryMenuB(_('Server down for maintenance'), '', '', '', ''))
                        self['B'].setList(self.jB)
                        self.ServerOn = False
                        self.MenuA()
                        return
                self['B'].setList(self.jB)

        def keyOK(self):
                if not self.ServerOn:
                        return
                if self.currentlist == 'A':
                        self.currentlist = 'B'
                        self['B'].selectionEnabled(1)
                        self['A'].selectionEnabled(0)
                        return
                self.name = self['B'].getCurrent()[0][3]
                self.jType = '1'
                if self.name.lower().find('dtt') != -1:
                        self.jType = '0'
                self.AutoTimer, NameSat, self.Data, Type, self.Personal, self.DowDate = Load()
                try:
                        nData = int(self.Data)
                except:
                        nData = 0

                try:
                        njData = int(self['B'].getCurrent()[0][1])
                except:
                        njData = 999999

                if NameSat != self.name or Type != self.jType:
                        self.session.openWithCallback(self.OnDownload, MessageBox, _('The new configurations are saved\nSetting: %s\nDate: %s\nThe choice is different from the previous\nDo you want to proceed with the manual upgrade?') % (self.name, self['B'].getCurrent()[0][4]), MessageBox.TYPE_YESNO, timeout=20)
                elif njData > nData:
                        self.session.openWithCallback(self.OnDownload, MessageBox, _('The new configurations are saved\nSetting: %s\nDate: %s \n The new setting has a more recent date\nDo you want to proceed with the manual upgrade?') % (self.name, self['B'].getCurrent()[0][4]), MessageBox.TYPE_YESNO, timeout=20)
                else:
                        self.session.openWithCallback(self.OnDownloadForce, MessageBox, _('Setting already updated, you want to upgrade anyway?'), MessageBox.TYPE_YESNO, timeout=20)

        def OnDownloadForce(self, conf):
                if conf:
                        self.OnDownload(True, False)

        def StartSetting(self):
                iTimerClass.StopTimer()
                iTimerClass.startTimerSetting(True)

        def OnDownload(self, conf, noForce = True):
                if conf:
                        if noForce:
                                WriteSave(self.name, self.AutoTimer, self.jType, self.Data, self.Personal, self.DowDate)
                        self.iTimer1.start(100, True)
                else:
                        WriteSave(self.name, self.AutoTimer, self.jType, '0', self.Personal, self.DowDate)
                self.Info()

        def keyUp(self):
                self[self.currentlist].up()
                if self.currentlist == 'A':
                        self.MenuB()

        def keyDown(self):
                self[self.currentlist].down()
                if self.currentlist == 'A':
                        self.MenuB()

        def keyRightLeft(self):
                self['A'].selectionEnabled(0)
                self['B'].selectionEnabled(0)
                if self.currentlist == 'A':
                        if not self.ServerOn:
                                return
                        self.currentlist = 'B'
                        self['B'].selectionEnabled(1)
                        self.MenuB()
                else:
                        self.currentlist = 'A'
                        self['A'].selectionEnabled(1)


jsession = None
iTimerClass = NgSetting(jsession)

def SessionStart(reason, **kwargs):
        if reason == 0:
                iTimerClass.gotSession(kwargs['session'])
        jsession = kwargs['session']


iTimerClass = NgSetting(jsession)

def AutoStart(reason, **kwargs):
        if reason == 1:
                iTimerClass.StopTimer()


def Main(session, **kwargs):
        session.open(MenuiSettingE2)


def Plugins(**kwargs):
        return [PluginDescriptor(name='Vhannibal AutoSetting ' + Version, description='Vhannibal Official Plugin by NGSetting', icon='Panel/Vhannibal.png', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=Main), PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=SessionStart), PluginDescriptor(where=PluginDescriptor.WHERE_AUTOSTART, fnc=AutoStart)]


global jsession ## Warning: Unused global
