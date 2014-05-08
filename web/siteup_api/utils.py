from django.utils.translation import ugettext, ugettext_lazy as _


def timedelta_to_string(td):
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 24 * 60 * 60)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return (_("{} days, {} hours and {} minutes").format(days, hours, minutes))
    elif hours:
        return (_("{} hours and {} minutes").format(hours, minutes))
    else:
        return (_("{} minutes").format(minutes))
