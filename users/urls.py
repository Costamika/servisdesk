from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # Управление пользователями (только для администраторов)
    path("", views.user_list, name="user_list"),
    path("create/", views.user_create, name="user_create"),
    path("<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path(
        "<int:user_id>/toggle-active/",
        views.user_toggle_active,
        name="user_toggle_active",
    ),
    path("<int:user_id>/delete/", views.user_delete, name="user_delete"),
    # Профиль пользователя
    path("profile/", views.profile_view, name="profile_view"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]
