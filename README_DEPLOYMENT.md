# 🚀 Развертывание сервис-деск системы

## 📦 Содержимое пакета

Этот пакет содержит все необходимое для развертывания сервис-деск системы на сервере:

### **Основные файлы:**
- `servisdesk/` - Основные настройки Django
- `users/` - Приложение управления пользователями
- `tickets/` - Приложение управления заявками
- `templates/` - HTML шаблоны
- `static/` - Статические файлы (CSS, JS)
- `manage.py` - Django управляющий скрипт

### **Конфигурационные файлы:**
- `requirements.txt` - Python зависимости
- `env.example` - Пример переменных окружения
- `nginx.conf` - Конфигурация Nginx
- `servisdesk.service` - systemd служба
- `gunicorn.conf.py` - Конфигурация Gunicorn

### **Скрипты развертывания:**
- `deploy_server.sh` - Автоматическое развертывание
- `deploy_local.sh` - Развертывание в локальной сети
- `manage_service.sh` - Управление службой

### **Архивы:**
- `servisdesk-deploy.tar.gz` - Полный архив для развертывания

## 🎯 Быстрое развертывание

### **Вариант 1: Автоматическое развертывание (рекомендуется)**

```bash
# Запустите скрипт развертывания
./deploy_server.sh SERVER_IP USERNAME

# Пример:
./deploy_server.sh 192.168.1.100 admin
```

### **Вариант 2: Ручное развертывание**

```bash
# 1. Подключитесь к серверу
ssh user@server-ip

# 2. Создайте папку для проекта
sudo mkdir -p /opt/servisdesk
sudo chown $USER:$USER /opt/servisdesk
cd /opt/servisdesk

# 3. Скопируйте файлы (с вашего компьютера)
scp -r * user@server-ip:/opt/servisdesk/

# 4. Следуйте инструкции в DEPLOY_SERVER.md
```

## 📋 Требования к серверу

- **ОС**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Python**: 3.8+
- **Память**: минимум 512MB RAM
- **Диск**: минимум 1GB свободного места
- **Сеть**: доступ к интернету для установки пакетов

## 🔧 Настройка системы

### **1. Установка зависимостей**
```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите необходимые пакеты
sudo apt install -y python3 python3-pip python3-venv nginx git curl
```

### **2. Настройка Python окружения**
```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### **3. Настройка переменных окружения**
```bash
# Скопируйте пример конфигурации
cp env.example .env

# Отредактируйте файл .env
nano .env

# Измените следующие строки:
# ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
# SECRET_KEY=your-secret-key-here
```

### **4. Настройка базы данных**
```bash
# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Создайте тестовые данные (опционально)
python create_test_data.py

# Соберите статические файлы
python manage.py collectstatic --noinput
```

### **5. Настройка Nginx**
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

### **6. Настройка systemd**
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

### **7. Настройка файрвола**
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

## 🛠 Управление системой

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

## 📚 Дополнительная документация

- `DEPLOY_SERVER.md` - Подробная инструкция развертывания
- `QUICK_DEPLOY_SERVER.md` - Быстрое развертывание
- `LOCAL_DEPLOYMENT.md` - Развертывание в локальной сети
- `USAGE_EXAMPLE.md` - Примеры использования системы

## 🎉 Готово!

Система успешно развернута и готова к использованию!

**URL**: http://your-server-ip/
**Статус**: ✅ Активна
**Версия**: 1.0.0

---

**Разработано в МИАЦ © 2025**
