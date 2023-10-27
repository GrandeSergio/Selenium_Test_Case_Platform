from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home.html'), name='home'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('<int:test_id>/', views.test_details, name='test_details'),
    path('<int:test_id>/code', views.test_code, name='test_code'),
    path('<int:test_id>/run/', views.run_test_cases, name='run_test_cases'),
    path('<int:test_id>/delete/', views.delete_test_case, name='delete_test_case'),
    path('<int:test_id>/test_history/', views.test_history, name='test_history'),
    path('runs/<int:run_id>/output/', views.run_output, name='run_output'),
    path('test_history/', views.test_history_list, name='test_history_list'),
    path('test/<int:test_id>/replace-file/', views.replace_file, name='replace_file'),
    path('upload/', views.upload, name='upload'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user_details/', views.user_details, name='user_details'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('change-password/', views.CustomPasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('change-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('schedulers/', views.scheduler_list, name='scheduler_list'),
    path('scheduler/<int:scheduler_id>/', views.scheduler_details, name='scheduler_details'),
    path('scheduler/<int:scheduler_id>/add_test_cases/', views.add_test_cases, name='add_test_cases'),
    path('scheduler/create/', views.create_scheduler, name='create_scheduler'),
    path('scheduler/<int:scheduler_id>/testcase/<int:testcase_id>/remove/', views.remove_test_case, name='remove_test_case'),
    path('scheduler/<int:scheduler_id>/history/', views.scheduler_history, name='scheduler_history'),
    path('scheduler/delete/<int:scheduler_id>/', views.delete_scheduler, name='delete_scheduler'),
    path('scheduler/run/<int:scheduler_run_id>/', views.scheduler_run_history, name='scheduler_run_history')

]
