import typing

from django.test import override_settings
from django.urls import reverse
from knox.models import AuthToken
from model_bakery import baker, random_gen
from rest_framework import status

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods
from schedulit.api.tests.users.helpers import get_user_params
from schedulit.authentication.models import User
from schedulit.utils.tests.helpers import same_email_variations


class UsersTest(ApiTestCase):
    url_users: str
    employee_users: typing.List[User]

    @classmethod
    def setUpTestData(cls):
        cls.url_users = reverse('users')
        cls.initialize_users()

    def setUp(self):
        # By default, all request are authenticated by the scheduler user
        self.set_auth_header(self.user_token_str)
        assert self.user.is_scheduler

    # User list retrieval:
    def test_users_get_should_retrieve_list_of_users(self):
        # Create more employees to have more users listed
        baker.make(User, role=User.Roles.EMPLOYEE, _quantity=3)
        all_users = User.objects.all()
        response = self.assert_get(self.url_users, status.HTTP_200_OK)
        self.assertEqual(len(response), all_users.count())
        self.assertEqual(response, UserSerializer(instance=all_users, many=True).data)

    # User creation
    def test_users_post_should_create_an_new_user(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        response = self.assert_post(self.url_users, params, status.HTTP_201_CREATED)

        self.assertIsNotNone(response['id'])
        # This endpoint shouldn't return a last_login value because the user was just created
        self.assertIsNone(response.get('last_login'))

        pre_user.id = response['id']
        self.assertEqual(response, UserSerializer(instance=pre_user).data)

        # Makes sure the user exists in the database
        user = User.objects.get(id=pre_user.id)
        self.assertEqual(UserSerializer(instance=user).data, UserSerializer(instance=pre_user).data)

        # Checks that the assigned password is the expected
        self.assertNotEqual(user.password, pre_user.password)
        self.assertTrue(user.check_password(pre_user.password))

        # There shouldn't be any token created for this new user
        self.assertIsNone(response.get('token'))
        self.assertFalse(AuthToken.objects.filter(user=pre_user).exists())

    def test_users_post_should_fail_to_create_user_with_duplicated_email(self):
        pre_user = baker.prepare(User, email=same_email_variations[0])
        params = get_user_params(pre_user)

        # First attempt should create ok
        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)

        for email in same_email_variations:
            params['email'] = email
            self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

    def test_users_post_should_fail_to_create_user_with_invalid_email(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        invalid_emails: typing.List[typing.Any] = [
            'null', None, '1', 'any string', '', '_', '@email.com', 'something@', 'something.com'
        ]
        for invalid_email in invalid_emails:
            params['email'] = invalid_email
            self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

        del params['email']
        self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

    # Enabling password validators in settings to verify that we actually check for that constrain too
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ])
    def test_users_post_should_fail_to_create_user_with_invalid_password(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        # List includes empty values, common passwords, too short, and user attributes
        invalid_passwords: typing.List[typing.Any] = [
            '', None, 'password', '12345678', 'short', pre_user.email, pre_user.name
        ]
        for invalid_password in invalid_passwords:
            params['password'] = invalid_password
            self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

        del params['password']
        self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

    def test_users_post_should_have_name_as_optional_parameter(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        valid_names: typing.List[typing.Any] = [None, 'some name', '', 'null']
        for valid_name in valid_names:
            params['name'] = valid_name
            self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
            user = User.objects.get(email=pre_user.email)
            self.assertEqual(user.name, valid_name or '')
            user.delete()

        # Name is optional, so it should work without it
        del params['name']

        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
        user = User.objects.get(email=pre_user.email)
        self.assertEqual(user.name, '')

    def test_users_post_should_create_employee_user(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        # Employee is the default role for the user, so indicating it or sending a blank value
        # should create an employee
        valid_roles: typing.List[typing.Any] = [User.Roles.EMPLOYEE, None, '']
        for role in valid_roles:
            params['role'] = role
            self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
            user = User.objects.get(email=pre_user.email)
            self.assertTrue(user.is_employee)
            user.delete()

        # Employee should be the default value for role if missing
        del params['role']
        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
        user = User.objects.get(email=pre_user.email)
        self.assertTrue(user.is_employee)

    def test_users_post_should_create_scheduler_user(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        params['role'] = User.Roles.SCHEDULER
        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
        user = User.objects.get(email=pre_user.email)
        self.assertTrue(user.is_scheduler)

    def test_users_post_should_fail_with_invalid_user_role(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        invalid_roles = ["anything", '1', '__']
        for invalid_role in invalid_roles:
            params['role'] = invalid_role
            self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

    def test_users_post_should_have_employee_id_as_optional(self):
        pre_user = baker.prepare(User)
        params = get_user_params(pre_user)
        valid_employee_ids = [None, 'some employee id', '', 'null']
        for valid_employee_id in valid_employee_ids:
            params['employee_id'] = valid_employee_id
            self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
            user = User.objects.get(email=pre_user.email)
            self.assertEqual(user.employee_id, valid_employee_id or '')
            user.delete()

        # Employee ID is optional, so it should work without it
        del params['employee_id']
        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)
        user = User.objects.get(email=pre_user.email)
        self.assertEqual(user.employee_id, '')

    def test_users_should_fail_if_employee_id_is_already_in_use(self):
        employee_id = random_gen.gen_string(10)
        pre_user = baker.prepare(User, employee_id=employee_id)
        params = get_user_params(pre_user)
        self.assert_post(self.url_users, params, status.HTTP_201_CREATED)

        pre_user2 = baker.prepare(User, employee_id=employee_id)
        params = get_user_params(pre_user2)
        self.assert_post(self.url_users, params, status.HTTP_400_BAD_REQUEST)

    def test_users_post_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.POST, self.url_users)

    # General api tests
    def test_users_should_fail_if_user_is_not_scheduler(self):
        employee = baker.make(User, role=User.Roles.EMPLOYEE)
        _, employee_token_str = AuthToken.objects.create(user=employee)

        # Login using employee user token
        self.set_auth_header(employee_token_str)
        self.assert_get(self.url_users, status.HTTP_403_FORBIDDEN)
        self.assert_post(self.url_users, {}, status.HTTP_403_FORBIDDEN)

    def test_users_should_fail_with_invalid_authentication_headers(self):
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.GET, self.url_users)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.POST, self.url_users)

    def test_users_should_only_accept_get_and_post(self):
        not_accepted_methods = [RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_users)

    def test_users_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_users)
