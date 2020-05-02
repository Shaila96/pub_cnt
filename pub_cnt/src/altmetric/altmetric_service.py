import logging
import requests
import json
import pandas as pd

class AltmetricService():
  def parse_data(self, data, keys):
    try:
      for key in keys:
        data = data[key]
      return [data]
    except:
      return 'Not Available'
  
  def download_data(self, parameter, _id):
    response = requests.get('https://api.altmetric.com/v1/%s/%s' % (parameter, str(_id)),
      headers = {'Accept': 'application/json'})
    
    if response.status_code == 200:
      try:
        json_data = json.loads(response.text.encode('utf-8'))
      except:
        logging.error("data not available")
        return
      
      get_value = lambda field: [json_data[field]] if field in json_data.keys() else 'Not Available'
      
      df = pd.DataFrame({
        'title': get_value('title'),
        'journal': get_value('journal'),
        'doi': get_value('doi'),
        'pmid': get_value('pmid'),
        'published_on': get_value('published_on'),
        'score': get_value('score'),
        'one_year_score': self.parse_data(json_data, ['history', '1y']),
        'readers_count': get_value('readers_count'),
        'cited_by_posts_count': get_value('cited_by_posts_count'),
        'cited_by_tweeters_count': get_value('cited_by_tweeters_count'),
        'cited_by_feeds_count': get_value('cited_by_feeds_count'),
        'cited_by_msm_count': get_value('cited_by_msm_count'),
        'cited_by_accounts_count': get_value('cited_by_accounts_count'),
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
