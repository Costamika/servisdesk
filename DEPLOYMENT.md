# Руководство по развертыванию сервис-деск системы

## 🚀 Способы развертывания

### 1. Классическое развертывание на сервере

#### Требования к серверу:
- Ubuntu 20.04+ или CentOS 8+
- Python 3.8+
- Nginx
- PostgreSQL (опционально)
- 2GB RAM минимум
- 10GB свободного места

#### Пошаговое развертывание:

##### Шаг 1: Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# Создание пользователя для приложения
sudo useradd -r -s /bin/false www-data
```

##### Шаг 2: Загрузка проекта
```bash
# Клонирование репозитория
git clone <repository-url> /var/www/servisdesk
cd /var/www/servisdesk

# Настройка прав доступа
sudo chown -R www-data:www-data /var/www/servisdesk
```

##### Шаг 3: Настройка виртуального окружения
```bash
# Создание виртуального окружения
sudo -u www-data python3 -m venv venv

# Активация и установка зависимостей
source venv/bin/activate
pip install -r requirements.txt
```

##### Шаг 4: Настройка базы данных
```bash
# Для SQLite (по умолчанию)
python manage.py migrate --settings=servisdesk.settings_production

# Для PostgreSQL
sudo -u postgres createdb servisdesk
sudo -u postgres createuser servisdesk
sudo -u postgres psql -c "ALTER USER servisdesk PASSWORD 'your_password';"
```

##### Шаг 5: Настройка переменных окружения
```bash
# Копирование примера
cp env.example .env

# Редактирование файла
nano .env
```

##### Шаг 6: Сбор статических файлов
```bash
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
```

##### Шаг 7: Настройка systemd сервиса
```bash
# Копирование файла сервиса
sudo cp servisdesk.service /etc/systemd/system/

# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable servisdesk
```

##### Шаг 8: Настройка Nginx
```bash
# Копирование конфигурации
sudo cp nginx.conf /etc/nginx/sites-available/servisdesk

# Создание символической ссылки
sudo ln -s /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/

# Удаление дефолтной конфигурации
sudo rm /etc/nginx/sites-enabled/default

# Проверка конфигурации
sudo nginx -t

# Перезапуск Nginx
sudo systemctl restart nginx
```

##### Шаг 9: Запуск сервисов
```bash
# Запуск приложения
sudo systemctl start servisdesk

# Проверка статуса
sudo systemctl status servisdesk
```

### 2. Развертывание с помощью Docker

#### Требования:
- Docker
- Docker Compose

#### Пошаговое развертывание:

##### Шаг 1: Подготовка файлов
```bash
# Клонирование репозитория
git clone <repository-url> servisdesk
cd servisdesk

# Создание .env файла
cp env.example .env
nano .env
```

##### Шаг 2: Сборка и запуск
```bash
# Сборка образов
docker-compose build

# Запуск сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

##### Шаг 3: Применение миграций
```bash
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Применение миграций
docker-compose exec web python manage.py migrate
```

### 3. Автоматическое развертывание

#### Использование скрипта deploy.sh:
```bash
# Сделать скрипт исполняемым
chmod +x deploy.sh

# Запуск развертывания
./deploy.sh production
```

## 🔧 Настройка безопасности

### 1. SSL сертификат (Let's Encrypt)
```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить строку: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Настройка файрвола
```bash
# Установка UFW
sudo apt install ufw

# Настройка правил
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 3. Настройка резервного копирования
```bash
# Создание скрипта резервного копирования
sudo nano /usr/local/bin/backup-servisdesk.sh

# Добавление в cron
sudo crontab -e
# Добавить строку: 0 2 * * * /usr/local/bin/backup-servisdesk.sh
```

## 📊 Мониторинг и логирование

### 1. Настройка логирования
```bash
# Создание директории для логов
sudo mkdir -p /var/log/servisdesk

# Настройка ротации логов
sudo nano /etc/logrotate.d/servisdesk
```

### 2. Мониторинг системы
```bash
# Установка htop для мониторинга
sudo apt install htop

# Установка netdata для веб-мониторинга
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

## 🔄 Обновление системы

### 1. Автоматическое обновление
```bash
# Использование скрипта управления
./manage_service.sh update
```

### 2. Ручное обновление
```bash
# Остановка сервиса
sudo systemctl stop servisdesk

# Создание резервной копии
./manage_service.sh backup

# Обновление кода
git pull origin main

# Обновление зависимостей
source venv/bin/activate
pip install -r requirements.txt

# Применение миграций
python manage.py migrate --settings=servisdesk.settings_production

# Сбор статических файлов
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Запуск сервиса
sudo systemctl start servisdesk
```

## 🛠️ Устранение неполадок

### 1. Проверка статуса сервисов
```bash
# Статус systemd сервисов
sudo systemctl status servisdesk
sudo systemctl status nginx

# Проверка портов
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :8000
```

### 2. Просмотр логов
```bash
# Логи systemd
sudo journalctl -u servisdesk -f

# Логи Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Логи приложения
sudo tail -f /var/log/servisdesk/django.log
```

### 3. Частые проблемы

#### Проблема: 502 Bad Gateway
```bash
# Проверка статуса Gunicorn
sudo systemctl status servisdesk

# Проверка конфигурации Nginx
sudo nginx -t

# Проверка прав доступа
sudo chown -R www-data:www-data /var/www/servisdesk
```

#### Проблема: Статические файлы не загружаются
```bash
# Пересборка статических файлов
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# Проверка прав доступа
sudo chown -R www-data:www-data /var/www/servisdesk/staticfiles
```

#### Проблема: Ошибки базы данных
```bash
# Проверка подключения к базе данных
python manage.py dbshell --settings=servisdesk.settings_production

# Применение миграций
python manage.py migrate --settings=servisdesk.settings_production
```

## 📈 Масштабирование

### 1. Горизонтальное масштабирование
```bash
# Настройка балансировщика нагрузки
sudo apt install haproxy

# Конфигурация HAProxy
sudo nano /etc/haproxy/haproxy.cfg
```

### 2. Вертикальное масштабирование
```bash
# Увеличение количества воркеров Gunicorn
# Редактирование gunicorn.conf.py
workers = 8  # Вместо 4
```

### 3. Кеширование
```bash
# Установка Redis
sudo apt install redis-server

# Настройка кеширования в Django
# Редактирование settings_production.py
```

## 🔐 Безопасность

### 1. Регулярные обновления
```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 2. Мониторинг безопасности
```bash
# Установка fail2ban
sudo apt install fail2ban

# Настройка правил
sudo nano /etc/fail2ban/jail.local
```

### 3. Аудит безопасности
```bash
# Проверка открытых портов
sudo nmap localhost

# Проверка процессов
sudo ps aux | grep -E "(nginx|gunicorn|postgres)"
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `./manage_service.sh logs`
2. Проверьте статус сервисов: `./manage_service.sh status`
3. Создайте резервную копию: `./manage_service.sh backup`
4. Обратитесь к документации Django
5. Создайте issue в репозитории проекта
