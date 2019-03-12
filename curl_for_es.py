import requests
import re
import datetime
import json
import os
import sys


indexList = []
expiryDateList = []
delIndex = []
DAYS_KEEP_ES_DATA = int(os.getenv('DAYS_KEEP_ES_DATA', 14))
ES_PORT = int(os.getenv('ES_PORT', 9200))
ES_HOST = os.getenv('ES_HOST', 'localhost')
BASE_URL = '{}:{}'.format(ES_HOST, ES_PORT)
SCHEME = 'http'
maxDate = datetime.date.today() - datetime.timedelta(days=DAYS_KEEP_ES_DATA)


def main():
    try:
        url = '{}://{}/_all'.format(SCHEME, BASE_URL)
        r = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        print("Error: {}".format(err))
        sys.exit(1)

    for i in r.json().keys():
        if 'logstash' in i:
            indexList.append(i)

    if len(indexList) > DAYS_KEEP_ES_DATA:

        for l in indexList:
            dateREGroup = re.search(r'([0-9]{4})\.([0-9]{2})\.([0-9]{2})', l)
            d = datetime.date(
                int(dateREGroup.group(1)),
                int(dateREGroup.group(2)),
                int(dateREGroup.group(3)))
            if d <= maxDate:
                expiryDateList.append(d)

        for i in expiryDateList:
            s = str(i)
            dateString = s.replace('-', '.')
            delIndex.append(dateString)
            try:
                url = '{}://{}/logstash-{}'.format(
                        SCHEME,
                        BASE_URL,
                        dateString)
                r = requests.get(url)
            except requests.exceptions.ConnectionError as err:
                print("Error: {}".format(err))
                sys.exit(1)

        d = {'Found': indexList, 'Deleted': delIndex}
        print(json.dumps(d, sort_keys=True, indent=2))

    else:
        print("indexes count < " + str(days))


if __name__ == '__main__':
    main()
