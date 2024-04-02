from django.db import models


# Text Choices enum type with a max_length method to use when defining model fields:
# field = models.CharField(max_length=choices.max_length(), choices=choices())
class TextChoices(models.TextChoices):
    @classmethod
    def max_length(cls) -> int:
        return max(len(value) for value in cls.values)

    @classmethod
    def model_field(cls, verbose_name: str = None, default: 'TextChoices' = None) -> models.CharField:
        return models.CharField(verbose_name=verbose_name, max_length=cls.max_length(),
                                choices=cls.choices, default=default)

    @classmethod
    def serialize_choices(cls):
        return [{'value': value, 'label': label} for value, label in cls.choices]
