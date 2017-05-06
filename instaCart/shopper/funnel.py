from django.db.models import Count
import collections
from datetime import datetime, timedelta
from models import Applicant
from django.core.cache import cache

def get_cache_key(week_start, week_end):
    return '%s-%s' % (str(week_start), str(week_end))


def get_analytics(start_date, end_date):
    analytic_metrics = collections.OrderedDict()
    # Calculate the nearest previous Monday of the start date
    # And nearest next Sunday of the end date
    report_start_date = start_date - timedelta(days=start_date.weekday())
    report_end_date = end_date + timedelta(days=6 - end_date.weekday())
    week_start = report_start_date

    # Loop through all the weeks and collect stats
    while week_start < report_end_date:
        weekly_workflow_stats = None
        week_end = week_start + timedelta(days=6)
        week_key = get_cache_key(week_start, week_end)

        # Try to fetch stats from cache
        weekly_workflow_stats = cache.get(week_key)
        if not weekly_workflow_stats:
            # If missed then query database
            workflow_state_counts = Applicant.objects.filter(
                application_date__range=(
                week_start, week_end)).values(
                'workflow_state').annotate(
                count=Count('workflow_state'))
            weekly_workflow_stats = {}
            # Calculate workflow_stats
            if workflow_state_counts:     
                for state in workflow_state_counts:
                    weekly_workflow_stats[state['workflow_state']] = state['count']
            # And set the cache
            cache.set(week_key, weekly_workflow_stats)
        
        # If there are entries then populate the result set
        if weekly_workflow_stats:
            analytic_metrics[week_key] = weekly_workflow_stats

        # Advance to next week
        week_start = week_start + timedelta(days=7)

    return analytic_metrics

def invalidate_cache(date):
    # Utility function to invalidate cache of the week in which the date falls
    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=6)
    week_key = get_cache_key(week_start, week_end)
    cache.delete(week_key)