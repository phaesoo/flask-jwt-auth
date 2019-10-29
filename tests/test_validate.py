from app.utils.validate import check_username, check_password, check_email


def test_check_username():
    valid_list = [
        "testusername",
        "testusername55",
    ]
    for valid in valid_list:
        is_valid, _ = check_username(valid)
        assert is_valid is True

    invalid_length = [
        "asd",
        "asdjlkasjdlkmlkq3mdlkmaslkdalksmdlkasd",
    ]
    for invalid in invalid_length:
        is_valid, _ = check_password(invalid)
        assert is_valid is False

    invalid_list = [
        "1testusername",
        "Testusername",
        "testusername!",
    ]
    for invalid in invalid_list:
        is_valid, _ = check_password(invalid)
        assert is_valid is False


def test_check_password():
    valid_list = [
        "Rr6#?1d",
        "dD/*23aasdEasd",
    ]
    for valid in valid_list:
        is_valid, _ = check_password(valid)
        assert is_valid is True

    invalid_length = [
        "Rr%1",
        "Rr%1aoisdjo8132jaiosdoiasmodmaosidm",
    ]
    for invalid in invalid_length:
        is_valid, _ = check_password(invalid)
        assert is_valid is False

    invalid_list = [
        "asudhaosudho",
        "ASUDNIUWNDWOIN",
        "12739898a",
        "quwdnSAKJDH12"
    ]
    for invalid in invalid_list:
        is_valid, _ = check_password(invalid)
        assert is_valid is False


def test_check_email():
    valid_list = [
        "test_email@email.com",
        "test_email55@email.com",
    ]
    for valid in valid_list:
        is_valid, _ = check_email(valid)
        assert is_valid is True

    invalid_list = [
        "test_email@@email.com",
        "test_email@email",
    ]
    for invalid in invalid_list:
        is_valid, _ = check_email(invalid)
        assert is_valid is False