# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=servisdesk.settings_production

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        curl \
        nginx \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для запуска приложения
RUN useradd --create-home --shell /bin/bash servisdesk

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем необходимые директории
RUN mkdir -p /app/logs /app/media /app/staticfiles /var/log/servisdesk

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Применяем миграции
RUN python manage.py migrate

# Настраиваем права доступа
RUN chown -R servisdesk:servisdesk /app /var/log/servisdesk

# Копируем конфигурации
COPY docker/nginx.conf /etc/nginx/sites-available/default
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/gunicorn.conf.py /app/gunicorn.conf.py

# Открываем порт
EXPOSE 80

# Переключаемся на пользователя servisdesk
USER servisdesk

# Запускаем supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
