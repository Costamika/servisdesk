#!/bin/bash

# Скрипт развертывания сервис-деск системы
# Использование: ./deploy.sh [production|staging]

set -e  # Остановка при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
ENVIRONMENT=${1:-production}
PROJECT_DIR="/var/www/servisdesk"
BACKUP_DIR="/var/backups/servisdesk"
LOG_FILE="/var/log/servisdesk/deploy.log"

log_info "Начинаем развертывание в окружении: $ENVIRONMENT"

# Создание директорий если не существуют
sudo mkdir -p $PROJECT_DIR
sudo mkdir -p $BACKUP_DIR
sudo mkdir -p /var/log/servisdesk
sudo mkdir -p /var/www/servisdesk/logs
sudo mkdir -p /var/www/servisdesk/media
sudo mkdir -p /var/www/servisdesk/staticfiles

# Создание пользователя www-data если не существует
if ! id "www-data" &>/dev/null; then
    log_info "Создание пользователя www-data"
    sudo useradd -r -s /bin/false www-data
fi

# Резервное копирование базы данных
if [ -f "$PROJECT_DIR/db.sqlite3" ]; then
    log_info "Создание резервной копии базы данных"
    sudo cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sqlite3"
fi

# Копирование файлов проекта
log_info "Копирование файлов проекта"
sudo cp -r . $PROJECT_DIR/
sudo chown -R www-data:www-data $PROJECT_DIR

# Переход в директорию проекта
cd $PROJECT_DIR

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    log_info "Создание виртуального окружения"
    sudo -u www-data python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Обновление pip
log_info "Обновление pip"
pip install --upgrade pip

# Установка зависимостей
log_info "Установка зависимостей"
pip install -r requirements.txt

# Настройка переменных окружения
if [ ! -f ".env" ]; then
    log_info "Создание файла .env"
    cat > .env << EOF
# Django settings
DJANGO_SETTINGS_MODULE=servisdesk.settings_production
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database settings (для PostgreSQL)
# DB_NAME=servisdesk
# DB_USER=servisdesk
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# Email settings
EMAIL_HOST=localhost
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# Gunicorn settings
GUNICORN_BIND=127.0.0.1:8000
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=30
GUNICORN_ACCESS_LOG=/var/log/servisdesk/gunicorn_access.log
GUNICORN_ERROR_LOG=/var/log/servisdesk/gunicorn_error.log
EOF
    sudo chown www-data:www-data .env
fi

# Применение миграций
log_info "Применение миграций базы данных"
python manage.py migrate --settings=servisdesk.settings_production

# Сбор статических файлов
log_info "Сбор статических файлов"
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Создание суперпользователя если не существует
if ! python manage.py shell --settings=servisdesk.settings_production -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>/dev/null | grep -q "True"; then
    log_info "Создание суперпользователя"
    python manage.py createsuperuser --settings=servisdesk.settings_production --noinput --username admin --email admin@example.com
    echo "admin:admin123" | sudo chpasswd
fi

# Настройка прав доступа
log_info "Настройка прав доступа"
sudo chown -R www-data:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
sudo chmod 660 $PROJECT_DIR/db.sqlite3
sudo chmod 660 $PROJECT_DIR/.env

# Копирование systemd сервиса
log_info "Настройка systemd сервиса"
sudo cp servisdesk.service /etc/systemd/system/
sudo systemctl daemon-reload

# Копирование конфигурации Nginx
log_info "Настройка Nginx"
sudo cp nginx.conf /etc/nginx/sites-available/servisdesk
sudo ln -sf /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации Nginx
if sudo nginx -t; then
    log_success "Конфигурация Nginx корректна"
else
    log_error "Ошибка в конфигурации Nginx"
    exit 1
fi

# Перезапуск сервисов
log_info "Перезапуск сервисов"
sudo systemctl enable servisdesk
sudo systemctl restart servisdesk
sudo systemctl restart nginx

# Проверка статуса сервисов
log_info "Проверка статуса сервисов"
if sudo systemctl is-active --quiet servisdesk; then
    log_success "Сервис servisdesk запущен"
else
    log_error "Ошибка запуска сервиса servisdesk"
    sudo systemctl status servisdesk
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    log_success "Сервис nginx запущен"
else
    log_error "Ошибка запуска сервиса nginx"
    sudo systemctl status nginx
    exit 1
fi

# Проверка доступности приложения
log_info "Проверка доступности приложения"
sleep 5
if curl -f http://localhost/ > /dev/null 2>&1; then
    log_success "Приложение доступно"
else
    log_warning "Приложение недоступно, проверьте логи"
    sudo journalctl -u servisdesk -n 20
fi

log_success "Развертывание завершено успешно!"
log_info "URL: http://your-domain.com"
log_info "Администратор: admin / admin123"
log_info "Логи: /var/log/servisdesk/"
