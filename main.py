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


def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Generate a list of users whose birthdays occur within the next 7 days. Returns congratulation dates
    :param users: List of users with (name and birthday)
    :return: List of users whose birthday withing next 7 days with congratulation date
    """
    today = datetime.today().date()
    upcoming_birthdays = []
    shift_days = {5: 2, 6: 1}  # Saturday - +2 days, Sunday - +1 day

    def get_next_birthday(bday: datetime.date) -> datetime.date:
        """
        Return the next birthday date for a given birthday

        :param bday: user's birthday
        :return: next birthday date
        """
        start_year = today.year
        while True:
            try:
                bday_this_year = bday.replace(year=start_year)
            except ValueError:
                # Handle Feb 29 in non-leap years by celebrating on March 1
                bday_this_year = datetime(today.year, 3, 1).date()

            if bday_this_year >= today:
                return bday_this_year

            start_year += 1

    for user in users:
        try:
            birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        except ValueError:
            print(f"User {user['name']} has invalid birthday")
            continue

        # change year
        birthday = get_next_birthday(birthday)

        # Calculate days until the next birthday
        days_until_birthday = get_days_from_today(birthday.strftime("%Y-%m-%d"))

        if days_until_birthday is None or days_until_birthday > 7:
            continue

        # shift congratulation day to Monday if birthday on Saturday and Sunday
        congratulation_date = birthday + timedelta(days=shift_days.get(birthday.weekday(), 0))

        upcoming_birthdays.append({
            "name": user["name"],
            "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
        })

    return upcoming_birthdays


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

assert len(get_upcoming_birthdays([
    {"name": "John Doe", "birthday": (datetime.today() - timedelta(days=(years := 25) * 365 + years // 4)).strftime('%Y.%m.%d') },
    {"name": "Jane Smith", "birthday": (datetime.today() - timedelta(days=(years := 35) * 365 + years // 4 + 100)).strftime('%Y.%m.%d') },
])) == 1
