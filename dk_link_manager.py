import traceback
import urlparse
import json
import sys
import requests
import shutil
import datetime

url = sys.argv[2]
name = sys.argv[1]

if 'digikala.com/Search/Category' in url:
    before_qry_str, after_qry_str = url.split('?')
    url_to_get = 'https://www.digikala.com/api/Search/{}'.format(before_qry_str.split("/")[-1])
    req_res = requests.get(url_to_get)
    res_json = req_res.json()
    after_qry_str = after_qry_str.replace("%5BA", "%5B")
    url = 'https://search.digikala.com/api/SearchApi?urlCode={}&{}'.format(res_json.get('categoryFilter').get('UrlCode'), after_qry_str)

result_dict = {}
attrib_dict = {}
query_dict = dict(urlparse.parse_qs(urlparse.urlsplit(url).query))
# print json.dumps(query_dict, indent=4)
for k in sorted(query_dict.keys()):
    v = query_dict[k]
    type_value = v[0]
    if k == 'urlCode':
        result_dict['urlCode'] = type_value

    elif k.startswith("type") or k.startswith("brand"):
        key, _ = k.split('[')
        key += 's'
        if key not in result_dict:
            result_dict[key] = []

        result_dict[key].append(type_value)

    elif k.startswith('price'):
        key, min_or_max = k.split('[')
        min_or_max = min_or_max.replace("]", "")
        if 'price' not in result_dict:
            result_dict['price'] = {}

        result_dict['price'][min_or_max] = type_value

    elif k.startswith('attribute'):
        first_ind, second_ind = k.lstrip('attribute[').rstrip(']').split('][')
        if first_ind not in attrib_dict:
            attrib_dict[first_ind] = []

        attrib_dict[first_ind].append(type_value)

    else:
        continue

if attrib_dict:
    result_dict['attributes'] = attrib_dict

print json.dumps(result_dict, indent=4)

conf_path = '/etc/bordeaux/bordeaux.conf'
inp = raw_input('Add to conf ({})? (y/N): '.format(conf_path))

if inp.lower() in ['y', "yes"]:
    with open(conf_path) as fp:
        current_conf = json.load(fp)

    print json.dumps(current_conf, indent=4, sort_keys=True)
    dk_confs = current_conf.get('searchers', {}).get('digikala', {})
    if name in dk_confs.get('phrases') or name in dk_confs.get('phrase_details'):
        print 'The name `{}` is already in search phrases.'.format(name)
        exit(1)

    if not dk_confs.get('phrases'):
        dk_confs['phrases'] = []

    dk_confs['phrases'].append(name)

    if not dk_confs.get('phrase_details'):
        dk_confs['phrase_details'] = {}

    dk_confs['phrase_details'][name] = result_dict

    now = datetime.datetime.now()
    try:
        shutil.copy(conf_path, conf_path+'.{}'.format(now.strftime("%Y-%m-%d-%H-%M")))

        with open(conf_path, 'w') as fp:
            json.dump(current_conf, fp, indent=4, sort_keys=True, separators=(',', ': '))

    except IOError:
        print 'Failed to move or write, do you have sufficient permissions? {}'.format(traceback.format_exc())
