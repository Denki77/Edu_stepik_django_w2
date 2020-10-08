import numpy

from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from tour.data.data_tour import departures
from tour.data.data_tour import description
from tour.data.data_tour import data_tours
from tour.data.data_tour import subtitle
from tour.data.data_tour import title


class MainView(View):
    def get(self, request):

        arr_tours = {}

        multiple_random_choice = numpy.random.choice(list(data_tours.keys()), size=6, replace=False)

        for key in multiple_random_choice:

            arr_tours[key] = data_tours[key]

            if len(data_tours[key]['description']) >= 157:
                arr_tours[key]['short_description'] = arr_tours[key]['description'][:157] + '...'
            else:
                arr_tours[key]['short_description'] = arr_tours[key]['description']

            arr_tours[key]['html_stars'] = ' '.join(['★' * int(arr_tours[key]['stars'])])

        return render(request, 'index.html', context={
            'title': title,
            'menu_title': title,
            'departures': departures,
            'subtitle': subtitle,
            'description': description,
            'data_tours': arr_tours,
        })


class DepartureView(View):
    def get(self, request, *args, **kwargs):

        data = {
            'col_find_variant': 0,
            'title': 'Туры с вылетом из ',
            'from': '',
            'min_price': 0,
            'max_price': 0,
            'min_nights': 0,
            'max_nights': 0,
            'find_data': {}
        }

        if kwargs['departure'] not in departures:
            raise Http404
        else:
            data['from'] = departures[kwargs['departure']].replace('Из ', '')
            data['title'] += data['from']

        for key, value in data_tours.items():
            if value['departure'] == kwargs['departure']:
                data['col_find_variant'] += 1

                if value['price'] < data['min_price'] or data['min_price'] == 0:
                    data['min_price'] = value['price']
                if value['price'] > data['max_price'] or data['max_price'] == 0:
                    data['max_price'] = value['price']

                if value['nights'] < data['min_nights'] or data['min_nights'] == 0:
                    data['min_nights'] = value['nights']
                if value['nights'] > data['max_nights'] or data['max_nights'] == 0:
                    data['max_nights'] = value['nights']

                data['find_data'][key] = value

                data['find_data'][key]['html_stars'] = ' '.join(['★' * int(data['find_data'][key]['stars'])])

                if len(data['find_data'][key]['description']) >= 157:
                    data['find_data'][key]['short_description'] = data['find_data'][key]['description'][:157] + '...'
                else:
                    data['find_data'][key]['short_description'] = data['find_data'][key]['description']

        return render(
            request, 'departure.html', context={
                'data': data,
                'departures': departures,
                'title': data['title'],
                'menu_title': title,
            }
        )


def custom_handler404(request, exception):
    return HttpResponseNotFound('<h1>Error 404</h1>Ой, что то сломалось... Простите, извините!')


class TourView(View):
    def get(self, request, *args, **kwargs):

        if kwargs['tour'] not in data_tours.keys():
            raise Http404

        data_tours[kwargs['tour']]['html_stars'] = ' '.join(['★' * int(data_tours[kwargs['tour']]['stars'])])

        return render(request, 'tour.html', context={
            'title': title,
            'menu_title': title,
            'departures': departures,
            'subtitle': subtitle,
            'description': description,
            'from': departures[data_tours[kwargs['tour']]['departure']].replace('Из ', ''),
            'data_tours': data_tours[kwargs['tour']],
        })
