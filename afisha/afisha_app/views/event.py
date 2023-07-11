import datetime

from django.views import View

from afisha_app.models import Event

from django.shortcuts import render, redirect
from afisha_app.forms import EventForm


class EventCreateView(View):

    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, 'event_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        self.validate_date(request.POST['date'])
        if self.error:
            return render(request, 'event_create.html', context={
                'error': "Дата не может быть указана в прошлом",
                'form': EventForm()
            })
        viewer = request.user
        try:
            Event.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                price=request.POST['price'],
                address=request.POST['address'],
                age_minimum=request.POST['age_minimum'],
                date=request.POST['date'],
                start_time=request.POST['start_time'],
                tickets_amount=request.POST['tickets_amount'],
                type=request.POST['type'],
                viewer=viewer,
            )
            return redirect('events')
        except Exception as err:
            raise Exception(f"Упс, что-то пошло не так: {err}")

    def validate_date(self, date):
        if date < str(datetime.date.today()):
            self.error = "Дата не может быть указана в прошлом"
            return
        self.error = ""
