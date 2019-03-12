FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY curl_for_es.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./curl_for_es.py" ]

