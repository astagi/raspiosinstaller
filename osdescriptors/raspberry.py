import requests
from bs4 import BeautifulSoup
import zipfile
import gzip

class Raspberry(object):

  def __str__(self):
    return self.id

  def get_images_list(self):
    return self._get_info()

  def _get_info(self):
    images_list = []
    image_details = []
    r = requests.get('http://www.raspberrypi.org/downloads/')
    html = r.text
    soup = BeautifulSoup(html)
    for image in soup.findAll('div', {'class':'image-info'}):
      if image.findNext('h3').next == str(self):
        imagelink = image.findNext('div', {'class':'image-download-links'})
        links = imagelink.findNext('a', {'class':'dl-zip'})
        for imagedetails in image.findAll('div', {'class':'image-details'})[:2]:
          image_details.append(imagedetails.findNext('strong').next)

        images_list.append({
          'url': links['href'],
          'name': str(self) + ' ' + image_details[0],
          'date': image_details[1],
          'size': ''})
        return images_list

  def _is_zip(self, header):
    zip_header = [0x50, 0x4b, 0x03, 0x04]
    for header_el in zip(header, zip_header):
      if ord(header_el[0]) != header_el[1]:
        return False
    return True

  def _is_gzip(self, header):
    zip_header = [0x1f, 0x8b]
    for header_el in zip(header, zip_header):
      if ord(header_el[0]) != header_el[1]:
        return False
    return True

  def unzip_file(self, zip_file, outpath):
    header = open(zip_file, 'rb').read(4)
    if self._is_gzip(header[:2]):
      fh = gzip.open(zip_file, 'rb')
      decoded = fh.read()
      uncompressed_path = zip_file + 'dec.iso'
      uncompressed_file = open(uncompressed_path,'wb')
      uncompressed_file.write(decoded)
      return uncompressed_path
    if self._is_zip(header):
      fh = open(zip_file, 'rb')
      z = zipfile.ZipFile(fh)
      img_name = ""
      for name in z.namelist():
        z.extract(name, outpath)
        img_name = name
      fh.close()
      return os.path.join(outpath, img_name)