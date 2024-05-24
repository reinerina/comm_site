from django import template

register = template.Library()

@register.filter
def time_format(value):
    minutes, seconds = value.split(':')
    return f'{minutes} 分 {seconds} 秒'