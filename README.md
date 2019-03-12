# delindex
Скрипт удаления индексов для elasticsearch.
Читает переменыне окруджения:
- ES_KEEP_DAYS  - кол-во дней хранения индексов (по умолчанию: 14)
- ES_PORT (по умолчанию: 9200)
- ES_HOST (по умолчанию: localhost)
- ES_SCHEME (по умолчанию: http)

Предпологается использовать в kubernetes cronjob
