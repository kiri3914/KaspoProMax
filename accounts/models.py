from django.db import models, transaction
from django.contrib.auth.models import User
from .utils import validation_currency, convert
from decimal import Decimal
from django.forms import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.user.username} Profile'


class Currency(models.Model):
    name = models.CharField(max_length=3, validators=[validation_currency])
    description = models.CharField(max_length=50)
    symbol = models.CharField(max_length=1)

    def __str__(self):
        return f'{self.name} {self.symbol}'


class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)
    expiration_date = models.DateField()
    balance = models.DecimalField(max_digits=16, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.owner.username} Card'

    def debit(self, amount, currency):
        if self.currency == currency:
            self.balance -= amount
            self.save()
        else:
            amount = Decimal(convert(amount, currency, self.currency.name))
            self.balance -= amount
            self.save()
    
    def credit(self, amount, currency):
        if self.currency == currency:
            self.balance += amount
            self.save()
        else:
            amount = Decimal(convert(amount, currency, self.currency.name))
            self.balance += amount
            self.save()


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username} \t {self.amount} {self.currency.symbol}'

    @transaction.atomic
    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Получение объектов карт отправителя и получателя из базы данных
                sender_card = Card.objects.get(owner=self.sender)
                receiver_card = Card.objects.get(owner=self.receiver)

                # Проверка, достаточно ли средств у отправителя (учитывая возможную конвертацию валют)
                if sender_card.currency != self.currency:
                    converted_amount = Decimal(convert(self.amount, self.currency.name, sender_card.currency.name))
                else:
                    converted_amount = self.amount

                if sender_card.balance < converted_amount:
                    raise ValidationError('Недостаточно средств на карте отправителя для совершения транзакции.')

                # Debit the sender's card and credit the receiver's card
                sender_card.debit(self.amount, self.currency.name)
                receiver_card.credit(self.amount, self.currency.name)

                super().save(*args, **kwargs)

        except Exception as e:
            # Handle exceptions if needed
            raise e

    def clean(self):
        # Получение объекта карты отправителя и получателя из базы данных
        sender_card = Card.objects.get(owner=self.sender)

        # Проверка, достаточно ли средств у отправителя (учитывая возможную конвертацию валют)
        if sender_card.currency != self.currency:
            converted_amount = Decimal(convert(self.amount, self.currency.name, sender_card.currency.name))
        else:
            converted_amount = self.amount

        if sender_card.balance < converted_amount:
            raise ValidationError('Недостаточно средств на карте отправителя для совершения транзакции.')
        
        # Проверка, не пытается ли отправитель отправить средства самому себе
        if self.sender == self.receiver:
            raise ValidationError('Вы не можете отправить сами себе')

