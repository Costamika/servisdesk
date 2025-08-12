from django import forms
from .models import Ticket, TicketComment
from django.contrib.auth.models import User
from typing import Optional


class TicketForm(forms.ModelForm):
    """
    Форма для создания и редактирования заявки
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'priority': 'Приоритет',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок заявки'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробно опишите проблему или запрос'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class TicketAdminForm(forms.ModelForm):
    """
    Расширенная форма для администраторов с возможностью назначения исполнителя
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'assigned_to']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'status': 'Статус',
            'priority': 'Приоритет',
            'assigned_to': 'Назначить исполнителя',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок заявки'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробно опишите проблему или запрос'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активных пользователей в списке назначения
        self.fields['assigned_to'].queryset = User.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')


class TicketCommentForm(forms.ModelForm):
    """
    Форма для добавления комментария к заявке
    """
    class Meta:
        model = TicketComment
        fields = ['content', 'is_internal']
        labels = {
            'content': 'Комментарий',
            'is_internal': 'Внутренний комментарий (виден только администраторам)',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий'
            }),
            'is_internal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class TicketSearchForm(forms.Form):
    """
    Форма для поиска заявок
    """
    search = forms.CharField(
        max_length=100, 
        required=False, 
        label="Поиск",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Заголовок или описание заявки'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'Все статусы')] + Ticket.STATUS_CHOICES,
        required=False,
        label="Статус",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'Все приоритеты')] + Ticket.PRIORITY_CHOICES,
        required=False,
        label="Приоритет",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    created_by = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name'),
        required=False,
        label="Создатель",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        label="Дата с",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        label="Дата по",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
