"""
Creating a calendar for a daily habit
"""
from django.db.models import Max, F
from manage_hab.models import HabitProgress

def get_daily_habit_progress(user_id, habit_id, start_day, end_day):
    """
    The habit is fully fulfilled - green (number of executions >= daily goal).
    The habit is partially fulfilled - yellow  (0 <number of executions < daily goal) 
    The habit is not fulfilled - we do not return anything (number of executions == 0)
    """
    # Get a list of all the trekking for the entire period
    progress_records = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[start_day, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'), goal=F('current_goal'))
    
    progress_dict = {}
    for record in progress_records:
        date_str = record['update_time'].strftime('%Y-%m-%d')
        goal = record['goal'] or 1  # Default goal is 1 if None or 0
        if record['max_value'] >= goal:
            progress_dict[date_str] = "green"
        elif record['max_value'] > 0:
            progress_dict[date_str] = "yellow"

    result = [{date: progress_dict[date]} for date in sorted(progress_dict.keys())]
    return result
