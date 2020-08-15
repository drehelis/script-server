from unittest import TestCase

from parameterized import parameterized

from scheduling.schedule_config import ScheduleConfig
from utils import date_utils


def to_datetime(short_datetime_string):
    dt_string = short_datetime_string + ':0.000000Z'
    return date_utils.parse_iso_datetime(dt_string.replace(' ', 'T'))


class TestGetNextTime(TestCase):
    @parameterized.expand([
        ('2020-03-19 11:30', '2020-03-15 16:13', 1, 'days', '2020-03-19 16:13'),
        ('2020-03-19 17:30', '2020-03-15 16:13', 1, 'days', '2020-03-20 16:13'),
        ('2020-03-15 11:30', '2020-03-15 16:13', 1, 'days', '2020-03-15 16:13'),
        ('2020-03-14 11:30', '2020-03-15 16:13', 1, 'days', '2020-03-15 16:13'),
        ('2020-03-15 16:13', '2020-03-15 16:13', 1, 'days', '2020-03-15 16:13'),
        ('2020-03-15 16:14', '2020-03-15 16:13', 1, 'days', '2020-03-16 16:13'),
        ('2020-03-19 11:30', '2020-03-15 16:13', 2, 'days', '2020-03-19 16:13'),
        ('2020-03-20 11:30', '2020-03-15 16:13', 2, 'days', '2020-03-21 16:13'),
        ('2020-03-19 16:13', '2020-03-15 16:13', 2, 'days', '2020-03-19 16:13'),
        ('2020-03-18 11:30', '2020-03-15 16:13', 5, 'days', '2020-03-20 16:13'),
        ('2020-03-20 11:30', '2020-03-15 16:13', 24, 'days', '2020-04-08 16:13'),
        ('2020-04-09 11:30', '2020-03-15 16:13', 24, 'days', '2020-05-02 16:13'),
        ('2020-03-19 11:30', '2020-03-15 16:13', 1, 'hours', '2020-03-19 12:13'),
        ('2020-03-19 17:30', '2020-03-15 16:13', 1, 'hours', '2020-03-19 18:13'),
        ('2020-03-15 11:30', '2020-03-15 16:13', 1, 'hours', '2020-03-15 16:13'),
        ('2020-03-14 11:30', '2020-03-15 16:13', 1, 'hours', '2020-03-15 16:13'),
        ('2020-03-15 16:13', '2020-03-15 16:13', 1, 'hours', '2020-03-15 16:13'),
        ('2020-03-15 16:14', '2020-03-15 16:13', 1, 'hours', '2020-03-15 17:13'),
        # big difference between start and now
        ('2023-08-29 16:14', '2020-03-15 16:13', 1, 'hours', '2023-08-29 17:13'),
        ('2020-03-19 10:30', '2020-03-15 16:13', 2, 'hours', '2020-03-19 12:13'),
        ('2020-03-19 11:30', '2020-03-15 16:13', 2, 'hours', '2020-03-19 12:13'),
        ('2020-03-19 16:13', '2020-03-15 16:13', 2, 'hours', '2020-03-19 16:13'),
        ('2020-03-18 11:30', '2020-03-15 16:13', 5, 'hours', '2020-03-18 14:13'),
        ('2020-03-20 11:30', '2020-03-15 16:13', 24, 'hours', '2020-03-20 16:13'),
        ('2020-04-09 17:30', '2020-03-15 16:13', 24, 'hours', '2020-04-10 16:13'),
        ('2020-03-19 11:30', '2020-03-15 16:13', 1, 'months', '2020-04-15 16:13'),
        ('2020-03-19 17:30', '2020-03-15 16:13', 1, 'months', '2020-04-15 16:13'),
        ('2020-03-15 11:30', '2020-03-15 16:13', 1, 'months', '2020-03-15 16:13'),
        ('2020-03-14 11:30', '2020-03-15 16:13', 1, 'months', '2020-03-15 16:13'),
        ('2020-03-15 16:13', '2020-03-15 16:13', 1, 'months', '2020-03-15 16:13'),
        ('2020-03-15 16:14', '2020-03-15 16:13', 1, 'months', '2020-04-15 16:13'),
        ('2020-04-01 16:11', '2020-03-31 16:13', 1, 'months', '2020-04-30 16:13'),
        ('2021-01-31 20:00', '2021-01-31 16:13', 1, 'months', '2021-02-28 16:13'),  # Roll to February
        ('2020-01-31 20:00', '2020-01-31 16:13', 1, 'months', '2020-02-29 16:13'),  # Roll to February leap year
        ('2020-03-19 10:30', '2020-03-15 16:13', 2, 'months', '2020-05-15 16:13'),
        ('2020-04-19 11:30', '2020-03-15 16:13', 2, 'months', '2020-05-15 16:13'),
        ('2020-03-15 16:13', '2020-03-15 16:13', 2, 'months', '2020-03-15 16:13'),
        ('2020-04-01 16:11', '2020-03-31 16:13', 2, 'months', '2020-05-31 16:13'),
        ('2020-03-18 11:30', '2020-03-15 16:13', 5, 'months', '2020-08-15 16:13'),
        ('2020-08-18 11:30', '2020-03-15 16:13', 5, 'months', '2021-01-15 16:13'),
        ('2021-01-18 11:30', '2020-03-15 16:13', 5, 'months', '2021-06-15 16:13'),
        ('2020-03-16 11:30', '2020-03-15 16:13', 13, 'months', '2021-04-15 16:13'),
        ('2020-03-19 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-20 16:13', ['monday', 'friday']),
        ('2020-03-15 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-16 16:13', ['monday', 'friday']),
        ('2020-03-16 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-16 16:13', ['monday', 'friday']),
        ('2020-03-16 16:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-20 16:13', ['monday', 'friday']),
        ('2020-03-20 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-20 16:13', ['monday', 'friday']),
        ('2020-04-04 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-06 16:13', ['monday', 'friday']),
        ('2020-04-07 11:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'friday']),
        ('2020-03-16 16:13', '2020-03-16 16:13', 1, 'weeks', '2020-03-16 16:13', ['monday', 'friday']),
        ('2020-03-16 16:14', '2020-03-16 16:13', 1, 'weeks', '2020-03-20 16:13', ['monday', 'friday']),
        # Test for testing start date on different weekdays, now tuesday
        ('2020-04-07 1:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 2:30', '2020-03-16 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 3:30', '2020-03-17 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 4:30', '2020-03-18 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 5:30', '2020-03-19 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 6:30', '2020-03-20 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-07 7:30', '2020-03-21 16:13', 1, 'weeks', '2020-04-08 16:13', ['monday', 'wednesday', 'friday']),
        # Test for testing start date on different weekdays, now thursday
        ('2020-04-09 1:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 2:30', '2020-03-16 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 3:30', '2020-03-17 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 4:30', '2020-03-18 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 5:30', '2020-03-19 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 6:30', '2020-03-20 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-09 7:30', '2020-03-21 16:13', 1, 'weeks', '2020-04-10 16:13', ['monday', 'wednesday', 'friday']),
        # Test for testing start date on different weekdays, now saturday
        ('2020-04-11 1:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 2:30', '2020-03-16 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 3:30', '2020-03-17 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 4:30', '2020-03-18 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 5:30', '2020-03-19 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 6:30', '2020-03-20 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-11 7:30', '2020-03-21 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        # Test for testing start date on different weekdays, now monday
        ('2020-04-13 1:30', '2020-03-15 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 2:30', '2020-03-16 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 3:30', '2020-03-17 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 4:30', '2020-03-18 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 5:30', '2020-03-19 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 6:30', '2020-03-20 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        ('2020-04-13 7:30', '2020-03-21 16:13', 1, 'weeks', '2020-04-13 16:13', ['monday', 'wednesday', 'friday']),
        # Test for testing start date on different weekdays, now wednesday, when larger interval
        ('2020-09-16 1:30', '2020-03-14 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 2:30', '2020-03-15 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 3:30', '2020-03-16 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 4:30', '2020-03-17 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 5:30', '2020-03-18 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 6:30', '2020-03-19 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-09-16 7:30', '2020-03-20 16:13', 1, 'weeks', '2020-09-19 16:13', ['tuesday', 'saturday']),
        ('2020-03-16 16:30', '2020-03-15 16:13', 1, 'weeks', '2020-03-18 16:13', ['wednesday']),
        ('2020-03-19 11:30', '2020-03-15 16:13', 2, 'weeks', '2020-03-23 16:13', ['monday', 'friday']),
        ('2020-03-24 11:30', '2020-03-15 16:13', 2, 'weeks', '2020-03-27 16:13', ['monday', 'friday']),
        ('2020-06-07 17:30', '2020-03-15 16:13', 2, 'weeks', '2020-06-15 16:13', ['monday', 'friday']),
        ('2020-06-07 17:30', '2020-03-15 16:13', 2, 'weeks', '2020-06-16 16:13', ['tuesday', 'wednesday']),
    ])
    def test_next_day_when_repeatable(self, now_dt, start, period, unit, expected, weekdays=None):
        date_utils._mocked_now = to_datetime(now_dt)

        config = ScheduleConfig(True, to_datetime(start))
        config.repeat_period = period
        config.repeat_unit = unit
        config.weekdays = weekdays

        next_time = config.get_next_time()
        self.assertEqual(to_datetime(expected), next_time)

    def tearDown(self) -> None:
        super().tearDown()

        date_utils._mocked_now = None