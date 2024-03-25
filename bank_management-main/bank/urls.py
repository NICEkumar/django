import os
from django.urls import path 
from . import views


urlpatterns = [
    # Other URL patterns...
    path("", views.home, name="Home"),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('usr_dashboard/<str:user_id>/', views.usr_dashboard, name='usr_dashboard'),
    path('accounts/<str:mgr_id>/', views.accounts, name='accounts'),
    path('add_accounts/<str:mgr_id>/', views.add_account, name='add_accounts'),
    path('internal_transfer/<str:user_id>/', views.internal_transfer, name='internal_transfer'),
    path('external_transfer/<str:user_id>/', views.external_transfer, name='external_transfer'),

    path('generate-pdf/<str:user_id>/', views.generate_pdf, name='generate_pdf'),
    path('self_transfer/<str:user_id>/', views.self_transfer, name='self_transfer'),
    path('other_transfer/<str:user_id>/', views.other_transfer, name='other_transfer'),
    path('notifications/<str:mgr_id>/', views.notifications, name='notifications'),
    path('delete_notification/<str:mgr_id>/', views.delete_notification, name='delete_notification'),
    path('create_account_request/<str:user_id>/', views.create_account_request, name='create_account_request'),
    path('account_statements/<str:user_id>/', views.account_statements, name='account_statements'),
    path('usr_accounts/<str:user_id>/', views.usr_accounts, name='usr_accounts'),
    path('mgr_dashboard/<str:mgr_id>/', views.mgr_dashboard, name='mgr_dashboard'),
    path('account_details/<str:mgr_id>/<int:accountNo>', views.account_details, name='account_details'),
    path('fetch_user_data/<str:user_id>', views.fetch_user_data, name='fetch_user_data'),
]

