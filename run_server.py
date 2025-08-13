#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска Django сервера с настройками из конфигурационного файла

Использование:
    python3 run_server.py
    python3 run_server.py --host 127.0.0.1 --port 8080
    python3 run_server.py --config custom_config.py
"""

import os
import sys
import argparse
from pathlib import Path

# Добавляем корневую директорию проекта в путь
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

def load_config(config_file="config_ip_system.py"):
    """Загружает конфигурацию из файла"""
    try:
        # Импортируем конфигурацию
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_file)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        return {
            'host': getattr(config, 'DEFAULT_HOST', '0.0.0.0'),
            'port': getattr(config, 'DEFAULT_PORT', 8000),
            'server_address': getattr(config, 'SERVER_ADDRESS', '0.0.0.0:8000'),
            'debug': getattr(config, 'DEBUG_MODE', True)
        }
    except ImportError as e:
        print(f"⚠️  Ошибка загрузки конфигурации: {e}")
        print("📁 Используются значения по умолчанию")
        return {
            'host': '0.0.0.0',
            'port': 8000,
            'server_address': '0.0.0.0:8000',
            'debug': True
        }

def check_django_ready():
    """Проверяет готовность Django к запуску"""
    try:
        import django
        from django.core.management import execute_from_command_line
        from django.core.management.base import CommandError
        
        # Проверяем настройки Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servisdesk.settings')
        django.setup()
        
        # Проверяем миграции
        from django.core.management import call_command
        try:
            call_command('check', verbosity=0)
            return True
        except CommandError as e:
            print(f"❌ Ошибка проверки Django: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Django не установлен: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка инициализации Django: {e}")
        return False

def main():
    """Основная функция запуска сервера"""
    parser = argparse.ArgumentParser(description='Запуск Django сервера ServisDesk')
    parser.add_argument('--host', help='IP адрес для запуска сервера')
    parser.add_argument('--port', type=int, help='Порт для запуска сервера')
    parser.add_argument('--config', default='config_ip_system.py', 
                       help='Путь к файлу конфигурации')
    
    args = parser.parse_args()
    
    print("🚀 Запуск ServisDesk...")
    print("=" * 50)
    
    # Загружаем конфигурацию
    config = load_config(args.config)
    
    # Переопределяем настройки аргументами командной строки
    if args.host:
        config['host'] = args.host
    if args.port:
        config['port'] = args.port
    
    config['server_address'] = f"{config['host']}:{config['port']}"
    
    print(f"📋 Конфигурация:")
    print(f"   🏠 Хост: {config['host']}")
    print(f"   🔌 Порт: {config['port']}")
    print(f"   🌐 Адрес: {config['server_address']}")
    print(f"   🐛 Режим отладки: {'Включен' if config['debug'] else 'Выключен'}")
    print("=" * 50)
    
    # Проверяем готовность Django
    if not check_django_ready():
        print("❌ Django не готов к запуску")
        sys.exit(1)
    
    print("✅ Django готов к запуску")
    print("🔄 Запуск сервера разработки...")
    print("=" * 50)
    
    # Запускаем сервер
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line([
            'manage.py', 
            'runserver', 
            config['server_address']
        ])
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
