import django.contrib.auth.validators
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Pact(models.Model):
    branch = models.ForeignKey('Branch', verbose_name='Филиал', on_delete=models.CASCADE, null=True)
    type = models.ForeignKey('TypePact', verbose_name='Вид', on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey('Staff', verbose_name='Сотрудник', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey('Client', verbose_name='Клиент', on_delete=models.CASCADE, null=True)
    term = models.ForeignKey('Term', verbose_name='Срок', on_delete=models.CASCADE, null=True)
    ssum = models.IntegerField(verbose_name='Страховая сумма')
    conclusionDate = models.DateField(auto_now_add=True, verbose_name='Дата заключения')
    archive = models.BooleanField(default=False, verbose_name='Архив')

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return str(self.client)


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    city = models.CharField(max_length=50, verbose_name='Город')
    road = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=10, verbose_name='Дом')
    office = models.CharField(max_length=10, verbose_name='Офис')
    telephone = models.CharField(max_length=12, verbose_name='Телефон')

    def get_absolute_url(self):
        return reverse('branch', kwargs={"branch_id": self.pk})

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name


class TypePact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид')
    description = models.CharField(max_length=300, verbose_name='Описание')
    stake = models.IntegerField(verbose_name='Ставка агенту (%)')
    cost = models.IntegerField(verbose_name='Цена в год')

    class Meta:
        verbose_name = 'Вид договора'
        verbose_name_plural = 'Виды договоров'

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    role = models.ForeignKey('StaffRole', verbose_name='Роль', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, verbose_name='Филиал', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey('StaffPost', verbose_name='Должность', on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя', blank=True, null=True)
    otchestvo = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True, null=True)
    road = models.CharField(max_length=50, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=10, verbose_name='Дом', blank=True, null=True)
    flat = models.CharField(max_length=10, verbose_name='Квартира', blank=True, null=True)
    telephone = models.CharField(max_length=12, verbose_name='Телефон', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.first_name


class Client(models.Model):
    estate = models.ForeignKey('ClientEstate', on_delete=models.CASCADE, null=True, verbose_name='Имущество',
                               blank=True)
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otchestvo = models.CharField(max_length=100, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='Дата рождения')
    city = models.CharField(max_length=50, verbose_name='Город')
    road = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=10, verbose_name='Дом')
    flat = models.CharField(max_length=10, verbose_name='Квартира')
    telephone = models.CharField(max_length=12, verbose_name='Телефон')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    passport = models.CharField(max_length=10, verbose_name='Серия и номер')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.surname


class Term(models.Model):
    long = models.IntegerField(verbose_name='Продолжительность')

    class Meta:
        verbose_name = 'Срок'
        verbose_name_plural = 'Сроки'

    def __str__(self):
        return str(self.long)


class ClientEstate(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имущество')
    cost = models.IntegerField(verbose_name='Цена')
    percent = models.IntegerField(verbose_name='Процент от стоимости')

    class Meta:
        verbose_name = 'Имущество клиента'
        verbose_name_plural = 'Имущества клиентов'

    def __str__(self):
        return self.name


class StaffRole(models.Model):
    name = models.CharField(max_length=30, verbose_name='Роль')

    class Meta:
        verbose_name = 'Роль сотрудника'
        verbose_name_plural = 'Роли сотрудников'

    def __str__(self):
        return self.name


class StaffPost(models.Model):
    name = models.CharField(max_length=30, verbose_name='Должность')
    salary = models.IntegerField(verbose_name='Зарплата')

    class Meta:
        verbose_name = 'Должность сотрудника'
        verbose_name_plural = 'Должности сотрудников'

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=50, verbose_name='Заголовок')
    description = models.CharField(max_length=300, verbose_name='Текст новости')
    addDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-addDate']

    def __str__(self):
        return self.name
