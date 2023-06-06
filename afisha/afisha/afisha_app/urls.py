from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'Event', views.EventViewSet)

urlpatterns = [
    path('', views.custom_main, name='homepage'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('purchase/', views.purchase_page, name='purchase'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('tickets/', views.TicketListView.as_view(), name='tickets'),
    path('viewers/', views.ViewerListView.as_view(), name='viewers'),
    path('event/', views.event_view, name='event'),
    path('ticket/', views.ticket_view, name='ticket'),
    path('viewer/', views.viewer_view, name='viewer'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
]
