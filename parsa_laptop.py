import json
from multiprocessing.pool import ThreadPool
import requests
import re


url = 'https://search.digikala.com/api/SearchApi?urlCode=Notebook-Netbook-Ultrabook&status=2&pageSize=300&pageno=0&price[max]=4024184&price[min]=2824184'
res = requests.get(url)
res_arr = res.json().get('hits').get('hits')
re_pattern = re.compile('(geforce).*?(\d+).*', flags=re.IGNORECASE)
gb_re_pattern = re.compile('.*(\d ?GB).*')

result = {}
fails = []


def async_get(detail_url, price):
    try:
        page = requests.get(detail_url).content
        search_res = re_pattern.search(page)
        if not search_res:
            return None

        gb_res = gb_re_pattern.search(page)

        match_line = search_res.group(2) + ' ' + gb_res.group(1)
        print '{}: {} {} {}'.format(detail_url, search_res.group(1), search_res.group(2), gb_res.group(1))

        if match_line not in result:
            result[match_line] = []

        result[match_line].append('{} - {}'.format(price, detail_url))

    except:
        fails.append(detail_url)

thread_pool = ThreadPool(50)
for laptop in res_arr:
    laptop_doc = laptop.get('_source', {})
    try:
        detail_url = 'https://www.digikala.com/Product/DKP-' + str(laptop_doc.get('Id'))
        price = int(float(laptop_doc.get('MinPrice')) / 10)
        thread_pool.apply_async(async_get, args=(detail_url, str(price)))

    except Exception as exc:
        print "failed ({}) for: {}".format(exc, laptop_doc)

thread_pool.close()
thread_pool.join()

print json.dumps(fails, indent=4)
print

for k in sorted(result.keys()):
    v = result.get(k)
    print '\n{}:'.format(k)
    for i in sorted(v):
        print i

# print json.dumps(result, indent=4, sort_keys=True)
