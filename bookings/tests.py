from datetime import date

from django.test import TestCase
from mock import patch, Mock

from .models import Holiday
from .service import HolidayUpdater


class HolidayUpdaterTests(TestCase):

    def setUp(self):
        self.service = HolidayUpdater(2015)

    def mock_response(self, mock, response):
        mock.get.return_value = Mock(json=Mock(return_value=response))

    @patch('bookings.service.requests')
    def test_update_empty(self, mock):
        self.mock_response(mock, [])

        self.service.update()

        mock.get.assert_called_with(
            'http://nolaborables.com.ar/API/v1/2015',
            params={u'excluir': u'opcional'}
        )
        self.assertEqual(Holiday.objects.count(), 0)

    @patch('bookings.service.requests')
    def test_update_adds_holiday(self, mock):
        self.mock_response(mock, [{'mes': 10, 'dia': 12, 'motivo': 'Foo'}])

        self.service.update()

        self.assertEqual(Holiday.objects.count(), 1)

        holiday = Holiday.objects.first()
        self.assertEqual(holiday.date, date(2015, 10, 12))
        self.assertEqual(holiday.description, 'Foo')

    @patch('bookings.service.requests')
    def test_update_handles_moved(self, mock):
        self.mock_response(mock, [{'mes': 10, 'dia': 12, 'motivo': 'Foo', 'traslado': 11}])

        self.service.update()

        holiday = Holiday.objects.first()
        self.assertEqual(holiday.date, date(2015, 10, 11))
