import logging
import requests
import json
import pandas as pd

class AltmetricService():
  
  def download_data(self, parameter, _id):
    response = requests.get('https://api.altmetric.com/v1/%s/%s' % (parameter, str(_id)),
      headers = {'Accept': 'application/json'})
    
    if response.status_code == 200:
      try:
        json_data = json.loads(response.text.encode('utf-8'))
      except:
        logging.error("data not available")
        return
      
      df = pd.DataFrame({'doi': [json_data['doi']],
        'pmid': [json_data['pmid']],
        'score': [json_data['score']],
      })
      
      return df
  
  def get_sp_data(self, doi = None, pmid = None):
    if doi:
      return self.download_data('doi', doi)
    elif pmid:
      return self.download_data('pmid', pmid)
    else:
      logging.error('doi or pubmed id must be provided')
      return