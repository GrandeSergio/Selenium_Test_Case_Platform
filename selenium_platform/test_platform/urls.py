from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:test_id>/', views.test_details, name='test_details'),
    path('<int:test_id>/run/', views.run_test_cases, name='run_test_cases'),
    #path('upload/', views.test_upload, name='test_upload'),
    path('<int:test_id>/delete/', views.delete_test_case, name='delete_test_case'),
    path('<int:test_id>/test_history/', views.test_history, name='test_history'),
    path('upload/', views.upload, name='upload'),
]
