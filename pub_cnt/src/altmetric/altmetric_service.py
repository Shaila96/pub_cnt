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
      
      doi = []
      pmid = []
      score = []
      
      doi.append(json_data['doi'])
      pmid.append(json_data['pmid'])
      score.append(json_data['score'])
      
      df = pd.DataFrame({'doi': doi,
        'pmid': pmid,
        'score': score,
      })
      
      return df
  
  def get_sp_data(self, doi = None, pmid = None):
    if doi:
      self.download_data('doi', doi)
    elif pmid:
      return self.download_data('pmid', pmid)
    else:
      logging.error('doi or pubmed id must be provided')
      return
