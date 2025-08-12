# 🚀 Развертывание сервис-деск системы на сервере

## 📋 Требования к серверу

- **ОС**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Python**: 3.8+
- **Память**: минимум 512MB RAM
- **Диск**: минимум 1GB свободного места
- **Сеть**: доступ к интернету для установки пакетов

## 🎯 Быстрое развертывание

### **Шаг 1: Подготовка сервера**

```bash
# Подключитесь к серверу по SSH
ssh user@your-server-ip

# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите необходимые пакеты
sudo apt install -y python3 python3-pip python3-venv nginx git curl
```

### **Шаг 2: Создание папки и копирование файлов**

```bash
# Создайте папку для проекта
sudo mkdir -p /opt/servisdesk
sudo chown $USER:$USER /opt/servisdesk
cd /opt/servisdesk

# Скопируйте архив на сервер (с вашего компьютера)
scp servisdesk-deploy.tar.gz user@your-server-ip:/opt/servisdesk/

# Распакуйте архив
tar -xzf servisdesk-deploy.tar.gz
```

### **Шаг 3: Настройка и запуск**

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Настройте переменные окружения
cp env.example .env
nano .env

# Измените в файле .env:
# ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
# SECRET_KEY=your-secret-key-here

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Соберите статические файлы
python manage.py collectstatic --noinput

# Создайте тестовые данные (опционально)
python create_test_data.py
```

### **Шаг 4: Настройка Nginx**

```bash
# Скопируйте конфигурацию Nginx
sudo cp nginx.conf /etc/nginx/sites-available/servisdesk

# Создайте символическую ссылку
sudo ln -s /etc/nginx/sites-available/servisdesk /etc/nginx/sites-enabled/

# Удалите дефолтный сайт
sudo rm /etc/nginx/sites-enabled/default

# Проверьте конфигурацию
sudo nginx -t

# Перезапустите Nginx
sudo systemctl restart nginx
```

### **Шаг 5: Настройка systemd**

```bash
# Скопируйте файл службы
sudo cp servisdesk.service /etc/systemd/system/

# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable servisdesk

# Запустите службу
sudo systemctl start servisdesk

# Проверьте статус
sudo systemctl status servisdesk
```

### **Шаг 6: Настройка файрвола**

```bash
# Откройте порты
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# Включите файрвол
sudo ufw enable
```

## 🌐 Доступ к системе

После завершения установки система будет доступна по адресу:
```
http://your-server-ip/
```

**Данные для входа:**
- **Администратор**: созданный вами суперпользователь
- **Тестовые пользователи**: `ivanov` / `user123`, `petrova` / `user123`, `sidorov` / `user123`

## 🔧 Управление системой

```bash
# Остановить систему
sudo systemctl stop servisdesk

# Запустить систему
sudo systemctl start servisdesk

# Перезапустить систему
sudo systemctl restart servisdesk

# Посмотреть логи
sudo journalctl -u servisdesk -f

# Обновить систему
cd /opt/servisdesk
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart servisdesk
```

## 📝 Настройка IP адреса

Если нужно изменить IP адрес, отредактируйте файлы:

1. **servisdesk/settings.py**:
```python
ALLOWED_HOSTS = ['your-new-ip', 'localhost', '127.0.0.1']
```

2. **nginx.conf**:
```nginx
server_name your-new-ip;
```

3. **servisdesk.service**:
```ini
Environment="ALLOWED_HOSTS=your-new-ip"
```

После изменений перезапустите службы:
```bash
sudo systemctl restart servisdesk
sudo systemctl restart nginx
```

## 🆘 Устранение неполадок

### **Проблема: Система не запускается**
```bash
# Проверьте логи
sudo journalctl -u servisdesk -f

# Проверьте права доступа
sudo chown -R www-data:www-data /opt/servisdesk
```

### **Проблема: Nginx не работает**
```bash
# Проверьте конфигурацию
sudo nginx -t

# Проверьте логи
sudo tail -f /var/log/nginx/error.log
```

### **Проблема: База данных**
```bash
# Создайте новую базу
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🎉 Готово!

Система успешно развернута и готова к использованию!

**URL**: http://your-server-ip/
**Статус**: ✅ Активна
**Версия**: 1.0.0
