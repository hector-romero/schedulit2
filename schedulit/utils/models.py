import typing

from django.db import models

from django.utils.translation import gettext_lazy as _

if typing.TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise


# Text Choices enum type with a max_length method to use when defining model fields:
# field = models.CharField(max_length=choices.max_length(), choices=choices())
class TextChoices(models.TextChoices):
    @classmethod
    def max_length(cls) -> int:
        return max(len(value) for value in cls.values)

    @classmethod
    def model_field(cls, verbose_name: 'StrOrPromise' = None, default: 'TextChoices' = None) -> models.CharField:
        return models.CharField(verbose_name=verbose_name, max_length=cls.max_length(),
                                choices=cls.choices, default=default)

    @classmethod
    def serialize_choices(cls):
        return [{'value': value, 'label': label} for value, label in cls.choices]


class TimestampedModel(models.Model):
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)

    class Meta:
        abstract = True
