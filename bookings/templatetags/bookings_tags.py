# coding: utf-8
from __future__ import unicode_literals
from datetime import date, timedelta

from constance import config
from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date as date_filter
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


def date_range(start, end):
    date = start
    while date <= end:
        yield date
        date = date + timedelta(days=1)


def group_by(iterable, fn):
    rv = {}
    for obj in iterable:
        key = fn(obj)
        rv.setdefault(key, [])
        rv[key].append(obj)
    return rv


@register.simple_tag(name='calendar', takes_context=True)
def calendar(context, booking_list):
    start = date.today()
    end = date.today() + timedelta(days=config.BOOKING_DAYS_FUTURE)

    bookings_by_day = group_by(booking_list, lambda b: b.date)

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
                if booking.status != 'x' and booking.user == context['request'].user:
                    actions = format_html('<a class="btn btn-xs btn-link" href="{}">Cancelar</a>', reverse('bookings:cancel', kwargs={'pk': booking.pk}))
                else:
                    actions = ''

                label_classes = {'x': 'danger', 'c': 'success', 'p': 'warning'}

                output.append(format_html('<div class="list-group-item"><div class="row"><div class="col-md-4">{} {}</div> <div class="col-md-6"><span style="position: relative; top: 1px;">{}</span></div><div class="col-md-2 text-right">{}</div></div></div>',
                    format_html('<span class="label label-{}">{}</span>', label_classes[booking.status], booking.get_status_display()),
                    format_html('<span class="label label-info">Turno {}</span>', booking.get_shift_display()),
                    format_html('<span data-toggle="tooltip" title="{}">{}</span>', booking.user.email, booking.user.get_full_name()),
                    actions,
                ))
            output.append('</div>')
        else:
            output.append(format_html('<p class="text-muted">{}</p>', 'No hay reservas para este día.'))

    return mark_safe(''.join(output))
