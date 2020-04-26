from production_scheduler.models import LineItem, Seamstress
from .models import Log, InboxReadControl
from users.models import CustomUser
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
import pytz

# Retrieve line item log from database
def retrieve_line_item_log__(line_item_id, user_id):
    # Update last event view for user
    current_datetime = make_aware(datetime.datetime.now())
    to_update = InboxReadControl.objects.filter(username=user_id, line_item_id=line_item_id).update(last_event_viewed_date=current_datetime)
    log = Log.objects.filter(line_item_id=line_item_id).order_by('publication_date')
    log_list = [event for event in log]
    return log_list


def add_log_event__(user_id, event_body, line_item_id):
    event = Log(
                line_item_id= LineItem.objects.get(pk=line_item_id),
                event_body = event_body,
                username=CustomUser.objects.get(pk=user_id),
                is_event = True
            )
    event.save()

# Create Inbox: last event read functionality
def create_inbox__(line_item_id):
    # Creating row for seamstress
    seamstress_id = LineItem.objects.get(line_item_id=line_item_id).assigned_to.seamstress_id
    seamtress_username = Seamstress.objects.get(seamstress_id=seamstress_id).username
    line_item_id_instance = LineItem.objects.get(line_item_id=line_item_id)
    new_row = InboxReadControl(username=seamtress_username,
        line_item_id=line_item_id_instance, last_event_viewed_date=make_aware(datetime.datetime.now()))
    new_row.save()
    # Creating row for all coordinators
    users = CustomUser.objects.filter(groups__name='coordinator')
    for user in users:
        new_row = InboxReadControl(username=user,
            line_item_id=line_item_id_instance, last_event_viewed_date=make_aware(datetime.datetime.now()))
        new_row.save()

# retrieve line items with new activity
def retrieve_line_items_with_new_activity(line_items, user_id):
    user = CustomUser.objects.get(id = user_id)
    new_activity_ls = []
    for item in line_items:
        last_event_viewed_date = InboxReadControl.objects.filter(username = user, line_item_id = item)[0].last_event_viewed_date
        last_publication_date = Log.objects.filter(line_item_id=item).order_by('-publication_date')[0].publication_date
        if last_publication_date >= last_event_viewed_date:
            new_activity_ls.append(True)
        else:
            new_activity_ls.append(False)
    return new_activity_ls
