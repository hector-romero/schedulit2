from django.urls import path

from schedulit.api.auth import views as auth_views


urlpatterns = [
    # Authentication
    path('account/', auth_views.UserProfileView.as_view()),
    path('account/login/', auth_views.LoginView.as_view()),
    path('account/logout/', auth_views.LogoutView.as_view()),
    path('account/logout/all/', auth_views.LogoutAllView.as_view()),

    path('account/register/', auth_views.RegisterView.as_view()),

]
