#!/bin/sh

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== ПРОВЕРКА ЭКЗАМЕНА ==="
echo

# Проверка 1: Конфиг синтаксис
echo -n "Проверка конфига: "
if nginx -t 2>&1 | grep -q "syntax is ok"; then
    echo -e "${GREEN}✓ OK${NC}"
    CONF_OK=true
else
    echo -e "${RED}✗ ОШИБКА В КОНФИГЕ${NC}"
    CONF_OK=false
fi

# Проверка 2: Процесс запущен
echo -n "Статус Nginx: "
if pgrep -x "nginx" > /dev/null; then
    echo -e "${GREEN}✓ ЗАПУЩЕН${NC}"
    PROC_OK=true
else
    echo -e "${RED}✗ НЕ ЗАПУЩЕН${NC}"
    PROC_OK=false
fi

# Проверка 3: Сайт отвечает
echo -n "Доступность сайта: "
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo -e "${GREEN}✓ ОТВЕЧАЕТ${NC}"
    SITE_OK=true
else
    echo -e "${RED}✗ НЕ ОТВЕЧАЕТ${NC}"
    SITE_OK=false
fi

echo
echo "=== РЕЗУЛЬТАТ ==="

if [ "$CONF_OK" = true ] && [ "$PROC_OK" = true ] && [ "$SITE_OK" = true ]; then
    echo -e "${GREEN}ЭКЗАМЕН СДАН!${NC}"
    echo "Вы нашли и исправили ошибку. Поздравляем!"
else
    echo -e "${RED}ЭКЗАМЕН НЕ СДАН${NC}"
    echo "Что-то пошло не так. Попробуйте ещё раз."
    echo "Подсказка: используй 'nginx -t' для диагностики"
fi