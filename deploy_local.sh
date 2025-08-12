#!/bin/bash

# Скрипт развертывания сервис-деск системы в локальной сети
# Использование: ./deploy_local.sh [IP_АДРЕС_СЕРВЕРА]

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
SERVER_IP=${1:-"192.168.0.149"}
PROJECT_DIR="/opt/servisdesk"
SERVICE_USER="servisdesk"

log_info "Развертывание сервис-деск системы на $SERVER_IP"

# Проверка подключения к серверу
log_info "Проверка подключения к серверу..."
if ! ping -c 1 $SERVER_IP > /dev/null 2>&1; then
    log_error "Не удается подключиться к серверу $SERVER_IP"
    exit 1
fi

# Создание архива проекта
log_info "Создание архива проекта..."
tar -czf servisdesk_deploy.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='db.sqlite3' \
    --exclude='logs' \
    --exclude='staticfiles' \
    .

# Копирование архива на сервер
log_info "Копирование файлов на сервер..."
scp servisdesk_deploy.tar.gz root@$SERVER_IP:/tmp/

# Выполнение команд на сервере
log_info "Настройка сервера..."
ssh root@$SERVER_IP << EOF
set -e

# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git curl

# Создание пользователя для приложения
useradd -r -s /bin/bash -m $SERVICE_USER || true

# Создание директорий
mkdir -p $PROJECT_DIR
mkdir -p /var/log/servisdesk
mkdir -p /var/backups/servisdesk

# Распаковка проекта
cd $PROJECT_DIR
tar -xzf /tmp/servisdesk_deploy.tar.gz
rm /tmp/servisdesk_deploy.tar.gz

# Настройка прав доступа
chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR
chown -R $SERVICE_USER:$SERVICE_USER /var/log/servisdesk

# Создание виртуального окружения
sudo -u $SERVICE_USER python3 -m venv venv

# Активация и установка зависимостей
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Настройка переменных окружения
cat > .env << 'ENVEOF'
DJANGO_SETTINGS_MODULE=servisdesk.settings_production
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1
DEBUG=False
ENVEOF

chown $SERVICE_USER:$SERVICE_USER .env

# Применение миграций
python manage.py migrate --settings=servisdesk.settings_production

# Сбор статических файлов
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Создание суперпользователя если не существует
if ! python manage.py shell --settings=servisdesk.settings_production -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>/dev/null | grep -q "True"; then
    python manage.py createsuperuser --settings=servisdesk.settings_production --noinput --username admin --email admin@local.net
    echo "admin:admin123" | chpasswd
fi

# Настройка systemd сервиса
cat > /etc/systemd/system/servisdesk.service << 'SERVICEEOF'
[Unit]
Description=Сервис-деск система
After=network.target

[Service]
Type=notify
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=servisdesk.settings_production"
Environment="SECRET_KEY=\$(cat $PROJECT_DIR/.env | grep SECRET_KEY | cut -d'=' -f2)"
Environment="ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config gunicorn.conf.py servisdesk.wsgi_production:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Настройка Nginx
cat > /etc/nginx/sites-available/servisdesk << 'NGINXEOF'
upstream servisdesk {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name $SERVER_IP;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 30d;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://servisdesk;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    server_tokens off;
}
NGINXEOF

# Активация конфигурации Nginx
ln -sf /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации Nginx
nginx -t

# Перезагрузка systemd и запуск сервисов
systemctl daemon-reload
systemctl enable servisdesk
systemctl restart servisdesk
systemctl restart nginx

# Настройка файрвола
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

# Создание скрипта управления
cat > /usr/local/bin/servisdesk-manage << 'MANAGEEOF'
#!/bin/bash
case "\$1" in
    start) systemctl start servisdesk ;;
    stop) systemctl stop servisdesk ;;
    restart) systemctl restart servisdesk ;;
    status) systemctl status servisdesk ;;
    logs) journalctl -u servisdesk -f ;;
    *) echo "Использование: \$0 {start|stop|restart|status|logs}" ;;
esac
MANAGEEOF

chmod +x /usr/local/bin/servisdesk-manage

EOF

# Очистка локального архива
rm servisdesk_deploy.tar.gz

log_success "Развертывание завершено!"
log_info "URL: http://$SERVER_IP"
log_info "Администратор: admin / admin123"
log_info "Управление: servisdesk-manage {start|stop|restart|status|logs}"
log_info "Логи: journalctl -u servisdesk -f"
