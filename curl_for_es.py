import requests
import re
import datetime
import json
import os


url = 'http://127.0.0.1:9200/_all'
try:
    r = requests.get(url)
except ConnectionRefusedError:
    print("connection error")

indexList = [] # logstash-2019.02.21
expiryDateList = []
delIndex = []
days = os.getenv('DAYS_KEEP_ES_DATA', 14)
maxDate = datetime.date.today() - datetime.timedelta(days=int(days))

for i in r.json().keys():
    if re.search("logstash", i):
        indexList.append(i)

if len(indexList) > int(days):

  for l in indexList:
      dateREGroup = re.search('([0-9]{4})\.([0-9]{2})\.([0-9]{2})', l)
      d = datetime.date(int(dateREGroup.group(1)), int(dateREGroup.group(2)), int(dateREGroup.group(3)))
      if d <= maxDate:
          expiryDateList.append(d)

  for i in expiryDateList:
      s = str(i)
      dateString = s.replace('-', '.')
      delIndex.append(dateString)
      #print("logstash-" + dateString)
      url = 'http://127.0.0.1:9200/' + 'logstash-' + dateString
      r = requests.get(url)
      #print(r.json())

  d = {'Found': indexList, 'Deleted': delIndex}
  print(json.dumps(d, sort_keys=True, indent=2))

else:
    print("indexes count < " + str(days))
