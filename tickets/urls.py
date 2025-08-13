from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    # Главная страница
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # Управление заявками
    path("list/", views.ticket_list, name="ticket_list"),
    path("create/", views.ticket_create, name="ticket_create"),
    path("<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("<int:ticket_id>/edit/", views.ticket_edit, name="ticket_edit"),
    # Административные функции
    path("<int:ticket_id>/assign/", views.ticket_assign, name="ticket_assign"),
    path(
        "<int:ticket_id>/change-status/",
        views.ticket_change_status,
        name="ticket_change_status",
    ),
    path("<int:ticket_id>/delete/", views.ticket_delete, name="ticket_delete"),
]
