# Cassandra

## Развернуть Cassandra в кластере

Для развертывания кластера использовался docker-compose.yaml на 3 узла.
Однако из-за того, что Cassandra очень требовательна к оперативной памяти оставил только 2.
Параметры настройки и файл запуска представлен в папке с домашним заданием:

```bash
docker compose up -d
```

![img.png](cassandra_docker.png)

# Создание базы данных

```shell
CREATE KEYSPACE IF NOT EXISTS store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };
```

Далее создадим две таблицы:
```shell
CREATE TABLE IF NOT EXISTS store.shopping_cart (
        userid uuid PRIMARY KEY,
        item_count int,
        last_update_timestamp timestamp
);
CREATE TABLE IF NOT EXISTS store.users (
        userid uuid PRIMARY KEY,
        first_name text,
        last_name text
        city text
        PRIMARY KEY (userid, first_name)
) WITH CLUSTERING ORDER BY userid;
```

# Далее был создан вторичный индекс

```shell
CREATE INDEX itemcountidx ON shopping_cart (item_count);
```

# Выполнение запросов

Простой запрос на отбор пользователя по имени: 
```shell
select * users where first_name = 'Олег';
```

```shell
select * shopping_cart where item_count > 0;
```
### Итоги

`Cassandra` - отличный инструмент для 
работы с большим количеством данных. 
Единственный недостаток, который был выявлен - это достаточно большое 
потребление оперативной памяти.