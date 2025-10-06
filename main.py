from datetime import datetime

def get_days_from_today(date: str) -> int | None:
    try:
        # Try to parse date
        initial_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print('Invalid date string: Date should be in format "YYYY-MM-DD"')
        return None

    today = datetime.now().date()
    diff = initial_date - today

    return diff.days



