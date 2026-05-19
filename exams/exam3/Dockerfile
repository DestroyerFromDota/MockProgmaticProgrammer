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

# Переменные для пользователя (можно переопределить при запуске)
ENV USERNAME=student
ENV PASSWORD=exam2026

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Создаем структуру директорий
RUN mkdir -p /opt/template /opt

# Копируем файлы в шаблонную директорию
COPY talk.sh /tmp/talk.sh
COPY README.md /tmp/README.md
COPY hints.txt /tmp/hints.txt

# Конвертируем окончания строк и раскладываем по местам
RUN dos2unix /tmp/talk.sh && \
    dos2unix /tmp/README.md && \
    dos2unix /tmp/hints.txt && \
    mv /tmp/talk.sh /opt/template/ && \
    mv /tmp/README.md /opt/template/ && \
    mv /tmp/hints.txt /opt/ && \
    chmod +x /opt/template/talk.sh

# Проверяем установку
RUN echo "=== Проверка установки ===" && \
    ls -la /usr/bin/cowsay && \
    fortune || echo "fortune не установлен, но это не страшно"

# Скрипт запуска: создаём пользователя из ENV и раскладываем файлы
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'USERNAME=${USERNAME:-student}' >> /start.sh && \
    echo 'PASSWORD=${PASSWORD:-exam2026}' >> /start.sh && \
    echo '' >> /start.sh && \
    echo 'adduser -D "$USERNAME"' >> /start.sh && \
    echo 'echo "$USERNAME:$PASSWORD" | chpasswd' >> /start.sh && \
    echo 'echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' >> /start.sh && \
    echo '' >> /start.sh && \
    echo 'mkdir -p /home/$USERNAME' >> /start.sh && \
    echo 'cp /opt/template/talk.sh /home/$USERNAME/' >> /start.sh && \
    echo 'cp /opt/template/README.md /home/$USERNAME/' >> /start.sh && \
    echo 'chmod +x /home/$USERNAME/talk.sh' >> /start.sh && \
    echo 'chown -R $USERNAME:$USERNAME /home/$USERNAME' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 22

CMD ["/start.sh"]