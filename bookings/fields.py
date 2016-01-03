from datetime import date

from bootstrap3.renderers import FieldRenderer as BaseFieldRenderer
from django import forms


class BootstrapDatepickerField(forms.DateInput):
    class Media:
        css = {
            'all': ('bootstrap-datepicker/css/bootstrap-datepicker3.min.css',)
        }
        js = (
            'bootstrap-datepicker/js/bootstrap-datepicker.js',
            'bootstrap-datepicker/locales/bootstrap-datepicker.es.min.js'
        )


class FieldRenderer(BaseFieldRenderer):
    def __init__(self, field, *args, **kwargs):
        super(FieldRenderer, self).__init__(field, *args, **kwargs)

    def make_input_group(self, html):
        if isinstance(self.widget, BootstrapDatepickerField):
            attrs = {
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy',
                'data-date-autoclose': 'true',
                'data-date-start-date': date.today().strftime('%d/%m/%Y'),
                'data-date-today-highlight': 'true',
                'data-date-language': 'es',
            }
            attrs = ['{name}="{value}"'.format(name=name, value=value)
                     for name, value in attrs.iteritems()]
            attrs = ' '.join(attrs)
            after = '<span class="input-group-addon"><i class="glyphicon glyphicon-th"></i></span>'
            html = '<div class="input-group date" {attrs}>{html}{after}</div>'.format(
                attrs=attrs,
                html=html,
                after=after,
            )
            return html
        else:
            return super(FieldRenderer, self).make_input_group(html)
