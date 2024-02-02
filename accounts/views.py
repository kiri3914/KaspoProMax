from django.shortcuts import render, redirect
from django.contrib.auth.models import User


from .models import Card, Currency, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal


@login_required
def transfer_money(request):
    currencies = Currency.objects.all()

    if request.method == 'POST':
        receiver_phone = request.POST.get('receiver')
        amount = Decimal(request.POST.get('amount'))
        currency_id = request.POST.get('currency')
        receiver_user = User.objects.filter(profile__phone=receiver_phone).first()

        if not receiver_user:
            messages.error(request, 'Не найден пользователь с таким номером!')
            return redirect('transfer_money')
        try:
            currency = Currency.objects.get(id=currency_id)

            transaction = Transaction.objects.create(
                sender=request.user,
                receiver=receiver_user,
                amount=amount,
                currency=currency
            )
            transaction.save()
            messages.success(request, 'Перевод успешно выполнен!')
            return redirect('transfer_money')
        except Exception as e:
            messages.error(request, 'Ошибка при переводе!')
            return redirect('transfer_money')
    
    context = {
        'currencies': currencies
    }
    return render(request, 'accounts/transfer.html', context)