from django import template

register = template.Library()


@register.simple_tag
def multiply(a, b):
    return a * b


@register.simple_tag
def divide(a, b):
    return int(a / b)


@register.filter
def resto(a):
    return int(a % 2)
