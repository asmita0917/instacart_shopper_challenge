from django.db.models import Count
import collections
from datetime import datetime, timedelta
from models import Applicant


def get_analytics(start_date, end_date):
    analytic_metrics = collections.OrderedDict()

    report_start_date = start_date - timedelta(days=start_date.weekday())
    report_end_date = end_date + timedelta(days=6 - end_date.weekday())
    week_start = report_start_date
    while week_start < report_end_date:
        weekly_workflow_stats = None
        week_end = week_start + timedelta(days=6)
        week_key = '%s-%s' % (str(week_start), str(week_end))
        
        workflow_state_counts = Applicant.objects.filter(
            application_date__range=(
            week_start, week_end)).values(
            'workflow_state').annotate(
            count=Count('workflow_state'))
        if workflow_state_counts:     
            weekly_workflow_stats = {}
            for state in workflow_state_counts:
                weekly_workflow_stats[state['workflow_state']] = state['count']        

        if weekly_workflow_stats:
            analytic_metrics[week_key] = weekly_workflow_stats

        week_start = week_start + timedelta(days=7)

    return analytic_metrics