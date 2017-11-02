import pytest

from fbseries.controller import Controller


class TestAutocomplete():

    @pytest.fixture
    def app(self):
        controller = Controller()
        return controller

    def test_returns_empty_if_no_match(self, app):
        name_list = ['arsenal', 'blackpool']
        result = app.autocomplete('k', name_list)
        expected = ""
        assert result == expected

    def test_returns_entire_name_if_only_match(self, app):
        name_list = ['arsenal', 'blackpool']
        result = app.autocomplete('a', name_list)
        expected = 'arsenal'
        assert result == expected

    def test_returns_least_common__denominator_if_multiple_matches(self, app):
        name_list = ['blackburn', 'blackpool']
        expected = 'black'
        result = app.autocomplete('b', name_list)
        assert result == expected

    def test_can_take_strings_with_spaces(self, app):
        name_list = ['man utd']
        expected = 'man utd'
        result = app.autocomplete('m', name_list)
        assert result == expected

    def test_keeps_case_formatting(self, app):
        name_list = ['Man Utd']
        expected = 'Man Utd'
        result = app.autocomplete('m', name_list)
        assert result == expected
