#!/usr/bin/env python

import os
import requests
import sys
import time
import re
import tempfile

from sdcardburner.imgburner import Burner, ProgressListener

import osdescriptors

class MyProgressListener(ProgressListener):
  def on_progress_update(self, progress_pct):
    sys.stdout.write("\rWriting: %d percent" % progress_pct)

  def on_error(self, error):
    print "\nError during writing!"

  def on_eject(self):
    print "\nEjecting..."

  def on_completed(self):
    print "\nYour sdcard is ready!"

def download_file(url, file_path) :
  localFilename = url.split('/')[-1]
  with open(file_path, 'wb') as f:
    start = time.clock()
    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length'))
    dl = 0
    if total_length is None: # no content length header
      f.write(r.content)
    else:
      for chunk in r.iter_content(1024):
        dl += len(chunk)
        f.write(chunk)
        done = int(50 * dl / total_length)
        sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)))
  return (time.clock() - start)

def main():
  print "Select the OS you want to install\n"
  i = 1
  for osdescriptor in osdescriptors.register:
    print "%d) %s" % (i, str(osdescriptor))
    i += 1
  os_index = -1
  while not 0 <= os_index < len(osdescriptors.register):
    os_index = int(input('\nSelect the OS you want to install: ')) - 1

  try:
    images = osdescriptors.register[os_index].get_images_list()
  except requests.exceptions.ConnectionError:
    print "Error fetching available images. Please check your connection and retry!"
    exit(0)

  i = 0
  print "\nAvailable images:\n"
  for image in images:
    i += 1
    print "%d) %s %s %s" % (i, image['name'], image['size'], image['date'])
  image_index = -1
  while not 0 <= image_index < len(images):
    image_index = int(input('\nSelect the image you want to flash: ')) - 1
  temp_dir = tempfile.gettempdir()
  img_zip = os.path.join(temp_dir, images[image_index]['name'])
  img_zip = img_zip.replace(' ', '_')
  try:
    print img_zip
    if not os.path.isfile(img_zip):
      download_file(images[image_index]['url'], img_zip)
  except requests.exceptions.ConnectionError:
    print "\nError downloading requested image. Please check your connection and retry!"
    exit(0)
  print "\nDownload completed!"
  print "Unzipping image... Please wait.."
  img_to_flash = osdescriptors.register[os_index].unzip_file(img_zip, temp_dir)
  print "Unzipping image completed!"
  #img_to_flash = img_zip
  progress_listener = MyProgressListener()
  burner = Burner()
  devices = burner.list_devices()
  i = 0
  print "\nAvailable devices:"
  for device in devices:
    i += 1
    print "%d\t%s" % (i, device['DeviceIdentifier'])
  device_index = -1
  while not 0 <= device_index < len(devices):
    device_index = int(input('\nSelect the device you want to use: ')) - 1
  selected_device = devices[device_index]
  burner.burn(selected_device, img_to_flash, progress_listener)

if __name__ == "__main__":
  main()
