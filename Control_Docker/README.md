# Docker Manager
Пока прототип
Контейнер для управления другими Docker контейнерами через Python SDK.

## Команды
Собрать образ
`docker build -t docker-manager .`

Запустить контейнер с образа
`docker run -v /var/run/docker.sock:/var/run/docker.sock docker-manager`

## Как это работает
Монтируется Docker сокет хоста (/var/run/docker.sock) внутрь контейнера

Python скрипт внутри контейнера получает доступ к Docker API хоста

Скрипт может управлять контейнерами на хосте