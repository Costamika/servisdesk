# 🚀 Сервис-деск система

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

Полнофункциональная система управления заявками (тикетами) с ролями администратора и пользователя, разработанная на Django.

## 🌟 Особенности

- ✅ **Двухролевая система**: Администраторы и пользователи
- ✅ **Управление заявками**: Создание, редактирование, удаление
- ✅ **Система комментариев**: Внутренние и публичные комментарии
- ✅ **Назначение исполнителей**: Администраторы могут назначать исполнителей
- ✅ **Отслеживание статусов**: Новые, в работе, решены, закрыты, отменены
- ✅ **Приоритеты**: Низкий, средний, высокий, критический
- ✅ **Современный UI**: Bootstrap 5 интерфейс
- ✅ **Гибкая конфигурация**: Настройка IP и порта через файл конфигурации
- ✅ **Умные скрипты запуска**: Автоматические проверки и цветной вывод
- ✅ **Готовность к продакшну**: Nginx + Gunicorn + systemd
- ✅ **Автоматическое развертывание**: Скрипты для быстрого деплоя

## 🚀 Быстрое развертывание

### **Локальная разработка**

```bash
# Клонируйте репозиторий
git clone https://github.com/your-username/servisdesk.git
cd servisdesk

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер (новый способ с конфигурацией)
./start_server.sh

# Или через Python скрипт
python3 run_server.py

# Или традиционный способ
python manage.py runserver
```

### **Продакшн развертывание**

```bash
# Автоматическое развертывание
./deploy_server.sh SERVER_IP USERNAME

# Пример:
./deploy_server.sh 192.168.1.100 admin
```

## 📋 Возможности системы

### **Для администраторов:**
- 🔧 Создание и управление пользователями
- 📊 Просмотр всех заявок в системе
- 👥 Назначение исполнителей заявок
- 🔄 Изменение статусов заявок
- 🗑️ Удаление заявок
- ✏️ Редактирование профилей пользователей
- ✅ Активация/деактивация пользователей

### **Для пользователей:**
- ➕ Создание новых заявок
- 📋 Просмотр своих заявок
- 💬 Добавление комментариев к заявкам
- 👤 Редактирование собственного профиля
- 📈 Отслеживание статуса заявок

## 🌐 Демо

После развертывания система будет доступна по адресу:
```
http://your-server-ip/
```

**Тестовые данные:**
- **Администратор**: `admin` / `admin123`
- **Пользователи**: `ivanov` / `user123`, `petrova` / `user123`, `sidorov` / `user123`

## ⚙️ Система конфигурации

ServisDesk поддерживает гибкую настройку IP адреса и порта через конфигурационный файл.

### **Настройка конфигурации**

Отредактируйте файл `config_ip_system.py`:

```python
# IP адрес для запуска сервера
DEFAULT_HOST = "0.0.0.0"  # Доступ со всех интерфейсов

# Порт для запуска сервера
DEFAULT_PORT = 8080  # Измените на нужный порт

# Режим отладки
DEBUG_MODE = True  # True для разработки, False для продакшена
```

### **Способы запуска**

```bash
# 1. Через bash скрипт (рекомендуется)
./start_server.sh

# 2. Через Python скрипт с переопределением
python3 run_server.py --host 127.0.0.1 --port 9000

# 3. Традиционный способ Django
python3 manage.py runserver 0.0.0.0:8080
```

### **Примеры конфигураций**

**Для локальной разработки:**
```python
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEBUG_MODE = True
```

**Для доступа из сети:**
```python
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
DEBUG_MODE = True
```

**Для продакшена:**
```python
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 9000
DEBUG_MODE = False
```

📖 **Подробная документация**: [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md)

## 📁 Структура проекта

```
servisdesk/
├── servisdesk/              # Основные настройки Django
├── users/                   # Приложение управления пользователями
├── tickets/                 # Приложение управления заявками
├── templates/               # HTML шаблоны
├── static/                  # Статические файлы (CSS, JS)
├── config_ip_system.py      # Конфигурация IP и порта
├── run_server.py            # Python скрипт запуска
├── start_server.sh          # Bash скрипт запуска
├── manage.py                # Django управляющий скрипт
├── requirements.txt         # Python зависимости
├── deploy_server.sh         # Автоматическое развертывание
├── nginx.conf               # Конфигурация Nginx
├── servisdesk.service       # systemd служба
├── gunicorn.conf.py         # Конфигурация Gunicorn
├── create_test_data.py      # Создание тестовых данных
├── setup_admin.py           # Настройка администратора
└── README.md                # Документация
```

## 🔧 Технологии

- **Backend**: [Django 5.2.5](https://www.djangoproject.com/)
- **Database**: SQLite (можно заменить на PostgreSQL)
- **Frontend**: HTML, CSS, [Bootstrap 5](https://getbootstrap.com/)
- **Server**: [Nginx](https://nginx.org/) + [Gunicorn](https://gunicorn.org/)
- **Process Manager**: systemd
- **Forms**: [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)

## 📋 Системные требования

- **ОС**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Python**: 3.8+
- **Память**: 512MB RAM
- **Диск**: 1GB свободного места
- **Сеть**: доступ к интернету

## 🛠 Управление системой

### **Локальная разработка:**
```bash
# Запуск (рекомендуется)
./start_server.sh

# Или через Python скрипт
python3 run_server.py

# Или традиционный способ
python manage.py runserver

# Остановка
Ctrl+C
```

### **Продакшн:**
```bash
# Остановить систему
sudo systemctl stop servisdesk

# Запустить систему
sudo systemctl start servisdesk

# Перезапустить систему
sudo systemctl restart servisdesk

# Посмотреть логи
sudo journalctl -u servisdesk -f
```

## 📚 Документация

- [📖 Подробная инструкция развертывания](DEPLOY_SERVER.md)
- [⚡ Быстрое развертывание](QUICK_DEPLOY_SERVER.md)
- [🏠 Локальная сеть](LOCAL_DEPLOYMENT.md)
- [⚙️ Руководство по конфигурации](CONFIGURATION_GUIDE.md)
- [📝 Примеры использования](USAGE_EXAMPLE.md)
- [📁 Обзор файлов проекта](FILES_OVERVIEW.md)

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, ознакомьтесь с нашими рекомендациями:

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 🐛 Сообщить об ошибке

Если вы нашли ошибку, пожалуйста, создайте issue в репозитории с подробным описанием проблемы.

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

## 👨‍💻 Авторы

- **МИАЦ** - *Начальная разработка* - [GitHub](https://github.com/your-username)

## 🙏 Благодарности

- [Django](https://www.djangoproject.com/) - за отличный веб-фреймворк
- [Bootstrap](https://getbootstrap.com/) - за красивые стили
- [Gunicorn](https://gunicorn.org/) - за WSGI сервер
- [Nginx](https://nginx.org/) - за веб-сервер

---

**⭐ Если этот проект вам понравился, поставьте звездочку!**

**🎉 Система готова к использованию!**
