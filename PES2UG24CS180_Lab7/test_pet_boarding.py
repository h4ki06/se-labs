import math

from hypothesis import given, settings, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee

# Inputs a fuzzer should throw at every function: text, None, numbers, bytes, lists
ANY_INPUT = (
    st.text()
    | st.none()
    | st.integers()
    | st.floats(allow_nan=True, allow_infinity=True)
    | st.binary()
    | st.lists(st.integers())
)

# Text built from the characters that matter to each parser, so Hypothesis
# reaches the interesting branches (separators, signs, exponents, nan/inf).
NASTY = st.text(alphabet="0123456789.,:|-+eE_ \tabcxyzNnIiFf٠²", max_size=30)


# ---------------------------------------------------------------- parse_booking
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@given(ANY_INPUT | NASTY)
def test_parse_booking_never_raises_and_has_valid_shape(s):
    result = parse_booking(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and result[0] != ""
        and isinstance(result[1], float)
        and math.isfinite(result[1])
        and result[1] >= 0
    )


@given(
    st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1, max_size=20),
    st.integers(min_value=0, max_value=10_000),
)
def test_parse_booking_valid_roundtrip(pet, days):
    assert parse_booking(f"{pet}:{days}") == (pet.strip().title(), float(days))


@given(st.text(), st.text())
def test_parse_booking_rejects_extra_separators(a, b):
    assert parse_booking(f"{a}:{b}:3") is None


# ---------------------------------------------------------------- stay_average
@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:
        assert False, f"stay_average crashed with: {e!r}"


@given(ANY_INPUT | NASTY)
def test_stay_average_never_raises_and_is_non_negative(s):
    result = stay_average(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=50))
def test_stay_average_within_min_max(values):
    result = stay_average(",".join(map(str, values)))
    assert min(values) <= result <= max(values)


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=50))
def test_stay_average_is_true_mean(values):
    result = stay_average(",".join(map(str, values)))
    assert math.isclose(result, sum(values) / len(values), rel_tol=1e-9, abs_tol=0.01)


def test_stay_average_edge_cases():
    for bad in ["", ",", "1,,3", "one,two", "1,2,", "-1,5", "1.5,2", None]:
        assert stay_average(bad) is None


# ----------------------------------------------------------------- payable_fee
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"


@given(ANY_INPUT | NASTY)
def test_payable_fee_never_raises_and_is_non_negative(s):
    result = payable_fee(s)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
)
def test_payable_fee_valid_inputs(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert result >= 0
    assert math.isclose(result, max(fee * 1.18 - discount, 0), abs_tol=0.01)


def test_payable_fee_edge_cases():
    for bad in ["", "|", "100", "100|", "|5", "1|2|3", "abc|1", "nan|1", "1|nan",
                "inf|1", "1|inf", "-100|5", "100|-5", "1e999|1", "1.7e308|0", None]:
        assert payable_fee(bad) is None
    assert payable_fee("1500|100") == 1670.0
    assert payable_fee("10|1000") == 0.0
