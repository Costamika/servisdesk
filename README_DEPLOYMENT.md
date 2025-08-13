# 🚀 Быстрое развертывание сервис-деск системы

## 📋 Что подготовлено

✅ **Production настройки Django** - `servisdesk/settings_production.py`  
✅ **WSGI конфигурация** - `servisdesk/wsgi_production.py`  
✅ **Gunicorn конфигурация** - `gunicorn.conf.py`  
✅ **Systemd сервис** - `servisdesk.service`  
✅ **Nginx конфигурация** - `nginx.conf`  
✅ **Docker поддержка** - `Dockerfile`, `docker-compose.yml`  
✅ **Скрипты автоматизации** - `deploy.sh`, `manage_service.sh`  
✅ **Переменные окружения** - `env.example`  
✅ **Документация** - `DEPLOYMENT.md`  

## 🎯 Быстрый старт

### Вариант 1: Автоматическое развертывание
```bash
# Сделать скрипт исполняемым
chmod +x deploy.sh

# Запустить развертывание
./deploy.sh production
```

### Вариант 2: Docker развертывание
```bash
# Создать .env файл
cp env.example .env
nano .env

# Запустить контейнеры
docker-compose up -d
```

### Вариант 3: Ручное развертывание
```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Настроить переменные окружения
cp env.example .env
nano .env

# 3. Применить миграции
python manage.py migrate --settings=servisdesk.settings_production

# 4. Собрать статические файлы
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# 5. Запустить с Gunicorn
gunicorn --config gunicorn.conf.py servisdesk.wsgi_production:application
```

## 🔧 Управление сервисом

```bash
# Статус сервиса
./manage_service.sh status

# Просмотр логов
./manage_service.sh logs

# Создание резервной копии
./manage_service.sh backup

# Обновление приложения
./manage_service.sh update

# Django shell
./manage_service.sh shell
```

## 🌐 Настройка домена

1. **Измените домен в конфигурациях:**
   - `nginx.conf` - замените `your-domain.com`
   - `servisdesk.service` - обновите `ALLOWED_HOSTS`
   - `env.example` - настройте переменные

2. **Настройте DNS записи:**
   ```
   A    your-domain.com    → IP_ВАШЕГО_СЕРВЕРА
   A    www.your-domain.com → IP_ВАШЕГО_СЕРВЕРА
   ```

3. **Получите SSL сертификат:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## 🔐 Безопасность

### Обязательные настройки:
- ✅ Измените `SECRET_KEY` в `.env`
- ✅ Настройте `ALLOWED_HOSTS`
- ✅ Включите HTTPS
- ✅ Настройте файрвол
- ✅ Регулярные обновления

### Рекомендуемые настройки:
- 🔒 PostgreSQL вместо SQLite
- 🔒 Redis для кеширования
- 🔒 Мониторинг и логирование
- 🔒 Резервное копирование

## 📊 Мониторинг

### Проверка работоспособности:
```bash
# Статус сервисов
sudo systemctl status servisdesk nginx

# Проверка портов
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :8000

# Логи в реальном времени
sudo journalctl -u servisdesk -f
```

### Метрики производительности:
- Количество активных пользователей
- Время отклика сервера
- Использование ресурсов
- Количество заявок

## 🔄 Обновления

### Автоматическое обновление:
```bash
./manage_service.sh update
```

### Ручное обновление:
```bash
# 1. Остановить сервис
sudo systemctl stop servisdesk

# 2. Создать резервную копию
./manage_service.sh backup

# 3. Обновить код
git pull origin main

# 4. Обновить зависимости
pip install -r requirements.txt

# 5. Применить миграции
python manage.py migrate --settings=servisdesk.settings_production

# 6. Собрать статические файлы
python manage.py collectstatic --noinput --settings=servisdesk.settings_production

# 7. Запустить сервис
sudo systemctl start servisdesk
```

## 🆘 Устранение неполадок

### Частые проблемы:

**502 Bad Gateway:**
```bash
sudo systemctl status servisdesk
sudo nginx -t
sudo chown -R www-data:www-data /var/www/servisdesk
```

**Статические файлы не загружаются:**
```bash
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
sudo chown -R www-data:www-data /var/www/servisdesk/staticfiles
```

**Ошибки базы данных:**
```bash
python manage.py migrate --settings=servisdesk.settings_production
python manage.py dbshell --settings=servisdesk.settings_production
```

## 📞 Поддержка

### Полезные команды:
```bash
# Полная диагностика
./manage_service.sh status
./manage_service.sh logs

# Резервное копирование
./manage_service.sh backup

# Восстановление
./manage_service.sh restore backup_file.tar.gz
```

### Логи для анализа:
- `/var/log/servisdesk/django.log` - логи приложения
- `/var/log/nginx/error.log` - ошибки Nginx
- `sudo journalctl -u servisdesk` - логи systemd

### Контакты:
- 📧 Создайте issue в репозитории
- 📖 Изучите `DEPLOYMENT.md` для подробной информации
- 🔍 Проверьте документацию Django

---

**🎉 Система готова к развертыванию!**

Выберите подходящий способ развертывания и следуйте инструкциям выше.
