import typing

from django.test import override_settings
from django.urls import reverse
from knox.auth import TokenAuthentication
from model_bakery import baker, random_gen
from rest_framework import status

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods

from schedulit.authentication.models import User


def get_register_params(email: str, password: str, name: str, role: User.Roles | str, employee_id: str) \
        -> dict[str, typing.Any]:
    return {
        "email": email,
        "password": password,
        "name": name,
        "role": role,
        "employee_id": employee_id
    }


def get_register_params_for_user(user: User) -> dict[str, typing.Any]:
    return get_register_params(user.email, user.password, user.name, user.role, user.employee_id)


class LogoutTest(ApiTestCase):
    url_register: str

    @classmethod
    def setUpTestData(cls):
        cls.url_register = reverse('account_register')

    def test_register_should_register_an_user(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        response = self.assert_post(self.url_register, params, status.HTTP_200_OK)

        pre_user.id = response['user']['id']
        pre_user.last_login = response['user']['last_login']
        self.assertEqual(response['user'], UserSerializer(instance=pre_user).data)

        # Makes sure the user exists in the database
        user = User.objects.get(id=pre_user.id)
        self.assertEqual(UserSerializer(instance=user).data, UserSerializer(instance=pre_user).data)

        # Checks that the assigned password is the expected
        self.assertNotEquals(user.password, pre_user.password)
        self.assertTrue(user.check_password(pre_user.password))

        # The token should be linked to the user
        user_from_token, _ = TokenAuthentication().authenticate_credentials(response['token'].encode())
        self.assertEqual(user, user_from_token)

    def test_register_should_fail_to_register_user_with_duplicated_email(self):
        same_email = [
            'test@email.com',
            'TEST@email.com',
            'test@EMAIL.com',
            'TEST@EMAIL.COM',
        ]
        pre_user = baker.prepare(User, email=same_email[0])
        params = get_register_params_for_user(pre_user)

        # First attempt should register ok
        self.assert_post(self.url_register, params, status.HTTP_200_OK)

        for email in same_email:
            params['email'] = email
            self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

    def test_register_should_fail_to_register_user_with_invalid_email(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        invalid_emails = [
            'null', None, '1', 'any string', '', '_', '@email.com', 'something@', 'something.com'
        ]
        for invalid_email in invalid_emails:
            params['email'] = invalid_email
            self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

        del params['email']
        self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

    # Enabling password validators in settings to verify that we actually check for that constrain too
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ])
    def test_register_should_fail_to_register_user_with_invalid_password(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        # List includes empty values, common passwords, too short, and user attributes
        invalid_passwords = [
            '', None, 'password', '12345678', 'short', pre_user.email, pre_user.name
        ]
        for invalid_password in invalid_passwords:
            params['password'] = invalid_password
            self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

        del params['password']
        self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

    def test_register_should_have_name_as_optional(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        valid_names = [None, 'some name', '', 'null']
        for valid_name in valid_names:
            params['name'] = valid_name
            self.assert_post(self.url_register, params, status.HTTP_200_OK)
            user = User.objects.get(email=pre_user.email)
            self.assertEqual(user.name, valid_name or '')
            user.delete()

        # Name is optional, so it should work without it
        del params['name']
        self.assert_post(self.url_register, params, status.HTTP_200_OK)
        user = User.objects.get(email=pre_user.email)
        self.assertEqual(user.name, '')

    def test_register_should_register_employee_user(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        # Employee is the default role for the user, so indicating it or sending a blank value
        # should create an employee
        valid_roles = [User.Roles.EMPLOYEE, None, '']
        for role in valid_roles:
            params['role'] = role
            self.assert_post(self.url_register, params, status.HTTP_200_OK)
            user = User.objects.get(email=pre_user.email)
            self.assertTrue(user.is_employee)
            user.delete()

        # Employee should be the default value for role if missing
        del params['role']
        self.assert_post(self.url_register, params, status.HTTP_200_OK)
        user = User.objects.get(email=pre_user.email)
        self.assertTrue(user.is_employee)

    def test_register_should_register_scheduler_user(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        params['role'] = User.Roles.SCHEDULER
        self.assert_post(self.url_register, params, status.HTTP_200_OK)
        user = User.objects.get(email=pre_user.email)
        self.assertTrue(user.is_scheduler)

    def test_register_should_fail_with_invalid_user_role(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        invalid_roles = ["anything", '1', '__']
        for invalid_role in invalid_roles:
            # noinspection PyTypedDict
            params['role'] = invalid_role
            self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

    def test_register_should_have_employee_id_as_optional(self):
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        valid_employee_ids = [None, 'some employee id', '', 'null']
        for valid_employee_id in valid_employee_ids:
            params['employee_id'] = valid_employee_id
            self.assert_post(self.url_register, params, status.HTTP_200_OK)
            user = User.objects.get(email=pre_user.email)
            self.assertEqual(user.employee_id, valid_employee_id or '')
            user.delete()

        # Name is optional, so it should work without it
        del params['employee_id']
        self.assert_post(self.url_register, params, status.HTTP_200_OK)
        user = User.objects.get(email=pre_user.email)
        self.assertEqual(user.employee_id, '')

    def test_register_should_fail_if_employee_id_is_already_in_use(self):
        employee_id = random_gen.gen_string(10)
        pre_user = baker.prepare(User)
        params = get_register_params_for_user(pre_user)
        params['employee_id'] = employee_id
        self.assert_post(self.url_register, params, status.HTTP_200_OK)

        pre_user2 = baker.prepare(User)
        params = get_register_params_for_user(pre_user2)
        params['employee_id'] = employee_id
        self.assert_post(self.url_register, params, status.HTTP_400_BAD_REQUEST)

    def test_register_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.POST, self.url_register)

    def test_register_should_only_accept_post(self):
        not_accepted_methods = [RequestMethods.GET, RequestMethods.PATCH, RequestMethods.PATCH, RequestMethods.DELETE]
        self.assert_not_allowed_methods(not_accepted_methods, self.url_register)

    def test_register_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_register)
