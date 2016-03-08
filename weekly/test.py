#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request as r
import datetime
# import zlib
# from bs4 import BeautifulSoup
import json
import dateutil.parser as dp

example = """
{'_number': 257239,
 '_sortkey': '0039cc6e0003ecd7',
 'branch': 'master',
 'change_id': 'I934c43a2507733a7f460e667ae070d550f0d18c5',
 'created': '2015-12-14 09:32:49.000000000',
 'id': 'openstack%2Fsenlin~master~I934c43a2507733a7f460e667ae070d550f0d18c5',
 'kind': 'gerritcodereview#change',
 'labels': {'Code-Review': {'approved': {'name': 'Qiming Teng'}},
            'Verified': {'approved': {'name': 'Jenkins'}},
            'Workflow': {'approved': {'name': 'Yanyan Hu'}}},
 'owner': {'name': 'Ethan Lynn'},
 'project': 'openstack/senlin',
 'status': 'MERGED',
 'subject': 'Refactor YamlLoader',
 'topic': 'parser_refactor',
 'updated': '2015-12-14 11:26:56.000000000'}
"""


def format_output(patch):
    link = 'https://review.openstack.org/'+str(patch['_number'])
    created = dp.parse(patch['created']).date().isoformat()
    updated = dp.parse(patch['updated']).date().isoformat()
    title = patch['subject']
    project = patch['project'].split('/')[1]
    return ('%(l)s [%(p)s][Created %(c)s][Updated %(u)s]%(t)s' % {
        'l': link,
        'c': created,
        'u': updated,
        't': title,
        'p': project
    })

name_list = [
    'xjunlin@cn.ibm.com',
    'dixiaobj@cn.ibm.com',
    'wkqwu@cn.ibm.com',
    'bjwqun@cn.ibm.com',
    'whaom@cn.ibm.com',
    'kansks@cn.ibm.com',
    'xiaohhui@cn.ibm.com',
    'lzklibj@cn.ibm.com',
]
result = {}

for name in name_list:
    result[name] = {}
    context = r.urlopen('https://review.openstack.org/changes'
                        '/?q=owner:%s&n=25&O=1' % name).read().decode('utf-8')
    content_dict = json.loads(context[4:])

    for dd in content_dict:
        update_date = dp.parse(dd['updated'])
        if datetime.datetime.utcnow() - update_date > datetime.timedelta(days=9):
            continue
        if not result[name].get(dd['status']):
            result[name][dd['status']] = []
        result[name][dd['status']].append(dd)


for name in result:
    print('\n### '+name+' ###')
    for status in result[name]:
        print('\n'+status)
        for patch in result[name][status]:
            print(format_output(patch))




