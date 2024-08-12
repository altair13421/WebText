import random
import string
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_date


class PasswordGenerator:

    @classmethod
    def generate(
        cls,
        length=12,
        symbols_include=True,
        numbers_include=True,
    ):
        generated = ""

        for n in range(length):
            x = random.randint(0, 94)
            generated += string.printable[x]
        if " " in generated:
            generated = generated.replace(" ", "0")
        if "\\" in generated:
            generated = generated.replace("\\", "0")
        return generated

    @classmethod
    def random(
        cls,
        length=12,
        symbols_include=True,
        numbers_include=True,
    ):
        return cls.generate(length, symbols_include, numbers_include)


def get_months_between(start_date, end_date):
    months = {}
    current_date = parse_date(start_date)
    while current_date <= parse_date(end_date):
        next_month = current_date + relativedelta(months=1)
        months[current_date.strftime("%Y-%m")] = (current_date, next_month)
        current_date = next_month
    return months
