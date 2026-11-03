from app.services.masking import TokenMap, mask, unmask


def roundtrip(text, enabled=None):
    t = TokenMap()
    m = mask(text, t, enabled)
    return m, unmask(m, t)


def test_phone_and_email():
    m, (back, unknown) = roundtrip("call 052-1234567 or foo@example.com")
    assert "[PHONE_1]" in m and "[EMAIL_1]" in m and "052" not in m
    assert back == "call 052-1234567 or foo@example.com" and unknown == []


def test_same_value_same_token():
    t = TokenMap()
    m = mask("050-1234567 and 050-1234567", t)
    assert m == "[PHONE_1] and [PHONE_1]"


def test_card_requires_luhn():
    assert "[CARD_1]" in mask("4111 1111 1111 1111", TokenMap())
    assert "[CARD_" not in mask("4111 1111 1111 1112", TokenMap())


def test_israeli_id_checksum():
    assert "[ID_1]" in mask("id 123456782", TokenMap())
    assert "[ID_" not in mask("id 123456789", TokenMap())


def test_toggle_off():
    m, _ = roundtrip("foo@example.com", {"email": False})
    assert m == "foo@example.com"


def test_invented_token_reported():
    t = TokenMap()
    _, unknown = unmask("Lorem [PHONE_9] ipsum", t)
    assert unknown == ["[PHONE_9]"]
