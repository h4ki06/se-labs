import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


@pytest.mark.parametrize("pet_type,days,premium,expected", [
    ("cat", 3, False, 0), ("cat", 4, False, 20),
    ("dog", 2, False, 0), ("dog", 3, False, 30),
    ("rabbit", 4, False, 0), ("rabbit", 5, False, 20),
    ("cat", 4, True, 0), ("cat", 5, True, 20),
    ("dog", 3, True, 0), ("dog", 4, True, 30),
    ("rabbit", 5, True, 20),
    ("dog", 12, False, 300), ("dog", 13, False, 495),
    ("cat", 13, False, 200), ("cat", 14, False, 330),
])
def test_boarding_fee_all_decision_outcomes(pet_type, days, premium, expected):
    assert boarding_fee(pet_type, days, premium) == expected


@pytest.mark.parametrize("pet_type,days", [("parrot", 2), ("cat", -2)])
def test_boarding_fee_error_branches(pet_type, days):
    with pytest.raises(ValueError):
        boarding_fee(pet_type, days, False)


@pytest.mark.parametrize("age,vaccinations,senior,expected", [
    (8, 3, True, True), (8, 2, True, False),
    (0.5, 5, False, False), (1, 2, False, True),
    (1, 1, False, False),
])
def test_admission_all_branches(age, vaccinations, senior, expected):
    assert admission_ok(age, vaccinations, senior) is expected


@pytest.mark.parametrize("minutes,long_stay,weekend,expected", [
    (30, True, False, "open"), (29, True, False, "late"),
    (14, True, False, "closed"),
    (15, False, False, "open"), (14, False, False, "late"),
    (-1, False, False, "closed"),
    (50, False, True, "open"), (34, False, True, "late"),
    (19, False, True, "closed"),
    (50, True, True, "open"), (35, True, True, "late"),
    (34, True, True, "closed"),
])
def test_checkout_all_branches(minutes, long_stay, weekend, expected):
    assert checkout_status(minutes, long_stay, weekend) == expected
