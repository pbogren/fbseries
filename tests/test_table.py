from fbseries.controller import Controller


def test_returns_empty_if_no_match():
    controller = Controller()
    name_list = ['arsenal', 'blackpool']
    controller
    result = controller.autocomplete('k', name_list)
    assert not result
