import requests
import re
from datetime import datetime, timedelta
import json
import os
import sys


indexList = []
expiryDateList = []
delIndex = []
DAYS_KEEP_ES_DATA = int(os.getenv('ES_KEEP_DAYS', 14))
ES_PORT = int(os.getenv('ES_PORT', 9200))
ES_HOST = os.getenv('ES_HOST', 'localhost')
SCHEME = os.getenv('ES_SCHEME', 'http')
BASE_URL = '{}://{}:{}'.format(SCHEME, ES_HOST, ES_PORT)
maxDate = datetime.today() - timedelta(days=DAYS_KEEP_ES_DATA)


def curl(url, method):
    try:
        if method == 'get':
            r = requests.get(url)
        elif method == 'delete':
            r = requests.delete(url)
        else:
            print('Unknow method : {}'.format(method))
    except requests.exceptions.ConnectionError as err:
        print('Error: {} {}'.format(url, err))
    return r


def main():
    url = '{}/_all'.format(BASE_URL)
    r = curl(url, 'get')

    for i in r.json().keys():
        if 'logstash' in i:
            indexList.append(i)

    if len(indexList) > DAYS_KEEP_ES_DATA:

        for l in indexList:
            d = datetime.strptime(l, "logstash-%Y.%m.%d")
            if d <= maxDate:
                expiryDateList.append(d)

        for d in expiryDateList:
            dateString = datetime.strftime(d, "%Y.%m.%d")
            delIndex.append(dateString)
            url = '{}/logstash-{}'.format(BASE_URL, dateString)
            curl(url, 'get')

        d = {'Found': indexList, 'Deleted': delIndex}
        print(json.dumps(d, sort_keys=True))

    else:
        print('indexes count < ' + str(days))


if __name__ == '__main__':
    main()
