from django.test import TestCase
from django.urls import reverse

from afisha_app.forms import User
from afisha_app.models import Event, Ticket


class HomePageTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'index.html')

    def test_exists_params_in_context(self):
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('events' in resp.context)
        self.assertTrue('tickets' in resp.context)
        self.assertTrue('viewers' in resp.context)


class RegisterUserTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'registration/register.html')

    def test_exists_params_in_context(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('form_errors' in resp.context)

    def test_register_user(self):
        resp = self.client.post(reverse('register'), data={
            'username': 'arinolick',
            'first_name': 'arina',
            'last_name': 'pruzinina',
            'password1': 'love9268',
            'password2': 'love9268',
            'email': 'admin@yandex.ru',
            'date_of_birth': "2004-06-22"
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, str(reverse('profile')))


class LoginUserTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru'
        )
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('profile'))
        self.assertRedirects(resp, '/accounts/login/?next=/profile/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='arinolick', password='love9268')
        resp = self.client.get(reverse('profile'))

        self.assertEqual(str(resp.context['user']), 'arinolick')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'pages/profile.html')

    def test_added_money(self):
        login = self.client.login(username='arinolick', password='love9268')
        resp = self.client.post(reverse('profile'), data={
            'money': 100
        })
        self.assertEqual(resp.status_code, 302)


class UserPurchaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000,
            date_of_birth = '2003-11-21'
        )

        self.event = Event.objects.create(
            name="Some name",
            description="Some description",
            price=1000,
            address="Some address",
            age_minimum=15,
            date="2023-06-06",
            start_time="18:49:38",
            tickets_amount=15,
            type="concert",
            viewer=self.user,
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        resp = self.client.get('/purchase/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('event' in resp.context)
        self.assertTrue('funds' in resp.context)
        self.assertTrue('enough_money' in resp.context)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('purchase'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('purchase'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'pages/purchase.html')

    def test_buy_ticket_for_event(self):
        self.client.force_login(self.user)
        resp = self.client.post(f"/purchase/?id={self.event.id}")
        self.assertEqual(resp.status_code, 302)


class EventTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000,
            date_of_birth = '2003-11-21'
        )
        self.event = Event.objects.create(
            name="Some name",
            description="Some description",
            price=1000,
            address="Some address",
            age_minimum=15,
            date="2023-06-06",
            start_time="18:49:38",
            tickets_amount=15,
            type="concert",
            viewer=self.user,
        )

    def test_event_url(self):
        self.client.force_login(self.user)
        resp = self.client.get(f"/event/?id={self.event.id}")
        self.assertEqual(resp.status_code, 200)


class EventCreateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000,
            date_of_birth = '2003-11-21'
        )

    def test_create_event_url(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('event_create'), data={
            'name': "Some name",
            'description': "Some description",
            'price': 1000,
            'address': "Some address",
            'age_minimum': 15,
            'date': "2023-06-28",
            'start_time': "18:49:38",
            'tickets_amount': 15,
            'type': "concert",
            'viewer': self.user,
        })
        self.assertEqual(resp.status_code, 302)


class EventListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000,
            date_of_birth = '2003-11-21'
        )

    def test_event_list_url(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('events'))
        self.assertEqual(resp.status_code, 200)




class TicketListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000
        )

    def test_ticket_list_url(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('tickets'))
        self.assertEqual(resp.status_code, 200)


class ViewerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000, 
            date_of_birth = '2003-11-21'
        )

    def test_viewer_url(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('viewer'), data={
            'id': self.user.id
        })
        self.assertEqual(resp.status_code, 200)


class ViewerListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='arinolick',
            first_name='arina',
            last_name='pruzinina',
            password='love9268',
            email='admin@yandex.ru',
            money=10000,
            date_of_birth = '2003-11-21'
        )

    def test_viewers_list_url(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse('viewers'))
        self.assertEqual(resp.status_code, 200)
