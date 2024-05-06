import json
import typing

from django.test import override_settings
from django.urls import reverse, NoReverseMatch
from knox.models import AuthToken
from model_bakery import baker, random_gen
from rest_framework import status

from schedulit.api.auth.serializers import UserSerializer
from schedulit.api.tests.helpers import ApiTestCase, RequestMethods
from schedulit.api.tests.users.helpers import get_user_params, UserParams
from schedulit.authentication.models import User
from schedulit.utils.tests.helpers import same_email_variations


def url_for_user(user: User) -> str:
    try:
        return reverse('user', kwargs={'pk': user.id})
    except NoReverseMatch:
        return f'/api/users/{user.id}/'


class UserTest(ApiTestCase):
    url_user: str
    sample_user: User

    @classmethod
    def setUpTestData(cls):
        cls.initialize_users()

    def setUp(self):
        # By default, all request are authenticated by the scheduler user
        self.set_auth_header(self.user_token_str)
        assert self.user.is_scheduler
        self.sample_user = baker.make(User)
        self.url_user = url_for_user(self.sample_user)

    ################################################################
    # Retrieve user
    ################################################################
    def test_user_get_should_retrieve_user_details(self):
        response = self.assert_get(self.url_user, status.HTTP_200_OK)
        self.assertEqual(response, UserSerializer(instance=self.sample_user).data)

    ################################################################
    # Update user:
    ################################################################
    def test_user_put_should_update_the_user(self):
        update_user = baker.prepare(User, id=self.sample_user.id)
        params = get_user_params(update_user)
        response = self.assert_put(self.url_user, params, status.HTTP_200_OK)

        self.assertEqual(response, UserSerializer(instance=update_user).data)

        # Checks that the data is different from the sample user data
        self.assertNotEqual(UserSerializer(instance=self.sample_user).data, UserSerializer(instance=update_user).data)

        # Checks that the changes where updated in database
        self.sample_user.refresh_from_db()
        self.assertEqual(UserSerializer(instance=self.sample_user).data, UserSerializer(instance=update_user).data)

        # Checks that the saved password is the changed one
        assert self.sample_user.check_password(update_user.password)

    def test_user_put_should_not_detect_user_current_email_as_already_used(self):
        params = get_user_params(self.sample_user)
        for email in same_email_variations:
            params['email'] = email
            self.assert_put(self.url_user, params, status.HTTP_200_OK)
            self.sample_user.refresh_from_db()
            self.assertEqual(self.sample_user.email, email)

    def test_user_put_should_not_allow_setting_the_email_to_an_already_user_email(self):
        baker.make(User, email=same_email_variations[0])
        self.assertNotEqual(self.sample_user.email, same_email_variations[0])

        params = get_user_params(self.sample_user)
        for email in same_email_variations:
            params['email'] = email
            self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_put_should_fail_to_update_user_with_invalid_email(self):
        params = get_user_params(self.sample_user)
        invalid_emails: typing.List[typing.Any] = [
            'null', None, '1', 'any string', '', '_', '@email.com', 'something@', 'something.com'
        ]
        for invalid_email in invalid_emails:
            params['email'] = invalid_email
            self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

        # Email is required in put request
        del params['email']
        self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    # Enabling password validators in settings to verify that we actually check for that constrain too
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ])
    def test_user_put_should_fail_to_update_user_with_invalid_password(self):
        params = get_user_params(self.sample_user)
        # List includes empty values, common passwords, too short, and user attributes
        invalid_passwords: typing.List[typing.Any] = [
            '', None, 'password', '12345678', 'short', self.sample_user.email, self.sample_user.name
        ]
        for invalid_password in invalid_passwords:
            params['password'] = invalid_password
            self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

        # Password is required in put request
        del params['password']
        self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_put_should_have_name_as_optional_parameter(self):
        params = get_user_params(self.sample_user)
        valid_names: typing.List[typing.Any] = [None, 'some name', '', 'null']
        for valid_name in valid_names:
            params['name'] = valid_name
            self.assert_put(self.url_user, json.dumps(params), status.HTTP_200_OK)
            self.sample_user.refresh_from_db(fields=['name'])
            self.assertEqual(self.sample_user.name, valid_name or '')

        # Name is optional, so it should work without it, setting to empty string as default
        self.sample_user.name = random_gen.gen_string(10)
        self.sample_user.save()
        del params['name']
        self.assert_put(self.url_user, params, status.HTTP_200_OK)
        self.sample_user.refresh_from_db(fields=['name'])
        self.assertEqual(self.sample_user.name, '')

    def test_user_put_should_allow_changing_user_to_employee(self):
        params = get_user_params(self.sample_user)

        # Employee is the default role for the user, so indicating it or sending a blank value
        # should update user to an employee
        valid_roles: typing.List[typing.Any] = [User.Roles.EMPLOYEE, None, 'employee']
        for role in valid_roles:
            self.sample_user.role = User.Roles.SCHEDULER
            self.sample_user.save()
            params['role'] = role
            self.assert_put(self.url_user, params, status.HTTP_200_OK)
            self.sample_user.refresh_from_db(fields=['role'])
            assert self.sample_user.is_employee

        self.sample_user.role = User.Roles.SCHEDULER
        self.sample_user.save()
        # Role is optional
        del params['role']
        self.assert_put(self.url_user, params, status.HTTP_200_OK)
        self.sample_user.refresh_from_db(fields=['role'])
        assert self.sample_user.is_employee

    def test_user_put_should_allow_changing_user_to_scheduler(self):
        params = get_user_params(self.sample_user)
        assert self.sample_user.is_employee
        params['role'] = User.Roles.SCHEDULER
        self.assert_put(self.url_user, params, status.HTTP_200_OK)
        self.sample_user.refresh_from_db(fields=['role'])
        assert self.sample_user.is_scheduler

    def test_user_put_should_fail_with_invalid_user_role(self):
        params = get_user_params(self.sample_user)
        invalid_roles = ["anything", '1', '__']
        for invalid_role in invalid_roles:
            params['role'] = invalid_role
            self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_put_should_have_employee_id_as_optional_parameter(self):
        params = get_user_params(self.sample_user)
        valid_employee_ids = [None, 'some employee id', '', 'null']
        for valid_employee_id in valid_employee_ids:
            params['employee_id'] = valid_employee_id
            self.assert_put(self.url_user, params, status.HTTP_200_OK)
            self.sample_user.refresh_from_db(fields=['employee_id'])
            self.assertEqual(self.sample_user.employee_id, valid_employee_id or '')

        # Employee_id is optional, so it should set empty string as default if the param is not sent
        self.sample_user.employee_id = random_gen.gen_string(10)
        self.sample_user.save()
        del params['employee_id']
        self.assert_put(self.url_user, params, status.HTTP_200_OK)
        self.sample_user.refresh_from_db(fields=['employee_id'])
        self.assertEqual(self.sample_user.employee_id, '')

    def test_user_put_should_fail_to_update_user_if_employee_id_is_already_in_use_by_another_user(self):
        employee_id = random_gen.gen_string(10)
        user_with_employee_id = baker.make(User, employee_id=employee_id)
        # Sending an update to the user with the employee id should work, since it is the owner of the id
        params = get_user_params(user_with_employee_id)
        self.assert_put(url_for_user(user_with_employee_id), params, status.HTTP_200_OK)

        # Sending an update to another user, with the used employee id should fail
        self.sample_user.employee_id = employee_id
        params = get_user_params(self.sample_user)
        self.assert_put(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_put_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.PUT, self.url_user)

    ################################################################
    # Partial update user:
    ################################################################
    def assert_verify_user_in_db_for_updated_field(self, field_name: str, field_value: typing.Any,
                                                   ignore_updated_field: bool = False) -> User:
        # Checks that the change was  applied to the database
        user_in_db = User.objects.get(id=self.sample_user.id)
        if not ignore_updated_field:
            self.assertEqual(getattr(user_in_db, field_name), field_value)

        # Just making sure that only the the required field changed:
        # (should remember to exclude any field that is supposed to be updated on all saves)
        for field in user_in_db._meta.fields:
            if field.attname == field_name:
                continue
            self.assertEqual(getattr(self.sample_user, field.attname), getattr(user_in_db, field.attname))
        return user_in_db

    def test_patch_empty_should_not_update_any_field(self):
        self.assert_patch(self.url_user, {}, status.HTTP_200_OK)
        self.assert_verify_user_in_db_for_updated_field('', None, ignore_updated_field=True)

    def test_user_patch_should_allow_to_updating_user_email(self):
        new_email = random_gen.gen_email()
        params = UserParams(email=new_email)
        self.assertNotEqual(new_email, self.sample_user.email)

        self.assert_patch(self.url_user, params, status.HTTP_200_OK)
        self.assert_verify_user_in_db_for_updated_field('email', new_email)

    def test_user_patch_should_not_detect_user_current_email_as_already_used(self):
        for email in same_email_variations:
            params = UserParams(email=email)
            self.assert_patch(self.url_user, params, status.HTTP_200_OK)
            self.sample_user.refresh_from_db()
            self.assertEqual(self.sample_user.email, email)

    def test_user_patch_should_not_allow_setting_the_email_to_an_already_user_email(self):
        baker.make(User, email=same_email_variations[0])
        self.assertNotEqual(self.sample_user.email, same_email_variations[0])
        for email in same_email_variations:
            params = UserParams(email=email)
            self.assert_patch(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_patch_should_fail_to_update_user_with_invalid_email(self):
        invalid_emails: typing.List[typing.Any] = [
            'null', None, '1', 'any string', '', '_', '@email.com', 'something@', 'something.com',
            random_gen.gen_string(10000)
        ]
        for invalid_email in invalid_emails:
            params = UserParams(email=invalid_email)
            self.assert_patch(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_patch_should_allow_updating_user_password(self):
        new_password = random_gen.gen_string(10)
        assert not self.sample_user.check_password(new_password)

        self.assert_patch(self.url_user, UserParams(password=new_password), status.HTTP_200_OK)
        user_in_db = self.assert_verify_user_in_db_for_updated_field(
            'password', 'new_password', ignore_updated_field=True)

        assert user_in_db.check_password(new_password)

    # Enabling password validators in settings to verify that we actually check for that constrain too
    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ])
    def test_user_patch_should_fail_to_update_user_with_invalid_password(self):
        # List includes empty values, common passwords, too short, and user attributes
        invalid_passwords: typing.List[typing.Any] = [
            '', None, 'password', '12345678', 'short', self.sample_user.email, self.sample_user.name
        ]
        for invalid_password in invalid_passwords:
            params = UserParams(password=invalid_password)
            self.assert_patch(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_patch_should_allow_updating_user_name(self):
        random_name = random_gen.gen_string(10)
        valid_names: typing.List[typing.Any] = [None, 'some name', '', 'null', 1]
        for valid_name in valid_names:
            self.sample_user.name = random_name
            self.sample_user.save()
            self.assertNotEqual(self.sample_user.name, valid_name)
            params = UserParams(name=valid_name)
            self.assert_patch(self.url_user, params, status.HTTP_200_OK)
            # Names should be converted to str, and should default to ''
            expected_name = str(valid_name or '')
            self.assert_verify_user_in_db_for_updated_field('name', expected_name)

    def test_user_patch_should_allow_changing_user_to_employee(self):
        # Employee is the default role for the user, so indicating it or sending a blank value
        # should create an employee
        valid_roles: typing.List[typing.Any] = [User.Roles.EMPLOYEE, None, 'employee']
        for role in valid_roles:
            self.sample_user.role = User.Roles.SCHEDULER
            self.sample_user.save()
            params = UserParams(role=role)
            self.assert_patch(self.url_user, params, status.HTTP_200_OK)
            user_from_db = self.assert_verify_user_in_db_for_updated_field(
                'role', role, ignore_updated_field=True)
            assert user_from_db.is_employee

    def test_user_patch_should_allow_changing_user_to_scheduler(self):
        assert self.sample_user.is_employee
        self.assert_patch(self.url_user, UserParams(role=User.Roles.SCHEDULER), status.HTTP_200_OK)
        user_from_db = self.assert_verify_user_in_db_for_updated_field(
            'role', User.Roles.SCHEDULER, ignore_updated_field=True)
        assert user_from_db.is_scheduler

    def test_user_patch_should_fail_to_update_user_with_invalid_user_role(self):
        for invalid_role in ["anything", '1', '__']:
            self.assert_patch(self.url_user, UserParams(role=invalid_role), status.HTTP_400_BAD_REQUEST)

    def test_patch_should_allow_updating_employee_id(self):
        random_employee_id = random_gen.gen_string(10)
        valid_employee_ids = [None, 'some employee id', '', 'null']
        for valid_employee_id in valid_employee_ids:
            self.sample_user.employee_id = random_employee_id
            self.sample_user.save()
            self.assertNotEqual(self.sample_user.employee_id, valid_employee_id)
            self.assert_patch(self.url_user, UserParams(employee_id=valid_employee_id), status.HTTP_200_OK)
            # Employee ID should be converted to str, and should default to ''
            expected_employee_id = str(valid_employee_id or '')
            self.assert_verify_user_in_db_for_updated_field('employee_id', expected_employee_id)

    def test_patch_should_fail_to_update_user_if_employee_id_is_already_in_use_by_another_user(self):
        employee_id = random_gen.gen_string(10)
        user_with_employee_id = baker.make(User, employee_id=employee_id)
        # Sending an update to the user with the employee id should work, since it is the owner of the id
        params = UserParams(employee_id=employee_id)
        self.assert_patch(url_for_user(user_with_employee_id), params, status.HTTP_200_OK)

        # Sending an update to another user, with the used employee id should fail
        self.assert_patch(self.url_user, params, status.HTTP_400_BAD_REQUEST)

    def test_user_patch_should_fail_if_receiving_invalid_json(self):
        self.assert_invalid_json_params(RequestMethods.PATCH, self.url_user)

    # ################################################################
    # Delete user:
    # ################################################################
    def test_user_delete_should_remove_user(self):
        self.assert_delete(self.url_user, status.HTTP_204_NO_CONTENT)
        self.assertRaises(User.DoesNotExist, self.sample_user.refresh_from_db)

        user = baker.make(User)
        self.assert_delete(url_for_user(user), status.HTTP_204_NO_CONTENT)
        self.assertRaises(User.DoesNotExist, user.refresh_from_db)

    ################################################################
    # General api tests
    ################################################################
    def test_user_endpoint_should_fail_if_user_is_not_scheduler(self):
        employee = baker.make(User, role=User.Roles.EMPLOYEE)
        _, employee_token_str = AuthToken.objects.create(user=employee)

        # Login using employee user token
        self.set_auth_header(employee_token_str)
        self.assert_get(self.url_user, status.HTTP_403_FORBIDDEN)
        self.assert_put(self.url_user, {}, status.HTTP_403_FORBIDDEN)
        self.assert_patch(self.url_user, {}, status.HTTP_403_FORBIDDEN)
        self.assert_delete(self.url_user, status.HTTP_403_FORBIDDEN)

    def test_user_get_should_fail_with_invalid_user_id(self):
        user = baker.prepare(User)
        # Hopping there's no user with id 1000000 :D
        invalid_ids: typing.List[typing.Any] = [-1, 0, 1000000, None, '', 'string', [], '_', '/', object]
        for invalid_id in invalid_ids:
            user.id = invalid_id
            self.assert_get(url_for_user(user), status.HTTP_404_NOT_FOUND)
            self.assert_put(url_for_user(user), {}, status.HTTP_404_NOT_FOUND)
            self.assert_patch(url_for_user(user), {}, status.HTTP_404_NOT_FOUND)
            self.assert_delete(url_for_user(user), status.HTTP_404_NOT_FOUND)

    def test_user_endpoint_should_fail_with_invalid_authentication_headers(self):
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.GET, self.url_user)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.PUT, self.url_user)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.PATCH, self.url_user)
        self.assert_invalid_authentication_header_tests_for_method(RequestMethods.DELETE, self.url_user)

    def test_user_endpoint_should_not_accept_post(self):
        self.assert_not_allowed_methods([RequestMethods.POST], self.url_user)

    def test_user_should_respond_to_options(self):
        self.assert_should_respond_to_options(self.url_user)
