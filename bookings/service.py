# coding: utf-8
from __future__ import unicode_literals
import requests

from datetime import date
from .models import Holiday



class HolidayUpdater(object):
    BASE_URL = 'http://nolaborables.com.ar/API/v1/'

    ConnectionError = requests.ConnectionError

    def __init__(self, year=None):
        self.year = year or date.today().year

    def update(self):
        # Response if of type:
        # [{"dia":1,"mes":1,"motivo":"Año Nuevo","tipo":"inamovible"}, ...]
        url = self.BASE_URL + unicode(self.year)
        data = requests.get(url).json()

        added = 0
        for item in data:
            day = date(self.year, item['mes'], item['dia'])

            if Holiday.objects.filter(date=day).exists():
                continue

            Holiday.objects.create(
                date=day, description=item.get('motivo')
            )
            added += 1
        return added
