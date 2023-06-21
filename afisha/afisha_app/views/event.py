from django.views import View

from afisha_app.models import Event

from django.shortcuts import render, redirect
from afisha_app.forms import EventForm

from django.shortcuts import render, redirect
from afisha_app.forms import EventForm

class EventCreateView(View):

    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, 'event_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        viewer = request.user
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.viewer = viewer
            event.save()
            return redirect('events')
        else:
            return render(request, 'event_create.html', {'form': form})