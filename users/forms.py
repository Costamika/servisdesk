from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from typing import Optional


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя администратором
    """
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    department = forms.CharField(max_length=100, required=False, label="Отдел")
    position = forms.CharField(max_length=100, required=False, label="Должность")
    is_staff = forms.BooleanField(required=False, label="Администратор")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit: bool = True) -> User:
        """Сохраняет пользователя и создает профиль"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data.get('is_staff', False)
        
        if commit:
            user.save()
            # Обновляем профиль
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.department = self.cleaned_data.get('department', '')
            profile.position = self.cleaned_data.get('position', '')
            profile.save()
        
        return user


class UserEditForm(forms.ModelForm):
    """
    Форма для редактирования пользователя администратором
    """
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    department = forms.CharField(max_length=100, required=False, label="Отдел")
    position = forms.CharField(max_length=100, required=False, label="Должность")
    is_staff = forms.BooleanField(required=False, label="Администратор")
    is_active = forms.BooleanField(required=False, label="Активен")
    
    # Поля для изменения пароля (необязательные)
    new_password1 = forms.CharField(
        max_length=128, 
        required=False, 
        label="Новый пароль",
        widget=forms.PasswordInput,
        help_text="Оставьте пустым, если не хотите менять пароль"
    )
    new_password2 = forms.CharField(
        max_length=128, 
        required=False, 
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput,
        help_text="Повторите новый пароль"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Заполняем поля профиля
            try:
                profile = self.instance.profile
                self.fields['phone'].initial = profile.phone
                self.fields['department'].initial = profile.department
                self.fields['position'].initial = profile.position
            except UserProfile.DoesNotExist:
                pass

    def clean_new_password2(self):
        """Проверяем совпадение паролей"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Пароли не совпадают")
        
        return password2

    def save(self, commit: bool = True) -> User:
        """Сохраняет пользователя и обновляет профиль"""
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Обновляем пароль, если указан новый
            if self.cleaned_data.get('new_password1'):
                user.set_password(self.cleaned_data['new_password1'])
                user.save()
            
            # Обновляем профиль
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.department = self.cleaned_data.get('department', '')
            profile.position = self.cleaned_data.get('position', '')
            profile.save()
        
        return user


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя
    """
    first_name = forms.CharField(max_length=30, label="Имя")
    last_name = forms.CharField(max_length=30, label="Фамилия")
    email = forms.EmailField(label="Email")

    class Meta:
        model = UserProfile
        fields = ('phone', 'department', 'position')
        labels = {
            'phone': 'Телефон',
            'department': 'Отдел',
            'position': 'Должность',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit: bool = True) -> UserProfile:
        """Сохраняет профиль и обновляет данные пользователя"""
        profile = super().save(commit=False)
        
        if commit:
            profile.save()
            # Обновляем данные пользователя
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        
        return profile


class UserSearchForm(forms.Form):
    """
    Форма для поиска пользователей
    """
    search = forms.CharField(
        max_length=100, 
        required=False, 
        label="Поиск",
        widget=forms.TextInput(attrs={'placeholder': 'Имя, фамилия, email или логин'})
    )
    department = forms.CharField(
        max_length=100, 
        required=False, 
        label="Отдел"
    )
    is_active = forms.ChoiceField(
        choices=[('', 'Все'), ('1', 'Активные'), ('0', 'Неактивные')],
        required=False,
        label="Статус"
    )
