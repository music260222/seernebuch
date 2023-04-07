from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput
from .models import News, Concert, Ticket
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ('datec', 'city', 'hall', 'price')
        widgets = {
            'datec': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'city': TextInput(attrs={"size":"100"}),
            'hall': TextInput(attrs={"size":"100"}),
            'price': NumberInput(attrs={"size":"10"}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('datet', 'concert', 'price', 'user')
        widgets = {
            'datet': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'concert': forms.Select(attrs={'class': 'chosen'}),
            'price': NumberInput(attrs={"size":"10"}),
            'user': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'concert': _('concert'),
            'concert': _('concert'),  
        }
        
# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

