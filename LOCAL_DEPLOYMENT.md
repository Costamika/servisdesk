# 🏠 Развертывание сервис-деск системы в локальной сети

## 📋 Требования к серверу

### Минимальные требования:
- **ОС**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **RAM**: 2GB
- **Диск**: 10GB свободного места
- **Сеть**: Статический IP в локальной сети
- **Доступ**: SSH доступ с правами root

### Рекомендуемые требования:
- **RAM**: 4GB+
- **Диск**: 20GB+ SSD
- **Процессор**: 2+ ядра
- **Сеть**: Гигабитное подключение

## 🚀 Быстрое развертывание

### Вариант 1: Автоматическое развертывание

```bash
# 1. Сделать скрипт исполняемым
chmod +x deploy_local.sh

# 2. Запустить развертывание
./deploy_local.sh 192.168.1.100
```

### Вариант 2: Ручное развертывание

#### Шаг 1: Подготовка сервера
```bash
# Подключение к серверу
ssh root@192.168.1.100

# Обновление системы
apt update && apt upgrade -y

# Установка необходимых пакетов
apt install -y python3 python3-pip python3-venv nginx git curl
```

#### Шаг 2: Создание пользователя и директорий
```bash
# Создание пользователя
useradd -r -s /bin/bash -m servisdesk

# Создание директорий
mkdir -p /opt/servisdesk
mkdir -p /var/log/servisdesk
mkdir -p /var/backups/servisdesk
```

#### Шаг 3: Загрузка проекта
```bash
# Клонирование репозитория
cd /opt
git clone <repository-url> servisdesk
cd servisdesk

# Настройка прав доступа
chown -R servisdesk:servisdesk /opt/servisdesk
```

#### Шаг 4: Настройка виртуального окружения
```bash
# Переключение на пользователя
sudo -u servisdesk bash

# Создание виртуального окружения
python3 -m venv venv

# Активация и установка зависимостей
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Шаг 5: Настройка переменных окружения
```bash
# Создание .env файла
cat > .env << EOF
DJANGO_SETTINGS_MODULE=servisdesk.settings_production
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=192.168.1.100,localhost,127.0.0.1
DEBUG=False
EOF

chown servisdesk:servisdesk .env
```

#### Шаг 6: Настройка базы данных
```bash
# Применение миграций
python manage.py migrate --settings=servisdesk.settings_production

# Сбор статических файлов
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Создание суперпользователя
python manage.py createsuperuser --settings=servisdesk.settings_production
```

#### Шаг 7: Настройка systemd сервиса
```bash
# Выход из пользователя servisdesk
exit

# Создание файла сервиса
cat > /etc/systemd/system/servisdesk.service << EOF
[Unit]
Description=Сервис-деск система
After=network.target

[Service]
Type=notify
User=servisdesk
Group=servisdesk
WorkingDirectory=/opt/servisdesk
Environment="PATH=/opt/servisdesk/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=servisdesk.settings_production"
Environment="SECRET_KEY=\$(cat /opt/servisdesk/.env | grep SECRET_KEY | cut -d'=' -f2)"
Environment="ALLOWED_HOSTS=192.168.1.100,localhost,127.0.0.1"
ExecStart=/opt/servisdesk/venv/bin/gunicorn --config gunicorn.conf.py servisdesk.wsgi_production:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### Шаг 8: Настройка Nginx
```bash
# Создание конфигурации Nginx
cat > /etc/nginx/sites-available/servisdesk << EOF
upstream servisdesk {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name 192.168.1.100;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /opt/servisdesk/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /opt/servisdesk/media/;
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
EOF

# Активация конфигурации
ln -sf /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации
nginx -t
```

#### Шаг 9: Запуск сервисов
```bash
# Перезагрузка systemd
systemctl daemon-reload

# Включение автозапуска
systemctl enable servisdesk

# Запуск сервисов
systemctl start servisdesk
systemctl restart nginx

# Проверка статуса
systemctl status servisdesk
systemctl status nginx
```

#### Шаг 10: Настройка файрвола
```bash
# Установка UFW
apt install ufw

# Настройка правил
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable
```

## 🔧 Управление системой

