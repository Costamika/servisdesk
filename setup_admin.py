#!/usr/bin/env python
"""
Скрипт для настройки пароля администратора
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servisdesk.settings')
django.setup()

from django.contrib.auth.models import User

def setup_admin_password():
    """Устанавливает пароль для пользователя admin"""
    try:
        admin_user = User.objects.get(username='admin')
        password = 'admin123'  # Простой пароль для демонстрации
        
        admin_user.set_password(password)
        admin_user.save()
        
        print(f"✅ Пароль для пользователя 'admin' установлен: {password}")
        print("🔗 Войдите в систему по адресу: http://127.0.0.1:8000/")
        print("👤 Логин: admin")
        print("🔑 Пароль: admin123")
        
    except User.DoesNotExist:
        print("❌ Пользователь 'admin' не найден. Создайте его командой:")
        print("python manage.py createsuperuser --username admin --email admin@example.com")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    setup_admin_password()
