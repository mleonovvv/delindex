import requests
import re
import datetime

url = 'http://127.0.0.1:9200/_all'
try:
    r = requests.get(url)
except ConnectionRefusedError:
    print("connection error")

indexList = [] # logstash-2019.02.21
expiryDateList = []
days = 18
maxDate = datetime.date.today() - datetime.timedelta(days=days)

for i in r.json().keys():
    if re.search("logstash", i):
        indexList.append(i)

if len(indexList) >= days:

  for l in indexList:
      dateREGroup = re.search('([0-9]{4})\.([0-9]{2})\.([0-9]{2})', l)
      d = datetime.date(int(dateREGroup.group(1)), int(dateREGroup.group(2)), int(dateREGroup.group(3)))
      if d <= maxDate:
          expiryDateList.append(d)

  for i in expiryDateList:
      s = str(i)
      dateString = s.replace('-', '.')
      print("logstash-" + dateString)
else:
    print("indexes count =< " + str(days))
