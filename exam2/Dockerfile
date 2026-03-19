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

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir pyyaml

# Создаем пользователя student
RUN adduser -D student && \
    echo "student:exam2026" | chpasswd && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Настраиваем SSH
RUN ssh-keygen -A && \
    echo "root:rootpass" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Создаем структуру директорий
RUN mkdir -p /home/student/myapp /var/log/myapp /opt

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
    mv /tmp/app.py /home/student/myapp/ && \
    mv /tmp/config.yaml /home/student/myapp/ && \
    mv /tmp/config.yaml.correct /home/student/myapp/ && \
    mv /tmp/README.md /home/student/ && \
    mv /tmp/hints.txt /opt/

# Исправляем app.py для использования виртуального окружения
RUN sed -i '1i#!/opt/venv/bin/python3' /home/student/myapp/app.py && \
    chmod +x /home/student/myapp/app.py

# Настраиваем supervisor для автозапуска Python-скрипта
RUN echo '[supervisord]' > /etc/supervisord.conf && \
    echo 'nodaemon=true' >> /etc/supervisord.conf && \
    echo '' >> /etc/supervisord.conf && \
    echo '[program:sshd]' >> /etc/supervisord.conf && \
    echo 'command=/usr/sbin/sshd -D' >> /etc/supervisord.conf && \
    echo '' >> /etc/supervisord.conf && \
    echo '[program:myapp]' >> /etc/supervisord.conf && \
    echo 'command=/opt/venv/bin/python3 /home/student/myapp/app.py' >> /etc/supervisord.conf && \
    echo 'user=student' >> /etc/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisord.conf && \
    echo 'stdout_logfile=/var/log/myapp/supervisor.log' >> /etc/supervisord.conf && \
    echo 'stderr_logfile=/var/log/myapp/supervisor.err' >> /etc/supervisord.conf

# Права
RUN chown -R student:student /home/student && \
    chown -R student:student /var/log/myapp && \
    chown -R student:student /opt/venv && \
    chmod 644 /opt/hints.txt

EXPOSE 22

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]