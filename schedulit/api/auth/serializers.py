from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions
from rest_framework.settings import api_settings

from schedulit.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    instance: 'User'

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'employee_id', 'is_employee', 'is_scheduler', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True, 'allow_blank': False},
        }

    # Used to run some special validations in users, namely email constrains,
    # which are not supported out of the box by django-rest-framework; and password
    # which requires other fields of the user to verify rules like "UserAttributeSimilarityValidator"
    def _get_fake_user_instance(self, attrs: dict):
        user = self.Meta.model.objects.construct_user(
            email=attrs.get('email'),
            password=attrs.get('password'),
            name=attrs.get('name'),
            role=attrs.get('role'),
            employee_id=attrs.get('employee_id')
        )
        if self.instance:
            user.id = self.instance.id
            if not user.email and attrs.get('email') is None:
                user.email = self.instance.email
            if not user.name and attrs.get('name') is None:
                user.email = self.instance.name
            if not user.role and attrs.get('role') is None:
                user.role = self.instance.role
            if not user.employee_id and attrs.get('employee_id') is None:
                user.employee_id = self.instance.employee_id
            # noinspection PyProtectedMember
            # pylint: disable=protected-access
            user._state.adding = False
        return user

    def validate_password(self, value: str) -> str:
        try:
            user = self._get_fake_user_instance(self.get_initial())
            # user.validate_password(password=value)
            user.set_password(raw_password=value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs: dict) -> dict:
        super().validate(attrs)
        # Using user model validation methods mostly to apply constraints, that are not handled automatically
        # by serializers
        # https://github.com/encode/django-rest-framework/issues/7173
        user = self._get_fake_user_instance(attrs=attrs)
        user.full_clean()
        return attrs

    def create(self, validated_data: dict):
        try:
            return self.Meta.model.objects.create_user(
                email=validated_data.get('email'),
                password=validated_data.get('password'),
                name=validated_data.get('name'),
                role=validated_data.get('role'),
                employee_id=validated_data.get('employee_id'),
            )
        except ValidationError as e:
            raise exceptions.ValidationError({api_settings.NON_FIELD_ERRORS_KEY: e.messages})
