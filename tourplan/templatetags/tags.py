from django import template
import re

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.filter
def last_two(value):
    return value[1:3]

@register.filter
def first_two(value):
    return value[:2]

@register.filter
def trans_min(value):
    return value[3:]

@register.filter
def trans(value):
    return bool(re.match(r"-[0-9]+",value))

@register.filter
def time(value):
    return bool(re.match(r"[0-9]+:[0-9]+",value))
