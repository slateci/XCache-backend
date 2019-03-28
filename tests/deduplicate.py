from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk
import pandas as pd

es = Elasticsearch(['atlas-kibana.mwt2.org:9200'], timeout=60)

my_query = {
    "_source": ["filename"],
    "query": {"match_all": {}}
}

scroll = scan(client=es, index="stress", query=my_query)
count = 0
requests = {}
for res in scroll:
    r = res['_source']
    # print(r)
    fn = r['filename']
    if not fn in requests:
        requests[fn] = []
    requests[fn].append(res['_id'])
    count += 1

print('records loaded:', count, 'unique files', len(requests))

todelete = []

for fn, ids in requests.items():
    # print(fn, ids)
    if len(ids) == 1:
        continue
    # print(ids)
    for did in ids[1:]:
        print(did)
        todelete.append(
            {
                '_op_type': 'delete',
                '_index': 'stress',
                '_type': 'docs',
                '_id': did
            }
        )

print('deleting ...', len(todelete))
bulk(es, todelete)

print('Done.')
