from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:test_id>/', views.test_details, name='test_details'),
    path('<int:test_id>/run/', views.run_test_cases, name='run_test_cases'),
    #path('upload_2/', views.test_upload, name='test_upload'),
    path('<int:test_id>/delete/', views.delete_test_case, name='delete_test_case'),
    path('<int:test_id>/test_history/', views.test_history, name='test_history'),
    path('runs/<int:run_id>/output/', views.run_output, name='run_output'),
    path('test_history/', views.test_history_list, name='test_history_list'),
    #path('test/<int:test_id>/replace_file/', views.replace_file, name='replace_file'),
    #path('<int:test_id>/test_code/', views.test_code, name='test_code'),
    path('upload/', views.upload, name='upload'),
]
