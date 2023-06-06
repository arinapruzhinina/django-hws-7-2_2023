from django.shortcuts import render
from .models import Event, Ticket, Viewer
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework import viewsets, permissions, status as status_codes, parsers, decorators
from .serializers import EventSerializer
from rest_framework.response import Response
from .forms import AddFundsForm, RegistrationForm
from django.contrib.auth import mixins, decorators as auth_decorators
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from os import listdir
from . import config

def register(request):
    form_errors = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Viewer.objects.create(user=user)
            return HttpResponseRedirect(reverse('profile'))
        form_errors = form.error
    return render(
        request,
        'registration/register.html', 
        context={
            'form': RegistrationForm(), 
            'form_errors': form_errors, 
            }
    )



@auth_decorators.login_required
def purchase_page(request):
    viewer = Viewer.objects.get(user=request.user)
    ticket_id = request.GET.get('id', '')
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Exception:
        ticket = None
    else:
        if request.method == 'POST' and viewer.money >= ticket.price:
            with transaction.atomic():
                viewer.money -= ticket.price
                viewer.ticket.add(ticket)
                viewer.save()
            url = reverse('ticket')
            return HttpResponseRedirect(f'{url}?id={ticket_id}')

    return render(
        request,
        template_name='pages/purchase.html',
        context={
            'ticket': ticket,
            'funds': viewer.money,
            'enough_money': viewer.money - ticket.price >= 0,
        },
    )

@auth_decorators.login_required
def profile_page(request):
    user = request.user
    viewer = Viewer.objects.get(user=user)
    form_errors = []

    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        
        if form.is_valid():
            funds_to_add = form.cleaned_data.get('money')
            digits= len(str(viewer.money + funds_to_add)) - 1
            if funds_to_add > 0 and digits <= 10:
                with transaction.atomic():
                    viewer.money += funds_to_add
                    viewer.save()
                return HttpResponseRedirect(reverse('profile'))
            form_errors.append('Amount field must be greater than zero and \
                                the number of all digits must be less than 10')
        else:
            form_errors.extend(form.errors.get('money'))

    user_data = {
        'username': user.username,
        'first name': user.first_name,
        'last name': user.last_name,
        'email': user.email,
        'money': viewer.money,
    }


    return render(
        request,
        'pages/profile.html',
        context={
            'form': AddFundsForm(),
            'user_data': user_data,
            'form_errors': '; '.join(form_errors), 
            'tickets': [ticket.name for ticket in viewer.tickets.all()],
        },
    )

def custom_main(request):
    return render(
        request,
        config.TEMPLATE_MAIN,
        context={
            'events': Event.objects.all().count(),
            'tickets': Ticket.objects.all().count(),
            'viewers': Viewer.objects.all().count(),
        },
    )
    


def catalog_view(cls_model, context_name, template):
    class CustomListView(mixins.LoginRequiredMixin, ListView):
        model = cls_model
        template_name = template
        paginate_by = 20
        context_object_name = context_name

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            instances = cls_model.objects.all()
            paginator = Paginator(instances, 20)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{context_name}_list'] = page_obj
            return context

    return CustomListView

def entity_view(cls_model, name, template):
    @auth_decorators.login_required
    def view(request):
        target_id = request.GET.get('id', '')
        context = {name: cls_model.objects.get(id=target_id)}
        if cls_model is Ticket:
            viewer = Viewer.objects.get(user=request.user)
            try:
                context['viewer_has_ticket'] = bool(viewer.tickets.get(id=target_id))
            except Exception:
                context['viewer_has_ticket'] = False

        return render(
            request,
            template,
            context=context,
        )
    return view

TicketListView = catalog_view(Ticket, 'tickets', 'catalog/tickets.html')
EventListView = catalog_view(Event, 'events', 'catalog/events.html')
ViewerListView = catalog_view(Viewer, 'viewers', 'catalog/viewers.html')

ticket_view = entity_view(Ticket, 'ticket',' entities/ticket.html')
event_view = entity_view(Event, 'event', 'entities/event.html')
viewer_view = entity_view(Viewer, 'viewer', 'entities/viewer.html')



class Permission(permissions.BasePermission):
    safe_methods = ('GET', 'HEAD', 'OPTIONS', 'PATCH')
    unsafe_methods = ('POST', 'PUT', 'DELETE')

    def has_permission(self, request, _):
        if request.method in self.safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in self.unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False


def query_from_request(cls_serializer, request) -> dict:
    query = {}
    for field in cls_serializer.Meta.fields:
        obj_value = request.GET.get(field, '')
        if obj_value:
            query[field] = obj_value
    return query


def create_viewset(cls_model, serializer, order_field):
    class CustomViewSet(viewsets.ModelViewSet):
        queryset = cls_model.objects.all()
        serializer_class = serializer
        permission_classes = [Permission]

        def get_queryset(self):
            query = query_from_request(serializer, self.request)
            queryset = cls_model.objects.filter(**query) if query else cls_model.objects.all()
            return queryset.order_by(order_field)

        def delete(self, request):
            def response_from_objects(num):
                if not num:
                    message = f'DELETE for model {cls_model.__name__}: query did not match any objects'
                    return Response(message, status=status_codes.HTTP_404_NOT_FOUND)
                status = status_codes.HTTP_204_NO_CONTENT if num == 1 else status_codes.HTTP_200_OK
                return Response(f'DELETED {num} instances of {cls_model.__name__}', status=status)

            query = query_from_request(serializer, request)
            if query:
                instances = cls_model.objects.all().filter(**query)
                num_objects = len(instances)
                try:
                    instances.delete()
                except Exception as error:
                    return Response(error, status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
                return response_from_objects(num_objects)
            return Response('DELETE has got no query', status=status_codes.HTTP_400_BAD_REQUEST)

        def put(self, request):
            # gets id from query and updates instance with this ID, creates new if doesnt find any.
            def serialize(target):
                attrs = parsers.JSONParser().parse(request)
                model_name = cls_model.__name__
                if target:
                    serialized = serializer(target, data=attrs, partial=True)
                    status = status_codes.HTTP_200_OK
                    body = f'PUT has updated {model_name} instance'
                else:
                    serialized = serializer(data=attrs, partial=True)
                    status = status_codes.HTTP_201_CREATED
                    body = f'PUT has created new {model_name} instance'
                if not serialized.is_valid():
                    return (
                        f'PUT could not serialize query {query} into {model_name}',
                        status_codes.HTTP_400_BAD_REQUEST,
                    )
                try:
                    model_obj = serialized.save()
                except Exception as error:
                    return error, status_codes.HTTP_500_INTERNAL_SERVER_ERROR
                body = f'{body} with id={model_obj.id}'
                return body, status

            query = query_from_request(serializer, request)
            target_id = query.get('id', '')
            if not target_id:
                return Response('PUT has got no id', status=status_codes.HTTP_400_BAD_REQUEST)
            try:
                target_object = cls_model.objects.get(id=target_id)
            except Exception:
                target_object = None
            message, status = serialize(target_object)
            return Response(message, status=status)

    return CustomViewSet

EventViewSet = create_viewset(Event, EventSerializer, 'name')