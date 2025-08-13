from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketAdminForm, TicketCommentForm, TicketForm, TicketSearchForm
from .models import Ticket


def is_admin(user: User) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
def ticket_list(request: HttpRequest) -> HttpResponse:
    """
    Список заявок (все для админов, только свои для пользователей)
    """
    search_form = TicketSearchForm(request.GET)

    if is_admin(request.user):
        # Администраторы видят все заявки
        tickets = Ticket.objects.select_related("created_by", "assigned_to").all()
    else:
        # Пользователи видят только свои заявки
        tickets = Ticket.objects.select_related("created_by", "assigned_to").filter(
            created_by=request.user
        )

    # Применяем фильтры поиска
    if search_form.is_valid():
        search = search_form.cleaned_data.get("search")
        status = search_form.cleaned_data.get("status")
        priority = search_form.cleaned_data.get("priority")
        created_by = search_form.cleaned_data.get("created_by")
        date_from = search_form.cleaned_data.get("date_from")
        date_to = search_form.cleaned_data.get("date_to")

        if search:
            tickets = tickets.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if status:
            tickets = tickets.filter(status=status)

        if priority:
            tickets = tickets.filter(priority=priority)

        if created_by:
            tickets = tickets.filter(created_by=created_by)

        if date_from:
            tickets = tickets.filter(created_at__date__gte=date_from)

        if date_to:
            tickets = tickets.filter(created_at__date__lte=date_to)

    # Сортировка по дате создания
    tickets = tickets.order_by("-created_at")

    # Пагинация
    paginator = Paginator(tickets, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_form": search_form,
        "total_tickets": tickets.count(),
        "is_admin": is_admin(request.user),
    }

    return render(request, "tickets/ticket_list.html", context)


@login_required
def ticket_create(request: HttpRequest) -> HttpResponse:
    """
    Создание новой заявки
    """
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect("tickets:ticket_detail", ticket_id=ticket.id)
    else:
        form = TicketForm()

    context = {
        "form": form,
        "title": "Создание заявки",
    }

    return render(request, "tickets/ticket_form.html", context)


@login_required
def ticket_detail(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Просмотр деталей заявки
    """
    if is_admin(request.user):
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, created_by=request.user)

    # Получаем комментарии
    if is_admin(request.user):
        comments = ticket.comments.all()
    else:
        comments = ticket.comments.filter(is_internal=False)

    # Форма для добавления комментария
    if request.method == "POST":
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен!")
            return redirect("tickets:ticket_detail", ticket_id=ticket.id)
    else:
        comment_form = TicketCommentForm()

    context = {
        "ticket": ticket,
        "comments": comments,
        "comment_form": comment_form,
        "is_admin": is_admin(request.user),
        "user_list": (
            User.objects.filter(is_active=True).order_by("first_name", "last_name")
            if is_admin(request.user)
            else []
        ),
    }

    return render(request, "tickets/ticket_detail.html", context)


@login_required
def ticket_edit(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Редактирование заявки
    """
    if is_admin(request.user):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form_class = TicketAdminForm
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, created_by=request.user)
        form_class = TicketForm

    # Проверяем права на редактирование
    if not (
        request.user == ticket.created_by
        or request.user.is_staff
        or request.user.is_superuser
        or request.user == ticket.assigned_to
    ):
        messages.error(request, "У вас нет прав для редактирования этой заявки!")
        return redirect("tickets:ticket_detail", ticket_id=ticket.id)

    if request.method == "POST":
        form = form_class(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка обновлена!")
            return redirect("tickets:ticket_detail", ticket_id=ticket.id)
    else:
        form = form_class(instance=ticket)

    context = {
        "form": form,
        "ticket": ticket,
        "title": f"Редактирование заявки #{ticket.id}",
    }

    return render(request, "tickets/ticket_form.html", context)


@login_required
@user_passes_test(is_admin)
def ticket_assign(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Назначение исполнителя заявки (только для администраторов)
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        assigned_to_id = request.POST.get("assigned_to")
        if assigned_to_id:
            assigned_to = get_object_or_404(User, id=assigned_to_id)
            ticket.assigned_to = assigned_to
            ticket.status = "in_progress"
            ticket.save()
            messages.success(
                request, f"Заявка назначена пользователю {assigned_to.get_full_name()}"
            )
        else:
            ticket.assigned_to = None
            ticket.save()
            messages.success(request, "Исполнитель снят с заявки")

    return redirect("tickets:ticket_detail", ticket_id=ticket.id)


@login_required
@user_passes_test(is_admin)
def ticket_change_status(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Изменение статуса заявки (только для администраторов)
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Ticket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
            messages.success(
                request,
                f'Статус заявки изменен на "{dict(Ticket.STATUS_CHOICES)[new_status]}"',
            )

    return redirect("tickets:ticket_detail", ticket_id=ticket.id)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Главная страница с статистикой
    """
    if is_admin(request.user):
        # Статистика для администраторов
        total_tickets = Ticket.objects.count()
        new_tickets = Ticket.objects.filter(status="new").count()
        in_progress_tickets = Ticket.objects.filter(status="in_progress").count()
        resolved_tickets = Ticket.objects.filter(
            status__in=["resolved", "closed"]
        ).count()
        total_users = User.objects.filter(is_active=True).count()

        # Последние заявки
        recent_tickets = Ticket.objects.select_related("created_by").order_by(
            "-created_at"
        )[:10]

        context = {
            "total_tickets": total_tickets,
            "new_tickets": new_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "total_users": total_users,
            "recent_tickets": recent_tickets,
            "is_admin": True,
        }
    else:
        # Статистика для пользователей
        user_tickets = Ticket.objects.filter(created_by=request.user)
        total_tickets = user_tickets.count()
        new_tickets = user_tickets.filter(status="new").count()
        in_progress_tickets = user_tickets.filter(status="in_progress").count()
        resolved_tickets = user_tickets.filter(
            status__in=["resolved", "closed"]
        ).count()

        # Последние заявки пользователя
        recent_tickets = user_tickets.order_by("-created_at")[:5]

        context = {
            "total_tickets": total_tickets,
            "new_tickets": new_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "recent_tickets": recent_tickets,
            "is_admin": False,
        }

    return render(request, "tickets/dashboard.html", context)


@login_required
@user_passes_test(is_admin)
def ticket_delete(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    Удаление заявки (только для администраторов)
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        ticket_title = ticket.title
        ticket.delete()
        messages.success(request, f'Заявка "{ticket_title}" успешно удалена!')
        return redirect("tickets:ticket_list")

    context = {
        "ticket": ticket,
        "title": f"Удаление заявки #{ticket.id}",
    }

    return render(request, "tickets/ticket_confirm_delete.html", context)
