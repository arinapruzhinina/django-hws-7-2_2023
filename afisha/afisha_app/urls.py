from django.urls import path, include
from rest_framework.routers import DefaultRouter
from afisha_app.views.old import *
from afisha_app.views.event import EventCreateView

router = DefaultRouter()
router.register(r'Event', EventViewSet)

urlpatterns = [
    path('', custom_main, name='homepage'),
    path('register/', register, name='register'),
    path('profile/', profile_page, name='profile'),
    path('purchase/', purchase_page, name='purchase'),

    path('event/', event_view, name='event'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('events/', EventListView.as_view(), name='events'),

    
    path('tickets/', TicketListView.as_view(), name='tickets'),

    path('viewer/', viewer_view, name='viewer'),
    path('viewers/', ViewerListView.as_view(), name='viewers'),

    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('django.contrib.auth.urls')),
]
