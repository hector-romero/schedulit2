from django.test import TestCase


class SettingsTest(TestCase):
    # Dumb tests
    # just making sure that files are loading without error
    # since some of these files are loaded only in certain environment
    # I don't see another way to introduce these files to the test-suite
    @staticmethod
    def test_should_load_dev():
        # noinspection PyUnresolvedReferences
        import schedulit.settings.dev  # pylint: disable=import-outside-toplevel,unused-import # noqa: F401
        assert True

    @staticmethod
    def test_should_load_prod():
        # noinspection PyUnresolvedReferences
        import schedulit.settings.prod  # pylint: disable=import-outside-toplevel,unused-import # noqa: F401
        assert True

    @staticmethod
    def test_should_load_test():
        # noinspection PyUnresolvedReferences
        import schedulit.settings.test  # pylint: disable=import-outside-toplevel,unused-import # noqa: F401
        assert True
