#!/usr/bin/env python
"""
Скрипт для создания тестовых данных
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servisdesk.settings')
django.setup()

from django.contrib.auth.models import User
from tickets.models import Ticket, TicketComment
from users.models import UserProfile

def create_test_users():
    """Создает тестовых пользователей"""
    users_data = [
        {
            'username': 'ivanov',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivanov@example.com',
            'password': 'user123',
            'department': 'IT отдел',
            'position': 'Программист',
            'phone': '+7-999-123-45-67'
        },
        {
            'username': 'petrova',
            'first_name': 'Мария',
            'last_name': 'Петрова',
            'email': 'petrova@example.com',
            'password': 'user123',
            'department': 'Бухгалтерия',
            'position': 'Бухгалтер',
            'phone': '+7-999-234-56-78'
        },
        {
            'username': 'sidorov',
            'first_name': 'Алексей',
            'last_name': 'Сидоров',
            'email': 'sidorov@example.com',
            'password': 'user123',
            'department': 'Отдел продаж',
            'position': 'Менеджер',
            'phone': '+7-999-345-67-89'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            # Обновляем профиль
            profile = user.profile
            profile.department = user_data['department']
            profile.position = user_data['position']
            profile.phone = user_data['phone']
            profile.save()
            
            created_users.append(user)
            print(f"✅ Создан пользователь: {user.get_full_name()} ({user.username})")
        else:
            print(f"⚠️  Пользователь {user_data['username']} уже существует")
    
    return created_users

def create_test_tickets(users):
    """Создает тестовые заявки"""
    tickets_data = [
        {
            'title': 'Проблема с принтером',
            'description': 'Принтер HP LaserJet не печатает документы. При попытке печати выдает ошибку "Paper jam". Проверял лоток для бумаги - бумага есть.',
            'priority': 'medium',
            'status': 'new',
            'created_by': 'ivanov'
        },
        {
            'title': 'Нужен доступ к базе данных',
            'description': 'Требуется предоставить доступ к базе данных для нового сотрудника отдела продаж. Нужны права на чтение таблиц customers и orders.',
            'priority': 'high',
            'status': 'in_progress',
            'created_by': 'petrova'
        },
        {
            'title': 'Обновление программного обеспечения',
            'description': 'Необходимо обновить Microsoft Office до последней версии на всех компьютерах в отделе. Текущая версия 2016, нужна 2021.',
            'priority': 'low',
            'status': 'resolved',
            'created_by': 'sidorov'
        },
        {
            'title': 'Сломанная клавиатура',
            'description': 'Клавиатура на рабочем месте в кабинете 305 не работает. При нажатии на клавиши ничего не происходит. Нужна замена.',
            'priority': 'medium',
            'status': 'new',
            'created_by': 'ivanov'
        },
        {
            'title': 'Проблема с интернетом',
            'description': 'Интернет работает очень медленно в отделе бухгалтерии. Скорость загрузки страниц очень низкая. Нужно проверить сетевое оборудование.',
            'priority': 'critical',
            'status': 'in_progress',
            'created_by': 'petrova'
        }
    ]
    
    created_tickets = []
    for ticket_data in tickets_data:
        created_by = User.objects.get(username=ticket_data['created_by'])
        
        # Создаем заявку с разными датами
        ticket = Ticket.objects.create(
            title=ticket_data['title'],
            description=ticket_data['description'],
            priority=ticket_data['priority'],
            status=ticket_data['status'],
            created_by=created_by
        )
        
        # Устанавливаем разные даты создания
        days_ago = len(created_tickets) + 1
        ticket.created_at = datetime.now() - timedelta(days=days_ago)
        ticket.save()
        
        created_tickets.append(ticket)
        print(f"✅ Создана заявка: {ticket.title} (статус: {ticket.get_status_display()})")
    
    return created_tickets

def create_test_comments(tickets, users):
    """Создает тестовые комментарии"""
    comments_data = [
        {
            'content': 'Принял заявку в работу. Буду разбираться с проблемой.',
            'is_internal': False,
            'ticket_index': 0,
            'author': 'admin'
        },
        {
            'content': 'Проверил принтер. Проблема в застревании бумаги в механизме. Нужно разобрать и почистить.',
            'is_internal': True,
            'ticket_index': 0,
            'author': 'admin'
        },
        {
            'content': 'Доступ предоставлен. Логин и пароль отправлены на email.',
            'is_internal': False,
            'ticket_index': 1,
            'author': 'admin'
        },
        {
            'content': 'Спасибо! Получил доступ, все работает.',
            'is_internal': False,
            'ticket_index': 1,
            'author': 'petrova'
        },
        {
            'content': 'Обновление завершено. Все компьютеры обновлены до Office 2021.',
            'is_internal': False,
            'ticket_index': 2,
            'author': 'admin'
        }
    ]
    
    for comment_data in comments_data:
        ticket = tickets[comment_data['ticket_index']]
        author = User.objects.get(username=comment_data['author'])
        
        comment = TicketComment.objects.create(
            ticket=ticket,
            author=author,
            content=comment_data['content'],
            is_internal=comment_data['is_internal']
        )
        
        print(f"✅ Добавлен комментарий к заявке #{ticket.id}")

def main():
    """Основная функция создания тестовых данных"""
    print("🚀 Создание тестовых данных...")
    print()
    
    # Создаем пользователей
    print("👥 Создание пользователей:")
    users = create_test_users()
    print()
    
    # Создаем заявки
    print("📋 Создание заявок:")
    tickets = create_test_tickets(users)
    print()
    
    # Создаем комментарии
    print("💬 Создание комментариев:")
    create_test_comments(tickets, users)
    print()
    
    print("✅ Тестовые данные созданы успешно!")
    print()
    print("🔗 Войдите в систему: http://127.0.0.1:8000/")
    print("👤 Администратор: admin / admin123")
    print("👤 Пользователи: ivanov / user123, petrova / user123, sidorov / user123")

if __name__ == '__main__':
    main()
