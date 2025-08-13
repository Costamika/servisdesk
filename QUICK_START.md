# Быстрый запуск сервис-деск системы

## 🚀 Быстрая установка

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Создание администратора
```bash
python setup_admin.py
```

### 4. Создание тестовых данных (опционально)
```bash
python create_test_data.py
```

### 5. Запуск сервера
```bash
# Рекомендуемый способ (с конфигурацией)
./start_server.sh

# Или через Python скрипт
python3 run_server.py

# Или традиционный способ
python manage.py runserver
```

## 🔗 Доступ к системе

- **URL**: http://127.0.0.1:8000/ (или настройте в `config_ip_system.py`)
- **Администратор**: admin / admin123
- **Тестовые пользователи**: ivanov / user123, petrova / user123, sidorov / user123

## ⚙️ Настройка конфигурации

Отредактируйте `config_ip_system.py` для изменения IP и порта:

```python
DEFAULT_HOST = "0.0.0.0"  # IP адрес
DEFAULT_PORT = 8080        # Порт
DEBUG_MODE = True          # Режим отладки
```

## 📋 Основные функции

### Для администраторов:
- Управление пользователями
- Просмотр всех заявок
- Назначение исполнителей
- Изменение статусов заявок

### Для пользователей:
- Создание заявок
- Просмотр своих заявок
- Добавление комментариев
- Редактирование профиля

## 🛠️ Структура проекта

```
servisdesk/
├── manage.py              # Управление Django
├── config_ip_system.py    # Конфигурация IP и порта
├── run_server.py          # Python скрипт запуска
├── start_server.sh        # Bash скрипт запуска
├── requirements.txt       # Зависимости
├── setup_admin.py         # Настройка администратора
├── create_test_data.py    # Создание тестовых данных
├── servisdesk/           # Основной проект
├── users/                # Управление пользователями
├── tickets/              # Управление заявками
├── templates/            # HTML шаблоны
└── static/               # Статические файлы
```

## 🔧 Команды для разработки

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск тестов
python manage.py test

# Сбор статических файлов
python manage.py collectstatic
```

## 📝 Примеры использования

### Создание заявки
1. Войдите в систему
2. Нажмите "Создать заявку"
3. Заполните форму
4. Нажмите "Создать заявку"

### Управление заявками (админ)
1. Перейдите в "Заявки"
2. Выберите заявку
3. Используйте административные действия

### Создание пользователя (админ)
1. Перейдите в "Пользователи"
2. Нажмите "Создать пользователя"
3. Заполните форму
4. Нажмите "Создать пользователя"

## 🐛 Устранение неполадок

### Ошибка "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Ошибка миграций
```bash
python manage.py makemigrations --empty app_name
python manage.py migrate
```

### Проблемы с базой данных
```bash
rm db.sqlite3
python manage.py migrate
python setup_admin.py
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи Django
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки в `servisdesk/settings.py`
