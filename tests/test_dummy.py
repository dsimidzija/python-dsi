import dsi


def test_prints_around_pytest_capture():
    maya = "some value"
    dsi.d(maya)
    some_dict = {
        "maya": "eat stuff",
        "other": [
            "sleep",
            "yawn",
            "fart",
            "fart some more",
        ],
    }
    dsi.j(some_dict)
