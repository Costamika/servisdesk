# 🚀 ServisDesk v1.1.0 - Полный пакет для GitHub

Этот пакет содержит все необходимые файлы для установки и использования системы ServisDesk.

## 📦 Содержимое пакета

### 🔧 Основные компоненты
- `servisdesk/` - основное Django приложение
- `tickets/` - модуль управления заявками
- `users/` - модуль управления пользователями
- `templates/` - HTML шаблоны
- `static/` - статические файлы (CSS, JS)

### ⚙️ Конфигурация
- `config_ip_system.py` - система конфигурации IP
- `requirements.txt` - зависимости Python
- `env.example` - пример переменных окружения
- `gunicorn.conf.py` - конфигурация Gunicorn
- `nginx.conf` - конфигурация Nginx
- `docker-compose.yml` - Docker Compose
- `Dockerfile` - Docker образ

### 🚀 Скрипты развертывания
- `deploy.sh` - основной скрипт развертывания
- `deploy_server.sh` - развертывание на сервер
- `deploy_local.sh` - локальное развертывание
- `start_server.sh` - запуск сервера
- `run_server.py` - Python скрипт запуска
- `manage_service.sh` - управление сервисом

### 📚 Документация
- `README.md` - основное руководство
- `QUICK_START.md` - быстрое начало
- `DEPLOYMENT.md` - руководство по развертыванию
- `CODE_QUALITY_GUIDE.md` - качество кода
- `CONFIGURATION_GUIDE.md` - настройка системы
- `USAGE_EXAMPLE.md` - примеры использования

## 🚀 Быстрый старт

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер
./start_server.sh
```

## 🔧 Настройка

```bash
# Настройте IP адрес и порт
python3 config_ip_system.py
```

## 📊 Системные требования

- **Python:** 3.8+
- **Django:** 5.2.5
- **Память:** 512MB
- **Диск:** 1GB
- **ОС:** Ubuntu 20.04+, Debian 11+, CentOS 8+

## 🔒 Безопасность

- ✅ Анализ уязвимостей с помощью Bandit
- ✅ Проверка качества кода с помощью Pylint
- ✅ Отчёты безопасности включены

---

**ServisDesk v1.1.0** - Готов к использованию! 🚀
