# Руководство по улучшению качества кода ServisDesk

## Обзор

Этот документ содержит инструкции по улучшению качества кода Django проекта ServisDesk в соответствии со стандартами PEP 8 и лучшими практиками Python.

## Быстрый старт

### 1. Автоматическое исправление

Для автоматического исправления большинства проблем запустите:

```bash
python fix_code_quality.py
```

Этот скрипт:
- Создаст резервную копию
- Установит необходимые инструменты
- Исправит форматирование
- Удалит неиспользуемые импорты
- Проверит безопасность

### 2. Ручное исправление

Если вы предпочитаете ручное исправление:

```bash
# Установка инструментов
pip install black isort autoflake bandit flake8 pylint ruff

# Форматирование кода
black tickets/ users/ servisdesk/ --line-length=88

# Сортировка импортов
isort tickets/ users/ servisdesk/

# Удаление неиспользуемых импортов
autoflake --in-place --remove-all-unused-imports --recursive tickets/ users/ servisdesk/

# Проверка безопасности
bandit -r tickets/ users/ servisdesk/
```

## Найденные проблемы

### Критические проблемы

1. **Хардкодированный секретный ключ** (`servisdesk/settings.py:23`)
   - **Риск**: Низкий (ключ для разработки)
   - **Решение**: Использовать переменные окружения

2. **374 нарушения стиля кода**
   - Длинные строки (56)
   - Лишние пробелы (244)
   - Неиспользуемые импорты (36)
   - Неправильные импорты (10)

### Проблемы архитектуры

1. **Дублирование кода** в миграциях и представлениях
2. **Слишком много предков** у `CustomUserCreationForm`
3. **Слишком мало публичных методов** у моделей

## Конфигурационные файлы

### setup.cfg
Настройки для flake8 с игнорированием Django-специфичных проблем.

### .pylintrc
Настройки для pylint с отключением ложных срабатываний для Django.

### pyproject.toml
Настройки для всех инструментов форматирования и анализа.

## Рекомендации по улучшению

### 1. Настройка pre-commit hooks

Создайте `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, .]
```

Установите и настройте:

```bash
pip install pre-commit
pre-commit install
```

### 2. Добавление тестов

Создайте тесты для всех представлений и моделей:

```python
# tickets/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Ticket

class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        
    def test_ticket_list_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, 200)
```

### 3. Улучшение безопасности

1. **Переменные окружения**
   Создайте `.env` файл:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Обновите settings.py**:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
   DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
   ```

### 4. Документация

Добавьте docstrings ко всем функциям:

```python
def ticket_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список заявок.
    
    Для администраторов показывает все заявки, для обычных пользователей
    только их собственные заявки.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HTTP ответ с отрендеренным шаблоном
    """
```

## Мониторинг качества кода

### Ежедневные проверки

```bash
# Быстрая проверка
flake8 tickets/ users/ servisdesk/ --count

# Полная проверка
python fix_code_quality.py
```

### CI/CD интеграция

Добавьте в ваш CI/CD pipeline:

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install black isort flake8 bandit
      - name: Check code formatting
        run: black --check tickets/ users/ servisdesk/
      - name: Check import sorting
        run: isort --check-only tickets/ users/ servisdesk/
      - name: Lint with flake8
        run: flake8 tickets/ users/ servisdesk/
      - name: Security check with bandit
        run: bandit -r tickets/ users/ servisdesk/
```

## Приоритеты исправления

### Высокий приоритет (выполнить немедленно)
1. ✅ Исправить форматирование (Black + isort)
2. ✅ Удалить неиспользуемые импорты
3. ✅ Исправить пробелы и отступы
4. ⏳ Вынести секретный ключ в переменные окружения

### Средний приоритет (выполнить в течение недели)
1. ⏳ Добавить тесты
2. ⏳ Рефакторинг дублированного кода
3. ⏳ Улучшить документацию
4. ⏳ Настроить CI/CD

### Низкий приоритет (выполнить в течение месяца)
1. ⏳ Оптимизация запросов к БД
2. ⏳ Добавление кэширования
3. ⏳ Улучшение UI/UX

## Полезные команды

### Проверка качества
```bash
# Flake8
flake8 tickets/ users/ servisdesk/ --count --statistics

# Pylint
pylint tickets/ users/ servisdesk/ --output-format=text

# Bandit
bandit -r tickets/ users/ servisdesk/ -f json

# Ruff
ruff check tickets/ users/ servisdesk/
```

### Форматирование
```bash
# Black
black tickets/ users/ servisdesk/ --line-length=88

# isort
isort tickets/ users/ servisdesk/

# autoflake
autoflake --in-place --remove-all-unused-imports --recursive tickets/ users/ servisdesk/
```

### Тестирование
```bash
# Запуск тестов
python manage.py test

# Покрытие кода
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Заключение

После применения всех рекомендаций:

1. **Оценка Pylint** должна улучшиться с 5.52/10 до 8.5+/10
2. **Количество нарушений flake8** должно уменьшиться с 374 до <50
3. **Код станет более читаемым** и поддерживаемым
4. **Безопасность улучшится** за счет использования переменных окружения
5. **Тестирование станет обязательным** для новых функций

Регулярно запускайте проверки качества кода и поддерживайте высокие стандарты в проекте.
