import logging
import requests, json
import pandas as pd
import sys
import time

def parse_data(data, keys):
  try:
    for key in keys:
      data = data[key]
    return [data]
  except:
    return 'Not Available'

def construct_data_frame(data, _id):
  get_value = lambda field: [data[field]] if field in data.keys() else 'Not Available'
  
  df = pd.DataFrame({
    'input_id': _id,
    'title': get_value('title'),
    'journal': get_value('journal'),
    'doi': get_value('doi'),
    'pmid': get_value('pmid'),
    'published_on': get_value('published_on'),
    'score': get_value('score'),
    'one_year_old_score': parse_data(data, ['history', '1y']),
    'readers_count': get_value('readers_count'),
    'cited_by_posts_count': get_value('cited_by_posts_count'),
    'cited_by_tweeters_count': get_value('cited_by_tweeters_count'),
    'cited_by_feeds_count': get_value('cited_by_feeds_count'),
    'cited_by_msm_count': get_value('cited_by_msm_count'),
    'cited_by_accounts_count': get_value('cited_by_accounts_count'),
    'type': get_value('type'),
    'altmetric_id': get_value('altmetric_id'),
    'publication_url': get_value('url')
  }, index = [0])
  
  return df

def handle_user_input(doi = None, pmid = None, dois = None, pmids = None):
  if doi:
    return 'doi', [str(doi)]
  if pmid:
    return 'pmid', [str(pmid)]
  if dois:
    return 'doi', list(map(str, dois))
  if dois:
    return 'pmid', list(map(str, pmids))
  
  return '', list('')

def get_data(doi = None, pmid = None, dois = None, pmids = None):
  id_type, ids = handle_user_input(doi, pmid, dois, pmids)
  result_df = pd.DataFrame({})
  
  for i, _id in enumerate(ids):
    try:
      response = requests.get(lambda id_type, _id:
      'https://api.altmetric.com/v1/%s/%s' % (id_type, _id),
        headers = {'Accept': 'application/json'})
      
      # if response.status_code == 429:
      #   print("Rate is limited and you finished your rate")
      #   time.sleep(3600)
      #   i = i - 1
      #   continue
      # elif response.status_code == 502:
      #   print("API under  maintenance")
      #   time.sleep(3600)
      #   i = i - 1
      #   continue
      
      json_data = json.loads(response.text.encode('utf-8'))
    
    except:
      logging.error('Data unavailable for %s:%s due to %s' % (id_type, _id, sys.exc_info()[0].__name__))
      json_data = {}

    result_df = result_df.append(construct_data_frame(json_data, _id))
  
  return result_df
