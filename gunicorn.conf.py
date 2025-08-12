"""
Конфигурация Gunicorn для сервис-деск системы
"""

import multiprocessing
import os

# Базовые настройки
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
workers = os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = os.environ.get('GUNICORN_WORKER_CONNECTIONS', 1000)
max_requests = os.environ.get('GUNICORN_MAX_REQUESTS', 1000)
max_requests_jitter = os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 100)

# Таймауты
timeout = os.environ.get('GUNICORN_TIMEOUT', 30)
keepalive = os.environ.get('GUNICORN_KEEPALIVE', 2)
graceful_timeout = os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', 30)

# Логирование
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Безопасность
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Перезагрузка
reload = os.environ.get('GUNICORN_RELOAD', 'false').lower() == 'true'
reload_engine = 'auto'

# Имя процесса
proc_name = 'servisdesk'

# Пользователь и группа (раскомментировать при необходимости)
# user = 'www-data'
# group = 'www-data'

# Предзагрузка приложения
preload_app = True

def when_ready(server):
    """Вызывается когда сервер готов к работе"""
    server.log.info("Сервер готов к работе")

def worker_int(worker):
    """Вызывается при получении сигнала INT рабочим процессом"""
    worker.log.info("Рабочий процесс получил сигнал INT")

def pre_fork(server, worker):
    """Вызывается перед форком рабочего процесса"""
    server.log.info("Форк рабочего процесса")

def post_fork(server, worker):
    """Вызывается после форка рабочего процесса"""
    server.log.info("Рабочий процесс создан")

def post_worker_init(worker):
    """Вызывается после инициализации рабочего процесса"""
    worker.log.info("Рабочий процесс инициализирован")
