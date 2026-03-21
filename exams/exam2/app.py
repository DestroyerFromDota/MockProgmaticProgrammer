#!/opt/venv/bin/python3
import yaml
import logging
import time
import os
import sys
from datetime import datetime

# Настройка логирования
log_file = '/var/log/myapp/app.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    """Загружает конфигурацию из YAML файла"""
    config_path = '/home/student/myapp/config.yaml'
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Проверяем наличие обязательных полей
        if 'app_name' not in config:
            logging.error("Отсутствует поле 'app_name' в конфиге")
            return None
        
        # !!! ЗДЕСЬ ОШИБКА !!!
        # В конфиге написано 'log_leve' вместо 'log_level'
        if 'log_level' not in config:
            logging.error("Отсутствует поле 'log_level' в конфиге")
            return None
            
        return config
    except Exception as e:
        logging.error(f"Ошибка загрузки конфига: {e}")
        return None

def main():
    logging.info("=" * 50)
    logging.info("Приложение запущено")
    
    # Счетчик попыток
    attempt = 1
    
    while True:
        config = load_config()
        
        if config:
            logging.info(f"Конфиг загружен успешно! Приложение: {config.get('app_name')}")
            logging.info(f"Уровень логирования: {config.get('log_level')}")
            logging.info("Все работает отлично!")
        else:
            logging.error(f"Попытка {attempt}: Не удалось загрузить конфиг")
            logging.error("Проверьте файл /home/student/myapp/config.yaml")
            attempt += 1
        
        # Ждем 10 секунд перед следующей попыткой
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Приложение остановлено")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        sys.exit(1)