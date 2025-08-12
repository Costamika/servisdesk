#!/bin/bash

# Скрипт управления сервис-деск системой
# Использование: ./manage_service.sh [start|stop|restart|status|logs|backup|update]

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

# Переменные
SERVICE_NAME="servisdesk"
PROJECT_DIR="/var/www/servisdesk"
BACKUP_DIR="/var/backups/servisdesk"

# Функция показа справки
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  start     - Запустить сервис"
    echo "  stop      - Остановить сервис"
    echo "  restart   - Перезапустить сервис"
    echo "  status    - Показать статус сервиса"
    echo "  logs      - Показать логи"
    echo "  backup    - Создать резервную копию"
    echo "  restore   - Восстановить из резервной копии"
    echo "  update    - Обновить приложение"
    echo "  shell     - Открыть Django shell"
    echo "  migrate   - Применить миграции"
    echo "  collect   - Собрать статические файлы"
    echo "  help      - Показать эту справку"
}

# Функция запуска сервиса
start_service() {
    log_info "Запуск сервиса $SERVICE_NAME"
    sudo systemctl start $SERVICE_NAME
    sudo systemctl start nginx
    log_success "Сервис запущен"
}

# Функция остановки сервиса
stop_service() {
    log_info "Остановка сервиса $SERVICE_NAME"
    sudo systemctl stop $SERVICE_NAME
    sudo systemctl stop nginx
    log_success "Сервис остановлен"
}

# Функция перезапуска сервиса
restart_service() {
    log_info "Перезапуск сервиса $SERVICE_NAME"
    sudo systemctl restart $SERVICE_NAME
    sudo systemctl restart nginx
    log_success "Сервис перезапущен"
}

# Функция показа статуса
show_status() {
    log_info "Статус сервиса $SERVICE_NAME"
    echo "=== Systemd статус ==="
    sudo systemctl status $SERVICE_NAME --no-pager -l
    echo ""
    echo "=== Nginx статус ==="
    sudo systemctl status nginx --no-pager -l
    echo ""
    echo "=== Процессы ==="
    ps aux | grep -E "(gunicorn|nginx)" | grep -v grep
}

# Функция показа логов
show_logs() {
    log_info "Показать логи"
    echo "=== Логи сервиса ==="
    sudo journalctl -u $SERVICE_NAME -n 50 --no-pager
    echo ""
    echo "=== Логи Nginx ==="
    sudo tail -n 50 /var/log/nginx/error.log
    echo ""
    echo "=== Логи приложения ==="
    if [ -f "/var/log/servisdesk/django.log" ]; then
        sudo tail -n 50 /var/log/servisdesk/django.log
    else
        log_warning "Файл логов Django не найден"
    fi
}

# Функция создания резервной копии
create_backup() {
    log_info "Создание резервной копии"
    BACKUP_FILE="$BACKUP_DIR/servisdesk_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    sudo mkdir -p $BACKUP_DIR
    
    # Остановка сервиса для консистентности
    stop_service
    
    # Создание архива
    sudo tar -czf $BACKUP_FILE \
        --exclude="$PROJECT_DIR/venv" \
        --exclude="$PROJECT_DIR/staticfiles" \
        --exclude="$PROJECT_DIR/logs" \
        --exclude="$PROJECT_DIR/.git" \
        -C /var/www servisdesk
    
    # Запуск сервиса
    start_service
    
    log_success "Резервная копия создана: $BACKUP_FILE"
}

# Функция восстановления из резервной копии
restore_backup() {
    if [ -z "$1" ]; then
        log_error "Укажите файл резервной копии"
        echo "Доступные резервные копии:"
        ls -la $BACKUP_DIR/
        exit 1
    fi
    
    BACKUP_FILE="$1"
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Файл резервной копии не найден: $BACKUP_FILE"
        exit 1
    fi
    
    log_info "Восстановление из резервной копии: $BACKUP_FILE"
    
    # Остановка сервиса
    stop_service
    
    # Восстановление файлов
    sudo tar -xzf $BACKUP_FILE -C /var/www/
    
    # Восстановление прав доступа
    sudo chown -R www-data:www-data $PROJECT_DIR
    
    # Запуск сервиса
    start_service
    
    log_success "Восстановление завершено"
}

# Функция обновления приложения
update_app() {
    log_info "Обновление приложения"
    
    # Создание резервной копии
    create_backup
    
    # Переход в директорию проекта
    cd $PROJECT_DIR
    
    # Активация виртуального окружения
    source venv/bin/activate
    
    # Обновление зависимостей
    log_info "Обновление зависимостей"
    pip install -r requirements.txt
    
    # Применение миграций
    log_info "Применение миграций"
    python manage.py migrate --settings=servisdesk.settings_production
    
    # Сбор статических файлов
    log_info "Сбор статических файлов"
    python manage.py collectstatic --noinput --settings=servisdesk.settings_production
    
    # Перезапуск сервиса
    restart_service
    
    log_success "Обновление завершено"
}

# Функция Django shell
django_shell() {
    log_info "Открытие Django shell"
    cd $PROJECT_DIR
    source venv/bin/activate
    python manage.py shell --settings=servisdesk.settings_production
}

# Функция применения миграций
run_migrations() {
    log_info "Применение миграций"
    cd $PROJECT_DIR
    source venv/bin/activate
    python manage.py migrate --settings=servisdesk.settings_production
    log_success "Миграции применены"
}

# Функция сбора статических файлов
collect_static() {
    log_info "Сбор статических файлов"
    cd $PROJECT_DIR
    source venv/bin/activate
    python manage.py collectstatic --noinput --settings=servisdesk.settings_production
    log_success "Статические файлы собраны"
}

# Основная логика
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    backup)
        create_backup
        ;;
    restore)
        restore_backup "$2"
        ;;
    update)
        update_app
        ;;
    shell)
        django_shell
        ;;
    migrate)
        run_migrations
        ;;
    collect)
        collect_static
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Неизвестная команда: $1"
        show_help
        exit 1
        ;;
esac
