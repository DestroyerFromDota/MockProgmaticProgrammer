FROM alpine:latest

# Устанавливаем пакеты (добавляем testing репозиторий)
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
    openssh-server \
    bash \
    curl \
    sudo \
    nano \
    vim \
    dos2unix \
    cowsay

# Пробуем установить fortune (в разных версиях называется по-разному)
RUN apk add --no-cache fortune-mod --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community/ || \
    apk add --no-cache fortune || true

# Если fortune не установился, создаем заглушку
RUN if ! command -v fortune > /dev/null; then \
        echo '#!/bin/sh' > /usr/bin/fortune && \
        echo 'echo "Привет от говорящей коровы!"' >> /usr/bin/fortune && \
        chmod +x /usr/bin/fortune; \
    fi

# Создаем пользователя student
RUN adduser -D student && \
    echo "student:exam2026" | chpasswd && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Создаем структуру директорий
RUN mkdir -p /home/student /opt

# Копируем файлы
COPY talk.sh /tmp/talk.sh
COPY README.md /tmp/README.md
COPY hints.txt /tmp/hints.txt

# Конвертируем окончания строк
RUN dos2unix /tmp/talk.sh && \
    dos2unix /tmp/README.md && \
    dos2unix /tmp/hints.txt && \
    mv /tmp/talk.sh /home/student/ && \
    mv /tmp/README.md /home/student/ && \
    mv /tmp/hints.txt /opt/

# Делаем скрипт исполняемым
RUN chmod +x /home/student/talk.sh && \
    chown -R student:student /home/student

# Проверяем установку
RUN echo "=== Проверка установки ===" && \
    ls -la /usr/bin/cowsay && \
    fortune || echo "fortune не установлен, но это не страшно"

# Скрипт запуска
RUN echo '#!/bin/sh' > /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 22

CMD ["/start.sh"]