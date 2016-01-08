from bootstrap3.renderers import FieldRenderer as BaseFieldRenderer
from django import forms


class BootstrapDatepickerField(forms.DateInput):
    DEFAULT_DATEPICKER = {
        'provide': 'datepicker',
        'date-format': 'dd/mm/yyyy',
        'date-autoclose': 'true',
        'date-today-highlight': 'true',
        'date-language': 'es',
    }

    class Media:
        css = {
            'all': ('bootstrap-datepicker/css/bootstrap-datepicker3.min.css',)
        }
        js = (
            'bootstrap-datepicker/js/bootstrap-datepicker.js',
            'bootstrap-datepicker/locales/bootstrap-datepicker.es.min.js'
        )

    def __init__(self, **kwargs):
        datepicker = kwargs.pop('datepicker', {})
        self.datepicker = self.DEFAULT_DATEPICKER.copy()
        self.datepicker.update(datepicker)

        super(BootstrapDatepickerField, self).__init__(**kwargs)


class FieldRenderer(BaseFieldRenderer):
    def __init__(self, field, *args, **kwargs):
        super(FieldRenderer, self).__init__(field, *args, **kwargs)

    def make_input_group(self, html):
        if isinstance(self.widget, BootstrapDatepickerField):
            attrs = ['data-{name}="{value}"'.format(name=name, value=value)
                     for name, value in self.widget.datepicker.iteritems()]
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
