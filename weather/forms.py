from django import forms

from weather.constants import WEATHER_DATA_SOURCES


class WeatherForm(forms.Form):
    CHOICES = [
        (k, v['display_name']) for k, v in WEATHER_DATA_SOURCES.items()
    ]

    latitude = forms.FloatField(min_value=-180, max_value=180, required=True)
    longitude = forms.FloatField(min_value=-90, max_value=90, required=True)
    sources = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple, required=True)
