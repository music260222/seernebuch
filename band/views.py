from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect, HttpResponseNotFound

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Подключение моделей
from .models import News, Concert, Ticket
# Подключение форм
from .forms import NewsForm, ConcertForm, TicketForm, SignUpForm
#from .forms import SignUpForm

import datetime

from django.db import models

import sys

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.shortcuts import get_object_or_404

from django.utils import timezone

import random

# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница
#@login_required 
def index(request):
    try:
        news1 = News.objects.all().order_by('-daten')[0:1]
        news24 = News.objects.all().order_by('-daten')[1:4]
        #raise Exception("Проверка")
        return render(request, "index.html", {"news1": news1, "news24": news24 , })
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# Страница Контакты
def contact(request):
    return render(request, "contact.html")

# Страница О группе
def about(request):
    return render(request, "about.html")

# Страница Слушать
def listen(request):
    return render(request, "listen.html")

# Страница Галерея
def gallery(request):
    return render(request, "gallery.html")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        #raise Exception("Проверка")
        return render(request, "news/index.html", {"news": news})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        #raise Exception("Проверка")
        return render(request, "news/list.html", {"news": news})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    if request.method == "POST":
        news = News()        
        news.daten = request.POST.get("daten")
        news.title = request.POST.get("title")
        news.details = request.POST.get("details")
        if 'photo' in request.FILES:                
            news.photo = request.FILES['photo']        
        news.save()
        return HttpResponseRedirect(reverse('news_index'))
    else:        
        #newsform = NewsForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
        newsform = NewsForm(initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), })
        return render(request, "news/create.html", {"form": newsform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def concert_index(request):
    try:
        concert = Concert.objects.all().order_by('datec')
        return render(request, "concert/index.html", {"concert": concert})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# Список для просмотра
def concert_list(request):
    try:
        # Концерты с датой больше или равно текущей дате
        concert = Concert.objects.filter(datec__gte=datetime.date.today()).order_by('datec')
        # Текущий пользователь
        _user_id = request.user.id
        if request.method == "POST":
            # Выделить concert_id
            concert_id = request.POST.dict().get("concert_id")
            print("concert_id ", concert_id)
            datec = request.POST.dict().get("datec")
            print("datec ", datec)
            city = request.POST.dict().get("city")
            print("city ", city)
            hall = request.POST.dict().get("hall")
            print("hall ", hall)
            price = request.POST.dict().get("price")
            print("price ", price)
            # Добавить запись в билет
            ticket = Ticket()        
            ticket.datet = datetime.datetime.now(tz=timezone.utc)
            ticket.concert_id = concert_id
            ticket.price = 1500
            ticket.user_id = _user_id
            ticket.save()    
            #return HttpResponseRedirect(reverse("ticket/list/", kwargs={"ticket": ticket, "concert_id": concert_id, "datec": datec, "city": city, "hall": hall, "price": price,}))
            #return render(request, "ticket/list.html", {"ticket": ticket, "concert_id": concert_id, "datec": datec, "city": city, "hall": hall, "price": price,})
            #return redirect(ticket_list, ticket = ticket, concert_id = concert_id, datec = datec, city = city, hall = hall, price = price)
            return redirect(ticket_list)
        else:
            return render(request, "concert/list.html", {"concert": concert})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def concert_create(request):
    if request.method == "POST":
        concert = Concert()        
        concert.datec = request.POST.get("datec")
        concert.city = request.POST.get("city")
        concert.hall = request.POST.get("hall")
        concert.price = request.POST.get("price")  
        concert.save()
        return HttpResponseRedirect(reverse('concert_index'))
    else:        
        #concertform = ConcertForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
        concertform = ConcertForm(initial={'datec': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), })
        return render(request, "concert/create.html", {"form": concertform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def concert_edit(request, id):
    try:
        concert = Concert.objects.get(id=id) 
        if request.method == "POST":
            concert.datec = request.POST.get("datec")
            concert.city = request.POST.get("city")
            concert.hall = request.POST.get("hall")
            concert.price = request.POST.get("price") 
            concert.save()
            return HttpResponseRedirect(reverse('concert_index'))
        else:
            # Загрузка начальных данных
            concertform = ConcertForm(initial={'datec': concert.datec.strftime('%Y-%m-%d %H:%M'), 'city': concert.city, 'hall': concert.hall, 'price': concert.price })
            return render(request, "concert/edit.html", {"form": concertform})
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def concert_delete(request, id):
    try:
        concert = Concert.objects.get(id=id)
        concert.delete()
        return HttpResponseRedirect(reverse('concert_index'))
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def concert_read(request, id):
    try:
        concert = Concert.objects.get(id=id) 
        return render(request, "concert/read.html", {"concert": concert})
    except Concert.DoesNotExist:
        return HttpResponseNotFound("<h2>Concert not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def ticket_index(request):
    try:
        ticket = Ticket.objects.all().order_by('datet')
        return render(request, "ticket/index.html", {"ticket": ticket})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))

# Список для текущего пользователя
@login_required
def ticket_list(request):
    try:
        # Текущий пользователь
        _user_id = request.user.id
        ticket = Ticket.objects.filter(user_id=_user_id).order_by('datet')
        return render(request, "ticket/list.html", {"ticket": ticket})
    except Exception as error:
        print(error)
        return HttpResponse(str(error))
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def ticket_create(request):
    # Текущий пользователь
    _user_id = request.user.id    
    if request.method == "POST":
        ticket = Ticket()
        ticket.datet = request.POST.get("datet")
        ticket.concert = Concert.objects.filter(id=request.POST.get("concert")).first()
        ticket.price = request.POST.get("price")
        ticket.user = _user_id
        ticket.save()
        return HttpResponseRedirect(reverse('ticket_index'))
    else:        
        ticketform = TicketForm(initial={'datet': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), })
        return render(request, "ticket/create.html", {"form": ticketform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def ticket_edit(request, id):
    try:
        ticket = Ticket.objects.get(id=id) 
        if request.method == "POST":
            ticket = Ticket()        
            ticket.datet = request.POST.get("datet")
            ticket.concert = Concert.objects.filter(id=request.POST.get("concert")).first()
            ticket.price = request.POST.get("price")
            ticket.user = _user_id
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_index'))
        else:
            # Загрузка начальных данных
            ticketform = TicketForm(initial={'datet': ticket.datet.strftime('%Y-%m-%d %H:%M'), 'concert': ticket.concert, 'price': ticket.price, 'user': ticket.user })
            return render(request, "ticket/edit.html", {"form": ticketform})
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def ticket_delete(request, id):
    try:
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        return HttpResponseRedirect(reverse('ticket_index'))
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def ticket_read(request, id):
    try:
        ticket = Ticket.objects.get(id=id) 
        return render(request, "ticket/read.html", {"ticket": ticket})
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("<h2>Ticket not found</h2>")
    
# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

