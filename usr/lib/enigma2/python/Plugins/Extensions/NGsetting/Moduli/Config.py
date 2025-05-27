from random import choice
import re
import os
import sys
from urllib.request import urlopen, Request
from enigma import *
from .Setting import *

Directory = os.path.dirname(sys.modules[__name__].__file__)
os.makedirs(os.path.join(Directory, 'NGsetting', 'Temp'), exist_ok=True)

def ConverDate(data):
    anno = data[:2]
    mese = data[-4:][:2]
    giorno = data[-2:]
    return f"{giorno}/{mese}/{anno}"

def ConverDate_noyear(data):
    mese = data[-4:][:2]
    giorno = data[-2:]
    return f"{giorno}/{mese}"

def DownloadSetting():
    result = []
    try:
        import requests
        response = requests.get('http://www.vhannibal.net/asd.php', headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
    except ImportError:
        try:
            req = Request('http://www.vhannibal.net/asd.php')
            req.add_header('User-Agent', 'VAS14')
            response = urlopen(req, timeout=3)
            html = response.read().decode('utf-8', errors='ignore')
        except Exception:
            return result
    except Exception:
        return result

    pattern = re.compile(r'<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL)
    for link, name, date in pattern.findall(html):
        result.append((date, name.replace('Vhannibal ', ''), f"http://www.vhannibal.net/{link}"))
    return result

def Load():
    AutoTimer = '0'
    NameSat = 'Hot Bird 13°E'
    Data = '0'
    Type = '0'
    Personal = '0'
    DowDate = '0'
    date_file_path = os.path.join(Directory, 'NGsetting', 'Date')

    if os.path.exists(date_file_path):
        with open(date_file_path, "r", encoding="utf-8", errors="ignore") as xf:
            lines = xf.readlines()
        for line in lines:
            line = line.strip()
            if '=' not in line:
                continue
            key, value = map(str.strip, line.split('=', 1))
            if key == 'AutoTimer':
                AutoTimer = value
            elif key == 'NameSat':
                NameSat = value
            elif key == 'Data':
                Data = value
            elif key == 'Type':
                Type = value
            elif key == 'Personal':
                Personal = value
            elif key == 'DowDate':
                DowDate = value
    else:
        with open(date_file_path, "w", encoding="utf-8") as xf:
            xf.write('AutoTimer = 0\n')
            xf.write('NameSat = Hot Bird 13°E\n')
            xf.write('Data = 0\n')
            xf.write('Type = 0\n')
            xf.write('Personal = 0\n')
            xf.write('DowDate = 0\n')

    return AutoTimer, NameSat, Data, Type, Personal, DowDate

def WriteSave(name, autotimer, Type, Data, Personal, DowDate):
    date_file_path = os.path.join(Directory, 'NGsetting', 'Date')
    with open(date_file_path, "w", encoding="utf-8") as xf:
        xf.write(f"AutoTimer = {autotimer}\n")
        xf.write(f"NameSat = {name}\n")
        xf.write(f"Data = {Data}\n")
        xf.write(f"Type = {Type}\n")
        xf.write(f"Personal = {Personal}\n")
        xf.write(f"DowDate = {DowDate}\n")

def Plugin():
    try:
        import requests
        response = requests.get('http://www.vhannibal.net/asu.php', headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
    except ImportError:
        try:
            req = Request('http://www.vhannibal.net/asu.php')
            req.add_header('User-Agent', 'VAS14')
            response = urlopen(req, timeout=3)
            html = response.read().decode('utf-8', errors='ignore')
        except Exception:
            return []
    except Exception:
        return []

    return re.compile(r'<a href="(.+?)" src="(.+?)">updater</a>').findall(html)