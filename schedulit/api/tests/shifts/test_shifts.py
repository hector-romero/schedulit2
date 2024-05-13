import typing
from datetime import datetime, timedelta

from django.urls import reverse, NoReverseMatch
from knox.models import AuthToken
from model_bakery import baker
from rest_framework import status

from schedulit.api.shifts.serializers import ShiftSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods
from schedulit.api.tests.shifts.helpers import get_shift_params, prepare_shift, generate_shift_params, ShiftParams
from schedulit.authentication.models import User
from schedulit.shift.models import Shift


def url_shifts_for_user(user: User) -> str:
    try:
        return reverse('user_shifts', kwargs={'pk': user.id})
    except NoReverseMatch:
        return f'/api/users/{user.id}/shifts/'


invalid_times: typing.List[typing.Any] = [
    -1, 0, 1000000, None, '', 'string', "[]", '_', '/', {}, "2030-13-32T28:89:90", "()", "12:32:10",
]


class ShiftsTest(ApiTestCase):
    url_shifts: str

    @classmethod
    def setUpTestData(cls):
        cls.initialize_users()
        cls.url_shifts = url_shifts_for_user(cls.user2)

    def setUp(self):
        # By default, all request are authenticated by the scheduler user
        self.set_auth_header(self.user_token_str)
        assert self.user.is_scheduler

    # ################################################################
    # Shift list retrieval:
    # ################################################################
    def test_shifts_get_should_retrieve_list_of_shifts_for_the_specified_user(self):
        [user1, user2] = baker.make(User, _quantity=2)
        baker.make(Shift, employee=user1, _quantity=3)
        baker.make(Shift, employee=user2, _quantity=2)
        shifts1 = Shift.objects.filter(employee=user1)
        shifts2 = Shift.objects.filter(employee=user2)

        result1 = self.assert_get(url_shifts_for_user(user1), status.HTTP_200_OK)
        self.assertEqual(len(result1), shifts1.count())
        self.assertEqual(result1, ShiftSerializer(instance=shifts1, many=True).data)

        result2 = self.assert_get(url_shifts_for_user(user2), status.HTTP_200_OK)
        self.assertEqual(len(result2), shifts2.count())
        self.assertEqual(result2, ShiftSerializer(instance=shifts2, many=True).data)

        self.assertNotEqual(result1, result2)

        # If there are no shifts, it should return an empty list
        shifts2.delete()
        result2 = self.assert_get(url_shifts_for_user(user2), status.HTTP_200_OK)
        self.assertEqual(len(result2), 0)
        self.assertEqual(result2, [])

    # ################################################################
    # Shift creation:
    # ################################################################
    def test_shifts_post_should_create_an_new_shift(self):
        baker.make(Shift, employee=self.user2, _quantity=2)
        new_shift = prepare_shift(self.user2)
        params = get_shift_params(new_shift)
        response = self.assert_post(self.url_shifts, params, status.HTTP_201_CREATED)
        # Update fields from response
        new_shift.id = response['id']
        new_shift.timestamp = response['timestamp']

        new_shift_serialized = ShiftSerializer(instance=new_shift).data
        self.assertEqual(new_shift_serialized, response)

        # Makes sure the new shift is in the database
        shift_in_db = Shift.objects.get(id=new_shift.id)
        self.assertEqual(new_shift_serialized, ShiftSerializer(instance=shift_in_db).data)

        # new shift status should be "created"
        self.assertEqual(shift_in_db.status, Shift.Statuses.CREATED)
        # Should have added 1 single shift to database for the user
        self.assertEqual(Shift.objects.filter(employee=self.user2).count(), 3)

    def test_shifts_post_should_not_allow_creating_shift_with_earlier_end_time_than_start_time(self):
        start_time = datetime.now()
        end_time = start_time - timedelta(seconds=1)
        params = ShiftParams(end_time=end_time, start_time=start_time)
        self.assert_post(self.url_shifts, params, status.HTTP_400_BAD_REQUEST)

    def test_shifts_post_should_fail_to_create_shift_with_invalid_start_time(self):
        params = generate_shift_params()
        for invalid_time in invalid_times:
            params['start_time'] = invalid_time
            self.assert_post(self.url_shifts, params, status.HTTP_400_BAD_REQUEST)
        # star_time is required
        del params['start_time']
        self.assert_post(self.url_shifts, params, status.HTTP_400_BAD_REQUEST)

    def test_shifts_post_should_fail_to_create_shift_with_invalid_end_time(self):
        params = generate_shift_params()
        for invalid_time in invalid_times:
            params['end_time'] = invalid_time
            self.assert_post(self.url_shifts, params, status.HTTP_400_BAD_REQUEST)
        # end_time is required
        del params['end_time']
        self.assert_post(self.url_shifts, params, status.HTTP_400_BAD_REQUEST)

    def test_shifts_post_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.POST, self.url_shifts)

    # General api tests
    def test_shifts_should_fail_with_invalid_user_id(self):
        user = baker.prepare(User)
        # Hopping there's no user with id 1000000 :D
        invalid_ids: typing.List[typing.Any] = [-1, 0, 1000000, None, '', 'string', [], '_', '/', object]
        for invalid_id in invalid_ids:
            user.id = invalid_id
            self.assert_get(url_shifts_for_user(user), status.HTTP_404_NOT_FOUND)
            self.assert_post(url_shifts_for_user(user), {}, status.HTTP_404_NOT_FOUND)

    def test_shifts_should_fail_if_user_is_not_scheduler(self):
        employee = baker.make(User, role=User.Roles.EMPLOYEE)
        _, employee_token_str = AuthToken.objects.create(user=employee)

        # Login using employee user token
        self.set_auth_header(employee_token_str)
        self.assert_get(self.url_shifts, status.HTTP_403_FORBIDDEN)
        self.assert_post(self.url_shifts, {}, status.HTTP_403_FORBIDDEN)

    def test_shifts_should_fail_with_invalid_authentication_headers(self):
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.GET, self.url_shifts)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.POST, self.url_shifts)

    def test_shifts_should_only_accept_get_and_post(self):
        not_accepted_methods = [RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_shifts)

    def test_shifts_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_shifts)