### Основные команды:
```bash
# Статус сервиса
systemctl status servisdesk

# Запуск/остановка/перезапуск
systemctl start servisdesk
systemctl stop servisdesk
systemctl restart servisdesk

# Просмотр логов
journalctl -u servisdesk -f

# Перезапуск Nginx
systemctl restart nginx
```

### Создание скрипта управления:
```bash
cat > /usr/local/bin/servisdesk-manage << 'EOF'
#!/bin/bash
case "$1" in
    start) systemctl start servisdesk ;;
    stop) systemctl stop servisdesk ;;
    restart) systemctl restart servisdesk ;;
    status) systemctl status servisdesk ;;
    logs) journalctl -u servisdesk -f ;;
    backup) tar -czf /var/backups/servisdesk/backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/servisdesk ;;
    *) echo "Использование: $0 {start|stop|restart|status|logs|backup}" ;;
esac
EOF

chmod +x /usr/local/bin/servisdesk-manage
```

## 📊 Мониторинг

### Проверка работоспособности:
```bash
# Проверка доступности
curl -I http://192.168.1.100/

# Проверка процессов
ps aux | grep gunicorn
ps aux | grep nginx

# Проверка портов
netstat -tlnp | grep :80
netstat -tlnp | grep :8000
```

### Логи для анализа:
```bash
# Логи приложения
tail -f /var/log/servisdesk/django.log

# Логи Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Логи systemd
journalctl -u servisdesk -f
```

## 🔄 Обновление системы

### Автоматическое обновление:
```bash
# Создание скрипта обновления
cat > /usr/local/bin/servisdesk-update << 'EOF'
#!/bin/bash
cd /opt/servisdesk
systemctl stop servisdesk
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=servisdesk.settings_production
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
systemctl start servisdesk
echo "Обновление завершено"
EOF

chmod +x /usr/local/bin/servisdesk-update
```

### Ручное обновление:
```bash
# Остановка сервиса
systemctl stop servisdesk

# Создание резервной копии
tar -czf /var/backups/servisdesk/backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/servisdesk

# Обновление кода
cd /opt/servisdesk
git pull origin main

# Обновление зависимостей
source venv/bin/activate
pip install -r requirements.txt

# Применение миграций
python manage.py migrate --settings=servisdesk.settings_production

# Сбор статических файлов
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Запуск сервиса
systemctl start servisdesk
```

## 🔐 Безопасность

### Рекомендации:
1. **Измените пароль администратора** после первого входа
2. **Настройте регулярные обновления** системы
3. **Ограничьте доступ** к серверу только из локальной сети
4. **Настройте резервное копирование** базы данных
5. **Мониторьте логи** на предмет подозрительной активности

### Настройка резервного копирования:
```bash
# Создание скрипта резервного копирования
cat > /usr/local/bin/servisdesk-backup << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/servisdesk"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/servisdesk_$DATE.tar.gz"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_FILE /opt/servisdesk --exclude=/opt/servisdesk/venv

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "servisdesk_*.tar.gz" -mtime +30 -delete

echo "Резервная копия создана: $BACKUP_FILE"
EOF

chmod +x /usr/local/bin/servisdesk-backup

# Добавление в cron (ежедневно в 2:00)
echo "0 2 * * * /usr/local/bin/servisdesk-backup" | crontab -
```

## 🌐 Доступ к системе

### URL для доступа:
- **Основной адрес**: http://192.168.1.100
- **Администратор**: admin / admin123

### Пользователи по умолчанию:
- **admin** / admin123 (администратор)
- **ivanov** / user123 (пользователь)
- **petrova** / user123 (пользователь)
- **sidorov** / user123 (пользователь)

## 🆘 Устранение неполадок

### Частые проблемы:

**502 Bad Gateway:**
```bash
systemctl status servisdesk
nginx -t
chown -R servisdesk:servisdesk /opt/servisdesk
```

**Статические файлы не загружаются:**
```bash
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
chown -R servisdesk:servisdesk /opt/servisdesk/staticfiles
```

**Ошибки базы данных:**
```bash
python manage.py migrate --settings=servisdesk.settings_production
python manage.py dbshell --settings=servisdesk.settings_production
```

**Проблемы с правами доступа:**
```bash
chown -R servisdesk:servisdesk /opt/servisdesk
chmod -R 755 /opt/servisdesk
chmod 660 /opt/servisdesk/.env
```

---

**🎉 Система готова к использованию в локальной сети!**
