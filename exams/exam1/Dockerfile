FROM alpine:latest

# Устанавливаем пакеты
RUN apk add --no-cache \
    openssh-server \
    nginx \
    nano \
    vim \
    curl \
    sudo \
    bash

# Переменные для пользователя (можно переопределить при запуске)
ENV USERNAME=student
ENV PASSWORD=exam2026

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Создаем нужные директории
RUN mkdir -p /var/www/html /home /opt /run/nginx /var/log/nginx /var/lib/nginx

# Создаем конфиг nginx с ошибкой (лишняя ; на 12 строке)
RUN echo 'user nginx;' > /etc/nginx/nginx.conf && \
    echo 'worker_processes auto;' >> /etc/nginx/nginx.conf && \
    echo 'pid /run/nginx.pid;' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo 'events {' >> /etc/nginx/nginx.conf && \
    echo '    worker_connections 768;' >> /etc/nginx/nginx.conf && \
    echo '    # !!! ЗДЕСЬ ОШИБКА !!! Убери лишнюю точку с запятой' >> /etc/nginx/nginx.conf && \
    echo '    use epoll;;' >> /etc/nginx/nginx.conf && \
    echo '}' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo 'http {' >> /etc/nginx/nginx.conf && \
    echo '    sendfile on;' >> /etc/nginx/nginx.conf && \
    echo '    tcp_nopush on;' >> /etc/nginx/nginx.conf && \
    echo '    include /etc/nginx/mime.types;' >> /etc/nginx/nginx.conf && \
    echo '    default_type application/octet-stream;' >> /etc/nginx/nginx.conf && \
    echo '    access_log /var/log/nginx/access.log;' >> /etc/nginx/nginx.conf && \
    echo '    error_log /var/log/nginx/error.log;' >> /etc/nginx/nginx.conf && \
    echo '    keepalive_timeout 65;' >> /etc/nginx/nginx.conf && \
    echo '' >> /etc/nginx/nginx.conf && \
    echo '    server {' >> /etc/nginx/nginx.conf && \
    echo '        listen 80;' >> /etc/nginx/nginx.conf && \
    echo '        server_name localhost;' >> /etc/nginx/nginx.conf && \
    echo '        root /var/www/html;' >> /etc/nginx/nginx.conf && \
    echo '        index index.html;' >> /etc/nginx/nginx.conf && \
    echo '    }' >> /etc/nginx/nginx.conf && \
    echo '}' >> /etc/nginx/nginx.conf

# Создаем index.html
RUN echo '<h1>Экзамен по Linux сдан!</h1>' > /var/www/html/index.html

# Создаем подсказку
RUN echo "=== ПОДСКАЗКА ===" > /opt/hints.txt && \
    echo "Ошибка в файле /etc/nginx/nginx.conf на строке 12" >> /opt/hints.txt && \
    echo "Там лишняя точка с запятой. Убери её!" >> /opt/hints.txt

# Создаем README (будет скопирован позже в домашнюю директорию пользователя)
RUN echo '# Экзамен: Работа с файлами и редакторами' > /opt/README.md && \
    echo '' >> /opt/README.md && \
    echo '## Ситуация' >> /opt/README.md && \
    echo 'На сервере установлен Nginx, но он не запускается.' >> /opt/README.md && \
    echo 'Ваша задача - найти и исправить ошибку.' >> /opt/README.md && \
    echo '' >> /opt/README.md && \
    echo '## Что нужно сделать' >> /opt/README.md && \
    echo '1. Подключись к серверу: `ssh student@localhost -p 2222` (пароль: exam2026)' >> /opt/README.md && \
    echo '2. Осмотрись в системе' >> /opt/README.md && \
    echo '3. Найди причину, почему Nginx не работает' >> /opt/README.md && \
    echo '4. Исправь ошибку с помощью редактора (`nano` или `vim`)' >> /opt/README.md && \
    echo '5. Запусти Nginx и проверь результат' >> /opt/README.md && \
    echo '' >> /opt/README.md && \
    echo '## Подсказки' >> /opt/README.md && \
    echo '- Проверь статус: `ps aux | grep nginx`' >> /opt/README.md && \
    echo '- Проверь конфиг: `sudo nginx -t`' >> /opt/README.md && \
    echo '- Посмотри подсказку: `cat /opt/hints.txt`' >> /opt/README.md && \
    echo '- Когда исправишь, запусти: `sudo nginx`' >> /opt/README.md && \
    echo '- Проверь работу: `curl http://localhost`' >> /opt/README.md

# Создаем скрипт запуска
RUN echo '#!/bin/sh' > /start.sh && \
    echo '# Создаем пользователя из переменных окружения' >> /start.sh && \
    echo 'adduser -D "$USERNAME"' >> /start.sh && \
    echo 'echo "$USERNAME:$PASSWORD" | chpasswd' >> /start.sh && \
    echo 'echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Копируем README в домашнюю директорию пользователя' >> /start.sh && \
    echo 'mkdir -p /home/$USERNAME' >> /start.sh && \
    echo 'cp /opt/README.md /home/$USERNAME/README.md' >> /start.sh && \
    echo 'chown -R $USERNAME:$USERNAME /home/$USERNAME' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Настраиваем права для nginx' >> /start.sh && \
    echo 'chown -R nginx:nginx /var/lib/nginx /var/log/nginx' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Запускаем SSH' >> /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Держим контейнер активным' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 22 80

CMD ["/start.sh"]