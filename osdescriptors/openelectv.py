import requests
import re

class OpenElecTV():

  def __str__(self):
    return "OpenElecTV"

  def get_images_list(self):
    r = requests.get('http://openelec.thestateofme.com/official_images/')
    html = r.text
    pattern = "<a href=\"(.*)\">(.*)</a> (.*)   (.*)"
    i = 0
    images_list = []
    for m in re.finditer(pattern, html):
      if i >= 2:
        images_list.append({
          'url': "http://openelec.thestateofme.com/official_images/" + m.group(1),
          'name': m.group(2),
          'date': m.group(3), 'size': m.group(4)})
      i += 1
    return images_list[::-1]