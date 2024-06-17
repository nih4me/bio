from django import template
from datetime import datetime
import re

register = template.Library()

@register.filter
def str_date_format(value, format):
    output_date = ''
    try:
        d = datetime.strptime(value, '%Y-%m-%d')
        output_date = d.strftime('%Y')
    except Exception as e:
        print(e)
        output_date = 'Undefined'
    return output_date

@register.filter
def estimate_reading_time(text, wpm=200) -> int:
    total_words = len(re.findall(r'\w+', text))
    time_minute = total_words // wpm + 1
    if time_minute == 0:
        time_minute = 1
    elif time_minute > 60:
        return str(time_minute // 60) + 'h'
    mn_str = 'minute'
    if time_minute > 1:
        mn_str = f'{mn_str}s'
    return f'{str(time_minute)} {mn_str}'