FROM alpine:latest

# Создаем директории
RUN mkdir -p \
    /app/game \
    /app/data \
    /app/logs \
    /app/config \
    /app/temp \
    /app/uploads \
    /app/scripts \
    /app/static

# Копируем файлы
COPY game.py /app/game/
COPY questions.py /app/game/
COPY config.py /app/logs/

# Устанавливаем права доступа
RUN chmod -R 777 /app


# Установка ssh демона и sudo
RUN apk add --no-cache bash openssh-server sudo \
    && ssh-keygen -A

# Переменные для пользователя (можно переопределить при запуске)
ENV USERNAME=student
ENV PASSWORD=exam2026

# Установка утилит (исправлено: awk заменен на gawk)
RUN apk update && apk add --no-cache \
    curl \
    wget \
    vim \
    nano \
    htop \
    git \
    tree \
    unzip \
    zip \
    tar \
    gzip \
    xz \
    busybox-extras \
    procps \
    util-linux \
    less \
    grep \
    sed \
    gawk \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Скрипт запуска: создаём пользователя из ENV и стартуем sshd
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'USERNAME=${USERNAME:-student}' >> /start.sh && \
    echo 'PASSWORD=${PASSWORD:-exam2026}' >> /start.sh && \
    echo '' >> /start.sh && \
    echo 'adduser -D "$USERNAME"' >> /start.sh && \
    echo 'echo "$USERNAME:$PASSWORD" | chpasswd' >> /start.sh && \
    echo 'echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

# Запуск
CMD ["/start.sh"]