from django.urls import path

from schedulit.api.auth import views as auth_views
from schedulit.api.users import views as users_views
from schedulit.api.shifts import views as shift_views


urlpatterns = [
    # Authentication
    path('account/', auth_views.UserProfileView.as_view()),
    path('account/login/', auth_views.LoginView.as_view()),
    path('account/logout/', auth_views.LogoutView.as_view()),
    path('account/logout/all/', auth_views.LogoutAllView.as_view()),

    path('account/register/', auth_views.RegisterView.as_view()),

    path('users/', users_views.UsersView.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', users_views.UsersView.as_view({'get': 'retrieve'})),
    path('shifts/<int:employee_id>/', shift_views.ShiftView.as_view({'get': 'list'}))


]
