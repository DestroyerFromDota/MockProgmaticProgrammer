# Ansible Playbook: Install Docker and Python 3.12 on Debian

## Описание

Данный Ansible playbook предназначен для автоматической установки Docker и Python 3.12 на серверах с операционной системой Debian. Playbook выполняет полный цикл установки и настройки необходимого программного обеспечения.

## Что устанавливается

- **Python 3.12** с поддержкой виртуальных окружений (venv)
- **pip** для управления Python-пакетами
- **Docker CE** (Community Edition) с необходимыми компонентами:
  - docker-ce (основной пакет)
  - docker-ce-cli (интерфейс командной строки)
  - containerd.io (контейнерный runtime)
- **Системные зависимости** для корректной работы Docker

## Требования

- **Целевые хосты**: Debian (проверено на Debian 11 Bullseye и Debian 12 Bookworm)
- **Права доступа**: root или пользователь с sudo-привилегиями
- **Ansible**: установленный на управляющей машине

## Использование

### 1. Подготовка inventory файла

Создайте файл `inventory.ini` со списком хостов:

```ini
[servers]
server1 ansible_host=192.168.1.10 ansible_user=debian
server2 ansible_host=192.168.1.11 ansible_user=debian

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

## Запуск
`ansible-playbook -i inventory.ini install-docker-python.yml`

## Playbook использует следующие переменные Ansible:
```
{ ansible_distribution_release }} - автоматически определяет версию Debian (bullseye, bookworm и т.д.)

{{ ansible_user }} - имя пользователя, под которым выполняется подключение
```