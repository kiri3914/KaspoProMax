from django.shortcuts import render
from accounts.utils import get_data

def index(request):
    data = get_data('KZT')
    context = {
        'data': data
    }
    return render(request, 'mainapp/index.html', context)

