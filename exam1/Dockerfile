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

# Создаем пользователя student
RUN adduser -D student && \
    echo "student:exam2026" | chpasswd && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Создаем нужные директории
RUN mkdir -p /var/www/html /home/student /opt /run/nginx /var/log/nginx /var/lib/nginx

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

# Создаем README
RUN echo '# Экзамен: Работа с файлами и редакторами' > /home/student/README.md && \
    echo '' >> /home/student/README.md && \
    echo '## Ситуация' >> /home/student/README.md && \
    echo 'На сервере установлен Nginx, но он не запускается.' >> /home/student/README.md && \
    echo 'Ваша задача - найти и исправить ошибку.' >> /home/student/README.md && \
    echo '' >> /home/student/README.md && \
    echo '## Что нужно сделать' >> /home/student/README.md && \
    echo '1. Подключись к серверу: `ssh student@localhost -p 2222` (пароль: exam2026)' >> /home/student/README.md && \
    echo '2. Осмотрись в системе' >> /home/student/README.md && \
    echo '3. Найди причину, почему Nginx не работает' >> /home/student/README.md && \
    echo '4. Исправь ошибку с помощью редактора (`nano` или `vim`)' >> /home/student/README.md && \
    echo '5. Запусти Nginx и проверь результат' >> /home/student/README.md && \
    echo '' >> /home/student/README.md && \
    echo '## Подсказки' >> /home/student/README.md && \
    echo '- Проверь статус: `ps aux | grep nginx`' >> /home/student/README.md && \
    echo '- Проверь конфиг: `sudo nginx -t`' >> /home/student/README.md && \
    echo '- Посмотри подсказку: `cat /opt/hints.txt`' >> /home/student/README.md && \
    echo '- Когда исправишь, запусти: `sudo nginx`' >> /home/student/README.md && \
    echo '- Проверь работу: `curl http://localhost`' >> /home/student/README.md

# Создаем скрипт запуска
RUN echo '#!/bin/sh' > /start.sh && \
    echo '/usr/sbin/sshd' >> /start.sh && \
    echo '# Nginx НЕ запускаем автоматически - пусть студент сам запустит' >> /start.sh && \
    echo 'tail -f /dev/null' >> /start.sh && \
    chmod +x /start.sh

# Права
RUN chown -R student:student /home/student && \
    chown -R nginx:nginx /var/lib/nginx /var/log/nginx

EXPOSE 22 80

CMD ["/start.sh"]