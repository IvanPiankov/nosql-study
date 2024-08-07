# Tarantool

## Установить Tarantool Cartridge CLI

Cartridge CLI - устаревший инструмент на его замену пришёл tt. 
Развертывание `Tarantool` провожу с использованием docker

Настройку кластера провожу с использованием документации с оф. сайте `Tarantool`. 

Создам один роутер, 3 реплика сет и 6 стореджей.

В реплика сетах два стореджа связанных как Мастер -> Реплика

Таким образом конфигурация получается следующая: 

```yaml
storage-a-001:
storage-a-002:
storage-b-001:
storage-b-002:
storage-c-001:
storage-c-002:
router-a-001:
```

После конфигурации файлов и запуска `Tarantool`. 
Была получена информация кластере:
```shell
replicasets:
    storage-a:
      replica:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3303
        name: storage-a-002
      bucket:
        available_rw: 333
      master:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3302
        name: storage-a-001
      name: storage-a
    storage-c:
      replica:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3307
        name: storage-c-002
      bucket:
        available_rw: 333
      master:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3306
        name: storage-c-001
      name: storage-c
    storage-b:
      replica:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3305
        name: storage-b-002
      bucket:
        available_rw: 334
      master:
        network_timeout: 0.5
        status: available
        uri: storage@127.0.0.1:3304
        name: storage-b-001
      name: storage-b
  bucket:
    unreachable: 0
    available_ro: 0
    unknown: 0
    available_rw: 1000
  identification_mode: name_as_key
  status: 0
  alerts: []
```

После этого был создана схема и индексы. 
Далее вставил данные в схему: 
```shell
crud.insert_many('computers', {{ 1, box.NULL, 'ThinkPad', 'laptop', 2005 },
{ 2, box.NULL, 'MacBook', 'desktop', 2006 },
{ 3, box.NULL, 'Comp', 'desktop', 2007 },
{ 4, box.NULL, 'Comp2', 'desktop', 2008 },
{ 5, box.NULL, 'Comp3', 'desktop', 2009 },
{ 6, box.NULL, 'MacBook2', 'laptop', 2010 },
{ 7, box.NULL, 'MacBook3', 'laptop', 2011 },
{ 8, box.NULL, 'MacBook4', 'laptop', 2012 },
{ 9, box.NULL, 'MacBook5', 'laptop', 2013 },
{ 10, box.NULL, 'MacBook6', 'laptop', 2014 }})
```

После чего проверил распределение данных по реплика сетам.

В репликасет `a` попали следующие данные
```shell
shared_db:storage-a-001> box.space.computers:select()
---
- - [1, 477, 'ThinkPad', 'laptop', 2005]
  - [2, 401, 'MacBook', 'desktop', 2006]
  - [9, 644, 'MacBook5', 'laptop', 2013]
  - [10, 569, 'MacBook6', 'laptop', 2014]
...

```

В репликасет `b`:
```shell
shared_db:storage-b-001> box.space.computers:select()
---
- - [3, 804, 'Comp', 'desktop', 2007]
  - [7, 693, 'MacBook3', 'laptop', 2011]
...
```

И репликасет `c`:

```shell
shared_db:storage-c-001> box.space.computers:select()
---
- - [4, 161, 'Comp2', 'desktop', 2008]
  - [5, 172, 'Comp3', 'desktop', 2009]
  - [6, 64, 'MacBook2', 'laptop', 2010]
  - [8, 185, 'MacBook4', 'laptop', 2012]
...
```

После этого провёл экскременты по остановки одного из стореджей в репликасете.
При работе всего одного Мастера в реплика сете данные доступны.
Однако, если остановить Мастер возникают ошибки подключения к данному реплика сету.

### Итоги

`Tarantool` - достаточно странная БД, честно говоря работать в ней не очень удобно в бесплатной версии + к этому не всегда понятно её назначение.
Но после написания `lua` скриптов, стало понятно, что `Tarantool` упростить какие-то простые запросы в БД и заменить сервис бэкенда. 
Однако, пока это единственный плюс который мне удалось найти, как разработчику, по мимо скорости получения данных.
