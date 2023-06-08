import calendar
import datetime

from django.forms.widgets import HiddenInput, SelectDateWidget
from django.utils import datetime_safe
from django.utils.formats import get_format


class MonthYearWidget(SelectDateWidget):
    def __init__(self, last_day=False, *args, **kwargs):
        self.last_day = last_day
        return super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        day_name = self.day_field % name
        day_subwidget = HiddenInput().get_context(
            name=day_name,
            value=1,
            attrs={**context["widget"]["attrs"], "id": "id_%s" % day_name},
        )
        context["widget"]["subwidgets"][0] = day_subwidget["widget"]

        return context

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if self.last_day is True:
            y = data.get(self.year_field % name)
            m = data.get(self.month_field % name)
            if y is not None and m is not None:
                input_format = get_format("DATE_INPUT_FORMATS")[0]
                monthrange = calendar.monthrange(int(y), int(m))
                date_value = datetime.date(int(y), int(m), monthrange[1])
                date_value = datetime_safe.new_date(date_value)
                return date_value.strftime(input_format)
        return value