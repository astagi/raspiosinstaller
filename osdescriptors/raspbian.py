from raspberry import Raspberry

class Raspbian(Raspberry):
  def __str__(self):
    return 'Raspbian'

if __name__ == "__main__":
  r = Raspbian()
  print r.get_images_list()