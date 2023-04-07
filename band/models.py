from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
    #def save(self):
    #    super().save()
    #    img = Image.open(self.photo.path) # Open image
    #    # resize image
    #    if img.width > 512 or img.height > 700:
    #        proportion_w_h = img.width/img.height  # Отношение ширины к высоте 
    #        output_size = (512, int(512/proportion_w_h))
    #        img.thumbnail(output_size) # Изменение размера
    #        img.save(self.photo.path) # Сохранение

# Концерты
class Concert(models.Model):
    datec = models.DateTimeField(_('datec'))
    city = models.CharField(_('city'), max_length=256)
    hall = models.CharField(_('hall'), max_length=256)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'concert'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datec']),
        ]
        # Сортировка по умолчанию
        ordering = ['datec']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}: {}, {}".format(self.datec.strftime('%d.%m.%Y %H:%M'), self.city, self.hall)
        
# Билеты
class Ticket(models.Model):
    datet = models.DateTimeField(_('datet'))
    concert = models.ForeignKey(Concert, related_name='ticket_concert', on_delete=models.CASCADE)    
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, related_name='ticket_user', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'ticket'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datet']),
        ]
        # Сортировка по умолчанию
        ordering = ['datet']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}, {}".format(self.concert, self.user)
        


