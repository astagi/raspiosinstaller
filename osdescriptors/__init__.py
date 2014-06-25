from openelectv import OpenElecTV
from raspbian import Raspbian
from raspberry import Raspberry

register = []
register.append(type('Raspbian', (Raspberry,), {'id':'Raspbian'})())
register.append(type('Pidora', (Raspberry,), {'id':'Pidora'})())
register.append(type('OpenElecTV', (Raspberry,), {'id':'OpenELEC'})())
register.append(type('RaspBMC', (Raspberry,), {'id':'RaspBMC'})())
register.append(type('RISC OS', (Raspberry,), {'id':'RISC OS'})())
register.append(type('ARCH LINUX', (Raspberry,), {'id':'Raspbian'})())
