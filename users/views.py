from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from .models import UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, UserEditForm, UserSearchForm
from typing import Optional


def is_admin(user: User) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_admin)
def user_list(request: HttpRequest) -> HttpResponse:
    """
    Список всех пользователей (только для администраторов)
    """
    search_form = UserSearchForm(request.GET)
    users = User.objects.select_related('profile').all()
    
    # Применяем фильтры поиска
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        department = search_form.cleaned_data.get('department')
        is_active = search_form.cleaned_data.get('is_active')
        
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(profile__department__icontains=search)
            )
        
        if department:
            users = users.filter(profile__department__icontains=department)
        
        if is_active:
            users = users.filter(is_active=bool(int(is_active)))
    
    # Сортировка по дате создания
    users = users.order_by('-date_joined')
    
    # Пагинация
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_users': users.count(),
    }
    
    return render(request, 'users/user_list.html', context)


@login_required
@user_passes_test(is_admin)
def user_create(request: HttpRequest) -> HttpResponse:
    """
    Создание нового пользователя (только для администраторов)
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Пользователь {user.username} успешно создан!')
            return redirect('users:user_list')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'title': 'Создание пользователя',
    }
    
    return render(request, 'users/user_form.html', context)


@login_required
@user_passes_test(is_admin)
def user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Редактирование пользователя (только для администраторов)
    """
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Пользователь {user.username} обновлен!')
            return redirect('users:user_list')
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
        'title': f'Редактирование пользователя {user.username}',
    }
    
    return render(request, 'users/user_form.html', context)


@login_required
@user_passes_test(is_admin)
def user_toggle_active(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Активация/деактивация пользователя (только для администраторов)
    """
    user = get_object_or_404(User, id=user_id)
    
    # Нельзя деактивировать самого себя
    if user == request.user:
        messages.error(request, 'Вы не можете деактивировать свой аккаунт!')
        return redirect('users:user_list')
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'активирован' if user.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {user.username} {status}!')
    
    return redirect('users:user_list')


@login_required
@user_passes_test(is_admin)
def user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Удаление пользователя (только для администраторов)
    """
    user = get_object_or_404(User, id=user_id)
    
    # Нельзя удалить самого себя
    if user == request.user:
        messages.error(request, 'Вы не можете удалить свой аккаунт!')
        return redirect('users:user_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Пользователь {username} удален!')
        return redirect('users:user_list')
    
    context = {
        'user_obj': user,
        'title': f'Удаление пользователя {user.username}',
    }
    
    return render(request, 'users/user_confirm_delete.html', context)


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """
    Редактирование собственного профиля
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('users:profile_edit')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'title': 'Редактирование профиля',
    }
    
    return render(request, 'users/profile_form.html', context)


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Просмотр собственного профиля
    """
    context = {
        'user_obj': request.user,
        'title': 'Мой профиль',
    }
    
    return render(request, 'users/profile_view.html', context)
