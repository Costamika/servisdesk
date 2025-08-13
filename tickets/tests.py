from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ticket, TicketComment


class TicketModelTest(TestCase):
    """Тесты для модели Ticket"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
    def test_ticket_creation(self):
        """Тест создания заявки"""
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user,
            priority='medium',
            status='new'
        )
        
        self.assertEqual(ticket.title, 'Test Ticket')
        self.assertEqual(ticket.status, 'new')
        self.assertEqual(ticket.priority, 'medium')
        self.assertEqual(ticket.created_by, self.user)
        self.assertIsNone(ticket.assigned_to)
        
    def test_ticket_str_method(self):
        """Тест строкового представления заявки"""
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )
        
        self.assertEqual(str(ticket), f'Заявка #{ticket.id}: Test Ticket')
        
    def test_ticket_status_colors(self):
        """Тест цветов статусов"""
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )
        
        self.assertEqual(ticket.get_status_color(), 'primary')  # new
        
        ticket.status = 'in_progress'
        self.assertEqual(ticket.get_status_color(), 'warning')
        
        ticket.status = 'resolved'
        self.assertEqual(ticket.get_status_color(), 'success')
        
    def test_ticket_priority_colors(self):
        """Тест цветов приоритетов"""
        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user,
            priority='low'
        )
        
        self.assertEqual(ticket.get_priority_color(), 'success')  # low
        
        ticket.priority = 'high'
        self.assertEqual(ticket.get_priority_color(), 'danger')
        
        ticket.priority = 'critical'
        self.assertEqual(ticket.get_priority_color(), 'dark')


class TicketViewsTest(TestCase):
    """Тесты для представлений заявок"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            is_staff=True
        )
        
    def test_ticket_list_view_requires_login(self):
        """Тест что список заявок требует авторизации"""
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(response.status_code, 302)  # редирект на логин
        
    def test_ticket_list_view_with_login(self):
        """Тест списка заявок для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_list.html')
        
    def test_ticket_create_view(self):
        """Тест создания заявки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_form.html')
        
    def test_ticket_create_post(self):
        """Тест POST запроса создания заявки"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'New Test Ticket',
            'description': 'Test Description',
            'priority': 'medium',
            'status': 'new'
        }
        
        response = self.client.post(reverse('tickets:ticket_create'), data)
        self.assertEqual(response.status_code, 302)  # редирект после создания
        
        # Проверяем что заявка создана
        ticket = Ticket.objects.get(title='New Test Ticket')
        self.assertEqual(ticket.created_by, self.user)
        self.assertEqual(ticket.status, 'new')
        
    def test_dashboard_view(self):
        """Тест главной страницы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/dashboard.html')


class TicketCommentTest(TestCase):
    """Тесты для комментариев"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            created_by=self.user
        )
        
    def test_comment_creation(self):
        """Тест создания комментария"""
        comment = TicketComment.objects.create(
            ticket=self.ticket,
            author=self.user,
            content='Test comment content'
        )
        
        self.assertEqual(comment.ticket, self.ticket)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'Test comment content')
        self.assertFalse(comment.is_internal)
        
    def test_comment_str_method(self):
        """Тест строкового представления комментария"""
        comment = TicketComment.objects.create(
            ticket=self.ticket,
            author=self.user,
            content='Test comment'
        )
        
        expected = f"Комментарий к заявке #{self.ticket.id} от {self.user.username}"
        self.assertEqual(str(comment), expected)
