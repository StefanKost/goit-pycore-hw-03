from datetime import datetime
import random


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