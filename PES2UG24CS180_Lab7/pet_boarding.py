import math

GST_RATE = 1.18


def _parse_non_negative_float(text):
    """Return a finite, non-negative float parsed from text, or None if invalid."""
    try:
        value = float(text)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(value) or value < 0:
        return None
    return value


def parse_booking(text):
    """Parse 'pet:days' into (Pet, days). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    pet = parts[0].strip()
    if not pet:
        return None
    days = _parse_non_negative_float(parts[1])
    if days is None:
        return None
    return pet.title(), days


def stay_average(days_csv):
    """Average of comma-separated whole-number stay lengths. None if invalid."""
    if not isinstance(days_csv, str):
        return None
    values = []
    for item in days_csv.split(','):
        item = item.strip()
        # ASCII digits only: rejects '', '-1', '1.5', '1_0', unicode digits
        if not (item.isascii() and item.isdigit()):
            return None
        try:
            values.append(int(item))
        except ValueError:  # absurdly long digit strings
            return None
    if not values:
        return None
    return sum(values) / len(values)


def payable_fee(text):
    """Fee after 18% tax and discount, never below 0. None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _parse_non_negative_float(parts[0])
    discount = _parse_non_negative_float(parts[1])
    if fee is None or discount is None:
        return None
    total = fee * GST_RATE - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0), 2)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result if result is not None else "Invalid input")

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", round(result, 2) if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
