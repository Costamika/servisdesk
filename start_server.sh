#!/bin/bash
# -*- coding: utf-8 -*-
"""
Скрипт для запуска Django сервера ServisDesk

Использование:
    ./start_server.sh
    ./start_server.sh --host 127.0.0.1 --port 8080
"""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверяем, что мы в правильной директории
if [ ! -f "manage.py" ]; then
    print_error "Файл manage.py не найден. Запустите скрипт из корневой директории проекта."
    exit 1
fi

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    print_warning "Виртуальное окружение не найдено. Создаем..."
    python3 -m venv venv
    print_success "Виртуальное окружение создано"
fi

# Активируем виртуальное окружение
print_info "Активация виртуального окружения..."
source venv/bin/activate

# Проверяем установку Django
if ! python3 -c "import django" 2>/dev/null; then
    print_warning "Django не установлен. Устанавливаем зависимости..."
    pip install -r requirements.txt
    print_success "Зависимости установлены"
fi

# Проверяем миграции
print_info "Проверка миграций..."
python3 manage.py check --deploy 2>/dev/null || python3 manage.py check

# Запускаем сервер
print_info "Запуск сервера..."
echo "=================================================="
python3 run_server.py "$@"
