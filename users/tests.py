from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile


class UserProfileTest(TestCase):
    """Тесты для модели UserProfile"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
    def test_userprofile_creation(self):
        """Тест автоматического создания профиля пользователя"""
        # Профиль должен создаться автоматически через сигнал
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        
    def test_userprofile_str_method(self):
        """Тест строкового представления профиля"""
        profile = self.user.profile
        expected = f"Профиль {self.user.username}"
        self.assertEqual(str(profile), expected)
        
    def test_userprofile_fields(self):
        """Тест полей профиля"""
        profile = self.user.profile
        
        # Проверяем значения по умолчанию
        self.assertEqual(profile.phone, '')
        self.assertEqual(profile.department, '')
        self.assertEqual(profile.position, '')
        
        # Изменяем значения
        profile.phone = '+7-999-123-45-67'
        profile.department = 'IT отдел'
        profile.position = 'Разработчик'
        profile.save()
        
        # Проверяем что изменения сохранились
        profile.refresh_from_db()
        self.assertEqual(profile.phone, '+7-999-123-45-67')
        self.assertEqual(profile.department, 'IT отдел')
        self.assertEqual(profile.position, 'Разработчик')


class UserViewsTest(TestCase):
    """Тесты для представлений пользователей"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            is_staff=True
        )
        
    def test_profile_view_requires_login(self):
        """Тест что просмотр профиля требует авторизации"""
        response = self.client.get(reverse('users:profile_view'))
        self.assertEqual(response.status_code, 302)  # редирект на логин
        
    def test_profile_view_with_login(self):
        """Тест просмотра профиля для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_view.html')
        
    def test_profile_edit_view(self):
        """Тест редактирования профиля"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_form.html')
        
    def test_profile_edit_post(self):
        """Тест POST запроса редактирования профиля"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone': '+7-999-123-45-67',
            'department': 'IT отдел',
            'position': 'Разработчик'
        }
        
        response = self.client.post(reverse('users:profile_edit'), data)
        self.assertEqual(response.status_code, 302)  # редирект после сохранения
        
        # Проверяем что данные обновились
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.phone, '+7-999-123-45-67')
        self.assertEqual(self.user.profile.department, 'IT отдел')
        self.assertEqual(self.user.profile.position, 'Разработчик')
        
    def test_user_list_view_requires_admin(self):
        """Тест что список пользователей требует прав администратора"""
        # Обычный пользователь
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 302)  # редирект на логин
        
        # Администратор
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')


class UserFormsTest(TestCase):
    """Тесты для форм пользователей"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
    def test_userprofile_form_validation(self):
        """Тест валидации формы профиля пользователя"""
        from .forms import UserProfileForm
        
        # Валидные данные
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '+7-999-123-45-67',
            'department': 'IT отдел',
            'position': 'Разработчик'
        }
        
        form = UserProfileForm(data=form_data, instance=self.user.profile)
        self.assertTrue(form.is_valid())
        
        # Невалидный email
        form_data['email'] = 'invalid-email'
        form = UserProfileForm(data=form_data, instance=self.user.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
