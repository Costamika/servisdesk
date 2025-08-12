from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from typing import Optional


class Ticket(models.Model):
    """
    Модель заявки/тикета
    """
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решена'),
        ('closed', 'Закрыта'),
        ('cancelled', 'Отменена'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]

    title = models.CharField(
        max_length=200, 
        verbose_name="Заголовок",
        validators=[MinLengthValidator(5, "Заголовок должен содержать минимум 5 символов")]
    )
    description = models.TextField(
        verbose_name="Описание",
        validators=[MinLengthValidator(10, "Описание должно содержать минимум 10 символов")]
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name="Статус"
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name="Приоритет"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_tickets',
        verbose_name="Создатель"
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets',
        verbose_name="Назначен"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата решения")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Заявка #{self.id}: {self.title}"

    def save(self, *args, **kwargs) -> None:
        """Переопределяем save для автоматического заполнения resolved_at"""
        if self.status in ['resolved', 'closed'] and not self.resolved_at:
            from django.utils import timezone
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_resolved(self) -> bool:
        """Проверяет, решена ли заявка"""
        return self.status in ['resolved', 'closed']

    @property
    def can_be_edited_by(self, user: User) -> bool:
        """Проверяет, может ли пользователь редактировать заявку"""
        return (user == self.created_by or 
                user.is_staff or 
                user.is_superuser or 
                user == self.assigned_to)

    def get_status_color(self) -> str:
        """Возвращает цвет для статуса"""
        status_colors = {
            'new': 'primary',
            'in_progress': 'warning',
            'resolved': 'success',
            'closed': 'secondary',
            'cancelled': 'danger',
        }
        return status_colors.get(self.status, 'secondary')

    def get_priority_color(self) -> str:
        """Возвращает цвет для приоритета"""
        priority_colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'dark',
        }
        return priority_colors.get(self.priority, 'secondary')


class TicketComment(models.Model):
    """
    Модель комментария к заявке
    """
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Заявка"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='ticket_comments',
        verbose_name="Автор"
    )
    content = models.TextField(
        verbose_name="Содержание",
        validators=[MinLengthValidator(1, "Комментарий не может быть пустым")]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_internal = models.BooleanField(
        default=False, 
        verbose_name="Внутренний комментарий"
    )

    class Meta:
        verbose_name = "Комментарий к заявке"
        verbose_name_plural = "Комментарии к заявкам"
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"Комментарий к заявке #{self.ticket.id} от {self.author.username}"
