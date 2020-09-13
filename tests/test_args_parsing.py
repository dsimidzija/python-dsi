import dsi


def test_function_call():
    with_some = 5
    params = {"five": "and six"}
    and_var = "varval"

    def function_call(*args, **kwargs):
        return "function retval"

    dsi.d(function_call(with_some, params), "drink", and_var)


def test_regular_args_only():
    params = ["arg1", "arg2", "arg3"]
    dsi.d(*params)


def test_regular_args_first():
    params = ["arg1", "arg2", "arg3"]
    last = "is last"
    dsi.d(*params, last)


def test_regular_args_last():
    one = "is one"
    params = ["arg1", "arg2", "arg3"]
    dsi.d(one, *params)


def test_regular_args_mid():
    one = "is one"
    params = ["arg1", "arg2", "arg3"]
    last = "is last"
    dsi.d(one, *params, last)


def test_regular_args_multiple():
    one = "is one"
    params = ["arg1", "arg2", "arg3"]
    other_params = ["oth1", "oth2", "oth3"]
    last = "is last"
    dsi.d(one, *params, *other_params, last)


def test_function_call_and_args():
    one = "is one"
    params = ["arg1", "arg2", "arg3"]
    other_params = ["oth1", "oth2", "oth3"]
    last = "is last"
    dsi.d(one, *params, *other_params, last)

    def function_call(*args, **kwargs):
        return "function retval"

    dsi.d(function_call(one, "farg"), *params, "drink", last)
    dsi.d(function_call(one, "farg"), *params, "drink", *other_params, last)


def test_dict():
    dsi.d({"how": "areya", "there": "areyou"}, "okay then")


def test_list():
    dsi.d(["how", "areya", "there", "areyou"], "okay then")
