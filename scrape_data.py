import sys
from Bio import Entrez

Entrez.email = 'bepnye@gmail.com'

def fetch_abstracts(pmids):
  handle = Entrez.efetch(db='pubmed', id=pmids, retmode='xml')
  xml_data = Entrez.read(handle)['PubmedArticle']
  articles = [a['MedlineCitation'] for a in xml_data]
  data = {pmid: {} for pmid in pmids}
  for a in articles:
    try:
      pmid = str(a['PMID'])
      try:
        mesh = [str(m['DescriptorName']) for m in a['MeshHeadingList']]
      except KeyError:
        mesh = []
      pubs = [str(p) for p in a['Article']['PublicationTypeList']]
      data[pmid]['mesh'] = mesh
      data[pmid]['pubs'] = pubs
    except IndexError:
      pass
  return data

def write_data(data):
  for pmid in data:
    #with open('/Users/ben/pico/resources/mesh/%s.txt' %pmid, 'w') as fp:
    #  fp.write('\n'.join(data[pmid]['mesh']))
    with open('/Users/ben/pico/resources/pubs/%s.txt' %pmid, 'w') as fp:
      fp.write('\n'.join(data[pmid]['pubs']))

pmids = open('/Users/ben/Desktop/pmids.txt').read().split('\n')
n = 100
for i in range(400, len(pmids), n):
  pmid_chunk = pmids[i:i+n]
  print 'Processing pmids %d - %d' %(i, i+n) 
  data = fetch_abstracts(pmid_chunk)
  write_data(data)
