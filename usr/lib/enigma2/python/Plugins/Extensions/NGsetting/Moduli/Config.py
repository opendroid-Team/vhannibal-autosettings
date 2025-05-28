import re
import os
import sys
from random import choice
from urllib.request import urlopen, Request
from .Setting import *

Directory = os.path.dirname(sys.modules[__name__].__file__)
os.makedirs(os.path.join(Directory, 'NGsetting', 'Temp'), exist_ok=True)

Samanta = ''
try:
        import dinaconvertdate
except:
        Samanta = "dina"

std_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
}

ListAgent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
]

def RequestAgent():
        return choice(ListAgent)

def make_request(url):
        try:
                import requests
                response = requests.get(url, verify=False)
                if response.status_code == 200:
                        return response.text
        except Exception:
                try:
                        req = Request(url)
                        req.add_header('User-Agent', 'E2 Plugin Vhannibal')
                        with urlopen(req, timeout=10) as response:
                                return response.read().decode('utf-8')
                except:
                        return
        return

def ConverDate(data):
        anno = data[:2]
        mese = data[-4:][:2]
        giorno = data[-2:]
        return f"{giorno}/{mese}/{anno}"

def ConverDate_noyear(data):
        mese = data[-4:][:2]
        giorno = data[-2:]
        return f"{giorno}/{mese}"

def TestDsl():
        try:
                req = Request(f"http://www.vhannibal.net/{Samanta}.php")
                req.add_header('User-Agent', "VAS14")
                with urlopen(req) as response:
                        link = response.read().decode('utf-8')
                return re.compile('<src="(.+?)">', re.DOTALL).findall(link)[0]
        except:
                return

def DownloadSetting():
        lista = []
        try:
                link = make_request('http://www.vhannibal.net/asd.php')
                matches = re.compile(r'<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL).findall(link)
                for href, name, date in matches:
                        name = name.replace('&#127381;', '').replace('Vhannibal ', '')
                        lista.append((date, name, f"http://www.vhannibal.net/{href}"))
        except Exception:
                pass
        return lista

def Load():
        AutoTimer = '0'
        NameSat = 'Hot Bird 13°E'
        Data = '0'
        Type = '0'
        Personal = '0'
        DowDate = '0'
        path = os.path.join(Directory, 'NGsetting', 'Date')
        if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="ignore") as xf:
                        for line in xf:
                                try:
                                        key, val = line.strip().split('=', 1)
                                        key, val = key.strip(), val.strip()
                                        if key == 'AutoTimer': AutoTimer = val
                                        elif key == 'NameSat': NameSat = val
                                        elif key == 'Data': Data = val
                                        elif key == 'Type': Type = val
                                        elif key == 'Personal': Personal = val
                                        elif key == 'DowDate': DowDate = val
                                except:
                                        pass
        else:
                with open(path, 'w', encoding="utf-8") as f:
                        f.write('AutoTimer = 0\nNameSat = Hot Bird 13°E\nData = 0\nType = 0\nPersonal = 0\nDowDate = 0\n')
        return AutoTimer, NameSat, Data, Type, Personal, DowDate

def WriteSave(name, autotimer, Type, Data, Personal, DowDate):
        path = os.path.join(Directory, 'NGsetting', 'Date')
        with open(path, 'w', encoding="utf-8") as f:
                f.write(f"AutoTimer = {autotimer}\n")
                f.write(f"NameSat = {name}\n")
                f.write(f"Data = {Data}\n")
                f.write(f"Type = {Type}\n")
                f.write(f"Personal = {Personal}\n")
                f.write(f"DowDate = {DowDate}\n")

