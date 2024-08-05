"""
Creating a calendar for a weekly habit
"""

from collections import defaultdict
from datetime import  timedelta

from django.db.models import Max

from manage_hab.models import HabitProgress, Habit
from manage_hab.services.due_dates import get_numbers_of_due_dates



def get_weekly_habit_progress(user_id, habit_id, start_day, end_day):
    """
    We work separately with each reporting week of a given period.
    For each week :
    Trekking days are green (dot on the calendar)
    Deadline days : yellow (dot on the calendar)
    If the tracking day appears, then we delete the nearest deadline 
    day of the current week
    """
    habit = Habit.objects.get(id=habit_id, user_id=user_id)
   
    # Creating a list of weeks for the reporting period
    week_periods = get_week_periods(start_day, end_day)

    # Get the ordinal numbers of the days of the week for deadlines
    numbers_due_dates = get_numbers_of_due_dates(habit.due_dates, period='week')
 
    result = defaultdict(str)

    # Get a list of all the trekking for the entire period
    all_progress = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[start_day, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'))

    progress_by_week = defaultdict(list)
    #Converting tracking habit data into a dictionary
    # {(start_week, end_week): [habit.trekking_day_1, habit.trekking_day_1]}
    # example {("2024-07-01", "2024-07-07"): ["2024-07-02", "2024-07-05"]}
    for entry in all_progress:
        update_time = entry['update_time']
        start_of_week = update_time - timedelta(days=update_time.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        progress_by_week[(start_of_week, end_of_week)].append(update_time)

    # iteration for each reporting week
    for start_week, end_week in week_periods:
        progress_dates = progress_by_week[(start_week, end_week)]

        # Creating a list of deadlines for the current week
        week_due_dates = [(start_week + timedelta(days=n)).strftime('%Y-%m-%d') for n in numbers_due_dates]

        # Deleting the nearest deadline for each tracking habit
        for date in progress_dates:
            result[date.strftime('%Y-%m-%d')] = 'green'
            if week_due_dates:
                week_due_dates.pop(0)

        # The remaining deadlines are marked as yellow
        for date in week_due_dates:
            if date not in result:
                result[date] = 'yellow'

    sorted_result = sorted(result.items())
    return [{date: color} for date, color in sorted_result]

def get_week_periods(start_day, end_day):
    """
    Getting a list of weekly periods from start_day to end_day.
    The last week is fully included
    """
    weeks = []
    current_start = start_day - timedelta(days=start_day.weekday())
    current_end = current_start + timedelta(days=6)

    while current_end <= end_day:
        weeks.append((current_start, current_end))
        current_start += timedelta(days=7)
        current_end += timedelta(days=7)
    # Check if the last period does not fully cover a week, add it
    if current_start <= end_day:
        weeks.append((current_start, current_end))

    return weeks
