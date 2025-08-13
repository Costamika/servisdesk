# 🚀 Инструкция по развертыванию ServisDesk

## 📦 Архив развертывания

**Файл:** `servisdesk_deployment_20250813_120022.tar.gz`  
**Размер:** 76KB  
**Дата создания:** 13 августа 2025

## 🎯 Быстрое развертывание

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Создание пользователя для приложения
sudo useradd -m -s /bin/bash servisdesk
sudo usermod -aG sudo servisdesk
```

### 2. Развертывание приложения

```bash
# Переключение на пользователя приложения
sudo su - servisdesk

# Создание директории для приложения
mkdir -p /home/servisdesk/app
cd /home/servisdesk/app

# Копирование архива на сервер (выполнить на локальной машине)
scp servisdesk_deployment_20250813_120022.tar.gz user@server:/home/servisdesk/app/

# Распаковка архива
tar -xzf servisdesk_deployment_20250813_120022.tar.gz

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python3 manage.py migrate

# Создание суперпользователя
python3 manage.py createsuperuser --username admin --email admin@example.com --noinput
python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()"

# Сбор статических файлов
python3 manage.py collectstatic --noinput
```

### 3. Настройка Nginx

```bash
# Создание конфигурации Nginx
sudo tee /etc/nginx/sites-available/servisdesk << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Замените на ваш домен или IP

    location /static/ {
        alias /home/servisdesk/app/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Активация сайта
sudo ln -s /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Настройка systemd службы

```bash
# Копирование файла службы
sudo cp servisdesk.service /etc/systemd/system/

# Активация службы
sudo systemctl daemon-reload
sudo systemctl enable servisdesk
sudo systemctl start servisdesk

# Проверка статуса
sudo systemctl status servisdesk
```

### 5. Настройка файрвола

```bash
# Открытие портов
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 🔧 Альтернативные способы развертывания

### Docker развертывание

```bash
# Использование Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Автоматическое развертывание

```bash
# Использование скрипта автоматического развертывания
./deploy.sh
```

## 📋 Проверка развертывания

### 1. Проверка доступности

```bash
# Проверка HTTP ответа
curl -I http://your-domain.com

# Проверка логирования
sudo journalctl -u servisdesk -f
```

### 2. Доступ к системе

- **URL:** http://your-domain.com
- **Админ панель:** http://your-domain.com/admin
- **Логин:** admin
- **Пароль:** admin123

## 🔒 Безопасность

### 1. Изменение паролей

```bash
# Изменение пароля администратора
python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('новый_пароль'); u.save()"
```

### 2. Настройка SSL

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com
```

## 📊 Мониторинг

### 1. Логи приложения

```bash
# Просмотр логов службы
sudo journalctl -u servisdesk -f

# Просмотр логов Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Мониторинг ресурсов

```bash
# Проверка использования ресурсов
htop
df -h
free -h
```

## 🆘 Устранение неполадок

### Частые проблемы:

1. **Ошибка 502 Bad Gateway**
   - Проверьте статус службы: `sudo systemctl status servisdesk`
   - Проверьте логи: `sudo journalctl -u servisdesk -f`

2. **Ошибка доступа к статическим файлам**
   - Проверьте права доступа: `sudo chown -R servisdesk:servisdesk /home/servisdesk/app/static/`
   - Перезапустите Nginx: `sudo systemctl restart nginx`

3. **Ошибка базы данных**
   - Примените миграции: `python3 manage.py migrate`
   - Проверьте права доступа к файлу БД

## 📞 Поддержка

- **Документация:** README_DEPLOYMENT.md
- **Быстрый старт:** QUICK_DEPLOY.md
- **Подробное руководство:** DEPLOYMENT.md

---

**Версия:** 1.0.0  
**Дата:** 13 августа 2025  
**Автор:** AI Assistant
