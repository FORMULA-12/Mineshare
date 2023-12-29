from django import template
import re

register = template.Library()


@register.filter
def paragraph(value):
    return value.replace("\n", "br")


@register.filter
def time_translate(value):
    return value + " назад"

