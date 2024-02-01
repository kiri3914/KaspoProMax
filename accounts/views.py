from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Card, Transaction, Currency
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal


@login_required
def transfer_money(request):
    user_cards = Card.objects.filter(owner=request.user, is_active=True)
    users = User.objects.exclude(id=request.user.id)
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

            # Create a transaction
            transaction = Transaction(sender=request.user, receiver=receiver_user, amount=amount, currency=currency)
            transaction.save()

            messages.success(request, 'Money transferred successfully.')
            return redirect('transfer_money')
        except Exception as e:
            messages.error(request, f'Transfer failed: {str(e)}')
    
    return render(request, 'accounts/transactions.html', {'user_cards': user_cards, 'users': users, 'currencies': currencies})
