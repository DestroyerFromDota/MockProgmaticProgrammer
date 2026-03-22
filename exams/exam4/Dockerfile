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


# Установка ssh демона
RUN apk add --no-cache bash openssh-server \
    && ssh-keygen -A \
    && adduser -D student \
    && echo "student:exam2026" | chpasswd

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

# Запуск ssh демона
CMD ["/usr/sbin/sshd", "-D"]