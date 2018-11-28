# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/NGsetting/__init__.py
from enigma import *
import os, glob

class DeletPy:

    def __init__(self):
        pass

    def Remove(self):
        for x in glob.glob('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/*'):
            jpy = x[-3:]
            if jpy == '.py':
                os.system('rm -fr ' + x)

        for x in glob.glob('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/*'):
            jpy = x[-3:]
            if jpy == '.py':
                os.system('rm -fr ' + x)

        open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/__init__.py', 'w')

    def RemovePy(self):
        self.iTimer = eTimer()
        self.iTimer.callback.append(self.Remove)
        self.iTimer.start(60000, True)