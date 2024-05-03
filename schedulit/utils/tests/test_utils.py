import django.db.models.fields
from django.test import TestCase

from schedulit.utils.models import TextChoices


class SampleTestTextChoices(TextChoices):
    CHOICE1 = 'Choice1 Value 1234'
    CHOICE2 = 'Choice2 Value'


class SampleTestTextChoices2(TextChoices):
    CHOICE_SHORT = '1'
    CHOICE_LONG = '123456789'


class UtilsTest(TestCase):
    def test_choices_should_return_correct_model_field(self):
        verbose_name = 'sample_test_choices'
        model_field = SampleTestTextChoices.model_field(
            verbose_name=verbose_name, default=SampleTestTextChoices.CHOICE2)
        self.assertIsInstance(model_field, django.db.models.fields.CharField)
        self.assertEqual(model_field.verbose_name, verbose_name)
        self.assertEqual(model_field.max_length,
                         max(len(SampleTestTextChoices.CHOICE1), len(SampleTestTextChoices.CHOICE2)))
        self.assertEqual(model_field.default, SampleTestTextChoices.CHOICE2)
        self.assertEqual(model_field.choices, [(choice, value) for choice, value in SampleTestTextChoices.choices])

    def test_choices_should_return_correct_max_length(self):
        self.assertEqual(SampleTestTextChoices.max_length(),
                         max(len(SampleTestTextChoices.CHOICE1), len(SampleTestTextChoices.CHOICE2)))
        self.assertEqual(SampleTestTextChoices2.max_length(), len(SampleTestTextChoices2.CHOICE_LONG))

    def test_choices_should_serialize_correctly(self):
        self.assertEqual(SampleTestTextChoices.serialize_choices(),
                         [{'value': choice, 'label': value} for choice, value in SampleTestTextChoices.choices])
        self.assertEqual(SampleTestTextChoices2.serialize_choices(),
                         [{'value': choice, 'label': value} for choice, value in SampleTestTextChoices2.choices])
