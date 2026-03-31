FROM alpine:latest

# Устанавливаем пакеты (включая dos2unix для конвертации строк)
RUN apk add --no-cache \
    openssh-server \
    python3 \
    py3-pip \
    py3-virtualenv \
    nano \
    vim \
    curl \
    sudo \
    bash \
    supervisor \
    dos2unix

# Переменные для пользователя (можно переопределить при запуске)
ENV USERNAME=student
ENV PASSWORD=exam2026

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir pyyaml

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Создаем структуру директорий
RUN mkdir -p /home /opt/myapp /var/log/myapp /opt

# Копируем файлы во временную директорию
COPY app.py /tmp/app.py
COPY config.yaml /tmp/config.yaml
COPY config.yaml.correct /tmp/config.yaml.correct
COPY README.md /tmp/README.md
COPY hints.txt /tmp/hints.txt

# Конвертируем окончания строк из Windows (CRLF) в Linux (LF)
RUN dos2unix /tmp/app.py && \
    dos2unix /tmp/config.yaml && \
    dos2unix /tmp/config.yaml.correct && \
    dos2unix /tmp/README.md && \
    dos2unix /tmp/hints.txt && \
    mv /tmp/app.py /opt/myapp/ && \
    mv /tmp/config.yaml /opt/myapp/ && \
    mv /tmp/config.yaml.correct /opt/myapp/ && \
    mv /tmp/README.md /opt/ && \
    mv /tmp/hints.txt /opt/

# Исправляем app.py для использования виртуального окружения
RUN sed -i '1i#!/opt/venv/bin/python3' /opt/myapp/app.py && \
    chmod +x /opt/myapp/app.py

# Создаем скрипт запуска
RUN echo '#!/bin/sh' > /start.sh && \
    echo '# Создаем пользователя из переменных окружения' >> /start.sh && \
    echo 'USERNAME=${USERNAME:-student}' >> /start.sh && \
    echo 'PASSWORD=${PASSWORD:-exam2026}' >> /start.sh && \
    echo '' >> /start.sh && \
    echo 'echo "=== Creating user: $USERNAME ==="' >> /start.sh && \
    echo 'adduser -D "$USERNAME"' >> /start.sh && \
    echo 'echo "$USERNAME:$PASSWORD" | chpasswd' >> /start.sh && \
    echo 'echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Копируем README в домашнюю директорию пользователя' >> /start.sh && \
    echo 'mkdir -p /home/$USERNAME' >> /start.sh && \
    echo 'cp /opt/README.md /home/$USERNAME/README.md 2>/dev/null || true' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Копируем приложение в домашнюю директорию пользователя' >> /start.sh && \
    echo 'cp -r /opt/myapp /home/$USERNAME/' >> /start.sh && \
    echo 'chown -R $USERNAME:$USERNAME /home/$USERNAME' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Настраиваем права для логов' >> /start.sh && \
    echo 'mkdir -p /var/log/myapp' >> /start.sh && \
    echo 'chown -R $USERNAME:$USERNAME /var/log/myapp' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Создаем конфиг supervisor с правильным пользователем' >> /start.sh && \
    echo 'cat > /etc/supervisord.conf << EOF' >> /start.sh && \
    echo '[supervisord]' >> /start.sh && \
    echo 'nodaemon=true' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '[program:sshd]' >> /start.sh && \
    echo 'command=/usr/sbin/sshd -D' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '[program:myapp]' >> /start.sh && \
    echo 'command=/opt/venv/bin/python3 /home/$USERNAME/myapp/app.py' >> /start.sh && \
    echo 'user=$USERNAME' >> /start.sh && \
    echo 'autostart=true' >> /start.sh && \
    echo 'autorestart=true' >> /start.sh && \
    echo 'stdout_logfile=/var/log/myapp/supervisor.log' >> /start.sh && \
    echo 'stderr_logfile=/var/log/myapp/supervisor.err' >> /start.sh && \
    echo 'EOF' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Проверяем конфиг' >> /start.sh && \
    echo 'echo "=== Supervisor config ==="' >> /start.sh && \
    echo 'cat /etc/supervisord.conf' >> /start.sh && \
    echo '' >> /start.sh && \
    echo '# Запускаем supervisor' >> /start.sh && \
    echo 'exec /usr/bin/supervisord -c /etc/supervisord.conf' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 22

CMD ["/start.sh"]