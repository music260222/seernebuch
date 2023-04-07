from django.contrib import admin

from .models import News, Concert, Ticket

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(News)
admin.site.register(Concert)
admin.site.register(Ticket)


