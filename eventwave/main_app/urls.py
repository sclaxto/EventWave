from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    # path('events/<int:event_id>', views.event_detail, name='detail'),
    path('results/', views.results, name='results'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<int:seekgeek_id>', views.events_details, name='detail'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    path('dashboard/<int:seekgeek_id>',
         views.dashboard_add, name='dashboard_add'),
    path('dashboard/<int:event_id>/delete',
         views.dashboard_delete, name='dashboard_delete'),
    path('about/', views.about, name='about')
]