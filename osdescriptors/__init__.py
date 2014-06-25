from openelectv import OpenElecTV
from raspbian import Raspbian
from raspberry import Raspberry

register = []
register.append(type('OpenElecTV', (Raspberry,), {'id':'OpenELEC'})())
register.append(type('Raspbian', (Raspberry,), {'id':'Raspbian'})())
