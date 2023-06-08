from django.views import View

from afisha_app.models import Event


class EventCreateView(View):

    def post(self, request, *args, **kwargs):
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
        except Exception as err:
            raise Exception(f"Упс, что-то пошло не так: {err}")
