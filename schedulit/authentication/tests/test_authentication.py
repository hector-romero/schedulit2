from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from schedulit.authentication.models import User
from schedulit.utils.tests.helpers import same_email_variations


class AuthenticationCreateUserTest(TestCase):

    @staticmethod
    def create_user(email: str, role: User.Roles = None, employee_id: str = None) -> User:
        return User.objects.create_user(email=email, name=None, password=None,
                                        role=role, employee_id=employee_id)

    def test_authentication_should_allow_to_create_user_with_valid_email(self):
        self.assertIsNotNone(self.create_user(email='test@email.com'))
        self.assertIsNotNone(self.create_user(email='test2@email.com'))

    def test_authentication_should_fail_to_create_user_with_invalid_email(self):
        self.assertRaises(ValidationError, self.create_user, email='test@email')
        self.assertRaises(ValidationError, self.create_user, email='@email.com')
        self.assertRaises(ValidationError, self.create_user, email='anythingno')
        self.assertRaises(ValidationError, self.create_user, email='12345')

    def test_authentication_should_fail_to_create_user_without_valid_email(self):
        self.assertRaises(ValidationError, self.create_user, email=None)
        self.assertRaises(ValidationError, self.create_user, email='')

    def test_authentication_should_not_allow_creating_users_with_repeated_email(self):
        self.assertIsNotNone(self.create_user(email=same_email_variations[0]))
        # It shouldn't matter if the email has different usage of upper-lower cases
        for email in same_email_variations:
            # self.assertRaises(IntegrityError, self.create_user, email=email, phone=None)
            self.assertRaises(ValidationError, self.create_user, email=email)

    def _test_employee_id(self, employee_id: str) -> None:
        user = self.create_user(email='test@email.com', employee_id=employee_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.employee_id, employee_id)

    def test_authentication_should_allow_creating_users_with_employee_id(self):
        self._test_employee_id('someemployee_id')

    def test_authentication_should_allow_creating_users_with_empty_employee_id(self):
        self._test_employee_id('')

    def test_authentication_should_not_allow_duplicated_employee_id(self):
        employee_id = 'duplicated_id'
        user1 = self.create_user(email='test@email.com', employee_id=employee_id)
        self.assertIsNotNone(user1)
        self.assertRaises(ValidationError, self.create_user, email='test2@email.com', employee_id=employee_id)

    def test_authentication_should_allow_creating_users_with_role(self):
        for role in [User.Roles.EMPLOYEE, User.Roles.SCHEDULER]:
            user = self.create_user(email=role.value + "@email.com", role=role)
            self.assertIsNotNone(user)
            self.assertEqual(user.role, role)

    def test_authentication_should_allow_creating_staff_user(self):
        user = User.objects.create_user(email="staff@email.com", is_staff=True)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_authentication_should_allow_creating_employee_user(self):
        user = User.objects.create_user(email="employee@email.com", role=User.Roles.EMPLOYEE)
        self.assertTrue(user.is_employee)
        self.assertFalse(user.is_scheduler)

    def test_authentication_should_allow_creating_employee_user_by_default(self):
        user = User.objects.create_user(email="employee_default@email.com")
        self.assertTrue(user.is_employee)
        self.assertFalse(user.is_scheduler)

    def test_authentication_should_allow_creating_scheduler_user(self):
        user = User.objects.create_user(email="scheduler@email.com", role=User.Roles.SCHEDULER)
        self.assertTrue(user.is_scheduler)
        self.assertFalse(user.is_employee)

    def test_authentication_should_allow_creating_super_user(self):
        user = User.objects.create_user(email="superuser1@email.com", is_superuser=True)
        self.assertTrue(user.is_superuser)
        # is_staff should be true for a super_user
        self.assertTrue(user.is_staff)

        user = User.objects.create_user(email="superuser3@email.com", is_superuser=True, is_staff=False)
        self.assertTrue(user.is_superuser)
        # is_staff should be true for a super_user
        self.assertTrue(user.is_staff)

        user = User.objects.create_superuser(email="superuser2@email.com")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class AuthenticationLoginTest(TestCase):
    user: User

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(email=same_email_variations[0], password='password')

    def test_should_allow_to_login_using_email(self):
        for email in same_email_variations:
            self.assertTrue(self.client.login(username=email, password='password'))

        self.assertFalse(self.client.login(username=same_email_variations[0], password='invalidpassword'))

    def test_should_not_allow_to_login_for_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.client.login(username=same_email_variations[0], password='password'))
