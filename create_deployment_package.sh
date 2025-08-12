#!/bin/bash

# Скрипт создания архива для развертывания сервис-деск системы
# Использование: ./create_deployment_package.sh [версия]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Функции для вывода
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка аргументов
VERSION=${1:-"1.0.0"}
PACKAGE_NAME="servisdesk-${VERSION}"
ARCHIVE_NAME="${PACKAGE_NAME}.tar.gz"

log_info "Создание пакета развертывания версии $VERSION"

# Проверка наличия необходимых файлов
log_info "Проверка файлов проекта..."
required_files=(
    "manage.py"
    "requirements.txt"
    "servisdesk/settings.py"
    "servisdesk/settings_production.py"
    "servisdesk/wsgi_production.py"
    "gunicorn.conf.py"
    "nginx.conf"
    "servisdesk.service"
    "deploy.sh"
    "manage_service.sh"
    "Dockerfile"
    "docker-compose.yml"
    "env.example"
    ".gitignore"
    "README.md"
    "DEPLOYMENT.md"
    "LOCAL_DEPLOYMENT.md"
    "QUICK_START.md"
    "USAGE_EXAMPLE.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        log_error "Файл $file не найден"
        exit 1
    fi
done

log_success "Все необходимые файлы найдены"

# Создание временной директории
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/$PACKAGE_NAME"

log_info "Создание структуры пакета..."

# Создание директорий
mkdir -p "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR/servisdesk"
mkdir -p "$PACKAGE_DIR/users"
mkdir -p "$PACKAGE_DIR/tickets"
mkdir -p "$PACKAGE_DIR/templates"
mkdir -p "$PACKAGE_DIR/static"

# Копирование основных файлов
log_info "Копирование файлов проекта..."

# Основные файлы Django
cp manage.py "$PACKAGE_DIR/"
cp requirements.txt "$PACKAGE_DIR/"
cp gunicorn.conf.py "$PACKAGE_DIR/"
cp nginx.conf "$PACKAGE_DIR/"
cp servisdesk.service "$PACKAGE_DIR/"
cp env.example "$PACKAGE_DIR/"
cp .gitignore "$PACKAGE_DIR/"

# Настройки Django
cp servisdesk/settings.py "$PACKAGE_DIR/servisdesk/"
cp servisdesk/settings_production.py "$PACKAGE_DIR/servisdesk/"
cp servisdesk/wsgi_production.py "$PACKAGE_DIR/servisdesk/"
cp servisdesk/urls.py "$PACKAGE_DIR/servisdesk/"
cp servisdesk/__init__.py "$PACKAGE_DIR/servisdesk/"

# Приложения
cp -r users/* "$PACKAGE_DIR/users/"
cp -r tickets/* "$PACKAGE_DIR/tickets/"

# Шаблоны
cp -r templates/* "$PACKAGE_DIR/templates/"

# Статические файлы
cp -r static/* "$PACKAGE_DIR/static/"

# Скрипты развертывания
cp deploy.sh "$PACKAGE_DIR/"
cp deploy_local.sh "$PACKAGE_DIR/"
cp manage_service.sh "$PACKAGE_DIR/"

# Docker файлы
cp Dockerfile "$PACKAGE_DIR/"
cp docker-compose.yml "$PACKAGE_DIR/"

# Документация
cp README.md "$PACKAGE_DIR/"
cp DEPLOYMENT.md "$PACKAGE_DIR/"
cp LOCAL_DEPLOYMENT.md "$PACKAGE_DIR/"
cp QUICK_START.md "$PACKAGE_DIR/"
cp USAGE_EXAMPLE.md "$PACKAGE_DIR/"

# Создание файла версии
echo "$VERSION" > "$PACKAGE_DIR/VERSION"

# Создание файла с информацией о развертывании
cat > "$PACKAGE_DIR/DEPLOYMENT_INFO.txt" << EOF
Сервис-деск система - Пакет развертывания
Версия: $VERSION
Дата создания: $(date)

Содержимое пакета:
- Django приложение (servisdesk, users, tickets)
- Шаблоны и статические файлы
- Конфигурации для production (Nginx, Gunicorn, systemd)
- Скрипты автоматического развертывания
- Docker конфигурация
- Документация

Способы развертывания:
1. Автоматическое: ./deploy_local.sh [IP_СЕРВЕРА]
2. Ручное: следовать инструкциям в LOCAL_DEPLOYMENT.md
3. Docker: docker-compose up -d

Требования к серверу:
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- Python 3.8+
- 2GB RAM минимум
- 10GB свободного места

Доступ к системе:
- URL: http://IP_СЕРВЕРА
- Администратор: admin / admin123

Поддержка:
- Документация: README.md, DEPLOYMENT.md, LOCAL_DEPLOYMENT.md
- Примеры использования: USAGE_EXAMPLE.md
- Быстрый старт: QUICK_START.md
EOF

# Создание архива
log_info "Создание архива $ARCHIVE_NAME..."
cd "$TEMP_DIR"
tar -czf "$ARCHIVE_NAME" "$PACKAGE_NAME"

# Перемещение архива в текущую директорию
mv "$ARCHIVE_NAME" "$(pwd)/"

# Очистка временных файлов
rm -rf "$TEMP_DIR"

# Проверка размера архива
ARCHIVE_SIZE=$(du -h "$ARCHIVE_NAME" | cut -f1)

log_success "Пакет развертывания создан успешно!"
log_info "Файл: $ARCHIVE_NAME"
log_info "Размер: $ARCHIVE_SIZE"
log_info "Версия: $VERSION"

# Создание контрольной суммы
log_info "Создание контрольной суммы..."
sha256sum "$ARCHIVE_NAME" > "${ARCHIVE_NAME}.sha256"

log_info "Контрольная сумма сохранена в ${ARCHIVE_NAME}.sha256"

# Информация о развертывании
echo ""
log_info "Для развертывания используйте:"
echo "  ./deploy_local.sh [IP_СЕРВЕРА]"
echo ""
log_info "Или следуйте инструкциям в LOCAL_DEPLOYMENT.md"
