from django.http import JsonResponse
from django.shortcuts import render

from weather import helpers
from weather.constants import WEATHER_DATA_SOURCES
from weather.forms import WeatherForm


def average_temp_view(request):
    form = WeatherForm(request.GET or None)

    if not form.is_valid():
        if request.GET and 'from_form' in request.GET:
            return average_temp_form(request)
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors.items())
            },
                status=422)

    source_apis = [WEATHER_DATA_SOURCES[source]['api_class'] for source in form.cleaned_data['sources']]

    latitude = form.cleaned_data['latitude']
    longitude = form.cleaned_data['longitude']

    average_temp = helpers.get_average_temp(latitude, longitude, source_apis)

    response_data = {
        'success': True,
        'result': {
            'average_temperature': average_temp,
            'latitude': latitude,
            'longitude': longitude,
        }
    }

    return JsonResponse(response_data)


def average_temp_form(request):
    form = WeatherForm(request.GET or None)

    context = {
        'form': form,
    }
    return render(request, 'average_temp_view.html', context)
