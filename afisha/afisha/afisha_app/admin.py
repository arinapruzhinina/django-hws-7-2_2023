from django.contrib import admin
from .models import Event, Ticket, EventTicket, ViewerTicket,  Viewer
from datetime import datetime 


class EventTicketInline(admin.TabularInline):
    model = EventTicket
    extra = 1

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

class ViewerTicketInline(admin.TabularInline):
    model = ViewerTicket
    extra = 1

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    inline = EventTicketInline
  

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event 
    inlines = (TicketInline,)

@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    model = Viewer
    inlines = (TicketInline,)

# class TicketClientInline(admin.TabularInline):
#     model = TicketClient
#     extra = 1

# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     model = Client
#     # inlines = (TicketClientInline,)