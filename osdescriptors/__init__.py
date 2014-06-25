from raspberryosmanager import RaspberryOSManager

def create_manager(name, id=None):
  if not id:
    id = name
  return type(name, (RaspberryOSManager,), {'id':id})()

register = []
register.append(create_manager('Raspbian'))
register.append(create_manager('Pidora'))
register.append(create_manager('OpenElecTV', 'OpenElec'))
register.append(create_manager('RaspBMC'))
register.append(create_manager('RISC OS'))
register.append(create_manager('ARCH LINUX'))

