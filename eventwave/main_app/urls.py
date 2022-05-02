from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    # path('events/<int:event_id>', views.event_detail, name='detail'),
    path('results/', views.results, name='results')
]