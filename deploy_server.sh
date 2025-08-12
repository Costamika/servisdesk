#!/bin/bash

# Скрипт для развертывания сервис-деск системы на сервере
# Использование: ./deploy_server.sh SERVER_IP USERNAME

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для логирования
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
if [ $# -ne 2 ]; then
    echo "Использование: $0 SERVER_IP USERNAME"
    echo "Пример: $0 192.168.1.100 admin"
    exit 1
fi

SERVER_IP=$1
USERNAME=$2
REMOTE_DIR="/opt/servisdesk"
ARCHIVE_NAME="servisdesk-deploy.tar.gz"

log_info "Начинаем развертывание сервис-деск системы на $SERVER_IP"

# Проверка наличия архива
if [ ! -f "$ARCHIVE_NAME" ]; then
    log_error "Архив $ARCHIVE_NAME не найден!"
    log_info "Создаем архив..."
    tar -czf $ARCHIVE_NAME --exclude='venv' --exclude='*.pyc' --exclude='__pycache__' --exclude='.git' --exclude='db.sqlite3' .
fi

# Проверка подключения к серверу
log_info "Проверяем подключение к серверу..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes $USERNAME@$SERVER_IP exit 2>/dev/null; then
    log_error "Не удается подключиться к серверу $SERVER_IP"
    log_info "Убедитесь, что:"
    log_info "1. Сервер доступен по IP $SERVER_IP"
    log_info "2. SSH сервис запущен"
    log_info "3. Пользователь $USERNAME существует"
    log_info "4. SSH ключи настроены или пароль введен"
    exit 1
fi

log_success "Подключение к серверу установлено"

# Создание директории на сервере
log_info "Создаем директорию на сервере..."
ssh $USERNAME@$SERVER_IP "sudo mkdir -p $REMOTE_DIR && sudo chown $USERNAME:$USERNAME $REMOTE_DIR"

# Копирование архива
log_info "Копируем архив на сервер..."
scp $ARCHIVE_NAME $USERNAME@$SERVER_IP:$REMOTE_DIR/

# Распаковка и настройка на сервере
log_info "Настраиваем систему на сервере..."
ssh $USERNAME@$SERVER_IP << EOF
    cd $REMOTE_DIR
    
    # Распаковка архива
    tar -xzf $ARCHIVE_NAME
    
    # Установка системных пакетов
    log_info "Устанавливаем системные пакеты..."
    sudo apt update -y
    sudo apt install -y python3 python3-pip python3-venv nginx git curl
    
    # Создание виртуального окружения
    log_info "Создаем виртуальное окружение..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Установка зависимостей
    log_info "Устанавливаем Python зависимости..."
    pip install -r requirements.txt
    
    # Настройка переменных окружения
    log_info "Настраиваем переменные окружения..."
    if [ ! -f .env ]; then
        cp env.example .env
    fi
    
    # Замена IP адреса в настройках
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1/" .env
    sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=['$SERVER_IP', 'localhost', '127.0.0.1']/" servisdesk/settings.py
    sed -i "s/server_name.*/server_name $SERVER_IP;/" nginx.conf
    sed -i "s/Environment=\"ALLOWED_HOSTS=.*/Environment=\"ALLOWED_HOSTS=$SERVER_IP\"/" servisdesk.service
    
    # Применение миграций
    log_info "Применяем миграции базы данных..."
    python manage.py migrate
    
    # Создание суперпользователя (если не существует)
    log_info "Создаем суперпользователя..."
    if [ ! -f superuser_created ]; then
        echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
        touch superuser_created
    fi
    
    # Создание тестовых данных
    log_info "Создаем тестовые данные..."
    python create_test_data.py
    
    # Сбор статических файлов
    log_info "Собираем статические файлы..."
    python manage.py collectstatic --noinput
    
    # Настройка Nginx
    log_info "Настраиваем Nginx..."
    sudo cp nginx.conf /etc/nginx/sites-available/servisdesk
    sudo ln -sf /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl restart nginx
    
    # Настройка systemd
    log_info "Настраиваем systemd службу..."
    sudo cp servisdesk.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable servisdesk
    sudo systemctl start servisdesk
    
    # Настройка файрвола
    log_info "Настраиваем файрвол..."
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 22/tcp
    sudo ufw --force enable
    
    log_success "Развертывание завершено!"
    log_info "Система доступна по адресу: http://$SERVER_IP/"
    log_info "Данные для входа: admin / admin123"
EOF

log_success "Развертывание успешно завершено!"
echo ""
echo "🎉 Сервис-деск система развернута на сервере!"
echo ""
echo "📋 Информация:"
echo "   URL: http://$SERVER_IP/"
echo "   Администратор: admin / admin123"
echo "   Пользователи: ivanov/user123, petrova/user123, sidorov/user123"
echo ""
echo "🔧 Управление:"
echo "   Остановить: ssh $USERNAME@$SERVER_IP 'sudo systemctl stop servisdesk'"
echo "   Запустить:  ssh $USERNAME@$SERVER_IP 'sudo systemctl start servisdesk'"
echo "   Логи:       ssh $USERNAME@$SERVER_IP 'sudo journalctl -u servisdesk -f'"
echo ""
