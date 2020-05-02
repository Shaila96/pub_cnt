import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from pub_cnt import AltmetricService

if __name__ == "__main__":
  altmetric = AltmetricService()
  
  try:
    # print(altmetric.get_sp_data(pmid = 31704939).score)
    print(altmetric.get_sp_data(pmid = 31704939))
  except:
    print('Error occured unavailable due to %s' % sys.exc_info()[0].__name__)
