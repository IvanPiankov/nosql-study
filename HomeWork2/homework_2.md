# MongoDB

## 1. Установка Mongo

MongoDB поднималось в `docker` с использованием `docker-compose.yaml` файла.
Конфигурация из файла

```yaml
version: '3'
services:
  
  mongo:
    image: mongo
    container_name: mongo
    restart: always
    ports: 
      - '27017:27017'
    volumes:
      - local_mongo:/var/lib/mongo/data
      
volumes:
  local_mongo:
```

## 2. Наполнение данными

С использованием `mongoimport` был произведён импорт данных в БД, команда приведена ниже.
В качестве дата сета использовался дата сет объявлений AirBnb

```shell
mongoimport --host localhost --port 27017 --collection listingsAndReviews --file listingsAndReviews.json
```
После команды необходимо проверить, что появилась новая база данных.

```sh
show collections
```

Ответ:

```json
[
  {
    "badge": "",
    "name": "listingsAndReviews"
  }
]
```


## 3. Выполнение запросов

Выполним стандартные операции для CRUD
1. Получение определённых полей из документа:

```js
db.listingsAndReviews.findOne(
    {_id: "10009999"},
    { name: 1, cleaning_fee: 1 }
)
```

Ответ:

```json
[
  {
    "_id": "10009999",
    "cleaning_fee": 187.00,
    "name": "Horto flat with small garden"
  }
]
```

2. Изменение данных в документе

Для изменения данных воспользуемся командой и зададим новое имя

```js
db.listingsAndReviews.updateOne(
   {_id: "10009999"},
   { $set: { name: "New name" }},
)
```

После этого получим результат по данному `_id`:

```json
[
  {
    "_id": "10009999",
    "cleaning_fee": 187.00,
    "name": "New name"
  }
]
```

3. Удаление документа

Для удаления документа воспользуемся следующей командой

```js
db.listingsAndReviews.deleteOne(
   {_id: "10009999"}
)
```

После удаления, документ по заданному `_id` не находит при выполнении команды `findOne`

4. Создание нового документа

Для создания нового документа воспользуемся командой

```js
db.listingsAndReviews.insertOne(
    {name: "New document insertion", cleaning_fee: 187.00}
)
```

Далее выполним команду `findOne` c именем, заданным для документа

```js
db.listingsAndReviews.findOne(
    {name: "New document insertion"},
    { name: 1, cleaning_fee: 1 }
)
```

И получим ответ

```json
[
  {
    "_id": "66b8fe095e369919c582468a",
    "cleaning_fee": 187,
    "name": "New document insertion"
  }
]
```


## Итоги
`MongoDB` - достаточно проста в развертывании, так же имеет удобный cli tool, которые позволят проводить различные импорты данных.
Имеет достаточно простой и удобный синтаксис запросов, за счёт того, что хранит все данные в документах и нет четкой 
привязки к схеме отлично подходит для манипуляции с `json` объектами.