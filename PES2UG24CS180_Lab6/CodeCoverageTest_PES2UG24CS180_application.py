import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


@pytest.mark.parametrize("pet_type,days,premium,expected", [
    ("cat", 1, False, 0),
    ("dog", 2, False, 0),
    ("rabbit", 4, True, 0),
    ("cat", 4, False, 20),
    ("cat", 5, True, 20),
    ("dog", 4, False, 60),
    ("dog", 4, True, 30),
    ("rabbit", 6, False, 40),
    ("cat", 14, False, 330),
    ("dog", 13, False, 495),
])
def test_boarding_fee_valid_scenarios(pet_type, days, premium, expected):
    assert boarding_fee(pet_type, days, premium) == expected


@pytest.mark.parametrize("pet_type,days", [("bird", 3), ("cat", -1)])
def test_boarding_fee_invalid_inputs(pet_type, days):
    with pytest.raises(ValueError):
        boarding_fee(pet_type, days, False)


@pytest.mark.parametrize("age,vaccinations,senior,expected", [
    (4, 2, False, True),
    (4, 1, False, False),
    (0.5, 3, False, False),
    (10, 3, True, True),
    (10, 2, True, False),
])
def test_admission_decisions(age, vaccinations, senior, expected):
    assert admission_ok(age, vaccinations, senior) is expected


@pytest.mark.parametrize("minutes,long_stay,weekend,expected", [
    (30, False, False, "open"),
    (15, False, False, "open"),
    (14, False, False, "late"),
    (-1, False, False, "closed"),
    (50, True, False, "open"),
    (29, True, False, "late"),
    (14, True, False, "closed"),
    (50, False, True, "open"),
    (34, False, True, "late"),
    (19, False, True, "closed"),
])
def test_checkout_status_scenarios(minutes, long_stay, weekend, expected):
    assert checkout_status(minutes, long_stay, weekend) == expected
