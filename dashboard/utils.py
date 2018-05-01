from django.contrib.auth import get_user_model
from django.utils import timezone

import datetime


def get_phantom_user(username='Deleted'):
    return get_user_model().objects.get_or_create(username=username)[0]


def status_label(**kwargs):
    btn = kwargs.get('btn', 'btn-default')
    status_message = kwargs.get('status', 'Not Available')
    output = '<span class="badge {}">{}</span>'.format(
        btn,
        status_message,
    )
    return output


def check_project_perm(user, project, perm):
    return project in user.projects_administered.all() and user.has_perm(perm)


class Week:

    def __init__(self, *args, **kwargs):

        # Get and intialize attributes
        self._start = None
        self._end = None
        self._duration = 0

        start_date = kwargs.get('start')
        if isinstance(start_date, datetime.date):
            self._start = start_date

        end_date = kwargs.get('end')
        if isinstance(end_date, datetime.date):
            self._end = end_date

        duration = kwargs.get('duration')
        if isinstance(duration, int):
            self._duration = abs(duration)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, datetime.date):
            self._start = value

    @property
    def end(self):
        if not self.start:
            return self._end
        elif self._end:
            return self._end
        else:
            return self.start + datetime.timedelta(days=self.duration)

    @end.setter
    def end(self, value):
        if isinstance(value, datetime.date) and value >= self.start:
            self._end = value
        else:
            self._end = None

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if isinstance(value, int):
            self._duration = abs(value)

    def get_all_weeks():
        pass

    def weeks(self):
        """
        Returns a list of tuples for all weeks between start and end
        Note: Weeks start on Monday and end on Sundays as per isocalendar
        """
        week_range = []
        w1_dow = self.start.isocalendar()[2]  # dow -> day of week

        # Get number of days left in the 1st week
        w1_days_left = 7 - w1_dow

        # Get end date of the first week (i.e. 1st Sunday)
        w1_end = self.start + datetime.timedelta(days=w1_days_left)

        # 1st week range tuple
        week_1 = (self.start, w1_end)
        week_range.append(week_1)

        last_week_dow = self.end.isocalendar()[2]
        last_week_length = last_week_dow - 1
        last_week_start_date = self.end - datetime.timedelta(
            days=last_week_length
        )
        week_last = (last_week_start_date, self.end)

        next_week_start = w1_end + datetime.timedelta(days=1)
        while next_week_start < last_week_start_date:
            week_delta = datetime.timedelta(days=6)
            next_week_end = next_week_start + week_delta
            week = (next_week_start, next_week_end)
            week_range.append(week)
            next_week_start += datetime.timedelta(weeks=1)

        week_range.append(week_last)
        return week_range
