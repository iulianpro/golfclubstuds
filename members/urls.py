# members/urls.py
from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # List all members
    path('', views.MemberListView.as_view(), name='list'),

    # Create a new member
    path('members/add/', views.MemberCreateView.as_view(), name='add'),

    # Member detail
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='detail'),

    # POST-only toggle status (redirects back to detail)
    path('members/<int:pk>/toggle/',
         views.MemberToggleView.as_view(), name='toggle'),
]
