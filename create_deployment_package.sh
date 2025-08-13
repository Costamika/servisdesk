#!/bin/bash

# Скрипт для создания архива развертывания ServisDesk
# Автор: AI Assistant
# Дата: $(date)

set -e  # Остановка при ошибке

echo "=== Создание архива развертывания ServisDesk ==="
echo "Дата: $(date)"
echo

# Проверяем, что мы в правильной директории
if [ ! -f "manage.py" ]; then
    echo "❌ Ошибка: manage.py не найден. Запустите скрипт из корневой директории проекта."
    exit 1
fi

# Создаем временную директорию для архива
TEMP_DIR="deployment_temp"
ARCHIVE_NAME="servisdesk_deployment_$(date +%Y%m%d_%H%M%S).tar.gz"

echo "📁 Создание временной директории..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

echo "📋 Копирование файлов проекта..."

# Основные файлы Django
cp -r servisdesk/ "$TEMP_DIR/"
cp -r tickets/ "$TEMP_DIR/"
cp -r users/ "$TEMP_DIR/"
cp -r templates/ "$TEMP_DIR/"
cp -r static/ "$TEMP_DIR/"

# Конфигурационные файлы
cp manage.py "$TEMP_DIR/"
cp requirements.txt "$TEMP_DIR/"
cp config_ip_system.py "$TEMP_DIR/"
cp gunicorn.conf.py "$TEMP_DIR/"
cp nginx.conf "$TEMP_DIR/"
cp docker-compose.yml "$TEMP_DIR/"
cp Dockerfile "$TEMP_DIR/"

# Документация
cp README.md "$TEMP_DIR/"
cp README_DEPLOYMENT.md "$TEMP_DIR/"
cp QUICK_DEPLOY.md "$TEMP_DIR/"
cp QUICK_DEPLOY_SERVER.md "$TEMP_DIR/"
cp LOCAL_DEPLOYMENT.md "$TEMP_DIR/"
cp DEPLOYMENT.md "$TEMP_DIR/"
cp DEPLOY_SERVER.md "$TEMP_DIR/"

# Скрипты развертывания
cp deploy.sh "$TEMP_DIR/"
cp deploy_server.sh "$TEMP_DIR/"
cp deploy_local.sh "$TEMP_DIR/"
cp start_server.sh "$TEMP_DIR/"
cp manage_service.sh "$TEMP_DIR/"

# Системные файлы
cp servisdesk.service "$TEMP_DIR/"
cp setup_admin.py "$TEMP_DIR/"
cp create_test_data.py "$TEMP_DIR/"

# Создаем .gitignore для архива
cat > "$TEMP_DIR/.gitignore" << 'EOF'
# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Temporary files
*.tmp
*.temp

# Backup files
backup/
*.bak

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite

# Cache
.cache/
*.cache

# Coverage
htmlcov/
.coverage
.coverage.*

# Test
.pytest_cache/
.tox/

# Documentation
docs/_build/

# Deployment
deployment_temp/
servisdesk_deployment_*.tar.gz
EOF

# Создаем README для архива
cat > "$TEMP_DIR/README_DEPLOYMENT.txt" << 'EOF'
=== ServisDesk - Система управления заявками ===

Этот архив содержит полную систему ServisDesk для развертывания на сервере.

=== Содержимое архива ===

📁 Основные компоненты:
- servisdesk/ - Основное приложение Django
- tickets/ - Модуль управления заявками
- users/ - Модуль управления пользователями
- templates/ - HTML шаблоны
- static/ - Статические файлы (CSS, JS)

📋 Конфигурация:
- config_ip_system.py - Настройки IP и порта
- gunicorn.conf.py - Конфигурация Gunicorn
- nginx.conf - Конфигурация Nginx
- docker-compose.yml - Docker Compose
- Dockerfile - Docker образ

📚 Документация:
- README.md - Основная документация
- README_DEPLOYMENT.md - Руководство по развертыванию
- QUICK_DEPLOY.md - Быстрое развертывание
- DEPLOYMENT.md - Подробное развертывание

🚀 Скрипты развертывания:
- deploy.sh - Основной скрипт развертывания
- deploy_server.sh - Развертывание на сервере
- deploy_local.sh - Локальное развертывание
- start_server.sh - Запуск сервера
- manage_service.sh - Управление службой

=== Быстрый старт ===

1. Распакуйте архив:
   tar -xzf servisdesk_deployment_*.tar.gz

2. Перейдите в директорию:
   cd deployment_temp

3. Запустите развертывание:
   ./deploy.sh

=== Подробная документация ===

См. файлы:
- README_DEPLOYMENT.md - Подробное руководство
- QUICK_DEPLOY.md - Быстрое развертывание
- DEPLOYMENT.md - Полная документация

=== Версия ===

Создан: $(date)
Версия: 1.0.0
EOF

# Создаем файл с информацией о версии
cat > "$TEMP_DIR/VERSION" << EOF
ServisDesk Deployment Package
Version: 1.0.0
Created: $(date)
Build: $(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
Python: $(python3 --version 2>/dev/null || echo "unknown")
Django: $(python3 -c "import django; print(django.get_version())" 2>/dev/null || echo "unknown")
EOF

echo "📦 Создание архива..."
tar -czf "$ARCHIVE_NAME" -C "$TEMP_DIR" .

echo "🧹 Очистка временных файлов..."
rm -rf "$TEMP_DIR"

echo
echo "✅ Архив создан успешно!"
echo "📁 Файл: $ARCHIVE_NAME"
echo "📏 Размер: $(du -h "$ARCHIVE_NAME" | cut -f1)"
echo
echo "🚀 Для развертывания:"
echo "1. Скопируйте архив на сервер"
echo "2. Распакуйте: tar -xzf $ARCHIVE_NAME"
echo "3. Запустите: ./deploy.sh"
echo
echo "📚 Документация по развертыванию:"
echo "- README_DEPLOYMENT.md"
echo "- QUICK_DEPLOY.md"
echo "- DEPLOYMENT.md"
