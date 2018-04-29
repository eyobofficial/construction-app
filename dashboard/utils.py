from django.contrib.auth import get_user_model

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


def week_calc(date1, date2):
    pass


def weeks(date1, date2):
    range = []
    w1_dow = date1.isocalendar()[2]  # dow -> day of week

    # Get number of days left in the 1st week
    w1_days_left = 7 - w1_dow

    # Get end date of the first week (i.e. 1st Sunday)
    w1_end = date1 + datetime.timedelta(days=w1_days_left)

    # 1st week range tuple
    week_1 = (date1, w1_end)
    range.append(week_1)

    last_week_dow = date2.isocalendar()[2]
    last_week_length = last_week_dow - 1
    last_week_start_date = date2 - datetime.timedelta(days=last_week_length)
    week_last = (last_week_start_date, date2)

    next_week_start = w1_end + datetime.timedelta(days=1)
    while next_week_start < last_week_start_date:
        week_delta = datetime.timedelta(days=6)
        next_week_end = next_week_start + week_delta
        week = (next_week_start, next_week_end)
        range.append(week)
        next_week_start += datetime.timedelta(weeks=1)

    range.append(week_last)
    return range
