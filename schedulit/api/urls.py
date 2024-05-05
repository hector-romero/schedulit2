from django.urls import path

from schedulit.api.auth import views as auth_views
from schedulit.api.users import views as users_views
from schedulit.api.shifts import views as shift_views
from schedulit.api.shifts_notes import views as shift_notes_views


urlpatterns = [
    # Authentication
    path('account/', auth_views.UserProfileView.as_view(), name='account'),
    path('account/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='account_logout'),
    path('account/logout/all/', auth_views.LogoutAllView.as_view(), name='account_logout_all'),

    path('account/register/', auth_views.RegisterView.as_view(), name='account_register'),

    # TODO Maybe, rename 'users' to 'employees'?
    path('users/', users_views.UsersView.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('users/<int:pk>/', users_views.UsersView.as_view(
        {'get': 'retrieve', 'put': 'partial_update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('users/<int:employee_id>/shifts/', shift_views.ShiftView.as_view({'get': 'list', 'post': 'create'})),

    path('shifts/<int:pk>/', shift_views.ShiftView.as_view(
        {'get': 'retrieve', 'put': 'partial_update', 'patch': 'partial_update', 'delete': 'destroy'})),

    path('shifts/<int:shift_id>/notes/', shift_notes_views.ShiftNotesView.as_view({'get': 'list', 'post': 'create'})),
    path('shift_notes/<int:pk>/', shift_notes_views.ShiftNotesView.as_view(
        {'get': 'retrieve', 'put': 'partial_update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
