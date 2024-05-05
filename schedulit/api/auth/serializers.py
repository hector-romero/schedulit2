import typing

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers

from schedulit.authentication.models import User


class UserSerializer(serializers.ModelSerializer['User']):
    instance: 'User'

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'employee_id', 'is_employee', 'is_scheduler', 'last_login', 'role')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True, 'allow_blank': False},
            'role': {'required': False, 'write_only': True, 'allow_blank': True, 'allow_null': True},
            'name': {'allow_null': True, 'required': False, 'allow_blank': True},
            'employee_id': {'allow_null': True, 'required': False, 'allow_blank': True},
            'last_login': {'read_only': True}
        }

    # Used to run some special validations in users, namely email constrains,
    # which are not supported out of the box by django-rest-framework; and password
    # which requires other fields of the user to verify rules like "UserAttributeSimilarityValidator"
    def _get_fake_user_instance(self, attrs: dict[str, typing.Any]) -> 'User':
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
                user.name = self.instance.name
            if not user.employee_id and attrs.get('employee_id') is None:
                user.employee_id = self.instance.employee_id
            # noinspection PyProtectedMember
            # pylint: disable=protected-access
            user._state.adding = False
        return user

    @staticmethod
    def validate_name(value: str) -> str:
        return value or ''

    @staticmethod
    def validate_role(value: str) -> User.Roles:
        try:
            return User.Roles(str(value).lower())
        except ValueError:
            return User.Roles.EMPLOYEE

    @staticmethod
    def validate_employee_id(value: str) -> str:
        return value or ''

    def validate_password(self, value: str) -> str:
        try:
            user = self._get_fake_user_instance(self.get_initial())
            password_validation.validate_password(password=value, user=user)
            if self.instance:
                password_validation.password_changed(password=value, user=user)
            user.set_password(raw_password=value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, attrs: dict[str, typing.Any]) -> dict[str, typing.Any]:
        super().validate(attrs)
        # Using user model validation methods mostly to apply constraints, that are not handled automatically
        # by serializers
        # https://github.com/encode/django-rest-framework/issues/7173
        user = self._get_fake_user_instance(attrs=attrs)
        user.full_clean()
        return attrs

    def create(self, validated_data: dict[str, typing.Any]) -> 'User':
        return self.Meta.model.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            name=validated_data.get('name'),
            role=validated_data.get('role'),
            employee_id=validated_data.get('employee_id'),
        )

    def update(self, instance: 'User', validated_data: dict[str, typing.Any]) -> 'User':
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        # If this is a partial update, let default update handle it
        if self.partial:
            return super().update(instance, validated_data)
        # DRF doesn't currently handle correctly non-partial updates:
        # Due to a wrong behaviour by DRF, when an optional field is provided in a PUT request, instead of being set
        # to the default value, it just retains its current value in the database, so it does a partial update.
        # This is not right, since a PUT request should be idempotent, so I'll handle that option manually

        for field in self._writable_fields:
            # Ignore password field
            if field.field_name is None or field.field_name == 'password':
                continue
            try:
                field_value = validated_data[field.field_name]

            except KeyError:
                # noinspection PyProtectedMember
                field_value = getattr(instance._meta.get_field(field.field_name), 'default', None)
            setattr(instance, field.field_name, field_value)

        instance.save()
        return instance
