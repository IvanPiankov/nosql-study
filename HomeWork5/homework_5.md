# ClickHouse

## Развернуть ClickHouse в контейнере

Для развертывания кластера использовался docker-compose.yaml.
Параметры настройки прописаны ниже:

```yaml
  clickhouse:
    image: clickhouse/clickhouse-server
    container_name: clickhouse
    hostname: clickhouse
    restart: always
    ports:
      - '8123:8123'
      - '9000:9000'
```

# Загрузка данных и тестовой базы данных

В качестве тестового dataset-а выбрал 
тестовые данные по ценам недвижимости в Великобритании
[ссылка на данные](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid)

# Замеры скорости записи и чтения

Были выполнены команды чтения и изменения данных:

```sql
SELECT count()
FROM uk_price_paid
WHERE postcode2 is null;
```
```sql
ALTER TABLE uk_price_paid
    UPDATE postcode2 = 'speed_test' WHERE postcode2 is null
```

Конечно получение элементов в значительно степени 
превосходит по скорости обновление данных 

### Итоги

`ClickHouse` - отличный инструмент для 
работы с аналитическим данными помимо 
этого `ClickHouse` отлично взаимодействует с брокерами такими как `Kafka`.
Очень гибкий и настраиваемый инструмент, конечно есть не очень удобные вещи, 
связанные с форматом данных, но если понять как это все работает то данным инструментом 
будет очень удобно и приятно пользоваться