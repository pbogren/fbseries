from fbseries.autocomplete import autocomplete


class TestAutocomplete():

    def test_returns_empty_if_no_match(self):
        name_list = ['arsenal', 'blackpool']
        result = autocomplete('k', name_list)
        expected = ""
        assert result == expected

    def test_returns_entire_name_if_only_match(self):
        name_list = "arsenal blackpool southampton".split()
        result = autocomplete('a', name_list)
        expected = 'arsenal'
        assert result == expected

    def test_returns_least_common__denominator_if_multiple_matches(self):
        name_list = "blackburn blackpool arsenal".split()
        expected = 'black'
        result = autocomplete('b', name_list)
        assert result == expected

    def test_can_take_strings_with_spaces(self):
        name_list = "man utd, Arsenal, Blackpool".split(",")
        expected = 'man utd'
        result = autocomplete('m', name_list)
        assert result == expected

    def test_keeps_case_formatting(self):
        name_list = ['Man Utd']
        expected = 'Man Utd'
        result = autocomplete('m', name_list)
        assert result == expected

    def test_name_is_substring_of_other_name(self):
        name_list = "Black Blackpool Arsenal".split()
        expected = "Black"
        result = autocomplete('b', name_list)
        assert result == expected
