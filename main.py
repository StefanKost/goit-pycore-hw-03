from datetime import datetime, timedelta
import random
import re


def get_days_from_today(date: str) -> int | None:
    """
    Get difference in days from today.

    :param date: date in string format "YYYY-MM-DD"
    :return: difference in days from today
    """
    try:
        initial_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print('Invalid date string: Date should be in format "YYYY-MM-DD"')
        return None

    today = datetime.now().date()
    diff = initial_date - today
    return diff.days


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """
    Generates a sorted list of unique random numbers for a lottery.

    :param min: the minimum possible number (not less than 1)
    :param max: the maximum possible number (not greater than 1000)
    :param quantity: the number of values to select
    :return: a sorted list of unique random numbers
    """

    if min < 1:
        print('Warning: min value should be equal or greater than 1')
        return []

    if max > 1000:
        print('Warning: max cannot exceeds 1000')
        return []

    if max < min:
        print('Warning: max should be less than min')
        return []

    if quantity <= 0 or quantity > (max - min + 1):
        print('Warning: quantity should be positive and do not exceed the range')
        return []

    numbers = random.sample(range(min, max + 1), quantity)
    return sorted(numbers)


def normalize_phone(phone_number: str) -> str:
    """
    Normalizes a phone number to the standard format.

    :param phone_number: raw phone number string in any format
    :return: normalized phone number string
    """

    ua_code = '38'
    ua_phone_len = 13
    prefix = '+'
    normalized_number = re.sub(r"[^\d+]", "", phone_number)

    if normalized_number.startswith(ua_code):
        normalized_number = f"{prefix}{normalized_number}"
    elif not normalized_number.startswith(prefix):
        normalized_number = f"{prefix}{ua_code}{normalized_number}"

    if normalized_number.startswith(f"{prefix}{ua_code}") and len(normalized_number) != ua_phone_len:
        raise ValueError('Invalid phone number.')
    return normalized_number


assert get_days_from_today(datetime.today().strftime('%Y-%m-%d')) == 0
assert get_days_from_today((datetime.today() + timedelta(days=10)).strftime('%Y-%m-%d')) == 10
assert get_days_from_today((datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')) == -10

assert len(get_numbers_ticket(1, 2, 1)) == 1
assert len(get_numbers_ticket(1, 3, 2)) == 2
assert len(get_numbers_ticket(2, 1, 2)) == 0

assert normalize_phone('067\\t123 4567') == '+380671234567'
assert normalize_phone('380501234567') == '+380501234567'
assert normalize_phone('+38(050)123-32-34') == '+380501233234'
try:
    normalize_phone('38050123456')
except ValueError:
    assert True
else:
    assert False
