# coding: utf-8
from __future__ import unicode_literals
from datetime import date, timedelta
from itertools import groupby

from django import template
from django.template.defaultfilters import date as date_filter
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


def date_range(start, end):
    date = start
    while date <= end:
        yield date
        date = date + timedelta(days=1)


@register.simple_tag(name='calendar')
def calendar(booking_list):
    start = date.today()
    end = date.today() + timedelta(days=14)

    bookings = groupby(booking_list, lambda b: b.date)
    bookings_by_day = {}
    for day, bookings_for_day in bookings:
        bookings_by_day[day] = list(bookings_for_day)

    output = []
    for d in date_range(start, end):
        if d < date.today():
            output.append(format_html('<h4 class="page-header text-muted">{}</h4>', date_filter(d, 'l j \d\e F')))
        elif d == date.today():
            output.append(format_html('<h4 class="page-header text-warning"><b>{} (hoy)</b></h4>', date_filter(d, 'l j \d\e F')))
        else:
            output.append(format_html('<h4 class="page-header">{}</h4>', date_filter(d, 'l j \d\e F')))

        if bookings_by_day.get(d, None):
            output.append('<div class="list-group">')
            for booking in bookings_by_day[d]:
                output.append(format_html('<div class="list-group-item"><div class="row"><div class="col-md-4">{} {}</div> <div class="col-md-8"><span style="position: relative; top: 1px;">{}</span></div></div></div>',
                    mark_safe('<span class="label label-success">Confirmada</span>'),
                    mark_safe('<span class="label label-info">Turno {}</span>'.format(booking.get_shift_display())),
                    booking.user.get_full_name()))
            output.append('</div>')
        else:
            output.append(format_html('<p>{}</p>', 'No hay reservas para este día.'))

    return mark_safe(''.join(output))
