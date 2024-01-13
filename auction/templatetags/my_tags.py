from datetime import datetime
import pytz
from django import template

register = template.Library()


@register.simple_tag(name='current_time')
def current_time():
    return pytz.utc.localize(datetime.now())
