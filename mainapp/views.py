from django.shortcuts import render
from accounts.utils import get_data


def raspakovka(data):
    data_list = []
    for key, value in data['conversion_rates'].items():
        data_list.append({'currency': key, 'value': 1 / value})
    return data_list

def index(request):
    data = get_data('KZT')
    context = {
        'data': raspakovka(data)
    }
    return render(request, 'mainapp/index.html', context)

