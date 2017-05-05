from django.db.models import Count
import datetime, collections

from models import Applicant

def get_analytics(start_date, end_date):
    analytic_metrics = collections.OrderedDict()
    week_start = start_date
    weekd_end = end_date
    workflow_state_counts = Applicant.objects.filter(
        application_date__range=(
        week_start, weekd_end)).values(
        'workflow_state').annotate(count=Count('workflow_state'))
    if workflow_state_counts:     
        weekly_workflow_stats = {}
        for state in workflow_state_counts:
            weekly_workflow_stats[state['workflow_state']] = state['count']
    week_key = '%s-%s' % (str(week_start), str(weekd_end))

    if weekly_workflow_stats:
        analytic_metrics[week_key] = weekly_workflow_stats

    return analytic_metrics